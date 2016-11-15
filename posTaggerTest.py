"""
This module is a module specific for unittest
of posTagger.py class:

    python posTaggerTest.py

"""
import unittest
import inspect
from collections import defaultdict
from posTagger import *


class PosTaggerTest(unittest.TestCase):
    """
    PosTaggerTest contains tests for posTagger.py
    """
    def setUp(self):
        """
        Sets up preconditions before the test suite runs.

        :param dummyFile
        :param dummyCsvFile
        """
        self.dummyFile = "testDummy"
        self.dummyCsvFile = "testDummyCsv"

    def test_posTagNormalFile(self):
        """
        Tests whether posTag worked well for the normal file.
        """
        result, _ = PosTagger(self.dummyFile).run()
        answer = defaultdict(int)
        answer['across'] = 1
        answer['near'] = 2
        answer['around'] = 1
        answer['in'] = 3
        self.assertEqual(result, answer, "{} failed".format(inspect.stack()[0][3]))

    def test_posTagCsvFile(self):
        """
        Tests whether posTag worked well for the csv file.
        """
        result, _ = PosTagger(self.dummyCsvFile, True, "contents").run()
        answer = defaultdict(int)
        answer['on'] = 1
        answer['like'] = 7
        answer['of'] = 1
        answer['inside'] = 1
        answer['near'] = 1
        answer['at'] = 2
        answer['in'] = 1
        answer['with'] = 3
        self.assertEqual(result, answer, "{} failed".format(inspect.stack()[0][3]))

    def test_topKNormalFile(self):
        """
        Tests whether top K algorithm worked well for the normal file.
        """
        _, result = PosTagger(self.dummyFile, False, "", 2).run()
        answer = ['in', 'near']
        self.assertEqual(result, answer, "{} failed".format(inspect.stack()[0][3]))

    def test_topKCsvFile(self):
        """
        Tests whether top K algorithm worked well for the csv file.
        """
        _, result = PosTagger(self.dummyCsvFile, True, "contents", 3).run()
        answer = ['like', 'with', 'at']
        self.assertEqual(result, answer, "{} failed".format(inspect.stack()[0][3]))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PosTaggerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
