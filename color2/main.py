from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import brain
import os

upload_folder = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD'] = upload_folder

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        brain.exact_color(img,900,12,5)
        pal = os.path.join(app.config['UPLOAD'], 'palette_result.png')
        return render_template('index.html', img=img, pal=pal)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)


