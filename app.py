from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def baixar(url, formato):
    base_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
        'retries': 5,
        'nocheckcertificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36'
        }
    }

    # 🔑 cookies (se existir arquivo)
    if os.path.exists("cookies.txt"):
        base_opts['cookiefile'] = "cookies.txt"

    if formato == "mp3":
        ydl_opts = {
            **base_opts,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    elif formato == "mp4":
        ydl_opts = {
            **base_opts,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }

    else:
        raise Exception("Formato inválido")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        if formato == "mp3":
            filename = filename.rsplit(".", 1)[0] + ".mp3"

        return filename


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    formato = data.get("format")

    try:
        file = baixar(url, formato)
        return jsonify({"ok": True, "file": file})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
