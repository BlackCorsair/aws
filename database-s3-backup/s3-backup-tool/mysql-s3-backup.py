#!/opt/s3upload/venv/bin/python3
import subprocess
import sys

'''
    Name: Backup
    Function: this class contains the functions and
        variables to make a dump from a given DB
        and then upload it to a S3 bucket
'''


class Backup:
    database = ""
    bucket = ""
    user = ""
    password = ""
    node = ""
    file = ""

    # inits the object with default values
    def __init__(self):
        self.database = ""
        self.bucket = ""
        self.user = ""
        self.password = ""
        # gets the hostname to diferenciate the backups
        self.node = subprocess.getoutput("hostname")

    # prints a help screen showing how to use the script
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

           mysql-s3-backup.sh -u root -p nein \
-d usersdb -b s3-bucket-backups

        #######################
            """)
    '''
        Name: GetVariables
        Input: nothing
        Output: nothing
        Function: given a user input while launching
            the script, the function saves the input
            into the class variables. If there're no
            variables missing, the script goes on and
            if at least one variable is missing, it will
            show the help screen
    '''

    def GetVariables(self):
        argv = sys.argv
        if len(argv) == 9:
            for i, arg in enumerate(argv):
                if '-d' == arg:
                    self.database = argv[i + 1]
                if '-b' == arg:
                    self.bucket = argv[i + 1]
                if '-u' == arg:
                    self.user = argv[i + 1]
                if '-p' == arg:
                    self.password = argv[i + 1]
            # once it validates the input, continues to
            # create the dump
            self.MySQLDump()
            # once the dump is finished, it uploads it
            # to S3
            self.UploadS3()
        else:
            self.Help()

    '''
        Name: MySQLDump
        Input: nothing
        Output: nothing
        Function: given the class variables, executes the
            mysqldump program with them and then compress
            the dump with gzip
    '''

    def MySQLDump(self):
        date = subprocess.getoutput("date +%Y%m%d-%H%M")
        self.file = "/tmp/" + date + "-" + self.database\
            + "-" + self.node + ".sql.gz"
        call = "mysqldump -u" + \
            str(self.user) + " -p" + str(self.password) + \
            " " + str(self.database) + " | gzip > " + self.file
        subprocess.call(call, shell=True, stdout=subprocess.DEVNULL)

    '''
        Name: UploadS3
        Input: nothing
        Output: nothing
        Function: uploads the gziped dump into a S3 bucket
            specified by the input
    '''

    def UploadS3(self):
        check = "cat " + self.file
        while(subprocess.call(check, shell=True,
                              stdout=subprocess.DEVNULL) != 0):
            print("please be patient...")
        call = "aws s3 cp " + self.file + " s3://" + self.bucket
        subprocess.call(call, shell=True, stdout=subprocess.DEVNULL)

# gets the script running


if __name__ == '__main__':
    baker = Backup()
    baker.GetVariables()
