from dashboard.routes import app
app.run(debug=True)

from flask import Flask
app = Flask(__name__, static_folder='dashboard/static', template_folder='dashboard/templates')

