GET
  FILE='C:\Program Files\SPSS\tutorial\sample files\demo.sav'.
FREQUENCIES
  VARIABLES=schulab  /ORDER=  ANALYSIS .
CROSSTABS
  /TABLES=palm  BY geschl  BY internet
  /FORMAT= AVALUE TABLES
  /CELLS= COUNT EXPECTED ROW .
FREQUENCIES
  VARIABLES=heirat  /ORDER=  ANALYSIS .
