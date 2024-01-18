from flask import Flask, request, jsonify, render_template, Response
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY, CollectorRegistry
import joblib
import numpy as np
import sklearn
import time
import os

print('sklearn: {}'.format(sklearn.__version__))

# 0 : setosa
# 1 : versicolor 
# 2 : virginica

app = Flask(__name__)

model_filename = 'knn_model.joblib'
knn_model = joblib.load(model_filename)

# setting up metrics
custom_registry = CollectorRegistry()

prediction_counter = Counter('predictions_total', 'Total number of predictions', registry=custom_registry)
prediction_duration = Gauge('prediction_duration_seconds', 'Duration of predictions', registry=custom_registry)

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            features = np.array(data.get('features', [])).reshape(1, -1)

            start_time = time.time()

            prediction = knn_model.predict(features)

            # Enregistrez la durée de la prédiction
            prediction_duration.set(time.time() - start_time)

            # Incrémentez le compteur de prédictions
            prediction_counter.inc()

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

@app.route('/metrics')
def metrics():
    return Response(generate_latest(custom_registry), content_type='text/plain; version=0.0.4')

if __name__ == '__main__':
    app.run(debug=True)