import atexit
import glob
from flask import Flask, render_template, request, redirect, url_for
import exifread
import time
import os
from typing import Tuple

from llm_model_api import image_recognition_ollama
from llm_model_install_check import check_ollama_model

s = check_ollama_model('PlaceholderModelName')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'exif'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'raw', '.webp'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_gps_from_exif(image_path: str) -> Tuple[float, float]:
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = tags['GPS GPSLatitude'].values
                lon = tags['GPS GPSLongitude'].values
                lat_deg = lat[0].num / lat[0].den
                lat_min = lat[1].num / lat[1].den
                lat_sec = lat[2].num / lat[2].den
                lon_deg = lon[0].num / lon[0].den
                lon_min = lon[1].num / lon[1].den
                lon_sec = lon[2].num / lon[2].den
                lat_deg = lat_deg + lat_min / 60 + lat_sec / 3600
                lon_deg = lon_deg + lon_min / 60 + lon_sec / 3600
                return lat_deg, lon_deg
            else:
                return None
    except Exception as e:
        return None

def cleanup():
    files = glob.glob('uploads/*')
    for f in files:
        if f == r'static\style.css' or f == r'static\\style.css' or not os.path.isfile(f):
            continue
        os.remove(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    lat_deg = None
    lon_deg = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part")

        file = request.files['file']
        model_name = request.form.get('model', 'qwen2.5vl')
        

        if file.filename == '':
            return render_template('index.html', error="No selected file")

        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # Try to get GPS from EXIF
                lat_deg, lon_deg = get_gps_from_exif(file_path)

            except Exception as exif_error:
                # If EXIF not found, try AI recognition
                try:
                    s = check_ollama_model(f'{model_name}')
                    
                    if s is None:
                        raise Exception("This image needs AI recognition, but Ollama or model is not installed or not running.")
                    
                    if s == False:
                        raise Exception("The model is not installed or not running. Please install the model first.")

                    is_place, result_lat_deg, result_lon_deg, description = image_recognition_ollama(file_path, model_name)

                    if is_place:
                        delete_file(file_path)
                        return render_template('result.html', 
                                               lat_deg=result_lat_deg, 
                                               lon_deg=result_lon_deg, 
                                               result=f'AI RECOGNITION (Model: {model_name})', 
                                               file_path=file_path, 
                                               description=description)
                    elif is_place is False or result_lat_deg == 0 or result_lon_deg == 0:
                        delete_file(file_path)
                        return render_template('index.html', error="Unable to determine location from image.")
                    else:
                        delete_file(file_path)
                        return render_template('index.html', error="AI recognition failed to determine location.")
                except Exception as ai_error:
                    delete_file(file_path)
                    return render_template('index.html', error=f"AI processing error: {str(ai_error)}")

            # If EXIF data was found
            if lat_deg is not None and lon_deg is not None:
                delete_file(file_path)
                return render_template('result.html', 
                                       lat_deg=lat_deg, 
                                       lon_deg=lon_deg, 
                                       result='EXIF DATA', 
                                       file_path=file_path)
            else:
                delete_file(file_path)
                return render_template('index.html', error="No location data found.")

        else:
            return render_template('index.html', error="Invalid file type.")

    elif request.method == 'GET':
        return render_template('index.html')

    return render_template('index.html')


# Helper function to delete file
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
    time.sleep(1)
    atexit.register(cleanup)
    os.system('taskkill /f /im ollama* > nul')
    os.removedirs(app.config['UPLOAD_FOLDER'])