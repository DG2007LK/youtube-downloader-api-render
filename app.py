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

    # YouTube Bot Detection මඟහරවා ගැනීමට නවතම extractor arguments
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'mweb']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # කෝඩ් එක වඩාත් ස්ථාවර කිරීමට direct extract
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
        error_msg = str(e)
        if "Sign in" in error_msg or "bot" in error_msg:
            # IP බ්ලොක් වූ විට විකල්ප මැසේජ් එකක් හෝ fallback එකක් ලබා දීම
            return jsonify({
                'success': False, 
                'error': 'YouTube සර්වර් එක මඟින් මෙම IP ලිපිනය තාවකාලිකව වළකා ඇත. කරුණාකර වෙනත් ලින්ක් එකක් උත්සාහ කරන්න.'
            }), 500
        return jsonify({'success': False, 'error': f'දෝෂයකි: {error_msg}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
