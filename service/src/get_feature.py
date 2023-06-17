import pickle
import os
import random
from utils.metrics import *
from PIL import ImageOps, Image
from torchvision import transforms
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.corpus import stopwords

DATASET_PATH = '../dataset'
SAVE_PATH = '../checkpoints'
MODEL_NAME = 'vit_ssl'
SPLIT = 'test'
EMBEDDINGS_FILE = os.path.join(SAVE_PATH, MODEL_NAME, 'feats_' + SPLIT + '.pkl')


def load_trained_features():
    with open(EMBEDDINGS_FILE, 'rb') as f:
        imfeats = pickle.load(f)
        recipefeats = pickle.load(f)
        ids = pickle.load(f)

    return {'imfeats': imfeats, 'recipefeats': recipefeats, 'ids': ids}
    # load embeddings



