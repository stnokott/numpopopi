from flask import Flask, render_template, request

from spotify import Client

app = Flask(__name__)

sp = Client(app.logger)


@app.route("/")
def spotify():
    return render_template("spotify.html")


@app.route("/api/spotify_search")
def spotify_search():
    q = request.args.get("q")
    if not q:
        results = []
    else:
        results = sp.search(q)
    return {"results": results}
