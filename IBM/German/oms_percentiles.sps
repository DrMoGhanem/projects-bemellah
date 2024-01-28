***oms_percentiles.sps***.
***falls c:\temp kein gültiger Pfad ist, bitte mit einem gültigen Pfad ersetzen***.
   
*** Erstellen der Perzentilwerte für gehalt und zusammenführen dieser Werte mit der Original Datendatei***.

GET
  FILE='c:\Program Files\spss\Bankangestellte.sav'.
PRESERVE.
SET TVARS NAMES TNUMBERS VALUES.

*** Datei aufteilen nach tätig um Gruppenperzentile zu erhalten***.
SORT CASES BY tätig.
SPLIT FILE LAYERED BY tätig. 

OMS 
  /SELECT TABLES
  /IF COMMANDS=['Frequencies'] SUBTYPES=['Statistics']
  /DESTINATION FORMAT=SAV
   OUTFILE='c:\temp\temp.sav'
  /COLUMNS SEQUENCE=[L1 R2].

FREQUENCIES
  VARIABLES=gehalt   
  /FORMAT=NOTABLE
  /PERCENTILES= 25 50 75.

OMSEND.

***Wiederherstellung der ursprünglichen SET Einstellungen.
RESTORE.

MATCH FILES FILE=*
  /TABLE='c:\temp\temp.sav'
  /rename (Var1=tätig)
  /BY tätig
 /DROP command_ TO gehalt_Missing.
EXECUTE.

