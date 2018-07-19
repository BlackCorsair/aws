#!/usr/bin/python3
import subprocess
import sys


class Backup:
    database = ""
    bucket = ""
    user = ""
    password = ""
    node = ""
    file = ""

    def __init__(self):
        self.database = ""
        self.bucket = ""
        self.user = ""
        self.password = ""
        self.node = subprocess.getoutput("hostname")

    def Help(self):
        print(
            """
        #######################
        This script has the following dependencies: awscli boto3
        #######################
           How to use this script:
           -h -> show this message
           -d database -> specifies the database name
           -u user -> specifies the database user
           -p password -> specifies the database user password
           -b bucket -> specifies the S3 bucket name
        @@@@ example @@@@

           mysql-s3-backup.sh -u root -p nein -n pre1\
            -d users -b db-backups -o dbs3.sql

        #######################
            """)

    def GetVariables(self):
        argv = sys.argv
        if len(argv) == 9:
            for i, arg in enumerate(argv):
                if '-d' in arg:
                    self.database = argv[i + 1]
                if '-b' in arg:
                    self.bucket = argv[i + 1]
                if '-u' in arg:
                    self.user = argv[i + 1]
                if '-p' in arg:
                    self.password = argv[i + 1]
            self.MySQLDump()
            self.UploadS3()
        else:
            self.Help()

    def MySQLDump(self):
        date = subprocess.getoutput("date +%Y%m%d-%H%M")
        self.file = "/tmp/" + date + "-" + self.database\
            + "-" + self.node + ".sql"
        call = "mysqldump -u" + \
            str(self.user) + " -p" + str(self.password) + \
            " " + str(self.database) + " > " + self.file
        subprocess.call(call, shell=True, stdout=subprocess.DEVNULL)

    def UploadS3(self):
        check = "cat " + self.file
        while(subprocess.call(check, shell=True,
                              stdout=subprocess.DEVNULL) != 0):
            print("please be patient...")
        call = "aws s3 cp " + self.file + " s3://" + self.bucket
        subprocess.call(call, shell=True, stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    baker = Backup()
    baker.GetVariables()
