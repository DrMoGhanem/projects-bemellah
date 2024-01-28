***Modify the following CD command to specify the Samples folder
   of the application installation directory,
   using the conventions for your operating system.

CD '/installdir/Samples'.

GET FILE='stroke_valid.sav'.


*Identify Unusual Cases.
DETECTANOMALY /VARIABLES
  CATEGORICAL=agecat gender active obesity diabetes bp af smoker choles
  angina mi nitro anticlot tia time doa rankin0 catscan clotsolv dhosp result
  surgery rehab rankin1 rankin2 rankin3 barthel1 barthel2 barthel3 recbart1
  recbart2 recbart3 stroke1 stroke2 stroke3
  SCALE=los_rehab cost
  ID=patid
 /PRINT ANOMALYLIST NORMS ANOMALYSUMMARY REASONSUMMARY CPS
 /SAVE ANOMALY(AnomalyIndex) PEERID(PeerId) PEERSIZE(PeerSize)
  PEERPCTSIZE(PeerPctSize) REASONVAR(ReasonVar) REASONMEASURE(ReasonMeasure)
  REASONVALUE(ReasonValue) REASONNORM(ReasonNorm)
 /HANDLEMISSING APPLY=YES CREATEMISPROPVAR=YES
 /CRITERIA PCTANOMALOUSCASES=2 ANOMALYCUTPOINT=NONE MINNUMPEERS=1
  MAXNUMPEERS=15 NUMREASONS=3.


*
* A plot that provides an interesting visualization of the results
*.
GRAPH
  /SCATTERPLOT(BIVAR)=ReasonMeasure_1 WITH AnomalyIndex BY PeerId
  /MISSING=LISTWISE .
