#	Devilry Sort

## DISCLAIMER
Be careful when running program - do not run except in a folder you *CAN STAND TO LOOSE THE CONTENTS OF*. This program utilizes the ```rm``` without prompting user in order to remove certain files.

##	About
Program goes through all folders downloaded from Devilry, moves the last delivery up to user_root directory, which is also renamed to user_id only (unless specified not to). Rest of deliveries is either stored in a new folder 'older' or removed based upon options parameters. Running with [-l]og to create a log file of what happens is recommended.

##	Usage

```
Usage: python sort_deliveries.py [options] path
Mandatory: path
      path -- the mandatory argument which is the output folder to have all user directories within when script is done
Options: -b -c -d -D -h -l -v -z [zipfile]
        -b -- bare move, no rename of user folder
        -c -- runs javac on each user, and prints those that fail
        -d -- delete the other files and folders
        -D -- DEBUG mode, program will not execute
        -h -- shows this menu
        -l -- creates a log file for what happens
        -v -- loud about what happens
        -z -- unzips the .zip file in path first (if only 1 is present)
-z zipfile -- unzipz the specified zip file in path first
Example usages
python sort_deliveries -z ~/Downloads/deliveries.zip .
Above command will first unzip the 'deliveries.zip' into current folder, and then sort all files
--
python sort_deliveries -z ~/Downloads/deliveries.zip ~/assignments/assignment1
Above command will first unzip the 'deliveries.zip' into the folder at '$HOME/assignments/assignment1/' before sorting said directory
--
python sort_deliveries .
Above command will sort deliveries from current directory - it should contain a SINGLE folder representing the first folder received when unzipping.
```

##	Example:

I start with an empty directory called ```assignemnts```:

```
assignemnts/
```

I have downloaded the zipfile ```deliveries.zip``` which is in the ```Downloads``` folder at home.
This zip file contains the work of 3 users - a regular ```unzip ~/Downloads/deliveries.zip``` could give the following tree from Devilry:

```
assignemnts/
-assignment1/
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
-----delivery2/
------file.java
------readme.txt
```

If instead run with this script using the following (explained) command:
```python sort_deliveries -z ~/Downloads/deliveries.zip .```
* ```python sort_deliveries``` runs the script
* ```-z ~/Downloads/deliveries.zip``` tells the script to un(z)ip the file ```~/Downloads/deliveries.zip```
* and into directory ```.``` -- which means current directory.

Ultimately it turns into:

```
assignemnts/
-assignment1/
--deliveries.zip
--log.txt
--user1/
---file1.java
---file2.java
---file3.java
---older/
----deadline1/
-----delivery1/
------file1.java
------file2.java
--user2/
---file1.java
--user3/
---file.java
---readme.txt
---older/
----deadline1/
-----delivery1/
------file1.java
------file2.java
------file3.java
```
