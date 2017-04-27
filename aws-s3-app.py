"""
Adam Shechter
Dec 1 2016

Python
CRUD implementation and testing of AWS S3 API.
uses boto3

python aws-s3-app.py -flag arg1 [arg2, arg3]

n  	number of new txt files to randomly 
flags:
-l  list the buckets
-g  generate and upload N new text files (followed by N)
-r 	download and print objects listed
-u  update files given
-d  delete the objects listed
"""

import boto3
import string
import random
from uuid import uuid1
import sys
import os
from datetime import datetime


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generateRandomTextFile(myBucket):
    try:
        fileCount += 1
    except UnboundLocalError:
        fileCount = 1

    uuidString = uuid1()
    filename = id_generator()+'.txt'
    with open(filename, "w") as f:
        f.write("filename: "+filename+" \n")
        f.write("File Count: "+str(fileCount)+" \n")
    print("new file "+str(filename)+" uploaded")
    myBucket.upload_file(filename, filename)
    os.remove(filename)


def printObjectListing(myBucket):
    objectListing = myBucket.objects.all()
    counter=0
    for obj in objectListing:
        counter+=1
        print(obj)
    print("total count: "+str(counter))


def readTextFiles(myBucket, fileNames):
    for currFile in fileNames:
        print("current file: "+currFile)
        try:
            myBucket.download_file(currFile, "s3-dwnld-"+currFile)
            print("file contents:")
            with open("s3-dwnld-"+currFile, 'r') as f:
                data = f.readlines()
                for line in data:
                    print(line)
            os.remove("s3-dwnld-"+currFile)
        except:
            print("Error. Skipping file.")


def deleteTextFiles(myBucket, fileNames):
    for currFile in fileNames:
        print("deleting current file: "+currFile)
        try:
            delObj = myBucket.Object(currFile)
            response = delObj.delete()
            print(response)
        except:
            print("Error. skipping file.")


def updateTextFile(myBucket, fileNames):
    for currFile in fileNames:
        print("updating current file: "+currFile)
        rightNow = datetime.now()
        try:
            myBucket.download_file(currFile, "s3-"+currFile)
            with open("s3-"+currFile, 'a') as f:
                f.write("File updated at ")
                f.write(str(rightNow))
                f.write("\n")
            myBucket.upload_file("s3-"+currFile, currFile)
            os.remove("s3-"+currFile)
        except:
            e = sys.exc_info()[0]
            print("Error.  Skipping file")
            print(e)


def main(argv):
    try:
        flag = sys.argv[1]
    except IndexError:
        print("Missing flag for operations.  -l -r -g -d -u")
        return
    argsList = sys.argv[2:]
    if flag in ('-r', '-d', '-u'):
        fileNames = argsList
        print("fileNames")
        print(fileNames)
    elif flag == '-g':
        fileTimes = int(argsList[0])
        print("filetimes: "+str(fileTimes))
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket('s3testing-development-adam')

    if flag == '-l':
        printObjectListing(s3bucket)
    elif flag == '-r':
        if fileNames:
            readTextFiles(s3bucket, fileNames)
    elif flag == '-g':
        for i in range(fileTimes):
            generateRandomTextFile(s3bucket)
    elif flag == '-d':
        if fileNames:
            deleteTextFiles(s3bucket, fileNames)
    elif flag == '-u':
        if fileNames:
            updateTextFile(s3bucket, fileNames)
    else:
        print("flag error detected.  -l -r -g -d -u")


if __name__ == "__main__":
    main(sys.argv)