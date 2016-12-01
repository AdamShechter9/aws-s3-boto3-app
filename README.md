Full CRUD operations on an AWS S3 bucket.
This is written in Python using amazon's boto3 API library.

python aws-s3-app.py

-l			listing all objects in bucket.
-g arg1			generates # (arg1) number of text files with random names.  
-r arg1[arg2...]	reads and prints specified files on the screen.
-u arg1[arg2...]	updated specified files with a new date.
-d arg1[arg2...]	deletes specified files and marks deleted.
