from flask import Flask, request, render_template
from extract_bbox_info import yolo_to_dict
from ultralytics import YOLO
from PIL import Image
import numpy as np
import datetime
import pydicom
import shutil
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/documentation")
def documentation():        
    return render_template('documentation.html')

@app.route("/conversion_tool")
def conversion_tool():        
    return render_template('dicom_to_png.html')

@app.route("/start_converting", methods=['GET', 'POST'])
def start_converting():        
    if request.method == 'POST':
        print('yes')
        remove_files()
        file = request.files.get('input-image')
        if file:
            file.save('static/convert-file.dicom')
            dicom_to_png('static/convert-file.dicom', 'static/convert-file.png')
    return render_template('dicom_to_png.html', file_path='static/convert-file.png')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    remove_files()
    if request.method == 'POST':
        patient_name = request.form['Name']
        age = request.form['Age']
        gender = request.form['Gender']
        side = request.form['Side']
        projection = request.form['Projection']
        file = request.files.get('input-image')

        if file and allowed_file(file.filename):
            filename = f"static/input-image.png"
            file.save(filename)
            os.chdir('static/')
            model = YOLO('YOLOv8x-best.pt')
            model('input-image.png', save=True, save_txt=True)
            os.chdir('../')

        now = datetime.datetime.now()
        date_of_scan = now.strftime("%B %d, %Y")
        if os.path.exists('static/runs/detect/predict/labels/input-image.txt'):
            annotations = yolo_to_dict('static/runs/detect/predict/labels/input-image.txt', 'static/runs/detect/predict/input-image.png')
        else:
            annotations = ''
        timestamp = now.strftime('%Y%m%d%H%M%S')
        return render_template('result.html', 
                            patient_name=patient_name, 
                            age=age, 
                            gender=gender,
                            side=side,projection=projection,
                            date_of_scan=date_of_scan, 
                            annotations=annotations,
                            timestamp=timestamp)

    return render_template('index.html')

@app.route('/dicom_to_png_api_index')
def dicom_to_png_api_index():
    return render_template('dicom_to_png_api.html')

@app.route("/dicom_to_png_api_start_converting", methods=['GET', 'POST'])
def dicom_to_png_api_start_converting():        
    if request.method == 'POST':
        remove_files()
        file = request.files.get('input-image')
        if file:
            file.save('static/dicom_to_png_api_convert-file.dicom')
            dicom_to_png('static/dicom_to_png_api_convert-file.dicom', 'static/dicom_to_png_api_convert-file.png')
            print('yes')
    return render_template('dicom_to_png_api.html', file_path='static/dicom_to_png_api_convert-file.png')

@app.route('/mobile_detection_api')
def detection_api_index():
    return render_template('android_detection_index.html')

@app.route('/mobile_detection_api_predict', methods=['GET', 'POST'])
def detection_api_predict():
    remove_files()
    if request.method == 'POST':
        file = request.files.get('file')

        if file:
            filename = f"static/detection_api_input-image.png"
            file.save(filename)
            os.chdir('static/')
            if not os.path.exists('API_DIR'):
                os.mkdir('API_DIR')
            os.chdir('API_DIR/')
            model = YOLO('../YOLOv8x-best.pt')
            model('../detection_api_input-image.png', save=True)
            os.chdir('../../')

        return render_template('android_detection_result.html')
    return render_template('android_detection_index.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_files():
    if os.path.isdir('static/runs/'):
        shutil.rmtree('static/runs')
    if os.path.isdir('static/API_DIR/runs/'):
        shutil.rmtree('static/API_DIR/runs')
    if os.path.exists('static/input-image.png'):
        os.remove('static/input-image.png')
    if os.path.exists('static/convert-file.dicom'):
        os.remove('static/convert-file.dicom')
    if os.path.exists('static/convert-file.png'):
        os.remove('static/convert-file.png')
    if os.path.exists('static/dicom_to_png_api_convert-file.dicom'):
        os.remove('static/dicom_to_png_api_convert-file.dicom')
    if os.path.exists('static/dicom_to_png_api_convert-file.png'):
        os.remove('static/dicom_to_png_api_convert-file.png')
    if os.path.exists('static/detection_api_input-image.png'):
        os.remove('static/detection_api_input-image.png')

def dicom_to_png(input_file, output_file):
    im = pydicom.dcmread(input_file)
    im = im.pixel_array.astype(float)
    rescaled_image = (np.maximum(im, 0)/im.max()) * 255
    final_image = np.uint8(rescaled_image)
    final_image = Image.fromarray(final_image)
    final_image.save(output_file)

if __name__ == "__main__":
    app.run(debug=True) 