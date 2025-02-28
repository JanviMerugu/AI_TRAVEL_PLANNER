import requests

def fetch_destination_images(destination, unsplash_api_key, count=3):
    url = f"https://api.unsplash.com/search/photos?query={destination}&per_page={count}&client_id={unsplash_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        images = [item['urls']['regular'] for item in data['results']]
        return images
    return []