from pdf2image import convert_from_path
import pytesseract
import timeit
import regex as re
try:
    from PIL import Image
except ImportError:
    import Image

# EasyOCR
# import easyocr
# reader = easyocr.Reader(['en'])


def extractor(pather):
    print('0th step')
    images = convert_from_path(pather)
    #images = convert_from_path(pather,poppler_path = config.POPPLER_PATH)
    print('1st step')
    for i in range(len(images)):
        return pytess(images[i])


def pytess(image):
    print('pytess')
    extractedInfo = pytesseract.image_to_string((image))
    extractedInfo = " ".join(extractedInfo.split())
    extractedInfo = re.sub(
        '[^A-Za-z0-9#/-]+', ' ', extractedInfo)
    print(extractedInfo)
    return extractedInfo


def easyOCR(image):
    string = ""
    result = reader.readtext(image, detail=0)
    for texter in result:
        string += texter + " "
    with open("easyocr.txt", "w") as output:
        output.write(str(string))


start = timeit.default_timer()
# easyOCR('/Users/iambankaratharva/CanspiritAI/bert-entity-extraction/records-0.png')
# extractor('/Users/iambankaratharva/CanspiritAI/bert-entity-extraction/Medical Records/records-0.pdf')
stop = timeit.default_timer()
print('Time: ', stop - start)
