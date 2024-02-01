import os
import json


def initialize_files():
    if not os.path.exists("conf"):
        os.makedirs("conf")

    if not os.path.exists("conf/accounts.json"):
        with open("conf/accounts.json", 'w') as fp:
            json.dump({}, fp)

    if not os.path.exists("conf/blacklist"):
        file = open('conf/blacklist', 'w')
        file.close()

    if not os.path.exists("conf/graphs.json"):
        with open("conf/graphs.json", 'w') as fp:
            json.dump({}, fp)
