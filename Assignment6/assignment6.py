from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import FloatType
import pyspark.sql.functions as f
import pandas as pd
import os

class PSTool:
    def __init__(self):
        print('Creating output folder')
        if os.path.exists('output'):
            pass
        else:
            os.makedirs('output')

    def pyspark_session(self, host_location):
        """
        Creates and returns spark session object
        """
        print('Starting session')
        sc = SparkContext(host_location)  # Create spark context
        spark = SparkSession(sc)  # Create session
        return spark

    def file_loader(self, path, delim, spark_obj):
        print('Loading in file')
        data = spark_obj.read.options(delimiter=delim).csv(path)  # load file
        print('File loaded')
        return data

    def get_questions(self, df):
    	pass

if __name__ == "__main__":
    pstool = PSTool()  # Instanciate object
    spk = pstool.pyspark_session('local[16]')  # start session
    # load data
    path = '/data/dataprocessing/interproscan/all_bacilli.tsv'
    # path = 'all_bacilli_subset.tsv'
    df = pstool.file_loader(path, '\t', spk)
    pstool.get_questions(df)
    print('Closing spark session')
    spk.sparkContext.stop()
    # df.printSchema()  # Shows column names and some info

