#!/bin/python2
'''
    Author: Jorge Hevia - jmhev@outlook.com
    What does this script do?: the script checks the
    replication state and attemps to repair it if needed
'''
from sys import argv
from commands import getoutput as cmd
import re

'''
    Name: checkStatus
    Inputs: none
    Output: 1 if correct execution, -1 if error
    Function: checks the master and slave status in the MySQL DB
'''


def checkStatus():
    master = {'host': argv[1], 'user': argv[2], 'pass': argv[3]}
    slave = {'user': argv[4], 'pass': argv[5]}

    io = cmd("mysql -u" + slave['user'] + " -p" + slave['pass'] +
             " -e \"show slave status\G;\" | grep -i Slave_SQL_Running")

    io_error = cmd("mysql -u" + slave['user'] + " -p" + slave['pass'] +
                   " -e \"show slave status\G;\" | grep -i Last_IO_Error")

    sql = cmd("mysql -u" + slave['user'] + " -p" + slave['pass'] +
              " -e \"show slave status\G;\" | grep Slave_IO_Running")

    # Checks if the replication is running fine
    if "Yes" in io and "Yes" in sql:
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

        while master_pos != slave_pos:
            slave_pos = int(re.findall(r'\d+',
                                       cmd("mysql -u" + slave['user'] +
                                           " -p" + slave['pass'] +
                                           " -e \"show slave status\G;\"\
                                     | grep Read_Master_Log_Pos")))
            print('Syncing...')
        print("All fine!")
        return 1
    else:
        print("There are errors")
        restoreReplication()


'''
    Name: restoreReplication
    Inputs: none
    Output: none
    Function: dumps the DB from the
'''


def restoreReplication():
    master = {'host': argv[1], 'user': argv[2], 'pass': argv[3]}
    slave = {'user': argv[4], 'pass': argv[5]}
    m_con = "mysql -u" + master['user'] + "-p" + \
        master['pass'] + " -h " + master['host'] + " "
    s_con = "mysql -u" + slave['user'] + "-p" + \
        slave['pass'] + " "
    # lock master
    # cmd(m_con + "-e \"FLUSH TABLES WITH READ LOCK;\"")
    # get log and log_pos
    m_status = cmd(m_con + "-e \"show master status\G;\"")
    m_status = re.findall(r'\d+', m_status)
    # get mysqldump
    cmd("mysqldump -u" + master['user'] + "-p" +
        master['pass'] + " -h " + master['host'] +
        " --all-databases > dump.sql")
    # unlocks master
    cmd(m_con + " -e \"UNLOCK TABLES;\"")

    # stop slave
    cmd(s_con + "-e \"STOP SLAVE;\"")
    # import dump
    cmd(s_con + " < dump.sql")
    # start slave
    cmd(s_con + "-e \"START SLAVE;\"")
    checkStatus()


'''
    Name: help
    Inputs: none
    Output: help and usage information
    Function: shows help and usage information
'''


def help():
    print('Use the program as follows:')
    print('./replication.py <master_host> <master_mysql_user> <master_mysql_pass \
        <slave_mysql_user> <slave_mysql_pass>')


if __name__ == '__main__':
    if '-h' in argv[1] or '--help' in argv[1]:
        help()
    elif len(argv) != 6:
        help()
    else:
        checkStatus()
