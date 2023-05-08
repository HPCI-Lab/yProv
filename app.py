from flask import Flask
from extension import neo4j

from documents import documents_bp
from elements import elements_bp
from relations import relations_bp


app = Flask(__name__)
neo4j.connect()

# load the endpoints
PRE = "/api/v0/"
app.register_blueprint(documents_bp, url_prefix=PRE+'documents')
app.register_blueprint(elements_bp, url_prefix=PRE+'documents/<string:doc_id>/elements')
app.register_blueprint(relations_bp, url_prefix=PRE+'documents/<string:doc_id>/relations')

'''
    host, port + neo4j conf variables devo metterle come env var
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=105)