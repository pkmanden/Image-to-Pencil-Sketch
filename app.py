import os
from flask import request, Flask, render_template, send_from_directory
from werkzeug.utils import secure_filename
import cv2



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SKETCH_FOLDER'] = 'sketches'


@app.route('/uploads/<filename>')
def upload_img(filename):
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/sketches/<filename>')
def sketch_img(filename):
    
    return send_from_directory(app.config['SKETCH_FOLDER'], filename)


def get_sketch(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    invert_img = cv2.bitwise_not(gray_image)
    blur_img = cv2.GaussianBlur(invert_img, (111, 111), 0)
    inv_blur_img = cv2.bitwise_not(blur_img)
    sketch = cv2.divide(gray_image, inv_blur_img, scale=256)
    
    return sketch

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    # About page
    return render_template('about.html')


@app.route('/view', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        # Save the file to uploads folder
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        file_name=os.path.basename(file_path)
        
        # reading the uploaded image
        img = cv2.imread(file_path)
        
        sketch_fname = file_name.split('.')[0] + "_sketch.jpg"
        sketch_img = get_sketch(img)
        sketch_path = os.path.join(
            basepath, 'sketches', secure_filename(sketch_fname))
        fname = os.path.basename(sketch_path)
        # save sketch 
        cv2.imwrite(sketch_path,sketch_img)
        
        return render_template('view.html',file_name=file_name, sketch_file=fname)
    return ""


if __name__ == '__main__':
        app.run(debug=True, host="localhost", port=8080)