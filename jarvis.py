from flask import Flask, render_template, jsonify
import datetime
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # In a real app, you would fetch real weather here.
    # We are using a random number as a placeholder.
    now = datetime.datetime.now().strftime("%H:%M:%S")
    temp = random.randint(18, 30) 
    return jsonify({'time': now, 'temperature': temp})

if __name__ == '__main__':
    # Running on local host
    app.run(debug=True, port=5000)
