#!/bin/bash

add_or_update_line() {
    local line_to_add="$1"
    local neo4j_conf_path="$2"

    # Check if the line already exists in the file
    if grep -q "^$line_to_add" "$neo4j_conf_path"; then
        return  # Line already exists, no changes needed.
    else
        # Check if the line is commented
        if grep -q "^#.*$line_to_add" "$neo4j_conf_path"; then
            # Uncomment the line
            sed -i "s/^#\(.*$line_to_add\)/\1/" "$neo4j_conf_path"
        else
            # Check if the line is present without the value after the equal sign
            if grep -q "^$(echo $line_to_add | cut -d'=' -f1)=" "$neo4j_conf_path"; then
                # Complete the line by adding the missing part after the equal sign
                sed -i "s/^\($(echo $line_to_add | cut -d'=' -f1)=\)/$line_to_add/" "$neo4j_conf_path"
            else
                # Add the line to the file
                echo "$line_to_add" >> "$neo4j_conf_path"
            fi
        fi
    fi
}

sed -i '/server.default_listen_address=0.0.0.0/s/^#//' /etc/neo4j/neo4j.conf
# Add the necessary lines to the neo4j.conf file
# echo 'dbms.security.procedures.unrestricted=gds.*' >> /etc/neo4j/neo4j.conf
# echo 'dbms.security.procedures.allowlist=gds.*' >> /etc/neo4j/neo4j.conf

add_or_update_line "dbms.security.procedures.unrestricted=gds.*" "/etc/neo4j/neo4j.conf"
add_or_update_line "dbms.security.procedures.allowlist=gds.*" "/etc/neo4j/neo4j.conf"

./../usr/bin/neo4j-admin dbms set-initial-password $PASSWORD
./../usr/bin/neo4j start

status_code=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:7474/)
while [ $status_code -ne 200 ]; do
    status_code=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:7474/)
done

python ./app.py
