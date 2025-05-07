from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
from werkzeug.utils import secure_filename
from hough import hough_transform

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', demo=True)

@app.route('/upload', methods=['GET', 'POST'])

def upload():
    if request.method == "GET":
        return render_template("index.html", demo=False)
    if request.method == "POST":
        file = request.files["image"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        divisions = int(request.form.get("divisions", 180))
        max_lines = int(request.form.get("max_lines", 5))
        freq_threshold = int(request.form.get("freq_threshold", 100))
        rho_thresh = int(request.form.get("rho_thresh", 20))
        theta_thresh = float(request.form.get("theta_thresh", np.pi/90))
        max_gap = int(request.form.get("max_gap", 5))

        output1_path, output2_path = hough_transform(
            filepath,
            divisions=divisions,
            max_lines=max_lines,
            freq_threshold=freq_threshold,
            rho_thresh=rho_thresh,
            theta_thresh=theta_thresh,
            max_gap=max_gap
        )
        return render_template("result.html", output1=output1_path, output2=output2_path)


@app.route('/back')
def back():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
