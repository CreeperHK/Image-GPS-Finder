import os

def image_recognition_ollama(file_path: str):
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
        3. Also come with a short description of the place.

        The final output should be in the format:
        True/False, latitude, longitude, description.
        Please do not return any other information.
        """,
        images=[image_bytes]
    )
    print(response['response'])

    result = response['response'].strip().split('\n')[0]

    response_parts = result.split(", ")
    
    is_place = True if response_parts[0] == "True" else False
    latitude = float(response_parts[1])
    longitude = float(response_parts[2])
    description = ", ".join(response_parts[3:])

    return is_place, latitude, longitude, description
    

if __name__ == "__main__":
    acc = image_recognition_ollama(r"\Victoria_Harbour.jpg")
    print(acc)