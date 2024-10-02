from flask import Flask, render_template, request
from scrap import scrap

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data=[], items=0)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    currency = request.form.get('currency')
    system = request.form.get('system')
    # Llama a tu función de web scraping con el parámetro de búsqueda
    data = scrap(query, currency, system)
    return render_template('index.html', data=data, items=len(data))

if __name__ == '__main__':
    app.run(debug=True)