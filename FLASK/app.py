from flask import Flask, render_template, request, send_from_directory, current_app as app
import os
import predict
import joblib
import transformers
import tensorflow as tf
import tensorflow as tf
import pdf_to_img
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

meta_data = joblib.load(
    "/Users/iambankaratharva/CanspiritAI/PDF-Extractor-NER-BERT/FLASK/meta.bin")

model_bert = tf.keras.models.load_model(
    '/Users/iambankaratharva/CanspiritAI/PDF-Extractor-NER-BERT/FLASK/my_model.h5', compile=False, custom_objects={'TFBertMainLayer': transformers.TFBertModel})

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Function for preparing images from pdf
def prepare_images(pdf_path):
    # Output dir
    output_dir = os.path.join(APP_ROOT, 'static/pdf_image/')

    with(Image(filename=pdf_path, resolution=300, width=600)) as source:
        images = source.sequence
        pages = len(images)
        for i in range(pages):
            Image(images[i]).save(filename=output_dir + str(i) + '.png')
    print('Prepare Images done')

# App routing
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    pdf_target = os.path.join(APP_ROOT, 'static/pdf')

    # Preparing directory
    if not os.path.isdir(pdf_target):
        os.mkdir(pdf_target)

    # Uploading File
    for file in request.files.getlist('file'):
        filename = file.filename
        destination = "/".join([pdf_target,filename])
        file.save(destination)
        print(destination)
        sentence = pdf_to_img.extractor(destination)
        final_info = predict.get_mapping([sentence], meta_data, model_bert)

        '''# Creating images
        if os.path.isfile(destination):
            prepare_images(destination)'''

    return final_info


if __name__ == '__main__':
    app.run(debug=True)