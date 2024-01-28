***oms_percentiles.sps***.

***Generate percentile values for salary and then
   merge those values back into original data file.

***Modify the following CD command to specify the Samples folder
   of the application installation directory,
   using the conventions for your operating system.

CD '/installdir/Samples'.

*pubsmarker:start.
GET
  FILE='Employee data.sav'.
PRESERVE.
SET TVARS NAMES TNUMBERS VALUES.
DATASET DECLARE freq_table.

***split file by job category to get group percentiles.
SORT CASES BY jobcat.
SPLIT FILE LAYERED BY jobcat. 

OMS 
  /SELECT TABLES
  /IF COMMANDS=['Frequencies'] SUBTYPES=['Statistics']
  /DESTINATION FORMAT=SAV
   OUTFILE='freq_table'
  /COLUMNS SEQUENCE=[L1 R2].

FREQUENCIES
  VARIABLES=salary   
  /FORMAT=NOTABLE
  /PERCENTILES= 25 50 75.

OMSEND.

***restore previous  SET settings.
RESTORE.

MATCH FILES FILE=*
  /TABLE='freq_table'
  /rename (Var1=jobcat)
  /BY jobcat
 /DROP command_ TO salary_Missing.
EXECUTE.

