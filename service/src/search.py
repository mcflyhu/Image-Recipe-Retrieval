import string

import numpy as np
# from bert_serving.client import BertClient
from vector_embedding import image_feature_embedding, recipe_feature_embedding
from milvus_toolkits import milvus_search
from mysql_toolkits import search_recipe_by_milvus_ids
from PIL import Image


def search_recipe(image_path, index_client, sql_connection, cursor, trained_model):
    try:
        query = image_feature_embedding(image_path, trained_model)
    except Exception as e:
        print("image2embedding error: ", e)
        return e
    print(query.shape)
    status, results = milvus_search(index_client, table_name='recipe', query=query)

    print(results)

    if len(results) != 0:
        milvus_result_ids = [res.id for res in results[0]]
        mysql_results = search_recipe_by_milvus_ids(sql_connection, cursor, milvus_result_ids)
        response = []
        for mysql_result in mysql_results:
            title = mysql_result[2]
            title = string.capwords(title)
            ingredients = eval(mysql_result[3])
            # Ingredients = [ingredient for ingredient in eval(mysql_result[3])]
            instructions = eval(mysql_result[4])
            # instructions = instructions = [instr['text'] for instr in instructions]
            # link = result[5]
            result = {"title": title, "ingredients": ingredients, "instructions": instructions}
            response.append(result)
        return response
    else:
        return "there is no data"


def search_image(recipe, index_client, sql_connection, cursor, trained_model):
    try:
        query = recipe_feature_embedding(recipe, trained_model)
    except Exception as e:
        print("image2embedding error: ", e)
        return e

    print(query.shape)
    status, results = milvus_search(index_client, table_name='image', query=query)

    print(results)

    if len(results) != 0:
        milvus_result_ids = [res.id for res in results[0]]
        mysql_results = search_recipe_by_milvus_ids(sql_connection, cursor, milvus_result_ids)
        response = []
        for mysql_result in mysql_results:
            image_path = mysql_result[5]
            # convert image binary format into Image
            result = convert_img_stream(image_path)

            response.append(result)

        return response
    else:
        return "there is no data"


# output = []
# for result in results:
# 	title = result[2]
# 	Ingredients = eval(result[3])
# 	Ingredients = [ingre['text'] for ingre in Ingredients]
# 	instructions = eval(result[4])
# 	instructions = instructions = [instr['text'] for instr in instructions]
# 	link = result[5]
# 	result = {"title":title,"ingredients":Ingredients,"instructions":instructions,"link":link}
# 	output.append(result)
def convert_img_stream(image_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(image_path, 'rb') as image_file:
        img_stream = image_file.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream
