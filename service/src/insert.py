import os
import pickle
import ijson
import numpy as np
import math
from PIL import ImageOps, Image
from milvus_toolkits import has_table, create_table, create_index, milvus_insert, milvus_collection_rows, drop_table
from mysql_toolkits import create_recipe_table, load_recipe_data_to_mysql
from config import image_collection_param, recipe_collection_param, temp_file_path
from get_feature import load_trained_features


def init_table(milvus_client, conn, cursor):
    status, ok = has_table(milvus_client, 'recipe')
    print("has_table:", status, ok)
    if ok:
        drop_table(milvus_client, 'recipe')
        drop_table(milvus_client, 'image')

    print("create table...")

    create_table(milvus_client, recipe_collection_param)
    create_table(milvus_client, image_collection_param)

    create_index(milvus_client, 'recipe')
    create_index(milvus_client, 'image')

    create_recipe_table(conn, cursor)


def get_image_path(dataset_sample):
    img_name = dataset_sample['images'][0]
    img_name = '../dataset/' + 'test' + '/' + '/'.join(img_name[:4]) + '/' + img_name
    return img_name


def record_temp_file(recipe_ids, milvus_ids):
    # create sql insert data
    dataset = pickle.load(open('../dataset/traindata/test.pkl', 'rb'))

    with open(temp_file_path, 'w') as temp_file:
        for i, recipe_id in enumerate(recipe_ids):
            dataset_sample = dataset[recipe_id]

            title = dataset_sample['title'].lower()
            ingredients = str(dataset_sample['ingredients'])
            instructions = str(dataset_sample['instructions'])
            image = get_image_path(dataset_sample)
            line = str(
                milvus_ids[i]) + '|' + recipe_id + '|' + title + '|' + ingredients + '|' + instructions + '|' + image
            temp_file.write(line + '\n')


"""
# generate sql dataset file
def record_temp_file(recipe_ids, milvus_ids):
    '''
    recipe_dicts, recipe_all_ids = read_recipe_json()
    print("read json success")
    disable_indexs = []
    with open(temp_file_path,'w') as f:
        for i, recipe_id in enumerate(recipe_ids):
            if recipe_id in recipe_all_ids:
                index = recipe_all_ids.index(recipe_id)
                line = str(milvus_ids[i]) + '|' + recipe_id + '|' + recipe_dicts[index]['title'] + '|' + str(recipe_dicts[index]['ingredients']) + '|' + str(recipe_dicts[index]['instructions']) + '|' + recipe_dicts[index]['url']
                f.write(line + '\n')
            else:
                disable_indexs.append(i)
    return disable_indexs
    '''
    recipe_all_ids = read_recipe_json_id()
    disable_indexs = []

    # exclude all diables indexs
    for i, recipe_id in enumerate(recipe_ids):
        if not recipe_id in recipe_all_ids:
            disable_indexs.append(i)

    with open(temp_file_path, 'w') as temp_file, open(recipe_json_fname, 'r') as json_file:
        for object in ijson.items(json_file, 'item'):
            object_id = object['id']
            for i, recipe_id in enumerate(recipe_ids):
                if recipe_id == object_id:
                    line = str(milvus_ids[i]) + '|' + recipe_id + '|' + object['title'] + '|' + str(
                        object['ingredients']) + '|' + str(object['instructions']) + '|' + \
                           object['url']
                    temp_file.write(line + '\n')

    return disable_indexs
"""


# get recipe features and load data into milvus and mysql
def do_insert(milvus_client, conn, cursor):
    # get recipe features(use feats_test.pkl read recipefeats and ids)
    info = load_trained_features()
    recipe_feats = info['recipefeats']
    image_feats = info['imfeats']
    recipe_ids = info['ids']
    print("loaded all vectors sucessfully")
    init_table(milvus_client, conn, cursor)
    try:
        milvus_rows = milvus_collection_rows(milvus_client, table_name='recipe')
        print("milvus rows: ", milvus_rows)

        milvus_ids = list(range(milvus_rows, milvus_rows + len(recipe_feats)))

        record_temp_file(recipe_ids, milvus_ids)
        print("temp file success")

        print("begin load data to mysql")
        load_recipe_data_to_mysql(conn, cursor)

        print("doing insert, the num of insert recipe vectors:", len(recipe_feats))
        print("doing insert, the num of insert recipe vectors:", len(image_feats))
        status, ids = milvus_insert(milvus_client, vectors=recipe_feats, ids_list=milvus_ids, table_name='recipe')
        status, ids = milvus_insert(milvus_client, vectors=image_feats, ids_list=milvus_ids, table_name='image')
        return status

    except Exception as e:
        print("Error with {}".format(e))
