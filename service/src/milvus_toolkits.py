import time
from milvus import Milvus, IndexType, MetricType, Status
from config import MILVUS_HOST, MILVUS_PORT


def milvus_client():
    try:
        milvus = Milvus(host=MILVUS_HOST, port=MILVUS_PORT)
        return milvus
    except Exception as e:
        print("Milvus client error:", e)


def has_table(client, table_name):
    try:
        status, ok = client.has_collection(collection_name=table_name)
        return status, ok
    except Exception as e:
        print("Milvus has_table error:", e)


def create_table(client, collection_param):
    try:
        status = client.create_collection(collection_param)
        return status
    except Exception as e:
        print("Milvus create table error:", e)


def drop_table(client, table_name):
    try:
        status = client.drop_collection(collection_name=table_name)
        return status
    except Exception as e:
        print("Milvus drop table error:", e)


def create_index(client, table_name):
    param = {'nlist': 16384}
    try:
        status = client.create_index(table_name, IndexType.IVF_FLAT, param)
        return status
    except Exception as e:
        print("Milvus create index error:", e)


def milvus_insert(client, table_name, vectors, ids_list):
    try:
        status, ids = client.insert(collection_name=table_name, records=vectors, ids=ids_list)
        return status, ids
    except Exception as e:
        print("Milvus insert error:", e)


def milvus_search(client, table_name, query):
    try:
        status, results = client.search(collection_name=table_name, query_records=query, top_k=5, params={"nprobe": 16})
        return status, results
    except Exception as e:
        print("Milvus search error:", e)


def milvus_collection_rows(client, table_name):
    try:
        status, rows = client.count_entities(collection_name=table_name)
        return rows
    except Exception as e:
        print("get milvus rows error: ", e)
