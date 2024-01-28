***oms_bootstrapping.sps***.
***falls c:\temp kein gültiger Pfad ist, bitte mit einem gültigen Pfad ersetzen***.

PRESERVE.
SET TVARS NAMES.

***erster OMS Befehl unterdrückt die Viewer Ausgabe***.
OMS /DESTINATION VIEWER=NO /TAG='suppressall'.

***wählt Tabelle der Regressionskoeffizienten aus und schreibt in eine Datedatei***.
***Bitte beachten, dass die Werte von DIMNAMES je nach Ausgabesprache variieren***.
***/COLUMNS SEQUENCE=[R2 C1] ergibt gleiches Ergebnis in allen Sprachen***.

OMS /SELECT TABLES
    /IF COMMANDS=['Regression'] SUBTYPES=['Coefficients']
    /DESTINATION FORMAT=SAV OUTFILE='c:\temp\temp.sav'
   /COLUMNS DIMNAMES=['Variables'  'Statistics']
   /TAG='reg_coeff'.

***Makrodefinition zum Ziehen einer Stichprobe mit Zurücklegen und ausführen des Regression Befehls***.
DEFINE regression_bootstrap (samples=!TOKENS(1)
                                           /depvar=!TOKENS(1)
                                           /indvars=!CMDEND)
                                          
COMPUTE dummyvar=1.
AGGREGATE
  /OUTFILE = * MODE = ADDVARIABLES
  /BREAK=dummyvar
  /filesize=N.
!DO !other=1 !TO !samples
SET SEED RANDOM.
WEIGHT OFF.
FILTER OFF.
DO IF $casenum=1.
- COMPUTE #samplesize=filesize.
- COMPUTE #filesize=filesize.
END IF.
DO IF (#samplesize>0 and #filesize>0).
- COMPUTE sampleWeight=rv.binom(#samplesize, 1/#filesize).
- COMPUTE #samplesize=#samplesize-sampleWeight.
- COMPUTE #filesize=#filesize-1.
ELSE.
- COMPUTE sampleWeight=0.
END IF.
WEIGHT BY sampleWeight.
FILTER BY sampleWeight.
REGRESSION
  /STATISTICS COEFF
  /DEPENDENT !depvar
  /METHOD=ENTER !indvars.
!DOEND
!ENDDEFINE.

***gültigen Pfad und Dateinamen angeben***.
GET FILE='c:\Program Files\SPSS\Bankangestellte.sav'.

*** Makroaufruf und Angabe des Stichprobenumfangs, abhängiger Variabel und unabhängigen Variablen***.
regression_bootstrap 
   samples=100
   depvar=gehalt 
   indvars=agehalt  dauer .

OMSEND.

GET FILE 'c:\temp\temp.sav'.

***Variablennamen hier indvar Variablennamen mit***.
*** "_B" and "_Beta" am Ende des Variablennamen angefügt***.
FREQUENCIES
  VARIABLES=agehalt_B agehalt_Beta dauer_B dauer_Beta
  /FORMAT NOTABLE
  /PERCENTILES= 2.5 97.5
  /HISTOGRAM NORMAL.

RESTORE.
