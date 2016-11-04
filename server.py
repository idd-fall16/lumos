from flask import Flask, render_template
# import play_audio as pa
import threading
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/lookout")
def alert():
  # pa.play_audio('owl.mp3')
  return 'hoot'

# @app.route("/heatmap")
# def heatmap():
#     return render_template("heatmap.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")