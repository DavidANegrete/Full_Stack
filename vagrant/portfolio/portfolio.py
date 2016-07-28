from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/portfolio')
def index():
    return render_template('portfolio.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
