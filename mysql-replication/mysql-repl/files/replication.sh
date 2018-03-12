#!/bin/sh
# Author: Jorge Hevia - jmhev@outlook.com
# What does this script do?: the script checks the replication state and attemps to repair it if needed
SLAVE_PASS = $5
SLAVE_USER = $4
MASTER_PASS = $3
MASTER_USER = $2
MASTER_HOST = $1

IO=$(mysql -u SLAVE_USER -p SLAVE_PASS -e "show slave status\G;" grep -i Slave_IO_Running)
SQL=$(mysql -u SLAVE_USER -p SLAVE_PASS -e "show slave status\G;" grep -i Slave_SQL_Running)

