#!/bin/bash

sed -i '/server.default_listen_address=0.0.0.0/s/^#//' /etc/neo4j/neo4j.conf
# Add the necessary lines to the neo4j.conf file
echo 'dbms.security.procedures.unrestricted=gds.*' >> /etc/neo4j/neo4j.conf
echo 'dbms.security.procedures.allowlist=gds.*' >> /etc/neo4j/neo4j.conf

./../usr/bin/neo4j-admin dbms set-initial-password $PASSWORD
./../usr/bin/neo4j start

status_code=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:7474/)
while [ $status_code -ne 200 ]; do
    status_code=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:7474/)
done

mv /neo4j-graph-data-science-2.5.6.jar /var/lib/neo4j/plugins/

./../usr/bin/neo4j restart

status_code=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:7474/)
while [ $status_code -ne 200 ]; do
    status_code=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:7474/)
done

python ./app.py
