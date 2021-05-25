from pdf2image import convert_from_path
import pytesseract
import os
import timeit
from tqdm import tqdm
import regex as re
try:
    from PIL import Image
except ImportError:
    import Image
import cv2

# EasyOCR
import easyocr
reader = easyocr.Reader(['en'])


def extractor_easyOCR(pather):
    images = convert_from_path(pather)
    #images = convert_from_path(pather,poppler_path = config.POPPLER_PATH)
    for i in range(len(images)):
        images[i].save(
            f"/Users/iambankaratharva/CanspiritAI/PDF-Extractor-NER-BERT/FLASK/static/pdf-images/page-{i}.png")
        return(easyOCR(f'/Users/iambankaratharva/CanspiritAI/PDF-Extractor-NER-BERT/FLASK/static/pdf-images/page-{i}.png'))


def extractor_pytess(pather):
    images = convert_from_path(pather)
    #images = convert_from_path(pather,poppler_path = config.POPPLER_PATH)
    for i in range(len(images)):
        return pytess(images[i])


def pytess(image):
    extractedInfo = pytesseract.image_to_string((image))
    extractedInfo = " ".join(extractedInfo.split())
    extractedInfo = re.sub(
        '[^A-Za-z0-9#/-]+', ' ', extractedInfo)
    return extractedInfo


def easyOCR(image):
    string = ""
    print(image)
    result = reader.readtext(image, detail=0)
    for texter in result:
        string += texter + " "
    return(string)


start = timeit.default_timer()
# easyOCR('/Users/iambankaratharva/CanspiritAI/bert-entity-extraction/records-0.png')
# extractor('/Users/iambankaratharva/CanspiritAI/bert-entity-extraction/Medical Records/records-0.pdf')
stop = timeit.default_timer()
print('Time: ', stop - start)
