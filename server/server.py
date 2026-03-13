#!/usr/bin/env python3
from flask import Flask, request, render_template_string
import os
import subprocess

app = Flask(__name__)

# -------------------------------
# CONFIG
# -------------------------------
VOCALS = "/home/radio/music/w-vocals"
NOVOCALS = "/home/radio/music/no-vocals"
CURRENT = "/home/radio/current_song.txt"
VOLUME_FILE = "/home/radio/volume.txt"

# Ensure volume file exists
if not os.path.exists(VOLUME_FILE):
    with open(VOLUME_FILE, "w") as f:
        f.write("16384")  # default volume for mpg123

# -------------------------------
# HTML TEMPLATE
# -------------------------------
PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Katherine's Little Radio</title>

<style>
body{
    font-family:-apple-system,BlinkMacSystemFont,sans-serif;
    background:#fae6a5;
    color:white;
    text-align:center;
    padding:20px;
}
h1{margin-bottom:25px; color:black;}
.card{
    background:#4d3925;
    border-radius:12px;
    padding:20px;
    margin:20px auto;
    max-width:420px;
}
button{
    width:100%;
    padding:15px;
    font-size:18px;
    border-radius:10px;
    border:none;
    margin-top:10px;
    color:white;
}
.upload{background:#2ecc71;}
.youtube{background:#9b59b6;}
.skip{background:#e67e22;}
input[type=range]{
    width:100%;
    margin-top:10px;
}
input,select{
    width:100%;
    padding:10px;
    margin-top:10px;
    border-radius:8px;
    border:none;
    font-size:16px;
}
.song{
    font-size:20px;
    margin-top:10px;
}
</style>
</head>

<body>

<h1>📻 Katherine's Little Radio</h1>

<div class="card">
<h2>Now Playing</h2>
<div class="song">{{song}}</div>
</div>

<div class="card">
<h2>Volume</h2>
<input type="range" min="0" max="32768" value="{{volume}}" id="volumeSlider" oninput="setVolume(this.value)">
</div>

<div class="card">
<h2>Upload Song</h2>
<form method="POST" action="/upload" enctype="multipart/form-data">
<input type="file" name="file" accept=".mp3" required>
<select name="playlist">
<option value="vocals">Vocals</option>
<option value="novocals">No Vocals / Jazz</option>
</select>
<button class="upload">Upload</button>
</form>
</div>

<div class="card">
<h2>Add from YouTube</h2>
<form method="POST" action="/youtube">
<input name="url" placeholder="Paste YouTube link" required>
<select name="playlist">
<option value="vocals">Vocals</option>
<option value="novocals">No Vocals / Jazz</option>
</select>
<button class="youtube">Add</button>
</form>
</div>

<div class="card">
<h2>Controls</h2>
<button class="skip" onclick="skipSong()">Skip Song</button>
</div>

<script>
function skipSong() {
    fetch('/skip', {method: 'POST'})
    .then(response => alert("Song skipped!"))
    .catch(err => alert("Error skipping song"));
}

function setVolume(val){
    fetch('/volume', {
        method:'POST',
        headers:{'Content-Type':'application/x-www-form-urlencoded'},
        body:'volume=' + val
    });
}
</script>

</body>
</html>
"""

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def index():
    song="Nothing playing"
    if os.path.exists(CURRENT):
        try:
            with open(CURRENT) as f:
                song=f.read().strip()
        except:
            pass
    try:
        with open(VOLUME_FILE) as f:
            volume = f.read().strip()
    except:
        volume = "16384"
    return render_template_string(PAGE, song=song, volume=volume)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    playlist = request.form.get("playlist")
    if not file:
        return "No file uploaded", 400

    folder = VOCALS if playlist=="vocals" else NOVOCALS
    filepath = os.path.join(folder, file.filename)
    file.save(filepath)

    return """
    <!DOCTYPE html>
    <html>
    <head><meta http-equiv="refresh" content="2; url=/" /></head>
    <body>
    ✅ Uploaded to {{playlist}} playlist!<br>
    Returning to main page...
    </body>
    </html>
    """.replace("{{playlist}}", playlist)

@app.route("/youtube", methods=["POST"])
def youtube():
    url = request.form.get("url")
    playlist = request.form.get("playlist")
    folder = VOCALS if playlist=="vocals" else NOVOCALS

    subprocess.Popen([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--no-playlist",
        "-o", folder + "/%(title)s.%(ext)s",
        url
    ])

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="3; url=/" />
        <title>Added to Playlist</title>
        <style>
            body { font-family: -apple-system,BlinkMacSystemFont,sans-serif; background:#111; color:white; text-align:center; padding:50px; }
            h1 { margin-bottom:20px; }
        </style>
    </head>
    <body>
        <h1>✅ Added to playlist!</h1>
        <p>Allow 2-3 minutes for the song to become available on the radio.</p>
        <p>Returning to main page...</p>
    </body>
    </html>
    """

@app.route("/skip", methods=["POST"])
def skip():
    os.system("pkill mpg123")
    return "", 200

@app.route("/volume", methods=["POST"])
def volume():
    vol = request.form.get("volume")
    try:
        int(vol)  # validate
        with open(VOLUME_FILE, "w") as f:
            f.write(vol)
    except:
        pass
    return "", 200

# -------------------------------
# RUN SERVER
# -------------------------------

app.run(host="0.0.0.0", port=80)
