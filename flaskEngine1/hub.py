from flask import Flask, render_template, abort

app = Flask(__name__)

# The Registry: Maps Data ID to a Template AND a Logic Engine (FlaskAppX)
fa_registry = {
    "1": {
        "engine": "flaskApp1.py", # Options Logic
        "temp": "grid.html", 
        "title": "XXXX Strategy", 
        "payload": {"Price": 22.85, "Target": 30.00, "IV": "High"}
    },
    "2": {
        "engine": "flaskApp2.py", # Task/Work Logic
        "temp": "tasks.html", 
        "title": "Field Work", 
        "payload": ["Pry Rocks", "Crossbow Maintenance"]
    },
    "3": {
        "engine": "flaskApp3.py", # Historical Archive
        "temp": "base.html", 
        "title": "Trade Lore", 
        "payload": "Chipping the tip on volatility spikes."
    }
}

@app.route('/')
def main_hub():
    # Extract unique engine names dynamically from the registry values
    # This creates a sorted list: ['flaskApp1.py', 'flaskApp2.py', ...]
    dynamic_engines = sorted(list(set(page['engine'] for page in fa_registry.values())))
    
    return render_template('index.html', registry=fa_registry, engines=dynamic_engines)

@app.route('/fa/<id>')
def generate_page(id):
    data = fa_registry.get(id)
    if not data:
        abort(404)
    
    # Logic: f( {FA_n} ) -> Template(temp) + Context(engine)
    return render_template(data['temp'], fa=data, id=id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
