from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import FloatType
import pyspark.sql.functions as f
import pandas as pd

class PSTool:
    def pyspark_session(self, host_location):
        """
        Creates and returns spark session object
        """
        sc = SparkContext(host_location)  # Create spark context
        spark = SparkSession(sc)  # Create session
        return spark

    def file_loader(self, path, delim, spark_obj):
        data = spark_obj.read.options(delimiter=delim).csv(path)  # load file
        return data

    def get_questions(self, df):
        # Q1
        Q1_exp = df.select("_c11").filter(df._c11 != '-').distinct()._jdf.queryExecution().simpleString()\
            .replace('\n', '')
        Q1_answer = df.select("_c11").filter(df._c11 != '-').distinct().count()
        Q1 = [1, Q1_answer, Q1_exp]

        # Q2
        Q2_exp = df.select("_c11").filter(df._c11 != '-').distinct()._jdf.queryExecution().simpleString().\
            replace('\n', '')
        Q2_answer = df.select("_c11").filter(df._c11 != '-').count() / df.select("_c11").filter(
            df._c11 != '-').distinct().count()
        Q2 = [2, Q2_answer, Q2_exp]

        # Q3
        Q3_exp = df.withColumn("_c13", explode(split(col("_c13"), '\\|'))).select("_c13").filter(df._c13 != '-').agg(
            {'_c13': 'max'})._jdf.queryExecution().simpleString().replace('\n', '')
        Q3_answer = df.withColumn("_c13", explode(split(col("_c13"), '\\|'))).select("_c13").filter(df._c13 != '-').agg(
            {'_c13': 'max'}).collect()[0][0]
        Q3 = [3, Q3_answer, Q3_exp]

        # Q4
        Q4_exp = df.select(abs(df._c7 - df._c8)).agg(
            {'abs((_c7 - _c8))': 'mean'})._jdf.queryExecution().simpleString().replace('\n', '')
        Q4_answer = df.select(abs(df._c7 - df._c8)).agg({'abs((_c7 - _c8))': 'mean'}).collect()[0][0]
        Q4 = [4, Q4_answer, Q4_exp]

        # Q5
        Q5_exp = df.filter(df._c11 != '-').groupBy('_c11').count()._jdf.queryExecution().simpleString().\
            replace('\n', '')
        df_g = df.filter(df._c11 != '-').groupBy('_c11').count()
        Q5_answer = df_g.orderBy(df_g['count'].desc()).head(10)
        Q5_answer = [Q5_answer[n].__getitem__('_c11') for n, i in enumerate(Q5_answer)]
        Q5 = [5, Q5_answer, Q5_exp]

        # Q6
        Q6_exp = df.withColumn('perc', (df._c7 - df._c8) / df._c2).sort(
            'perc')._jdf.queryExecution().simpleString().replace('\n', '')
        df_2 = df.withColumn('perc', (df._c7 - df._c8) / df._c2).sort('perc')
        Q6_answer = df_2.filter(df._c11 != '-').filter(df_2.perc > 0.9).groupBy('_c11').count().\
            sort('count', ascending=False).head(10)
        Q6_answer = [Q6_answer[n].__getitem__('_c11') for n, i in enumerate(Q6_answer)]
        Q6 = [6, Q6_answer, Q6_exp]

        # Q7
        Q7_exp = df.filter(df._c12 != '-').select('_c12').withColumn("_c12", explode(split(col("_c12"), ' '))).groupBy(
            '_c12').count().sort('count', ascending=False)._jdf.queryExecution().simpleString().replace('\n', '')
        Q7_answer = df.filter(df._c12 != '-').select('_c12').withColumn("_c12",
                                                                        explode(split(col("_c12"), ' '))).groupBy(
            '_c12').count().sort('count', ascending=False).head(10)
        Q7_answer = [Q7_answer[n].__getitem__('_c12') for n, i in enumerate(Q7_answer)]
        Q7 = [7, Q7_answer, Q7_exp]

        # Q8
        Q8_exp = df.filter(df._c12 != '-').select('_c12').withColumn("_c12", explode(split(col("_c12"), ' '))).groupBy(
            '_c12').count().sort('count', ascending=True)._jdf.queryExecution().simpleString().replace('\n', '')
        Q8_answer = df.filter(df._c12 != '-').select('_c12').withColumn("_c12",
                                                                        explode(split(col("_c12"), ' '))).groupBy(
            '_c12').count().sort('count', ascending=True).head(10)
        Q8_answer = [Q8_answer[n].__getitem__('_c12') for n, i in enumerate(Q8_answer)]
        Q8 = [8, Q8_answer, Q8_exp]

        # Q9
        Q9_exp = df.where(f.col('_c11').isin(Q6_answer)).filter(df._c12 != '-').select('_c12').\
            withColumn("_c12",explode(split(col("_c12"),' '))).groupBy(
            '_c12').count().sort('count', ascending=False)._jdf.queryExecution().simpleString().replace('\n', '')
        df3 = df.where(f.col('_c11').isin(Q6_answer)).filter(df._c12 != '-').select('_c12').withColumn("_c12", explode(
            split(col("_c12"), ' '))).groupBy('_c12').count().sort('count', ascending=False).head(10)
        Q9_answer = [df3[n].__getitem__('_c12') for n, i in enumerate(df3)]
        Q9 = [9, Q9_answer, Q9_exp]

        # Q10
        Q10_exp = df.select(df._c0, df._c11, df._c2).filter(df._c11 != "-").groupby(df._c0,"_c2")\
            .count()._jdf.queryExecution().simpleString().replace('\n', '')
        Q10 = df.select(df._c0, df._c11, df._c2).filter(df._c11 != "-").groupby(df._c0, "_c2").count()
        Q10_answer = Q10.withColumn('_c2', Q10['_c2'].cast(FloatType()))
        Q10_answer = Q10_answer.corr('_c2', 'count') ** 2
        Q10 = [10, Q10_answer, Q10_exp]

        # Getting everything together and writing to file
        print('Getting everything into a single dataframe')
        Questnum = list(range(1, 11))
        Answers = list(
            [Q1_answer, Q2_answer, Q3_answer, Q4_answer, Q5_answer, Q6_answer, Q7_answer, Q8_answer, Q9_answer,
             Q10_answer])
        Explains = list([Q1_exp, Q2_exp, Q3_exp, Q4_exp, Q5_exp, Q6_exp, Q7_exp, Q8_exp, Q9_exp, Q10_exp])
        zipped = list(zip(Questnum, Answers, Explains))
        data = pd.DataFrame(zipped, columns=['Questnum', 'Answers', 'Explains'])
        print('Writing to CSV')
        data.to_csv("assignment5.csv", index=False)
        print('Done!')


if __name__ == "__main__":
    # Instanciate object
    pstool = PSTool()
    # start session
    spk = pstool.pyspark_session('local')
    # load data
    path = '/data/dataprocessing/interproscan/all_bacilli.tsv'
    # path = 'all_bacilli_subset.tsv'
    df=pstool.file_loader(path, '\t', spk)
    pstool.get_questions(df)
    print('Closing spark session')
    spk.sparkContext.stop()
    # df.printSchema()  # Shows column names and some info

