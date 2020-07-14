import os
import shutil
import subprocess
import tarfile
from pathlib import Path
import pickle
from aibolit.model.model import TwoFoldRankingModel  # type: ignore
from aibolit.config import Config
import pandas as pd


def collect_dataset(args):
    """
    Run bash scripts to collect metrics and patterns for java files
    """

    def make_patterns(args, cur_work_dir):
        print('Compute patterns...')
        result = subprocess.run(['make', 'patterns'], stdout=subprocess.PIPE, encoding='utf-8', cwd=cur_work_dir)
        print(result.returncode)
        if result.returncode != 0:
            print(result.stderr)
            exit(3)
        else:
            print(result.stdout)
            if args.dataset_file:
                dataset_file_path = Path(cur_work_dir, args.dataset_file)
                if not dataset_file_path.parent.exists():
                    dataset_file_path.parent.mkdir(parents=True)
                shutil.copy(Path(Config.dataset_file()), dataset_file_path)
            else:
                dataset_file_path = Path(Config.dataset_file())
            print('dataset was saved to {}'.format(str(dataset_file_path.absolute())))

    def run_cmd(metrics_cmd, cur_work_dir):
        result = subprocess.run(metrics_cmd, stdout=subprocess.PIPE, encoding='utf-8', cwd=cur_work_dir)
        if result.returncode != 0:
            print(result.stderr)
            exit(1)
        else:
            print(result.stdout)

    # path to java files which will be analyzed
    java_folder = args.java_folder
    max_classes = args.max_classes
    os.chdir(Path(Config.home_aibolit_folder(), 'scripts'))
    if not java_folder:
        java_folder = Path('target/01').absolute()
        print('Analyzing {} dir:'.format(java_folder))
    cur_work_dir = Path(os.getcwd())
    print('Current working directory: ', cur_work_dir)
    print('Directory with JAVA classes: ', java_folder)
    print('Filtering java files...')

    filter_cmd = ['make', 'filter']
    metrics_cmd = ['make', 'metrics']
    merge_cmd = ['make', 'merge']
    build_halstead_cmd = ['make', 'build_halstead']
    make_hl_cmd = ['make', 'hl']

    if java_folder is not None:
        filter_cmd.append(f'dir={java_folder}')
        metrics_cmd.append(f'dir={java_folder}')
    if max_classes is not None:
        filter_cmd.append(f'max_classes={max_classes}')

    run_cmd(filter_cmd, cur_work_dir)
    print('Download PMD and compute metrics...')
    run_cmd(metrics_cmd, cur_work_dir)
    make_patterns(args, cur_work_dir)
    print('Building halstead.jar...')
    run_cmd(build_halstead_cmd, cur_work_dir)
    print('Calculating halstead metrics...')
    run_cmd(make_hl_cmd, cur_work_dir)

    print('Merge results and create dataset...')
    run_cmd(merge_cmd, cur_work_dir)


def train_process():
    """
    Define needed columns for dataset and run model training
    """
    config = Config.get_patterns_config()
    only_patterns = [
        x['code'] for x in list(config['patterns'])
        if x['code'] not in config['patterns_exclude']
    ]
    only_metrics = \
        [x['code'] for x in list(config['metrics'])
         if x['code'] not in config['metrics_exclude']] \
        + ['halstead volume']
    columns_features = only_metrics + only_patterns
    features_number = len(columns_features)
    print("General number of features in config: ", features_number)

    gzip_arc = Config.get_dataset_archive()
    tar = tarfile.open(str(gzip_arc))
    tar.extractall(path=gzip_arc.parent)
    tar.close()

    train_dataset = pd.read_csv(Config.train_csv(), index_col=None)
    model = TwoFoldRankingModel()
    features_conf = {
        "features_order": only_patterns,
        "patterns_only": only_patterns
    }
    model.features_conf = features_conf
    print('Scaling features...')
    scaled_dataset = model.scale_dataset(train_dataset)
    dataset = scaled_dataset[only_patterns]
    print('Training model...')
    model.fit(dataset, scaled_dataset['M4'])

    save_model_file = Path(Config.folder_to_save_model_data(), 'model.pkl')
    print('Saving model to loaded model from file {}:'.format(save_model_file))
    with open(save_model_file, 'wb') as fid:
        pickle.dump(model, fid)

    load_model_file = Path(Config.folder_to_save_model_data(), 'model.pkl')
    print('Test loaded model from file {}:'.format(load_model_file))
    test_dataset = pd.read_csv(Config.test_csv(), index_col=None)
    scaled_test_dataset = model.scale_dataset(test_dataset).sample(n=20, random_state=17)
    # add ncss, ncss is needed in informative as a  last column
    X_test = scaled_test_dataset[only_patterns + ['M2']]
    with open(load_model_file, 'rb') as fid:
        model_new = pickle.load(fid)
        print('Model has been loaded successfully')
        for _, row in X_test.iterrows():
            snippet = [x for x in row]
            preds, importances = model_new.informative(snippet)
            print(preds)
    path_with_logs = Path(os.getcwd(), 'catboost_info')
    print('Removing path with catboost logs {}'.format(path_with_logs))
    if path_with_logs.exists():
        shutil.rmtree(path_with_logs)
