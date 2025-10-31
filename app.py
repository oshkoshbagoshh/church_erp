from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret key"  # TODO: replace with actual key

toolbar = DebugToolbarExtension(app)


# app.config["DEBUG"] = True


# index view
@app.route("/")
def index():
    return render_template("index.html")



# sandbox
@app.route("/sandbox")
def sandbox():
    return render_template("sandbox.html")



if __name__ == "__main__":
    app.run(debug=True)

