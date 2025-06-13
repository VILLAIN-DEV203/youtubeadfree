from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os
import uuid

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "✅ YouTube Downloader API is running!"}

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")
    quality = data.get("quality")

    if not url or not quality:
        return JSONResponse(status_code=400, content={"error": "Missing URL or quality"})

    formats = {
        "4k": "bestvideo[height<=2160]+bestaudio/best",
        "2k": "bestvideo[height<=1440]+bestaudio/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "audio": "bestaudio"
    }

    if quality not in formats:
        return JSONResponse(status_code=400, content={"error": "Invalid quality"})

    os.makedirs("downloads", exist_ok=True)
    uid = str(uuid.uuid4())
    output_template = f"downloads/{uid}.%(ext)s"

    ydl_opts = {
        "format": formats[quality],
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }] if quality == "audio" else [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if quality == "audio":
                file_path = file_path.rsplit(".", 1)[0] + ".mp3"
            else:
                file_path = file_path.rsplit(".", 1)[0] + ".mp4"
        return FileResponse(file_path, filename=os.path.basename(file_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
