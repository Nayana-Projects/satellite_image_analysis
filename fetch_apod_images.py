import os
import requests
from datetime import datetime

# Your API key
API_KEY = "W6RyAOONWxfilmDGKi1u5l4pUFyjV7QgQchsKgFR"  # Replace with your API key

# API Endpoint
API_URL = "https://api.nasa.gov/planetary/apod"

# Target Folder
RAW_DATA_DIR = "data/raw/"

def fetch_apod_image(output_dir):
    """
    Fetch the APOD image for the current date and save it locally.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Get the current date dynamically
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Construct the API request parameters
    params = {
        "api_key": API_KEY,
        "date": current_date,
    }

    print(f"Fetching APOD image for date: {current_date}")
    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data (Status: {response.status_code})")
        print("Response:", response.text)
        return

    # Parse the JSON response
    data = response.json()
    if "url" in data and data["media_type"] == "image":
        image_url = data["url"]
        filename = data["date"] + "_" + os.path.basename(image_url)
        file_path = os.path.join(output_dir, filename)

        print(f"Downloading {filename} from {image_url}...")
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in image_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Saved: {file_path}")
        else:
            print(f"Failed to download {filename}: {image_response.status_code}")
    else:
        print(f"No image available for date: {current_date}")

if __name__ == "__main__":
    # Fetch and store the image for the current date
    fetch_apod_image(RAW_DATA_DIR)

