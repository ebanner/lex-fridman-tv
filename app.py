from flask import Flask, Response

from datetime import datetime


app = Flask(__name__)


START_STRING = "2026-01-18T15:21:37.690583"

START = datetime.fromisoformat(START_STRING)

VIDEOS = [
    {
        "id": "14OPT6CcsH4",
        "length": 13938
    },
    {
        "id": "Z-FRe5AKmCU",
        "length": 11179
    }
]

TOTAL_LENGTH = sum(video['length'] for video in VIDEOS)


def get_video_index(offset):
    start = 0
    for i, video in enumerate(VIDEOS):
        if start <= offset <= start+video['length']:
            return i

        start += video_length['length']


def get_offset(video_length=13938):
    elapsed = datetime.now() - START
    seconds_since = elapsed.seconds
    offset = seconds_since % TOTAL_LENGTH
    return offset


@app.get("/")
def index():
    offset = get_offset()
    video_index = get_video_index(offset)

    video = VIDEOS[video_index]

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

    """.replace("{{VIDEO_ID}}", video['id']).replace("{{OFFSET}}", str(offset))

    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

