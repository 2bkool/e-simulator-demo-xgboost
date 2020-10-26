from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import numpy as np
import xgboost as xgb
import data


Flask.jinja_options.update(
    dict(
        variable_start_string='[[',
        variable_end_string=']]'
    )
)


app = Flask(__name__)
CORS(app)
sio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/target')
def get_target():
    x = data.get_dataframe().index.strftime('%Y-%m-%d').tolist()
    y = data.get_dataframe()[data.TARGET_KEY].tolist()
    return jsonify({'x': x, 'y': y})


@app.route('/features')
def get_features():
    df = data.get_dataframe()
    columns = df.columns.tolist()
    columns.remove(data.TARGET_KEY)
    return jsonify(columns)


@app.route('/feature/<name>')
def get_data_by_feature(name):
    df = data.get_dataframe()
    dates = df.index.tolist()
    values = df[name].tolist()
    stats = df[name].describe().round(2).to_dict()
    return jsonify({'dates': dates, 'values': values, 'stats': stats})


@app.route('/train', methods=['post'])
def train():
    feature_names = request.get_json()
    print(feature_names)
    df = data.get_dataframe()
    feature_names.append(data.TARGET_KEY)
    df = df[feature_names]
    x_train, x_test, y_train, y_test = train_test_split(df)
    xgbr = xgb.XGBRegressor(n_estimators=2000)
    xgbr.fit(x_train, y_train, early_stopping_rounds=400,
             eval_set=[(x_test, y_test)], callbacks=[record])

    print(xgbr.feature_importances_)

    actual = df['2020':][data.TARGET_KEY]
    pred = xgbr.predict(df['2020':].drop(data.TARGET_KEY, axis=1))
    err = np.abs(actual - pred)
    # importances = dict()
    # for k, v in zip(feature_names, xgbr.feature_importances_):
    #     importances[k] = str(v)
    # imporance_sorted = {k: v for k, v in sorted(importances.items(),
    #                     key=lambda item: item[1], reverse=True)}

    return jsonify({
        'date': df['2020'].index.strftime('%Y-%m-%d').tolist(),
        'actual': actual.tolist(),
        'pred': pred.tolist(),
        'err': err.tolist(),
        'mape': np.round(mape(actual, pred), 2),
        'features': feature_names,
        'importances': xgbr.feature_importances_.tolist()
    })


def record(result):
    print(result.model)
    print(type(result.model))
    sio.emit('eval', result.evaluation_result_list[0][1])


def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def train_test_split(df):
    x = df.drop([data.TARGET_KEY], axis=1)
    y = df[data.TARGET_KEY]
    # split_date = '2019-09'
    x_train = x[: '2019-09']
    x_test = x['2019-10': '2019-12']
    y_train = y[: '2019-09']
    y_test = y['2019-10': '2019-12']
    return x_train, x_test, y_train, y_test


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, threaded=True, port=5001)
