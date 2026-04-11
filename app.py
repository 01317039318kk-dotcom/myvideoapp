from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import time
import threading

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# ফাইল ডিলিট করার ফাংশন (সার্ভার স্টোরেজ বাঁচাতে)
def delayed_delete(file_path):
    time.sleep(300) # ৫ মিনিট পর ডিলিট হবে
    if os.path.exists(file_path):
        try: os.remove(file_path)
        except: pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    video_url = request.form.get('url')
    if not video_url:
        return jsonify({"error": "URL missing"}), 400

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt', # বট শনাক্তকরণ এড়াতে
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            # সরাসরি প্লে করার লিঙ্ক বের করা
            formats = [f for f in info.get('formats', []) if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            play_url = formats[0]['url'] if formats else info.get('url')
            return jsonify({
                "title": info.get('title', 'Video'),
                "video_url": play_url,
                "thumbnail": info.get('thumbnail', ''),
                "url": video_url
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/download')
def download():
    video_url = request.args.get('url')
    # নির্দিষ্ট ফরম্যাট এর বদলে 'best' ব্যবহার করা হয়েছে এরর কমাতে
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
        'nocheckcertificate': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            threading.Thread(target=delayed_delete, args=(filename,)).start()
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

