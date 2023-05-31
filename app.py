import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from deepface import DeepFace



app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = 'static/uploads/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the API"
        }
    }), 200

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        image = request.files["image"]
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            result = DeepFace.analyze(image_path, actions=['age', 'gender', 'race', 'emotion'])
            # print(result)
            for res in result:
                race = res['dominant_race']
                gender = res['dominant_gender']
            # for res in result:
            #     print("Race:", res['race'])

            return jsonify({
                "status": {
                    "code": 200,
                    "message": race +", "+ gender,
                    "data": "http://127.0.0.1:5000/" +race+gender
                }
            }), 200
        else:
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "Please upload image with JPG format"
                    
                }
            }), 400
    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed"
            }
        }), 405


if __name__ == "__main__":
    app.run()