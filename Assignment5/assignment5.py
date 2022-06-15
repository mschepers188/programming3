from pyspark import SparkContext
from pyspark.sql.session import SparkSession

path = 'all_bacilli.tsv'

sc = SparkContext('local')  # Create spark context
spark = SparkSession(sc)  # Create session
df = spark.read.options(delimiter='\t').csv(path)  # load csv

df.show()  # shows dataframe(Limited to first 20)
df.printSchema()  # Shows column names and some info
