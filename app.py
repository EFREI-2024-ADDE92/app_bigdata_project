from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model_filename = 'model/knn_model.joblib'
knn_model = joblib.load(model_filename)

@app.route('/predict', methods=['POST'])
def prediction_endpoint():
    try:
        data = request.get_json(force=True)
        features = np.array(data['features']).reshape(1, -1)

        prediction = knn_model.predict_endpoint(features)

        return jsonify({'prediction': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)})

#@app.route('/')
#def home():
#    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)