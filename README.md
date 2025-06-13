# YouTube Downloader API (FastAPI)

This is the backend server for downloading YouTube videos in 4K, 2K, 1080p or audio only formats.

## 🚀 Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🔥 POST /download

**Request Body (JSON):**
```json
{
  "url": "https://youtube.com/...",
  "quality": "4k" | "2k" | "1080p" | "audio"
}
```

**Response:** MP4 or MP3 file download.

## ✅ CORS enabled for all origins
