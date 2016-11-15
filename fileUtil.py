"""
Helper module for file IO
"""
import pandas as pd
import sys


def readFile(filename):
    """
    Read file and returns list of lines.

    :param filename
    :return list of lines
    """
    try:
        with open(filename, 'rb') as f:
            return f.readlines()
    except IOError:
        print >> sys.stderr, "Error while opening the file {}".format(filename)
        sys.exit(-1)
    raise Exception("Unexpected error while reading the file {}".format(filename))

def writeFile(filename, result):
    """
    Not yet implemented
    """
    pass

def readColFromCsvFile(filename, column):
    """
    Read csv file and return the rows of certain column.

    :param filename
    :param column
    :return rows
    """
    df = pd.read_csv(filename)
    rows = [row for index, row in df[column].iteritems()]
    return rows

def writeCsvFile(filename, result):
    """
    Not yet implemented
    """
    pass

def readData(filename, isCsv, col):
    """
    Read the given file by checking whether it is csv or not.

    :param isCsv
    :param col
    :return list of lines or rows
    """
    if isCsv:
        return readColFromCsvFile(filename, col)
    else:
        return readFile(filename)
    raise Exception("Unexpected error while reading the data from {}".format(filename))
