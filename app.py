from flask import Flask
from extension import neo4j

from documents import documents_bp
from entities import entities_bp
from agents import agents_bp
from activities import activities_bp
from relations import relations_bp


app = Flask(__name__)
neo4j.connect()

# load the endpoints
PRE = "/api/v0/"
app.register_blueprint(documents_bp, url_prefix=PRE+'documents')
app.register_blueprint(entities_bp, url_prefix=PRE+'documents/<string:doc_id>/entities')
app.register_blueprint(agents_bp, url_prefix=PRE+'documents/<string:doc_id>/agents')
app.register_blueprint(activities_bp, url_prefix=PRE+'documents/<string:doc_id>/activities')
app.register_blueprint(relations_bp, url_prefix=PRE+'documents/<string:doc_id>/relations')

'''
    host, port + neo4j conf variables devo metterle come env var
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=105)