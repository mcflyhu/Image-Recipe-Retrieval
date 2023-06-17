import os

from fastapi import Depends, FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from milvus_toolkits import milvus_client
from search import *

from mysql_toolkits import connect_mysql

from models import get_model
from dataset import get_loader
import torch.backends.cudnn as cudnn
from config import get_args
import torch
from utils.utils import load_checkpoint, count_parameters

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_mysql_connection():
    connection = connect_mysql()
    cursor = connection.cursor()
    return connection, cursor


def load_trained_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    map_loc = None if torch.cuda.is_available() else 'cpu'
    # set model args
    args = get_args()
    vars_to_replace = ['eval_split', 'root', 'model_name']
    store_dict = {'eval_split': 'test', 'root': '../dataset', 'model_name': 'vit_ssl'}
    for var in vars_to_replace:
        setattr(args, var, store_dict[var])

    if device != 'cpu':
        cudnn.benchmark = True
    checkpoints_dir = os.path.join(args.save_dir, args.model_name)
    # make sure these arguments are kept from commandline and not from loaded args
    vars_to_replace = ['batch_size', 'eval_split', 'imsize', 'root', 'save_dir']
    store_dict = {}
    for var in vars_to_replace:
        store_dict[var] = getattr(args, var)
    args, model_dict, _ = load_checkpoint(checkpoints_dir, 'best', map_loc,
                                          store_dict)
    for var in vars_to_replace:
        setattr(args, var, store_dict[var])

    loader, dataset = get_loader(args.root, args.batch_size, args.resize,
                                 args.imsize,
                                 augment=False,
                                 split=args.eval_split, mode='test',
                                 drop_last=False)
    print("Extracting features for %d samples from the %s set..." % (len(dataset),
                                                                     args.eval_split))
    vocab_size = len(dataset.get_vocab())
    model = get_model(args, vocab_size)

    print("recipe encoder", count_parameters(model.text_encoder))
    print("image encoder", count_parameters(model.image_encoder))

    model.load_state_dict(model_dict, strict=False)

    if device != 'cpu' and torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)

    model = model.to(device)
    model.eval()

    print("Loaded model from %s ..." % (checkpoints_dir))

    return model


index_client = milvus_client()
trained_model = load_trained_model()


@app.post('/image')
async def search_recipe_api(image: UploadFile = File(...)):
    try:
        upload_image = await image.read()
        image_name = image.filename
        image_path = '../upload_image' + '/' + str(image_name)
        print(image_name)
        # print(image_path)
        with open(image_path, 'wb') as f:
            f.write(upload_image)

        sql_connection, cursor = create_mysql_connection()
        results = search_recipe(image_path, index_client, sql_connection, cursor, trained_model)
        return results
    except Exception as e:
        return "{0}".format(e)
    finally:
        cursor.close()
        sql_connection.close()


@app.post('/recipe')
async def search_image_api(title: str = Form(), ingredients: str = Form(), instructions: str = Form()):
    try:
        # split string to better fit the model
        ingredients = ingredients.split('\r\n')
        instructions = instructions.split('\r\n')
        recipe = {'title': title, 'ingredients': ingredients, 'instructions': instructions}

        sql_connection, cursor = create_mysql_connection()
        results = search_image(recipe, index_client, sql_connection, cursor, trained_model)
        return results
    except Exception as e:
        return "{0}".format(e)
    finally:
        cursor.close()
        sql_connection.close()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='192.168.20.100', port=8030, reload=True, debug=True)
