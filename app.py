import os

from flask import Flask

from extensions import neo4j
from routes import documents_bp
from routes import elements_bp
from routes import entities_bp
from routes import activities_bp
from routes import agents_bp
from routes import relations_bp

PORT = os.environ['PORT']

# create app
app = Flask(__name__)

# load the endpoints
# PRE = "/api/v0/"
app.register_blueprint(documents_bp)  # url_prefix=PRE+'documents')
app.register_blueprint(elements_bp)  # url_prefix=PRE+'documents/<string:doc_id>/elements')
app.register_blueprint(entities_bp)  # url_prefix=PRE+'documents/<string:doc_id>/entities')
app.register_blueprint(activities_bp)  # url_prefix=PRE+'documents/<string:doc_id>/activities')
app.register_blueprint(agents_bp)  # url_prefix=PRE+'documents/<string:doc_id>/agents')
app.register_blueprint(relations_bp)  # url_prefix=PRE+'documents/<string:doc_id>/relations')

# connect to neo4j service
neo4j.connect()

# run
if __name__ == '__main__':
    app.run()
