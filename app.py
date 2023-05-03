from flask import Flask, request, render_template, url_for, Response
from flask.helpers import send_file
import cv2
import os

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("index.html")
	
@app.route('/upload', methods=['POST'])	
def upload():
	image_file = request.files['image']
	if not image_file:
        	return "Please upload an image."
        		
#save the uploaded image in temporary folder
	image_filename = image_file.filename
	image_path = os.path.join('static', 'uploads', image_filename)
	image_file.save(image_path)	
	
#convert the image in pencil sketch
	img = cv2.imread(image_path)
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	inverted_img = 255 - gray_img
	blurred_img = cv2.GaussianBlur(inverted_img, (21,21), 0)
	inverted_blurred_img = 255-blurred_img
	pencil_sketch = cv2.divide(gray_img,inverted_blurred_img, scale=256.0)

# Save the converted image to a temporary file
	sketch_filename = 'sketch_' + image_filename
	sketch_path = os.path.join('static', 'downloads', sketch_filename)
	cv2.imwrite(sketch_path, pencil_sketch)
	
# Delete the temporary image file
	os.remove(image_path)	
	
# Return the converted image as a download
	return send_file(sketch_path, as_attachment=True)
	
if __name__ == "__main__":
	app.run(debug=True)
