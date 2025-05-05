from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for Jenkins verification"""
    return jsonify({
        'status': 'healthy',
        'message': 'Bookstore API is running'
    }), 200

def create_app():
    return app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)