# Image GPS Finder with EXIF and AI Recognition

A Flask web application that extracts GPS coordinates from image EXIF data or uses AI to recognize locations. Displays results on a map.

---

## 📌 Description

This application allows users to upload images and retrieve their geographic coordinates. It first checks for GPS data in the image's EXIF metadata. If unavailable, it uses a AI model to analyze the image and estimate the location(In this project we use Ollama for local LLM model, see [Ollama](https://ollama.com/) for more detail). The result is displayed on a map with latitude and longitude.

---

## 🛠 Installation

### 1. **Prerequisites**
- Python 3.x
- [Ollama](https://ollama.com/)
- A Local LLM model which support Image as input (Using gemma3:12b-it-qat in this case)

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Install Ollama Model**
Ensure the Ollama model `gemma3:12b-it-qat`(Or your LLM model) is pulled:
```bash
ollama pull <Model_Name>
```

---

## 🚀 Usage

### 1. **Run the Application**
```bash
python app.py
```
The app will start on `http://127.0.0.1:5000`.

### 2. **Upload an Image**
- Navigate to the homepage.
- Upload an image file (supported formats: `.jpg`, `.jpeg`, `.png`, `.raw`, `.webp`).
- The app will:
  - Extract GPS data from EXIF if available.
  - Use AI to recognize the location if EXIF data is missing.

### 3. **View Results**
- The result will display on a Google Map with the detected coordinates.
- You can return to the upload page to try another image.

---

## 🧠 Notes

- **AI Accuracy**: The AI model may not always provide accurate coordinates. EXIF data is more reliable.
- **Ollama Dependency**: The application assumes Ollama is running locally. Ensure it's installed and accessible.
- **Temporary Files**: Uploaded images are stored in the `uploads/` directory and automatically cleaned up on exit.
- **Map Embed**: The map uses Google Maps' embed API. A stable internet connection is required for maps to load.

---

## 📁 Directory Structure

```
/your-project-folder/
├── app.py                  # Main Flask application
├── ollama_api.py           # AI image recognition logic
├── requirements.txt        # Python dependencies
├── uploads/                # Uploaded image storage (auto-created)
└── templates/
    ├── index.html          # Upload form
    └── result.html         # Result display
```

---

## 📝 Known Issues

- **Ollama Process Cleanup**: The script attempts to terminate Ollama processes on exit, but this may not always work reliably.
- **File Cleanup**: The `uploads/` directory is cleaned up automatically, but manual deletion may be needed in some cases.

---

## 📄 License

This project is for personal use only. See the [LICENSE](LICENSE) file for details.

---

## ✏️ Customize

If you want to use another model or use API. You only need to edit the `ollama_api.py`.
the logic inside the code should be look like this:
```python
def image_recognize_gps(image_file_path):

    # Your model or API request logic, the model/API should answer 3 things as follow.
    # Please edit the prompt to ensure 3 things return.

    is_place = bool(result.is_place)  #Does the location be found? False if not found
    latitude = float(result.latitude)  #The GPS latitude, 0 if not found
    longitude = float(result.longitude) #The GPS longitude, 0 if not found

    return is_place, latitude, longitude
```
---

## 📚 Credits

- **EXIF Parsing**: [ExifRead](https://pypi.org/project/ExifRead/)
- **AI Backend**: [Ollama](https://ollama.com/)
- **AI Model**: [Gemma3](https://deepmind.google/models/gemma/)
- **Flask Framework**: [Flask](https://flask.palletsprojects.com/)
