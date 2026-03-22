from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "flaskApp2 is Online"

@app.route('/fa/<id>')
def sub_page(id):
    return f"<h1>Engine 2</h1><p>Displaying data for {id}</p>"

if __name__ == '__main__':
    # Running on port 5002
    app.run(port=5002, debug=True)