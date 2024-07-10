#!/usr/bin/python3
from . import create_app

if __name__ == "__main__":
    """Main Function"""
    host = '0.0.0.0'
    port = '5000'
    app = create_app()
    app.run(debug=True, host=host, port=port, threaded=True)
