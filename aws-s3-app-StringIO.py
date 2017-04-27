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
-g  generate and upload new text file
-r 	download and print objects listed
-d  delete the objects listed
"""

import boto3
import string
import random
import io
import sys
import os
from datetime import datetime


def generateKeyFile(myBucket, key, text):
    print("Generating: Key: {}      Text: {}".format(key, text))
    print(text, type(text))
    src_obj = io.BytesIO(text)
    keyobj = myBucket.Object(key)
    print("Uploading obj")
    keyobj.upload_fileobj(src_obj)
    src_obj.close()
    print("Retrieving obj")
    trgt_obj = io.BytesIO()
    keyobj.download_fileobj(trgt_obj)
    data = trgt_obj.getvalue()
    trgt_obj.close()
    print(data, type(data))
    return


def printObjectListing(myBucket):
    objectListing = myBucket.objects.all()
    outList = []
    for obj in objectListing:
        print(obj.key)
        outList.append(obj.key)
    return outList

def readTextFiles(myBucket, fileNames):
    for currFile in fileNames:
        print("current key: "+currFile)
        try:
            trgt_obj = io.BytesIO()
            keyobj  = myBucket.Object(currFile)
            keyobj.download_fileobj(trgt_obj)
            print("file contents:")
            data = trgt_obj.getvalue()
            print(data)
            trgt_obj.close()
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



def main(argv):
    try:
        flag = sys.argv[1]
    except IndexError:
        print("Missing flag for operations.  -l -g -d -u")
        return
    argsList = sys.argv[2:]
    if flag in ('-r', '-d'):
        keyNames = argsList
        print("fileNames")
        print(keyNames)
    elif flag == '-g':
        key = argsList[0]
        text = argsList[1]
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket('s3testing-development-adam')

    if flag == '-l':
        printObjectListing(s3bucket)
    elif flag == '-r':
        if keyNames:
            readTextFiles(s3bucket, keyNames)
    elif flag == '-g':
        generateKeyFile(s3bucket, key, text)
    elif flag == '-d':
        if keyNames:
            deleteTextFiles(s3bucket, keyNames)

    else:
        print("flag error detected.  -l -r -g -d")


if __name__ == "__main__":
    main(sys.argv)