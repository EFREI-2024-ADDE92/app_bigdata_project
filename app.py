from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import sklearn
import os

# Get the absolute path to the 'knn_model.joblib' file
model_path = os.path.join(os.path.dirname(__file__), 'model/knn_model.joblib')
print(model_path)

print('sklearn: {}'.format(sklearn.__version__))

# 0 : setosa
# 1 : versicolor 
# 2 : virginica

app = Flask(__name__)

model_filename = 'model/knn_model.joblib'
knn_model = joblib.load(model_path)

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            features = np.array(data.get('features', [])).reshape(1, -1)

            prediction = knn_model.predict(features)

            pred_fleur = ""

            if int(prediction[0]) == 0:
                pred_fleur = "setosa"
            elif int(prediction[0]) == 1:
                pred_fleur = "versicolor"
            else:
                pred_fleur = "virginica"

            return jsonify({'prediction': pred_fleur})

        except ValueError:
            return jsonify({'error': 'Invalid JSON or feature data'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)