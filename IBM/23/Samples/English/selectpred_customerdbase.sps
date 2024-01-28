***Modify the following CD command to specify the Samples folder
   of the application installation directory,
   using the conventions for your operating system.

CD '/installdir/Samples'.

GET FILE='customer_dbase.sav'.


* First run.  Toss in all variables except the other response variables and the customer ID variable.
*.
SELECTPRED response_01 
  /EXCEPT VARIABLES=custid response_02 response_03
  /MISSING USERMISSING=INCLUDE. 


* Widen search criteria so selected list includes more variables with p-value < 0.05.
* Also show first 10 unselected predictors
*.
SELECTPRED response_01 
  /EXCEPT VARIABLES=custid response_02 response_03
  /SCREENING PCTMISSING=80
  /CRITERIA SIZE=50 SHOWUNSELECTED=10
  /MISSING USERMISSING=INCLUDE. 


