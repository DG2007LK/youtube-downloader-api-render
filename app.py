from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Tech With Dasun Python Downloader API is running successfully!"

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'success': False, 'error': 'කරුණාකර YouTube URL එකක් ලබා දෙන්න!'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'web']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            title = info.get('title', 'Unknown Title')
            thumbnail = info.get('thumbnail', '')
            
            formats_list = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    formats_list.append({
                        'quality': f.get('format_note', f.get('resolution', 'Standard')),
                        'container': f.get('ext', 'mp4'),
                        'url': f.get('url')
                    })

            return jsonify({
                'success': True,
                'title': title,
                'thumbnail': thumbnail,
                'formats': formats_list
            })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': f'දෝෂයකි: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
