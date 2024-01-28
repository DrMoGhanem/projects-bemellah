***scoring.sps***.

/**** Get data to be scored ****.

GET FILE='file specification'.


/**** Read in the XML model files ****.

MODEL HANDLE NAME=mregression FILE='file specification'.
      
MODEL HANDLE NAME=tree FILE='file specification'.


/**** Apply the model to the data ****.

COMPUTE PredCatReg = ApplyModel(mregression,'predict').
COMPUTE PredCatTree = ApplyModel(tree,'predict').


* Compute comparison variable.
COMPUTE ModelsAgree = PredCatReg=PredCatTree.


/**** Save sample results ****.

SAVE OUTFILE='file specification'.
