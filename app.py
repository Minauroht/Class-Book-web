from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/checking')
def checking():
    return render_template('checking.html')


if __name__ == "__main__":
    app.run(port=0, host='0.0.0.0', debug=True)
