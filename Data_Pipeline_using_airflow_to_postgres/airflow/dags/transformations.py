##import required libraries
import pyspark

##create spark session
spark = (
    pyspark.sql.SparkSession.builder.appName("Python Spark SQL basic example")
    .config(
        "spark.driver.extraClassPath",
        "/Users/ayushi/Downloads/postgresql-42.2.18.jar",
    )
    .getOrCreate()
)


##read table from db using spark jdbc
def extract_movies_to_df():
    movies_df = (
        spark.read.format("jdbc")
        .option("url", "jdbc:postgresql://localhost:5432/ayushi")
        .option("dbtable", "movies")
        .option("user", "ayushi")
        .option("password", "ayushi")
        .option("driver", "org.postgresql.Driver")
        .load()
    )
    return movies_df


## read table from db using spark jdbc
def extract_users_to_df():
    users_df = (
        spark.read.format("jdbc")
        .option("url", "jdbc:postgresql://localhost:5432/ayushi")
        .option("dbtable", "users")
        .option("user", "ayushi")
        .option("password", "ayushi")
        .option("driver", "org.postgresql.Driver")
        .load()
    )
    return users_df


## transform the user table
def transform_avg_ratings(users_df, movies_df):
    avg_rate = users_df.groupBy("movie_id").mean("rating")
    ## Join the tables
    df = movies_df.join(avg_rate, movies_df.id == avg_rate.movie_id)
    df = df.drop("movie_id")
    return df


## Load the data to the database
def load_df_to_db(df):
    mode = "overwrite"
    url = "jdbc:postgresql://localhost:5432/ayushi"
    table = "avg_ratings"
    properties = {
        "user": "ayushi",
        "password": "ayushi",
        "driver": "org.postgresql.Driver",
    }
    df.write.jdbc(url=url, table=table, mode=mode, properties=properties)


if __name__ == "__main__":
    movies_df = extract_movies_to_df()
    users_df = extract_users_to_df()
    df = transform_avg_ratings(users_df, movies_df)
    load_df_to_db(df)
