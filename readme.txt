#	Devilry Sort

##	About
Program goes through all folders downloaded from Devilry, moves the last delivery up to user_root directory, which is also renamed to user_id only. Rest of deliveries is either stored in a new folder 'older' or removed based upon options parameters. Run with [-l]og option is recommended if debug is needed.


##	Usage

```
python sort_deliveries.py [options] path
Options: -bhlkvz || -b -h -l -k -v -z
 -b -- bare move, no rename of user folder
 -h -- shows this menu
 -l -- creates a log file for what happens
 -d -- delete the other files and folders
 -v -- loud about what happens
 -z -- unzips the .zip file in path first
```

##	Example:

```
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
```

Run command: ```sort_deliveries -zl assignment1```
Will turn into:

```
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
```
