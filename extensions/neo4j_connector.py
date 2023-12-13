import os

from py2neo import ClientError, DatabaseError, GraphService

ADDRESS = os.environ['ADDRESS']
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']

# based on py2neo client.py
class Neo4j:

    def __init__(self):
        self.service = None
        self.connected = False

    def is_connected(self):
        return self.connected

    def connect(self):    
        try:
            self.service = GraphService(
                address=ADDRESS,
                user=USER,
                password=PASSWORD
            )
        except Exception as ex:
            msg = f"Failed to establish a connection to '{ADDRESS}' with user '{USER}' and the specified password."
            raise ConnectionError(msg) from None

        # print('DBMS connected')
        self.connected = True

    def get_db(self, db_name):
        if not self.is_connected:
            self.connect()

        if db_name not in self.service.keys():
            return 
        else:
            return self.service[db_name]
    
    def get_all_dbs(self):
        # return db that are not system or neo4j
        return list(filter(lambda db_name: db_name not in {'system', 'neo4j'}, self.service.keys()))
    
    def create_db(self, db_name):
        try:
            system = self.service.system_graph
            system.run(f"CREATE DATABASE $name IF NOT EXISTS;", parameters={"name": db_name})
        except ClientError as cex:
            raise cex
        except DatabaseError as dbex:
            raise dbex from None
        
        return self.service[db_name]

    def delete_db(self, db_name):
        try:
            system = self.service.system_graph
            system.run(f"DROP DATABASE $name;", parameters={"name": db_name})
        except ClientError as cex:
            raise cex
        except DatabaseError as dbex:
            raise dbex from None
        
        return True
    ''' 
    def add_uniqueness_constraints(self) -> None:
        """Add uniqueness constraints to the property key 'id' for all basic PROV types.
        We consider ProvActivity, ProvAgent, ProvEntity, ProvBundle to be basic PROV types.
        Parameters
        ----------
        """
        if self.graph_db is None:
            return
        for label in NODE_LABELS.values():
            if "id" not in self.graph_db.schema.get_uniqueness_constraints(label):
                self.graph_db.schema.create_uniqueness_constraint(label, "id")
    '''  