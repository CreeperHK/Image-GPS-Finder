---

# Image GPS Finder with EXIF and AI Recognition

A Flask web application that extracts GPS coordinates from image EXIF data or uses AI to recognize locations. Displays results on a map.

---

## 📌 Description

This application allows users to upload images and retrieve their geographic coordinates. It first checks for GPS data in the image's EXIF metadata. If unavailable, it uses a AI model to analyze the image and estimate the location (In this project we use Ollama for local LLM model, see [Ollama](https://ollama.com/) for more detail). The result is displayed on a map with latitude and longitude.

---

## 🛠 Installation

### 1. **Prerequisites**
- Python >3.7 (Dev in 3.12.10)
- [Ollama](https://ollama.com/)
- A Local LLM model which support Image as input

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Install Ollama Model**
Ensure the Ollama model is pulled: (Using qwen2.5vl as example)
```bash
ollama pull qwen2.5vl
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
├── llm_model_api.py        # AI image recognition logic
├── llm_model_install_check # Use to check is Ollama and the model running
├── requirements.txt        # Python dependencies
├── LICENSE                 # License for this application
├── uploads/                # Uploaded image storage (auto-created and delete after use)
└── templates/
    ├── index.html          # Upload form
    └── result.html         # Result display
```

---

## 📝 Known Issues

- **Ollama Process Cleanup**: The script attempts to terminate Ollama processes on exit, but this may not always work reliably.
- **File Cleanup**: The `uploads/` directory is cleaned up automatically, but manual deletion may be needed in some cases.
- **Description Showing**: The description will only show up when the image runs on AI recognition, if the image is run on exif data, it won't show the description.
- **Accuracy on Map**: the pointer on the map is based on the GPS coordinate provided by the LLM model. After many tests, the pointer can only indicate the vicinity of the target location but not the exact location.
---

## ✏️ Customize

If you want to use another model or use API. You only need to edit the `llm_model_api.py`.  
The logic inside the code should look like this:
```python
def image_recognize_gps(image_file_path, model):

    # Your model or API request logic, the model/API should answer 4 things as follow.
    # Please edit the prompt to ensure 4 things return.

    # Recommend for using this prompt
    prompt="""
        Where is this image taken? Please provide the GPS coordinates in the format of latitude and longitude. 
        Please only return in the format: 
        1. If you can identify the location, return True, latitude, longitude.
        2. If you cannot identify the location, return False, 0, 0.
        3. Also come with a short description of the place.

        The final output should be in the format:
        True/False, latitude, longitude, description.
        Please do not return any other information.
        """

    is_place = bool(result.is_place)  # Does the location be found? False if not found
    latitude = float(result.latitude)  # The GPS latitude, 0 if not found
    longitude = float(result.longitude) # The GPS longitude, 0 if not found
    description = str(result.description) # The description for user checking, None if not found

    return is_place, latitude, longitude, description
```

---

## 📚 Credits

- **EXIF Parsing**: [ExifRead](https://pypi.org/project/ExifRead/)
- **AI Backend**: [Ollama](https://ollama.com/)
- **AI Model**: [Gemma3](https://deepmind.google/models/gemma/)
- **Flask Framework**: [Flask](https://flask.palletsprojects.com/)

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---