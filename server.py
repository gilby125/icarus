# new relic ping
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

import os
from flask import Flask, render_template, request, abort, jsonify, url_for
from threading import Thread
import icarus

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async
def get_async_data(f, t, days):
    icarus.main(f, t, days)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    url_for('static', filename='viz.js')
    # f = request.args['f'] or 'BOS'
    # t = request.args['t'] or 'LAX'
    # days = request.args['days'] or 3
    f = 'BOS'
    t = 'LAX'
    days = 10
    if ('f' in request.args):
        f = request.args['f']
        print('f: ' + request.args['f'])
    if ('t' in request.args):
        t = request.args['t']
        print('t: ' + request.args['t'])
    if ('days' in request.args):
        days = int(request.args['days'])
        print('days: ' + str(request.args['days']))

    get_async_data(f, t, days)
    return '_'.join([f,t,str(days)])
    # return jsonify(**{'name': data['name'], 'data': data['data']})
    # get_async_data(f, t, days)

@app.route('/data/<name>.json')
def show_data(name):
    data = icarus.find(name)
    if data:
        return jsonify(**data)
    else:
        abort(404)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, port=port, host='0.0.0.0')