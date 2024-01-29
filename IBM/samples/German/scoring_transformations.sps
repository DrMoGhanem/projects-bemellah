***scoring_transformations.sps***.

/**** Export the transformations ****.

TMS BEGIN
    /DESTINATION OUTFILE='file specification'.
    
* Recode Age into a categorical variable.
RECODE Age
     ( MISSING = -9 )
     ( LO THRU 37 =1 )
     ( LO THRU 43 =2 )
     ( LO THRU 49 =3 )
     ( LO THRU HI = 4 ) INTO Age_Group.

* The Amount distribution is skewed, so take the log of it.
COMPUTE Log_Amount = ln(Amount).

TMS END.

/**** Merge the transformations with the model ****.

TMS MERGE
	/DESTINATION OUTFILE='file specification'
	/TRANSFORMATIONS INFILE='file specification'
	/MODEL INFILE='file specification'.
