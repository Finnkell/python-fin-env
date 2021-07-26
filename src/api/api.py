from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
        
MODEL_SVM = joblib.load('src/api/models/SVR.pkl')

MODEL_LABELS = ['BUY', 'SELL', 'HOLD']

HTTP_BAD_REQUEST = 404

@app.route('/')
def app_root():
    return jsonify(status='complete')


@app.route('/predict_svm')
def predict_svm():
    open_price = request.args.get('open_price')
    high_price = request.args.get('high_price')
    low_price = request.args.get('low_price')
    close_price = request.args.get('close_price')

    features = [[open_price, high_price, low_price, close_price]]

    try:
        label_index = MODEL_SVM.predict(features)
    except Exception as err:
        message = (f'Failed to score the model. Exception: {err}')
        
        response = jsonify(status='error', error_message=message)
        response.status_code = HTTP_BAD_REQUEST

        return response

    label = label_index[0]

    return jsonify(status='complete', label=f"{'BUY' if label == 1 else 'SELL' if label == 0 else label}")

@app.route('/svm_stats')
def get_svm_stats():
    pass

@app.route('/predict_decision_tree')
def predict_decision_tree():
    pass


def server_run(debug=True, host='127.0.0.1', port=5000):
    app.run(debug=debug, host=host, port=port, threaded=True)