import os

def image_recognition_ollama(file_path):
    try:
        os.system('ollama list> nul')
        import ollama
    except:
        return 'False', 0, 0

    
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    response = ollama.generate(
        model="gemma3:12b-it-qat",
        prompt="""
        Where is this image taken? Please provide the GPS coordinates in the format of latitude and longitude. 
        Please only return in the format: 
        1. If you can identify the location, return True, latitude, longitude.
        2. If you cannot identify the location, return False, 0, 0.
        """,
        images=[image_bytes]
    )
    #print(response['response'])

    result = response['response'].strip().split('\n')[0]
    is_place, latitude, longitude = result.split(',', 3)
    is_place = str(is_place.strip())
    latitude = float(latitude.strip())
    longitude = float(longitude.strip())

    return is_place, latitude, longitude
    

if __name__ == "__main__":
    acc = image_recognition_ollama(r"\Victoria_Harbour.jpg")
    print(acc)