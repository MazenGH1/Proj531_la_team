from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1 style='color:red'>Quiz app</h1>"

app.run()