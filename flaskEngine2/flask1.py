from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "flaskApp1 is Online"

# This handles the dynamic sub-pages for this specific engine
@app.route('/fa/<id>')
def sub_page(id):
    return f"<h1>Engine 1</h1><p>Displaying data for {id}</p>"

if __name__ == '__main__':
    # Running on port 5001
    app.run(port=5001, debug=True)