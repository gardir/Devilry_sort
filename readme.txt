usr@host:~/path/ $ python sort_deliveries.py [options] path
Usage:
python sort_deliveries.py [options] path
Options:
-h -- shows this menu
-z -- unzip


Program goes through all folders downloaded from Devilry, moves the last delivery up to user_root/ directory, removes rest of files and directories, and rename user_root to uio_id.

Example:

~/
-sort_deliveries.py
-assignment1/
--deliveries.zip
---user1 (111)/
----deadline1/
-----delivery1/
------file1.java
------file2.java
-----delivery2/
------file1.java
------file2.java
------readme.txt
---user2 (112)/
----deadline1/
-----delivery1/
------file1.java
---user3 (131)/
----deadline1/
-----delivery1/
------file1.java
------file2.java
------file3.java
-----delivery2/
------file.java
------readme.txt

Run command: sort_deliveries -z assignment1
Will turn into:
~/
-sort_deliveries.py
-assignment1/
--deliveries.zip
--user1/
---file1.java
---file2.java
---file3.java
--user2/
---file1.java
--user3/
---file.java
---readme.txt
