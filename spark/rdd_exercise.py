import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('RDD Exercise').getOrCreate()

# Load CSV file into a data frame
score_sheet_df = spark.read.load('/user/krystenng/score-sheet.csv', \
    format='csv', sep=';', inferSchema='true', header='true')

score_sheet_df.show()

#Sort the data frame by score
score_sheet_df_sort = score_sheet_df.sort("Score")

#Get the minmum and maximum from the dataframe
min = score_sheet_df_sort.collect()[0][1]
max = score_sheet_df_sort.collect()[-1][1]

#Filter by excluding the max and min in the dataframe
score_sheet_exclude = score_sheet_df_sort.filter((score_sheet_df_sort.Score > min) & (score_sheet_df_sort.Score < max))
score_sheet_exclude.show()

# Get RDD from the data frame
score_sheet_rdd = score_sheet_exclude.rdd
score_sheet_rdd.first()

# Project the second column of scores with an additional 1
score_rdd = score_sheet_rdd.map(lambda x: (x[1], 1))
score_rdd.first()

# Get the sum and count by reduce
(sum, count) = score_rdd.reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]))
print('Average Score : ' + str(sum/count))

# Load Parquet file into a data frame
posts_df = spark.read.load('/user/krystenng/input/hardwarezone.parquet')
posts_rdd = posts_df.rdd

# Project the author name, content length and count
author_content_rdd = posts_rdd.map(lambda x: (x[1],(len(x[2]), 1)))
author_content_rdd.first()

#Reduce by key to get the total length of all the posts of each author
count_rdd = author_content_rdd.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

# Map the author name with the average length of posts by every author
avg_rdd = count_rdd.map(lambda x: (x[0], x[1][0]/x[1][1]))

#Get the list of authors
list_of_authors = avg_rdd.collect()

# To get the results
result = ''
for x in list_of_authors:
    result += x[0] + ' ' + str(x[1]) + '\n'

print('\n')
print('Average post length : \n' + result)
