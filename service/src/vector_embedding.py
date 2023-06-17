# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import multiprocessing
import numpy as np
from dataset import get_loader
from models import get_model
import torch.backends.cudnn as cudnn
from config import get_args
import torchvision.transforms as transforms
from PIL import Image
import torch
import torch.nn as nn

from utils.utils import get_token_ids, list2Tensors
import pickle


def image_feature_embedding(image_path, model):
    transforms_list = [transforms.Resize((256))]

    transforms_list.append(transforms.CenterCrop(224))
    transforms_list.append(transforms.ToTensor())
    transforms_list.append(transforms.Normalize((0.485, 0.456, 0.406),
                                                (0.229, 0.224, 0.225)))

    transforms_ = transforms.Compose(transforms_list)
    # load image
    # check image format first
    extension = os.path.basename(image_path).split('.')[-1]
    if extension not in ['jpeg', 'jpg', 'png']:
        raise Exception("Wrong image format.")

    img = Image.open(image_path)
    if transforms_ is not None:
        img = transforms_(img)

    img = img.view((1,) + img.shape)

    # get model output
    if img is not None:
        img_feat = model.image_encoder(img)
    else:
        img_feat = None

    image_feat = img_feat.cpu().detach().numpy()

    return image_feat


def recipe_feature_embedding(entry, model):
    # define default arguments
    max_ingrs = 20
    max_instrs = 20
    max_length_ingrs = 15
    max_length_instrs = 15

    # load vocabulary
    vocab_inv = pickle.load(open('../data/vocab.pkl', 'rb'))
    vocab = {}
    for k, v in vocab_inv.items():
        if type(v) != str:
            v = v[0]
        vocab[v] = k

    # load recipe data
    title = entry['title']
    ingrs = entry['ingredients']
    instrs = entry['instructions']

    # turn text into indexes
    title = torch.Tensor(get_token_ids(title, vocab)[:max_length_instrs])
    instrs = list2Tensors(
        [get_token_ids(instr, vocab)[:max_length_instrs] for instr in instrs[:max_instrs]])
    ingrs = list2Tensors([get_token_ids(ingr, vocab)[:max_length_ingrs] for ingr in ingrs[:max_ingrs]])

    title = torch.unsqueeze(title, 0)
    ingrs = torch.unsqueeze(ingrs, 0)
    instrs = torch.unsqueeze(instrs, 0)

    title = pad_input(title)
    ingrs = pad_input(ingrs)
    instrs = pad_input(instrs)

    # get recipe model output
    text_features = []
    projected_text_features = {'title': {},
                               'ingredients': {},
                               'instructions': {},
                               'raw': {}}

    elems = {'title': title, 'ingredients': ingrs, 'instructions': instrs}

    names = list(elems.keys())

    for name in names:
        # for each recipe component, extracts features and projects them to all other spaces
        input_source = elems[name]
        text_feature = model.text_encoder(input_source, name)
        text_features.append(text_feature)

    recipe_feat = model.merger_recipe(torch.cat(text_features, dim=1))
    recipe_feat = nn.Tanh()(recipe_feat)

    recipe_feat = recipe_feat.cpu().detach().numpy()

    return recipe_feat


def pad_input(input):
    """
    creates a padded tensor to fit the longest sequence in the batch
    """
    if len(input[0].size()) == 1:
        l = [len(elem) for elem in input]
        targets = torch.zeros(len(input), max(l)).long()
        for i, elem in enumerate(input):
            end = l[i]
            targets[i, :end] = elem[:end]
    else:
        n, l = [], []
        for elem in input:
            n.append(elem.size(0))
            l.append(elem.size(1))
        targets = torch.zeros(len(input), max(n), max(l)).long()
        for i, elem in enumerate(input):
            targets[i, :n[i], :l[i]] = elem
    return targets
