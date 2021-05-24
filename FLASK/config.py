import warnings
from transformers import BertTokenizer, TFBertModel, BertConfig
from tokenizers import BertWordPieceTokenizer
from sklearn import preprocessing
from tensorflow.keras import layers
from tensorflow import keras
import pandas as pd
import numpy as np
import string
import json
import re
import transformers
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '1'
warnings.filterwarnings("ignore")

MAX_LEN = 400
TRAIN_BATCH_SIZE = 64
VALID_BATCH_SIZE = 16
EPOCHS = 10
 
META_MODEL_PATH = r"Resource\meta.bin"
MODEL_PATH = r"Resource\my_model.h5"
tokenizer = BertWordPieceTokenizer(r"Resource\bert-base-uncased\vocab.txt", lowercase=True)
POPPLER_PATH = r"Resource\poppler-0.67.0_x86\poppler-0.67.0\bin"
# tokenizer = BertWordPieceTokenizer(r"/Users/iambankaratharva/CanspiritAI/bert-entity-extraction/FLASK/bert-base-uncased/vocab.txt", lowercase=True)
 
