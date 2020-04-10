import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved
from typing import List


class CountNumberOfLeaves:
    '''
    Returns number of leaves for each method in class.
    input: file_path
    output: list of numbers. Size of this list == number of methods in class.
    '''
    def __init__(self):
        pass

    def value(self, filename: str):

        tree = JavalangImproved(filename)

        nodes = tree.tree_to_nodes()
        traversed = []
        for each_noda in nodes:
            if type(each_noda.node) == javalang.tree.MethodDeclaration:
                traversed.append(countLeaves(each_noda.node))

        return (traversed)


def countLeaves(root):
    # forming the same data type for each object
    root_arr = root if isinstance(root, List) else [root]
    leaves = 0

    # traverse through all childs of object. If there is no child, hence we faced leaf
    for node in root_arr:

        if not hasattr(node, 'children') and node not in [None]:
            return leaves + 1

        elif node in [None]:
            continue

        for each_child in node.children:
            leaves += countLeaves(each_child)

    return leaves
