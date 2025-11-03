from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config["DEBUG"] = True

name = "Pai Church ERP"

app.config["SECRET_KEY"] = "secret key"  # TODO: replace with actual key

toolbar = DebugToolbarExtension(app)

# index view
@app.route("/")
def index():
    return render_template("index.html")





# sandbox
@app.route("/sandbox")
def sandbox():
    return render_template("sandbox.html")


# dashboard view
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)

