from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyAj_ZB8TOSQViO5MYQAfYEnf-T9LlcuFks" #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/videos')
def get_videos():
    page_token = request.args.get('pageToken', '')
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q=Bangla song 2026&type=video&pageToken={page_token}&key={API_KEY}"
    r = requests.get(url).json()
    videos = []
    for item in r.get('items', []):
        videos.append({
            "title": item['snippet']['title'],
            "thumbnail": item['snippet']['thumbnails']['high']['url']
        })
    return jsonify({"videos": videos, "nextPageToken": r.get('nextPageToken', '')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

