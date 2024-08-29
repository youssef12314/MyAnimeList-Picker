from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

CLIENT_ID = '93c11ab080968951f661f2e298b7028b'

def fetch_plan_to_watch(username):
    url = f'https://api.myanimelist.net/v2/users/{username}/animelist'
    params = {
        'status': 'plan_to_watch',
        'limit': 1000,  # Use a smaller limit for debugging
        'fields': 'title,main_picture'
    }
    headers = {
        'X-MAL-Client-ID': CLIENT_ID
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print("API Response Status:", response.status_code)  # Debugging
        response_data = response.json()
        print("API Response JSON:", response_data)  # Debugging

        anime_list = response_data.get('data', [])
        anime_info = [
            {
                'title': anime['node']['title'],
                'image_url': anime['node'].get('main_picture', {}).get('large', '')
            }
            for anime in anime_list
        ]
        return anime_info
    except requests.RequestException as e:
        print("Request failed:", e)
        return []
    
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get-random-anime', methods=['POST'])
def get_random_anime():
    username = request.form.get('username')
    print("Received Username:", username)  # Debugging
    anime_info_list = fetch_plan_to_watch(username)
    if anime_info_list:
        random_anime_info = random.choice(anime_info_list)
        print("Random Anime Info:", random_anime_info)  # Debugging
        return render_template(
            'index.html',
            random_anime_title=random_anime_info['title'],
            random_anime_image_url=random_anime_info['image_url'],
            username=username
        )
    else:
        print("No anime found or API call failed.")  # Debugging
        return render_template(
            'index.html',
            error='No anime found in your plan to watch list',
            username=username
        )
    
if __name__ == '__main__':
    app.run(debug=True)
