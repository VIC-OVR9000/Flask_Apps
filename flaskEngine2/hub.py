import requests
from flask import Flask, render_template

app = Flask(__name__)

# Registry now includes the 'port' where each sub-app lives
fa_registry = {
    "1": {"engine": "flaskApp1.py", "port": 5001, "temp": "grid.html", "title": "Options Alpha"},
    "2": {"engine": "flaskApp2.py", "port": 5002, "temp": "tasks.html", "title": "Field Log"},
}

def get_engine_status(registry):
    statuses = {}
    unique_engines = {page['engine']: page['port'] for page in registry.values()}
    
    for engine, port in unique_engines.items():
        try:
            # We try to hit the root of the sub-app with a 0.5s timeout
            response = requests.get(f"http://127.0.0.1:{port}", timeout=0.5)
            statuses[engine] = "online" if response.status_code == 200 else "offline"
        except:
            statuses[engine] = "offline"
    return statuses

@app.route('/')
def main_hub():
    engine_statuses = get_engine_status(fa_registry)
    dynamic_engines = sorted(list(engine_statuses.keys()))
    
    return render_template('index.html', 
                           registry=fa_registry, 
                           engines=dynamic_engines, 
                           statuses=engine_statuses)

@app.route('/fa/<id>')
def generate_page(id):
    data = fa_registry.get(id)
    if not data:
        abort(404)
    
    # Logic: f( {FA_n} ) -> Template(temp) + Context(engine)
    return render_template(data['temp'], fa=data, id=id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)