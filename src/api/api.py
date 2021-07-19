from flask import Flask, request, jsonify
import joblib

MODEL_SVM = joblib.load('models/svm.pkl')
MODEL_DECISION_TREE = joblib.load('models/decision_tree.pkl')

MODEL_LABELS = ['BUY', 'SELL', 'HOLD']

HTTP_BAD_REQUEST = 404

@app.route('/')
def app_root():
    return jsonify(status='complete')


@app.route('/predict_svm')
def predict():
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

    label = MODEL_LABELS[label_index[0]]

    return jsonify(status='complete', label=label)

@app.route('/predict_decision_tree')
def predict():
    pass