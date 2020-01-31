# coding=utf-8
import unittest


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def runAnalysis(self):
        super(JavaTestCase, self).setUp()
        from main import CCMetric

        metric = CCMetric('tests/javafiles/', True)
        data = list(filter(lambda x: x['file'] == 'tests/javafiles/Complicated.java', metric.value['data']))
        self.assertEqual(data[0]['complexity'], 12)

        data = list(filter(lambda x: x['file'] == 'tests/javafiles/OtherClass.java', metric.value['data']))
        self.assertEqual(data[0]['complexity'], 3)

        errors = list(filter(lambda x: x['file'] == 'tests/javafiles/ooo.java', metric.value['errors']))
        self.assertEqual(errors[0]['message'][0:12], 'PMDException')

        file = 'tests/javafiles/Complicated.java'
        metric = CCMetric(file, True)
        self.assertEqual(metric.value['data'][0]['complexity'], 12)
        self.assertEqual(metric.value['data'][0]['file'], file)

        file = 'tests/javafiles/ooo.java'
        metric = CCMetric(file, True)
        self.assertEqual(metric.value['errors'][0]['message'][0:12], 'PMDException')
        self.assertEqual(metric.value['errors'][0]['file'], file)

        file = 'tests/javafiles/ooo1.java'
        metric = CCMetric(file, True)
        self.assertEqual(metric.value['errors'][0]['message'], 'File does not exist')
        self.assertEqual(metric.value['errors'][0]['file'], file)

        file = 'tests/javafiles/OtherClass.java'
        metric = CCMetric(file, True)
        self.assertEqual(metric.value['data'][0]['complexity'], 3)
