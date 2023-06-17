from milvus_toolkits import milvus_client
from insert import do_insert
from mysql_toolkits import connect_mysql


milvus_client = milvus_client()
connection = connect_mysql()
cursor = connection.cursor()
status = do_insert(milvus_client, connection, cursor)
cursor.close()
connection.close()
print(status)
