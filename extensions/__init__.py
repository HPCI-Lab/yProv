# https://stackoverflow.com/questions/55523299/best-practices-for-persistent-database-connections-in-python-when-using-flask
from .neo4j_connector import Neo4j
from .init_files import initialize_files

neo4j = Neo4j()
initialize_files()
