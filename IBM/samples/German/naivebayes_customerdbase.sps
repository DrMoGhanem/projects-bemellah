***Modify the following CD command to specify the Samples folder
   of the application installation directory,
   using the conventions for your operating system.

CD '/installdir/Samples'.

GET FILE='customer_dbase.sav'.


* Should use SELECTPRED outputs as inputs
*.
NAIVEBAYES response_01 
  BY addresscat callcard callid callwait card card2 churn 
      commutecarpool confer ebill edcat equip forward internet 
      multline owngame ownipod ownpc spousedcat tollfree voice
  WITH cardmon ed equipmon equipten lncardmon lntollmon 
      pets_saltfish spoused tollmon tollten
  /SUBSET NOSELECTION
  /SAVE PREDPROB.


* Compute predicted response using probability > 30% and crosstabulate
*.
COMPUTE predresponse = PredictedProbability_2 > 0.30 .
EXECUTE .

CROSSTABS
  /TABLES=response_01  BY predresponse
  /FORMAT= AVALUE TABLES
  /CELLS= COUNT
  /COUNT ROUND CELL .



