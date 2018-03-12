#!/bin/python2
'''
    Author: Jorge Hevia - jmhev@outlook.com
    What does this script do?: the script checks the
    replication state and attemps to repair it if needed
'''
from sys import argv
from commands import getoutput as cmd
import re

master = {'host': argv[1], 'user': argv[2], 'pass': argv[3]}
slave = {'user': argv[4], 'pass': argv[5]}

io = cmd("mysql -u" + slave['user'] + " -p" + slave['pass'] +
         " -e \"show slave status\G;\" | grep -i Slave_SQL_Running")

io_error = cmd("mysql -u" + slave['user'] + " -p" + slave['pass'] +
               " -e \"show slave status\G;\" | grep -i Last_IO_Error")

sql = cmd("mysql -u" + slave['user'] + " -p" + slave['pass'] +
          " -e \"show slave status\G;\" | grep Slave_IO_Running")

master_pos = cmd("mysql -u" + master['user'] +
                 " -p" + master['pass'] +
                 " -h " + master['host'] +
                 " -e \"show master status\G;\"\
                                 | grep Position")
master_pos = int(re.findall(r'\d+', str(master_pos))[0])

slave_pos = cmd("mysql -u" + slave['user'] +
                " -p" + slave['pass'] +
                " -e \"show slave status\G;\"\
                                 | grep Read_Master_Log_Pos")

slave_pos = int(re.findall(r'\d+', str(slave_pos))[0])

# Checks if the replication is running fine
if "Yes" in io and "Yes" in sql:
    while master_pos != slave_pos:
        slave_pos = int(re.findall(r'\d+',
                                   cmd("mysql -u" + slave['user'] +
                                       " -p" + slave['pass'] +
                                       " -e \"show slave status\G;\"\
                                 | grep Read_Master_Log_Pos")))
    print("All fine!")
else:
    print("There are errors")
    print(io_error)
