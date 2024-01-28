***Modify the following CD command to specify the Samples folder
   of the application installation directory,
   using the conventions for your operating system.

CD '/installdir/Samples'.

GET FILE='bankloan.sav'.


* 
* First set the random seed and select about
* 70% of the cases for model building
*.
SET SEED 9191972.

IF ($casenum < 701) training = rv.bernoulli(.7) .
EXECUTE .


* use subset
*.
NAIVEBAYES default
  /EXCEPT VARIABLES=preddef1 preddef2 preddef3 training
  /TRAININGSAMPLE VARIABLE=training
  /SAVE PREDVAL PREDPROB.


* produce a means table and crosstabulation to look at the 
* distributions of predictors by PredictedValue
*.
MEANS
  TABLES=employ address debtinc creddebt  BY PredictedValue
  /CELLS MEAN COUNT STDDEV  .

CROSSTABS
  /TABLES=ed  BY PredictedValue
  /FORMAT= AVALUE TABLES
  /CELLS= COUNT ROW
  /COUNT ROUND CELL .
