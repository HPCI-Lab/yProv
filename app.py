from flask import Flask

from extension import neo4j
from routes import documents_bp
from routes import elements_bp
from routes import relations_bp

# create app
app = Flask(__name__)

# load the endpoints
PRE = "/api/v0/"
app.register_blueprint(documents_bp, url_prefix=PRE+'documents')
app.register_blueprint(elements_bp, url_prefix=PRE+'documents/<string:doc_id>/elements')
app.register_blueprint(relations_bp, url_prefix=PRE+'documents/<string:doc_id>/relations')

# connect to neo4j service
neo4j.connect()

# run
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=105)