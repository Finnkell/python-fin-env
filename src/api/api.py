from flask import Flask, request, jsonify, render_template, Response
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError
import os
import joblib

from src.api.error_handler.error_handlers import ErrorHandlers

app = Flask(__name__)

error_handlers = ErrorHandlers()

MODEL_SVR = joblib.load('src/api/models/SVR.pkl')
MODEL_NU_SVR = joblib.load('src/api/models/SVR.pkl')
MODEL_LINEAR_SVR = joblib.load('src/api/models/SVR.pkl')
MODEL_SVC = joblib.load('src/api/models/SVC.pkl')
MODEL_SVC_SUMMARY = joblib.load('src/api/models/SVC_SUMMARY.pkl')
MODEL_NU_SVC = joblib.load('src/api/models/SVC.pkl')
MODEL_LINEAR_SVC = joblib.load('src/api/models/SVC.pkl')
MODEL_DECISION_TREE_CLASSIFIER = joblib.load('src/api/models/DecisionTreeClassifier.pkl')

MODEL_SVC_LABELS = ['BUY', 'SELL', 'HOLD']

HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400

HTTP_INTERNAL_ERROR = 500

HOME_LABEL = 'public/home/home.html'
SVC_LABEL = 'public/svm/svc_home.html'

@app.errorhandler(HTTP_NOT_FOUND)
def page_404_error_handler(e):
    return error_handlers.not_found(error_description=e.description, error_code=HTTP_NOT_FOUND)

@app.errorhandler(HTTP_BAD_REQUEST)
def page_400_error_handler(e):
    return error_handlers.not_found(error_description=e.description, error_code=HTTP_BAD_REQUEST)

@app.errorhandler(HTTP_INTERNAL_ERROR)
def page_500_error_handler(e):
    return error_handlers.not_found(error_description=e.description, error_code=HTTP_INTERNAL_ERROR)

@app.route('/')
def app_root():
    return render_template(HOME_LABEL)

@app.route('/svc_predict')
def svc_predict():

    if len(request.args) == 0:
        return render_template(SVC_LABEL)

    values_list = [request.args.get('open_price'), request.args.get('high_price'), request.args.get('low_price'), request.args.get('close_price')]
    names_list = ['open_price', 'high_price', 'low_price', 'close_price']

    features = [verify_field(values_list, names_list)]

    response_features = features.pop()

    if str(type(response_features)) == "<class 'flask.wrappers.Response'>":
        return response_features

    try:
        label_index = MODEL_SVC.predict(features)
    except Exception as err:
        message = (f'Failed to score the model. Exception: {err}')

        if not 'Content-Type' in request.headers:
            response = jsonify(status='error', error_message=message)
            response.status_code = HTTP_INTERNAL_ERROR

            return response

        raise InternalServerError(description=f'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application. {message}')

    label = label_index[0]

    return jsonify(status='complete', label=f"{'BUY' if label == 1 else 'SELL' if label == 0 else label}")

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
    values_list = [request.args.get('close_price'), request.args.get('macd'), request.args.get('signal_line'), request.args.get('rsi'), request.args.get('ema'), request.args.get('sma')]
    names_list = ['close_price', 'macd', 'signal_line', 'rsi', 'ema', 'sma']

    features = [verify_field(values_list, names_list)]

    response_features = features.pop()

    if str(type(response_features)) == "<class 'flask.wrappers.Response'>":
        return response_features

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


'''
>>> Server methods
'''
def server_run(debug=True, host='127.0.0.1', port=5000):
    app.run(debug=debug, host=host, port=port, threaded=True)

def verify_field(params_field_value=[], params_field_names=[]):
    features = []

    featuresDict = {}

    if len(params_field_value) != len(params_field_names):
        raise('Array size different')

    while len(params_field_names) > 0:
        field_name = params_field_names.pop()

        if request.args.get(field_name) == None:
            if 'Content-Type' in request.headers:
                message = (f'{field_name} field not filled')
            
                response = jsonify({'status': f'error {HTTP_BAD_REQUEST}', 'error_message': message})
                response.status_code = HTTP_BAD_REQUEST

                return response

            raise BadRequest(description=f'The browser (or proxy) sent a request that this server could not understand. Maybe you didn\'t expecify the {params_field_names} field')

        field_value = params_field_value.pop()

        featuresDict[str(field_name)] = field_value

        try:
            field_value = float(field_value)
        except:
            if 'Content-Type' in request.headers:
                message = (f'{field_name} field not filled')
            
                response = jsonify({'status': f'error {HTTP_INTERNAL_ERROR}', 'error_message': message})
                response.status_code = HTTP_INTERNAL_ERROR

                return response

            raise BadRequest(description=f'Cannot convert {field_value} to float')

        features.append(field_value)

    return features.reverse()
