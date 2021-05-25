import warnings
from tokenizers import BertWordPieceTokenizer
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '1'
warnings.filterwarnings("ignore")

MAX_LEN = 400
TRAIN_BATCH_SIZE = 64
VALID_BATCH_SIZE = 16
EPOCHS = 10

META_MODEL_PATH = r"/Users/iambankaratharva/CanspiritAI/PDF-Extractor-NER-BERT/FLASK/Resource/meta.bin"
MODEL_PATH = r"/Users/iambankaratharva/CanspiritAI/PDF-Extractor-NER-BERT/FLASK/Resource/my_model.h5"
# tokenizer = BertWordPieceTokenizer(
#     r"/Users/iambankaratharva/CanspiritAI/bert-entity-extraction/FLASK/bert-base-uncased/vocab.txt", lowercase=True)
#POPPLER_PATH = r"Resource\poppler-0.67.0_x86\poppler-0.67.0\bin"
tokenizer = BertWordPieceTokenizer(
    r"/Users/iambankaratharva/CanspiritAI/bert-entity-extraction/FLASK/bert-base-uncased/vocab.txt", lowercase=True)
