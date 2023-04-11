from flask import Flask, request, render_template
from extract_bbox_info import yolo_to_dict
from ultralytics import YOLO
from PIL import Image
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
        return render_template('result.html', 
                            patient_name=patient_name, 
                            age=age, 
                            gender=gender,
                            side=side,projection=projection,
                            date_of_scan=date_of_scan, 
                            annotations=annotations)

    return render_template('index.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_files():
    if os.path.isdir('static/runs/'):
        shutil.rmtree('static/runs')
    if os.path.exists('static/input-image.png'):
        os.remove('static/input-image.png')

def dicom_to_png(input_file, output_file):
    # dicom_data = pydicom.dcmread(input_file)
    # img = Image.fromarray(dicom_data.pixel_array)
    # img.save(output_file)
    pass

if __name__ == "__main__":
    app.run(debug=True) 
