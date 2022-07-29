# CoursePlanner

A script to plan your enrollment automatically by finding all possible sections combinations of the desired courses that do not have clashing times. A significant amount of pre-processing is needed, which can be automated but is quite tedious, due to lack of standardization in course schedules released by unverisities.

## Usage

### Inputs
The script takes two main inputs:
1. Your desired courses (at the end of the file)
2. A .csv file of all available courses with specific columns (check columns and required preprocessing below)

### Outputs

* A file named "working.csv" will be generated in the working directory, with the course names as the column headers, and the section number for each column as the row data
* Each row is one valid combination
* Labs and Lectures of the same courses are counted as a single course, therefore, requires no further tweaking

### Requirements

* Run `pip install pandas` to install pandas, and simply run the file after changing your desired courses, and input file

### Input File Format and Pre-processing

* The input file must be a .csv with the following columns: Course, Type, Section, Day, StartTimeNum, EndTimeNum (image shown below)
![File Columns](https://i.imgur.com/lmG1RKI.png)

* Type must be one of: LEC or LAB
* Section must be a non negative integer
* Day must be a non-spaced combo of the following: M, T, W, Th, F
* StartTimeNum and EndTimeNum are decimal representations of the class timings. You can use any calculation that comes to mind, as long as it is consistent across all rows
* In this version, the following formula on Google Sheets was used: =TIMEVALUE(TIME(time_hour_integer,time_minute_integer,0))*60
* time_hour_integer,time_minute_integer represent the hour and minute of the starting/ending time respectively, in 24 hour format
* Check on every row if ending time num is greater than starting time num. If it is not, there was a mistake made in the preprocessing. The class cannot end before it starts.
* Make sure after pre-processing, change the input file name on Line 178
* ***You can use RegEx on Google Sheets to extract the hour and minute integer values from the course schedules***

## TODO
* Allow user to input courses from command line
* Automate pre-preprocessing routine
