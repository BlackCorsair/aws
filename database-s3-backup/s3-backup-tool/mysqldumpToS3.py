#!/opt/s3upload/venv/bin/python3
from subprocess import call
from subprocess import DEVNULL
from subprocess import getoutput
from time import sleep
import argparse

'''
 TO-DO:
    * IMPLEMENT LOGS
    * IMPLEMENT CHECKSUM
    * IMPLEMENT DOCKER VERIFICATION???
'''


class SimpleStorageService:
    bucket = ""

    def __init__(self, bucket):
        assert(bucket != ""), "bucket can't be empty"
        self.bucket = bucket

    def upload(self, file):
        assert(file != ""), "file can't be empty"
        check = "cat {}".format(file)
        self.fileExist(check)
        command = "aws s3 cp {} s3://{}".format(file, self.bucket)
        call(command, shell=True, stdout=DEVNULL)
        call("rm {}".format(file), shell=True, stdout=DEVNULL)

    def fileExist(self, check):
        while(call(check, shell=True, stdout=DEVNULL)):
            print("[INFO]: Waiting until the dump is done")
            sleep(10)


class MySQL:
    user = ""
    password = ""
    database = ""

    def __init__(self, user, password, database):
        self.user = user
        self.password = password
        self.database = database

    def dump(self):
        date = getoutput("date +%Y%m%d-%H%M")
        node = getoutput("hostname")
        file = "/tmp/{}-{}-{}.sql.gz".format(date,
                                             self.database,
                                             node)
        command = "mysqldump -u{} -p{} {} | gzip > {}".format(
            self.user, self.password, self.database, file)
        call(command, shell=True, stdout=DEVNULL)
        return file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Uploads a MySQL\
     database to AWS S3')
    parser.add_argument('-u', '--user', required=True,
                        help="enter the mysql user")
    parser.add_argument('-p', '--pass', required=True,
                        help="enter the mysql user password")
    parser.add_argument('-d', '--database', required=True,
                        help="enter the mysql database to be dumped")
    parser.add_argument('-b', '--bucket', required=True,
                        help="enter the S3 bucket where\
                         the dump will be uploaded")
    parser.add_argument('-f', '--file', required=False,
                        help="[OPTIONAL]: enter the file where\
                         the temporary dump will be saved")
    parser.add_argument('--dry-run', required=False, help="shows the\
     commands that will be executed without being executed")
    args = parser.parse_args()

    # TO-DO: implement dry-run

    mySQL = MySQL(args.user, args.password, args.database)

    # TO-DO: implement choose file
    dumpFile = mySQL.dump()

    s3 = SimpleStorageService(args.bucket)
    s3.upload(dumpFile)
    print("[INFO]: ended without errors")
