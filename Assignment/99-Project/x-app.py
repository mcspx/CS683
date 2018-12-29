import time
import json
import redis

from flask import Flask, render_template, make_response
#from flask_socketio import SocketIO
from time import time
from random import random

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'TUCS2018@secret!'
    
cache = redis.Redis(host='redis', port=6379)

#socketio = SocketIO(app)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

def get_hit_count():
    retries = 5

    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc

            retries -= 1
            time.sleep(0.5)

#@socketio.on('message')
#def handle_message(message, methods=['GET', 'POST']):
    #send(message)
#    print('received message: ' + message)
#    socketio.emit('message', message, callback=messageReceived)

#@socketio.on('party')
#def handle_party(json):
#    send(json, json=True)
#    print('received json: ' + str(json))

@app.route('/')
def live():
    #count = get_hit_count()
    #return 'Hello from Docker ! I have been seen {} times.\n'.format(count)
    # ส่งตามเวลาได้ไหม
    legend = 'Thailand political party popular'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]

    return render_template('index.html', values=values, labels=labels, legend=legend)

@app.route("/live-data")
def live_data():
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route("/chart")
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)

@app.route("/line_chart")
def line_chart():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('line_chart.html', values=temperatures, labels=times, legend=legend)

@app.route("/time_chart")
def time_chart():
    legend = 'Temperatures'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = [time(hour=11, minute=14, second=15),
             time(hour=11, minute=14, second=30),
             time(hour=11, minute=14, second=45),
             time(hour=11, minute=15, second=00),
             time(hour=11, minute=15, second=15),
             time(hour=11, minute=15, second=30),
             time(hour=11, minute=15, second=45),
             time(hour=11, minute=16, second=00),
             time(hour=11, minute=16, second=15),
             time(hour=11, minute=16, second=30),
             time(hour=11, minute=16, second=45),
             time(hour=11, minute=17, second=00),
             time(hour=11, minute=17, second=15),
             time(hour=11, minute=17, second=30),
             time(hour=11, minute=17, second=45),
             time(hour=11, minute=18, second=00),
             time(hour=11, minute=18, second=15),
             time(hour=11, minute=18, second=30)]
    return render_template('time_chart.html', values=temperatures, labels=times, legend=legend)

if __name__ == "__main__":
#   socketio.run(app, debug=True)
    app.run(host="0.0.0.0", debug=True)
