***Modify the following CD command to specify the Samples folder
   of the application installation directory,
   using the conventions for your operating system.

CD '/installdir/Samples'.


***oms_bootstrapping.sps***.

PRESERVE.
SET TVARS NAMES.

***first OMS command just suppresses Viewer output***.
OMS /DESTINATION VIEWER=NO /TAG='suppressall'.

DATASET DECLARE bootstrap_example.

***select regression coefficients tables and write to data file***.
***Note that DIMNAMES values vary based on output language***.
***/COLUMNS SEQUENCE=[R2 C1] will achieve the same result in all languages***.

OMS /SELECT TABLES
    /IF COMMANDS=['Regression'] SUBTYPES=['Coefficients']
    /DESTINATION FORMAT=SAV OUTFILE='bootstrap_example'
   /COLUMNS DIMNAMES=['Variables'  'Statistics']
   /TAG='reg_coeff'.

***define a macro to draw samples with replacement and run Regression commands***.
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

***insert any valid path\data file name***.
GET FILE='Employee data.sav'.

***Call the macro, and specify number of samples, dependent variable, and independent variables***.
regression_bootstrap 
   samples=100
   depvar=salary 
   indvars=salbegin  jobtime .

OMSEND.

DATASET ACTIVATE bootstrap_example.

***Variable names here indvar variable names with***.
*** "_B" and "_Beta" appended to end of variable names***.
FREQUENCIES
  VARIABLES=salbegin_B salbegin_Beta jobtime_B jobtime_Beta
  /FORMAT NOTABLE
  /PERCENTILES= 2.5 97.5
  /HISTOGRAM NORMAL.

RESTORE.
