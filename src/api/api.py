from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)
        
MODEL_SVR = joblib.load('src/api/models/SVR.pkl')
MODEL_NU_SVR = None
MODEL_LINEAR_SVR = None
MODEL_SVC = joblib.load('src/api/models/SVC.pkl')
MODEL_SVC_SUMMARY = joblib.load('src/api/models/SVC_SUMMARY.pkl')
MODEL_NU_SVC = None
MODEL_LINEAR_SVC = None

MODEL_DECISION_TREE_CLASSIFIER = joblib.load('src/api/models/DecisionTreeClassifier.pkl')

MODEL_SVC_LABELS = ['BUY', 'SELL', 'HOLD']

HTTP_BAD_REQUEST = 404

HOME_LABEL = 'public/home.html'

@app.route('/')
def app_root():
    return render_template(HOME_LABEL)

@app.route('/svc_predict')
def svc_predict():
    open_price = request.args.get('open_price')
    high_price = request.args.get('high_price')
    low_price = request.args.get('low_price')
    close_price = request.args.get('close_price')

    features = [[open_price, high_price, low_price, close_price]]

    try:
        label_index = MODEL_SVC.predict(features)
    except Exception as err:
        message = (f'Failed to score the model. Exception: {err}')
        
        response = jsonify(status='error', error_message=message)
        response.status_code = HTTP_BAD_REQUEST

        return response

    label = label_index[0]

    return jsonify(status='complete', label=f"{'BUY' if label == 1 else 'SELL' if label == 0 else label}")

# TODO: Create a route to get svc stats
@app.route('/svc_stats')
def get_svc_stats():
    return jsonify(status='complete', label=MODEL_SVC_SUMMARY)

@app.route('/linear_svc_predict')
def linear_svc_predict():
    return jsonify(status='complete')

@app.route('/nu_svc_predict')
def nu_svc_predict():
    return jsonify(status='complete')

@app.route('/svr_predict')
def svr_predict():
    return jsonify(status='complete')

@app.route('/linear_svr_predict')
def linear_svr_predict():
    return jsonify(status='complete')

@app.route('/nu_svr_predict')
def nu_svr_predict():
    return jsonify(status='complete')

@app.route('/decision_tree_predict')
def predict_decision_tree():
    close_price = request.args.get('close_price')
    macd = request.args.get('macd')
    signal_line = request.args.get('signal_line')
    rsi = request.args.get('rsi')
    ema = request.args.get('ema')
    sma = request.args.get('sma')

    features = [[close_price, macd, signal_line, rsi, ema, sma]]

    try:
        label_index = MODEL_DECISION_TREE_CLASSIFIER.predict(features)
    except Exception as err:
        message = (f'Failed to score the model. Exception: {err}')
        
        response = jsonify(status='error', error_message=message)
        response.status_code = HTTP_BAD_REQUEST

        return response

    label = label_index[0]

    return jsonify(status='complete', label=f"{'BUY' if label == 1 else 'SELL' if label == 0 else label}")

@app.route('/decision_tree_stats')
def get_decision_tree_stats():
    return jsonify(status='complete')

def server_run(debug=True, host='127.0.0.1', port=5000):
    app.run(debug=debug, host=host, port=port, threaded=True)