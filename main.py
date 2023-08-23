import os
import cv2
from flask import Flask, render_template,request, flash, redirect, url_for
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "aOCEINksdfhER#092d9012#E#ID"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp','jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename} ")
    img = cv2.imread(f"uploads/{filename}")

    match operation:
        case 'cgray':
            imgProcessed=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename=f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            flash(f"Image coverted successfully and is available at uploads folder")
            return newFilename
    
        case 'webp':
            newFilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            flash(f"Image coverted successfully and is available at uploads folder")
            return newFilename
    
        case 'cjpg':
            newFilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            flash(f"Image coverted successfully and is available at uploads folder")
            return newFilename
    
        case 'cpng':
            newFilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            flash(f"Image coverted successfully and is available at uploads folder")
            return newFilename
    

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html') 

@app.route("/edit", methods=['GET','POST'])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error 1"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'error no selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImage(filename, operation)
            return render_template('index.html')
  


app.run(debug=True, port=5001)