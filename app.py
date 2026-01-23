import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, Response, redirect

load_dotenv()


app = Flask(__name__)


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


START_STRING = "2026-01-18T15:21:37.690583"

START = datetime.fromisoformat(START_STRING)


def get_total_length():
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/total_youtube_duration",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }
    )

    total_length = response.json()

    return total_length


TOTAL_LENGTH = get_total_length()


def get_video(offset):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/get_video_by_offset",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "target_offset": offset
        }
    )

    video, = response.json()
    return video


def get_offset():
    elapsed = datetime.now() - START
    seconds_since = int(elapsed.total_seconds())
    offset = seconds_since % TOTAL_LENGTH
    return offset


def get_video_offset(video, offset):
    start_offset = video['end_offset'] - video['duration']
    video_offset = offset - start_offset
    return video_offset


@app.get("/")
def index():
    offset = get_offset()
    video = get_video(offset)
    video_offset = get_video_offset(video, offset)

    html = """

    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Lex Fridman TV</title>
        <style>
        body { margin: 0; display: grid; place-items: center; min-height: 100vh; }
        </style>
    </head>
    <body>
        <iframe
            width="560"
            height="315"
            src="https://www.youtube.com/embed/{{VIDEO_ID}}?start={{OFFSET}}&autoplay=1&mute=1"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen>
        </iframe>
    </body>
    </html>

    """.replace("{{VIDEO_ID}}", video['video_id']).replace("{{OFFSET}}", str(video_offset))

    video_id = video['video_id']
    url = f"https://www.youtube.com/watch?v={video_id}&t={video_offset}"

    return Response(html, mimetype="text/html")


@app.get("/youtube")
def youtube():
    offset = get_offset()
    video = get_video(offset)
    video_offset = get_video_offset(video, offset)
    video_id = video['video_id']
    url = f"https://www.youtube.com/watch?v={video_id}&t={video_offset}"
    return redirect(url)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

