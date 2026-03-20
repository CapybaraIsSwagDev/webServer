# run.py
from app import create_app
from app.development import run
from flask import render_template
import os

app = create_app()


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        run()
    app.run(debug=True,port=8000)
