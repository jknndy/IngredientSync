from flask import Flask, request, jsonify, render_template
from recipe_scrapers import scrape_me

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = request.form.get('url') if request.method == 'POST' else None

    if url:
        try:
            scraper = scrape_me(url, wild_mode=True)
            result = {
                'success': True,
                'title': scraper.title() or "N/A",
                'host': scraper.host() or "N/A",
                'total_time': scraper.total_time() or "N/A",
                'image': scraper.image() or "N/A",
                'ingredients': scraper.ingredients() or [],
                'instructions': scraper.instructions() or "N/A",
                'instructions_list': scraper.instructions_list() or [],
                'yields': scraper.yields() or "N/A",
                'nutrients': scraper.nutrients() or {},
                'category': scraper.category() or "N/A",
                'cuisine': scraper.cuisine() or "N/A",
                'ratings': scraper.ratings() or {},
                'description': scraper.description() or "N/A",
                'author': scraper.author() or "N/A"
            }
        except Exception as e:  # It's better to catch specific exceptions, but this is a general catch for simplicity.
            result = {'success': False, 'error_message': str(e)}
    else:
        result = {'success': False, 'error_message': 'Please provide a valid URL.'}

    if request.method == 'POST':
        return jsonify(result)
    else:
        return render_template('index.html')

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'success': False, 'error_message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
