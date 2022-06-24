from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import mean, abs
from collections import Counter
import pyspark.sql.functions as f
from pyspark.sql.types import FloatType

class PSTool:
    def pyspark_session(self, host_location):
        """
        Creates and returns spark session object
        """
        sc = SparkContext(host_location[16])  # Create spark context
        spark = SparkSession(sc)  # Create session
        return spark

    def file_loader(self, path, delim, spark_obj):
        data = spark_obj.read.options(delimiter=delim).csv(path)  # load file
        return data

    def questions(self, df):


        # Getting everything together and writing to file


if __name__ == "__main__":
    # Instanciate object
    pstool = PSTool()
    # start session
    spk = pstool.pyspark_session('local')
    # load data
    path = '/data/dataprocessing/interproscan/all_bacilli.tsv'
    df=pstool.file_loader(path, '\t', spk)

    # df_sub.show()
    # df.printSchema()  # Shows column names and some info

