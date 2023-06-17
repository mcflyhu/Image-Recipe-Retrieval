import pymysql
import time
from config import temp_file_path, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


def connect_mysql():
    try:
        connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PASSWORD,
                                     database=MYSQL_DATABASE, local_infile=True)
        return connection
    except Exception as e:
        print("CONNECT MYSQL ERROR:", e)
    # return "connect mysql faild"


def create_recipe_table(conn, cursor):
    sql = "create table if not exists " + "recipe" + "(milvus_id bigint, recipe_id varchar(10),title varchar(64), ingredients text, instructions text, image_url varchar(64), index index_id (milvus_id));"
    try:
        cursor.execute(sql)
    # print("create table")
    except Exception as e:
        print("CREATE MYSQL TABLE ERROR:", e)
    # conn.rollback()
    # print("create table faild")


# 将数据批量存入mysql中
def load_recipe_data_to_mysql(conn, cursor):
    sql = "load data local infile '" + temp_file_path + "' into table " + "recipe" + " fields terminated by '|';"
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("LOAD DATA TO MYSQL ERROR:", e)
    # conn.rollback()
    # print("load data faild")


# 通过milvus_id查找对应的食谱
def search_recipe_by_milvus_ids(conn, cursor, ids):
    str_ids = str(ids).replace('[', '').replace(']', '')
    sql = "select * from " + "recipe" + " where milvus_id in (" + str_ids + ") order by field (milvus_id," + str_ids + ");"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print("mysql search faild:", e)
