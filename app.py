-tfrom flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url: return "URL missing", 400
    
    ydl_opts = {
        'format': 'best',
        'cookiefile': 'cookies.txt', # কুকি ফাইল ব্যবহার
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            return send_file(ydl.prepare_filename(info), as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

