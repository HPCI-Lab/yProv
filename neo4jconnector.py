from py2neo import ClientError, DatabaseError, GraphService

# based on py2neo client.py
class Client:

    def __init__(self):
        self.service = None
        self.connected = False

    @staticmethod
    def create_database(service: GraphService, name: str):
        try:
            system = service.system_graph
            system.run(f"CREATE DATABASE $name IF NOT EXISTS;", parameters={"name": name})
        except ClientError as cex:
            raise cex
        except DatabaseError as dbex:
            raise dbex from None

    @property
    def is_connected(self):
        return self.connected

    def connect(self):
        
        try:
            self.service = GraphService(
                address='localhost:7687',
                scheme='bolt',
                user='neo4j',
                password='password'
            )
            '''
            service = GraphService(
                address=address,
                scheme=scheme,
                user=user,
                password=password
            )
            '''
        except Exception as ex:
            # msg = f"Failed to establish a connection to '{scheme}://{address}' with user '{user}' and the specified password."
            msg = "a"
            raise ConnectionError(msg) from None
        '''
        if dbname not in service.keys():
            # self.create_database(service, dbname)
            return # error

        self.graph_db = service[dbname]
        # self.add_uniqueness_constraints()
        '''
        self.connected = True

    def get_db(self, dbname):
        if not self.is_connected:
            self.connect()

        if dbname not in self.service.keys():
            # self.create_database(service, dbname)
            return # error
        
        return self.service[dbname]


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