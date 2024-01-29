***Modify the following CD command to specify the Samples folder
   of the application installation directory,
   using the conventions for your operating system.

CD '/installdir/Samples'.

GET FILE='stroke_invalid.sav'.

* First run the basic checks
*.
* Validate Data.
* Validate Data.
VALIDATEDATA
  VARIABLES=hospsize age agecat gender active obesity diabetes bp af smoker
  choles angina mi nitro anticlot tia time doa rankin0 catscan clotsolv dhosp
  result surgery rehab los_rehab cost rankin1 rankin2 rankin3 barthel1
  barthel2 barthel3 recbart1 recbart2 recbart3
  ID=hospid patid physid
 /VARCHECKS STATUS=ON PCTMISSING=70 PCTEQUAL=95 PCTUNEQUAL=90 CV=0.001
  STDDEV=0
 /IDCHECKS INCOMPLETE DUPLICATE
 /CASECHECKS REPORTEMPTY=YES SCOPE=ALLVARS
 /CASEREPORT DISPLAY=YES MINVIOLATIONS=1 CASELIMIT=FIRSTN(100).


* Next, apply the data dictionary from patient_los.sav and run some standard rules
*.
APPLY DICTIONARY
  /FROM 'patient_los.sav'
  /SOURCE VARIABLES = age agecat gender diabetes bp smoker choles active obesity
  angina mi nitro anticlot time doa clotsolv result cost
  /FILEINFO ATTRIBUTES = REPLACE
  /VARINFO ATTRIBUTES = REPLACE.


* Now validate data according to these rules.
*.
* Delete existing single-variable validation rules.
DATAFILE ATTRIBUTE DELETE=$VD.SRule.
* Delete existing links between variables and rules.
VARIABLE ATTRIBUTE  VARIABLES=ALL  DELETE=$VD.SRuleRef.
* (Re)define single-variable validation rules.
DATAFILE ATTRIBUTE ATTRIBUTE=
      $VD.SRule[1]("Label='0 to 1 Dichotomy', Type='Numeric', Domain='List',"+
 " FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '1' ")
      $VD.SRule[2]("Label='0 to 2 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '1' '2' ")
      $VD.SRule[3]("Label='0 to 3 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '1' '2' '3' ")
      $VD.SRule[4]("Label='1 to 4 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='1' '2' '3' '4' ")
      $VD.SRule[5]("Label='Nonnegative integer', Type='Numeric',"+
 " Domain='Range', Minimum='0', Maximum='', FlagUserMissing='No',"+
 " FlagSystemMissing='Yes', FlagBlank='No', FlagNoninteger='Yes',"+
 " FlagUnlabeled='No' ")
      $VD.SRule[6]("Label='Nonnegative number', Type='Numeric',"+
 " Domain='Range', Minimum='0', Maximum='', FlagUserMissing='No',"+
 " FlagSystemMissing='Yes', FlagBlank='No', FlagNoninteger='No',"+
 " FlagUnlabeled='No' ").
* (Re)define links between variables and rules.
VARIABLE ATTRIBUTE
    VARIABLES=recbart3  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_recbart3_' ")
    /VARIABLES=catscan  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_catscan_' ")
    /VARIABLES=doa  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_doa_'"+
 " ")
    /VARIABLES=gender  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_gender_' ")
    /VARIABLES=dhosp  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_dhosp_'"+
 " ")
    /VARIABLES=angina  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_angina_' ")
    /VARIABLES=smoker  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_smoker_' ")
    /VARIABLES=af  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_af_' ")
    /VARIABLES=tia  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_tia_'"+
 " ")
    /VARIABLES=anticlot  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[3]'"+
 ",OutcomeVar='@0to3Categorical_anticlot_' ")
    /VARIABLES=agecat  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_agecat_' ")
    /VARIABLES=obesity  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_obesity_' ")
    /VARIABLES=clotsolv  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[3]'"+
 ",OutcomeVar='@0to3Categorical_clotsolv_' ")
    /VARIABLES=active  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_active_' ")
    /VARIABLES=age  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[5]'"+
 ",OutcomeVar='Nonnegativeinteger_age_' ")
    /VARIABLES=los_rehab  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[5]'"+
 ",OutcomeVar='Nonnegativeinteger_los_rehab_' ")
    /VARIABLES=cost  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[6]'"+
 ",OutcomeVar='Nonnegativenumber_cost_' ")
    /VARIABLES=result  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_result_' ")
    /VARIABLES=mi  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_mi_' ")
    /VARIABLES=surgery  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[2]'"+
 ",OutcomeVar='@0to2Categorical_surgery_' ")
    /VARIABLES=bp  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[2]',OutcomeVar='@0to2Categorical_bp_'"+
 " ")
    /VARIABLES=diabetes  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_diabetes_' ")
    /VARIABLES=recbart1  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_recbart1_' ")
    /VARIABLES=time  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[5]'"+
 ",OutcomeVar='Nonnegativeinteger_time_' ")
    /VARIABLES=recbart2  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_recbart2_' ")
    /VARIABLES=rehab  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[3]'"+
 ",OutcomeVar='@0to3Categorical_rehab_' ")
    /VARIABLES=nitro  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_nitro_'"+
 " ")
    /VARIABLES=choles  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_choles_' ") .
* 0 to 3 Categorical.
COMPUTE @0to3Categorical_anticlot_ = NOT(ANY(VALUE(anticlot), 0, 1, 2, 3) OR
  (MISSING(anticlot) AND NOT(SYSMIS(anticlot)))) OR SYSMIS(anticlot).
COMPUTE @0to3Categorical_rehab_ = NOT(ANY(VALUE(rehab), 0, 1, 2, 3) OR
  (MISSING(rehab) AND NOT(SYSMIS(rehab)))) OR SYSMIS(rehab).
COMPUTE @0to3Categorical_clotsolv_ = NOT(ANY(VALUE(clotsolv), 0, 1, 2, 3) OR
  (MISSING(clotsolv) AND NOT(SYSMIS(clotsolv)))) OR SYSMIS(clotsolv).
* 0 to 1 Dichotomy.
DO REPEAT #OV=@0to1Dichotomy_obesity_ @0to1Dichotomy_dhosp_
  @0to1Dichotomy_tia_ @0to1Dichotomy_af_ @0to1Dichotomy_nitro_
  @0to1Dichotomy_smoker_ @0to1Dichotomy_active_ @0to1Dichotomy_doa_
  @0to1Dichotomy_mi_ @0to1Dichotomy_gender_ @0to1Dichotomy_catscan_
  @0to1Dichotomy_angina_ @0to1Dichotomy_diabetes_ @0to1Dichotomy_choles_
  /#IV=obesity dhosp tia af nitro smoker active doa mi gender catscan angina
  diabetes choles.
COMPUTE #OV=NOT(ANY(VALUE(#IV), 0, 1) OR (MISSING(#IV) AND NOT(SYSMIS(#IV))))
  OR SYSMIS(#IV).
END REPEAT.
* 1 to 4 Categorical.
DO REPEAT #OV=@1to4Categorical_recbart3_ @1to4Categorical_recbart2_
  @1to4Categorical_recbart1_ @1to4Categorical_agecat_ @1to4Categorical_result_
  /#IV=recbart3 recbart2 recbart1 agecat result.
COMPUTE #OV=NOT(ANY(VALUE(#IV), 1, 2, 3, 4) OR (MISSING(#IV) AND
  NOT(SYSMIS(#IV)))) OR SYSMIS(#IV).
END REPEAT.
* 0 to 2 Categorical.
COMPUTE @0to2Categorical_bp_ = NOT(ANY(VALUE(bp), 0, 1, 2) OR (MISSING(bp)
  AND NOT(SYSMIS(bp)))) OR SYSMIS(bp).
COMPUTE @0to2Categorical_surgery_ = NOT(ANY(VALUE(surgery), 0, 1, 2) OR
  (MISSING(surgery) AND NOT(SYSMIS(surgery)))) OR SYSMIS(surgery).
* Nonnegative number.
COMPUTE Nonnegativenumber_cost_ = NOT(VALUE(cost)>=0 OR (MISSING(cost) AND
  NOT(SYSMIS(cost)))) OR SYSMIS(cost).
* Nonnegative integer.
COMPUTE Nonnegativeinteger_los_rehab_ = NOT(VALUE(los_rehab)>=0 AND
  VALUE(los_rehab)=TRUNC(VALUE(los_rehab)) OR (MISSING(los_rehab) AND
  NOT(SYSMIS(los_rehab)))) OR SYSMIS(los_rehab).
COMPUTE Nonnegativeinteger_time_ = NOT(VALUE(time)>=0 AND
  VALUE(time)=TRUNC(VALUE(time)) OR (MISSING(time) AND NOT(SYSMIS(time)))) OR
  SYSMIS(time).
COMPUTE Nonnegativeinteger_age_ = NOT(VALUE(age)>=0 AND
  VALUE(age)=TRUNC(VALUE(age)) OR (MISSING(age) AND NOT(SYSMIS(age)))) OR
  SYSMIS(age).
* Mark rule outcome variables as such in SPSS data dictionary.
VARIABLE ATTRIBUTE
   VARIABLES=@0to3Categorical_anticlot_  TO Nonnegativeinteger_age_
   ATTRIBUTE=$VD.RuleOutcomeVar("Yes").
VARIABLE LABELS @1to4Categorical_recbart3_  '1 to 4 Categorical:Recoded'+
 ' Barthel index at 6 months'.
VARIABLE LABELS @0to1Dichotomy_catscan_  '0 to 1 Dichotomy:CAT scan result'.
VARIABLE LABELS @0to1Dichotomy_doa_  '0 to 1 Dichotomy:Dead on arrival'.
VARIABLE LABELS @0to1Dichotomy_gender_  '0 to 1 Dichotomy:Gender'.
VARIABLE LABELS @0to1Dichotomy_dhosp_  '0 to 1 Dichotomy:Died in hospital'.
VARIABLE LABELS @0to1Dichotomy_angina_  '0 to 1 Dichotomy:History of angina'.
VARIABLE LABELS @0to1Dichotomy_smoker_  '0 to 1 Dichotomy:Smoker'.
VARIABLE LABELS @0to1Dichotomy_af_  '0 to 1 Dichotomy:Atrial fibrillation'.
VARIABLE LABELS @0to1Dichotomy_tia_  '0 to 1 Dichotomy:History of transient'+
 ' ischemic attack'.
VARIABLE LABELS @0to3Categorical_anticlot_  '0 to 3 Categorical:Taking anti'+
 '-clotting drugs'.
VARIABLE LABELS @1to4Categorical_agecat_  '1 to 4 Categorical:Age category'.
VARIABLE LABELS @0to1Dichotomy_obesity_  '0 to 1 Dichotomy:Obesity'.
VARIABLE LABELS @0to3Categorical_clotsolv_  '0 to 3 Categorical:Clot'+
 '-dissolving drugs'.
VARIABLE LABELS @0to1Dichotomy_active_  '0 to 1 Dichotomy:Physically active'.
VARIABLE LABELS Nonnegativeinteger_age_  'Nonnegative integer:Age in years'.
VARIABLE LABELS Nonnegativeinteger_los_rehab_  'Nonnegative integer:Length of'+
 ' stay for rehabilitation'.
VARIABLE LABELS Nonnegativenumber_cost_  'Nonnegative number:Total treatment'+
 ' and rehabilitation costs in thousands'.
VARIABLE LABELS @1to4Categorical_result_  '1 to 4 Categorical:Treatment'+
 ' result'.
VARIABLE LABELS @0to1Dichotomy_mi_  '0 to 1 Dichotomy:History of myocardial'+
 ' infarction'.
VARIABLE LABELS @0to2Categorical_surgery_  '0 to 2 Categorical:Post-event'+
 ' preventative surgery'.
VARIABLE LABELS @0to2Categorical_bp_  '0 to 2 Categorical:Blood pressure'.
VARIABLE LABELS @0to1Dichotomy_diabetes_  '0 to 1 Dichotomy:History of'+
 ' diabetes'.
VARIABLE LABELS @1to4Categorical_recbart1_  '1 to 4 Categorical:Recoded'+
 ' Barthel index at 1 month'.
VARIABLE LABELS Nonnegativeinteger_time_  'Nonnegative integer:Time to'+
 ' hospital'.
VARIABLE LABELS @1to4Categorical_recbart2_  '1 to 4 Categorical:Recoded'+
 ' Barthel index at 3 months'.
VARIABLE LABELS @0to3Categorical_rehab_  '0 to 3 Categorical:Post-event'+
 ' rehabilitation'.
VARIABLE LABELS @0to1Dichotomy_nitro_  '0 to 1 Dichotomy:Prescribed'+
 ' nitroglycerin'.
VARIABLE LABELS @0to1Dichotomy_choles_  '0 to 1 Dichotomy:Cholesterol'.
VALUE LABELS @0to3Categorical_anticlot_  TO Nonnegativeinteger_age_  1
  'Invalid' 0 'Valid'.
FORMAT @0to3Categorical_anticlot_  TO Nonnegativeinteger_age_  (F1.0).
VARIABLE WIDTH @0to3Categorical_anticlot_  TO Nonnegativeinteger_age_  (4).
VARIABLE LEVEL @0to3Categorical_anticlot_  TO Nonnegativeinteger_age_
  (NOMINAL).
* Validate Data.
VALIDATEDATA
  VARIABLES=hospsize age agecat gender active obesity diabetes bp af smoker
  choles angina mi nitro anticlot tia time doa rankin0 catscan clotsolv dhosp
  result surgery rehab los_rehab cost rankin1 rankin2 rankin3 barthel1
  barthel2 barthel3 recbart1 recbart2 recbart3
  ID=hospid patid physid
 /VARCHECKS STATUS=ON PCTMISSING=70 PCTEQUAL=95 PCTUNEQUAL=90 CV=0.001
  STDDEV=0
 /IDCHECKS INCOMPLETE DUPLICATE
 /CASECHECKS REPORTEMPTY=YES SCOPE=ALLVARS
 /CASEREPORT DISPLAY=YES MINVIOLATIONS=1 CASELIMIT=FIRSTN(100)
 /RULESUMMARIES BYVARIABLE.


* Finally, create some rules of your own
*.

DELETE VARIABLES @0to3Categorical_anticlot_ @0to3Categorical_rehab_
  @0to3Categorical_clotsolv_ @0to1Dichotomy_obesity_ @0to1Dichotomy_dhosp_
  @0to1Dichotomy_tia_ @0to1Dichotomy_af_ @0to1Dichotomy_nitro_
  @0to1Dichotomy_smoker_ @0to1Dichotomy_active_ @0to1Dichotomy_doa_
  @0to1Dichotomy_mi_ @0to1Dichotomy_gender_ @0to1Dichotomy_catscan_
  @0to1Dichotomy_angina_ @0to1Dichotomy_diabetes_ @0to1Dichotomy_choles_
  @1to4Categorical_recbart3_ @1to4Categorical_recbart2_
  @1to4Categorical_recbart1_ @1to4Categorical_agecat_ @1to4Categorical_result_
  @0to2Categorical_bp_ @0to2Categorical_surgery_ Nonnegativenumber_cost_
  Nonnegativeinteger_los_rehab_ Nonnegativeinteger_time_
  Nonnegativeinteger_age_.
* (Re)define cross-variable validation rules.
DATAFILE ATTRIBUTE ATTRIBUTE=
   $VD.CRule[1]("Label='DiedTwice',OutcomeVar='DiedTwice_'"+
 ",Expression='(doa=1) & (dhosp=1)' ").
* Delete existing single-variable validation rules.
DATAFILE ATTRIBUTE DELETE=$VD.SRule.
* Delete existing links between variables and rules.
VARIABLE ATTRIBUTE  VARIABLES=ALL  DELETE=$VD.SRuleRef.
* (Re)define single-variable validation rules.
DATAFILE ATTRIBUTE ATTRIBUTE=
      $VD.SRule[1]("Label='0 to 1 Dichotomy', Type='Numeric', Domain='List',"+
 " FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '1' ")
      $VD.SRule[2]("Label='0 to 2 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '1' '2' ")
      $VD.SRule[3]("Label='0 to 3 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '1' '2' '3' ")
      $VD.SRule[4]("Label='1 to 4 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='1' '2' '3' '4' ")
      $VD.SRule[5]("Label='Nonnegative integer', Type='Numeric',"+
 " Domain='Range', Minimum='0', Maximum='', FlagUserMissing='No',"+
 " FlagSystemMissing='Yes', FlagBlank='No', FlagNoninteger='Yes',"+
 " FlagUnlabeled='No' ")
      $VD.SRule[6]("Label='Nonnegative number', Type='Numeric',"+
 " Domain='Range', Minimum='0', Maximum='', FlagUserMissing='No',"+
 " FlagSystemMissing='Yes', FlagBlank='No', FlagNoninteger='No',"+
 " FlagUnlabeled='No' ")
      $VD.SRule[7]("Label='1 to 3 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='1' '2' '3' ")
      $VD.SRule[8]("Label='0 to 5 Categorical', Type='Numeric', Domain='List'"+
 ", FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '1' '2' '3' '4' '5' ")
      $VD.SRule[9]("Label='0 to 100 by 5', Type='Numeric', Domain='List',"+
 " FlagUserMissing='No', FlagSystemMissing='Yes', FlagBlank='No',"+
 " CaseSensitive='No',List='0' '5' '10' '15' '20' '25' '30' '35' '40' '45' '50'"+
 " '55' '60' '65' '70' '75' '80' '85' '90' '95' '100' ").
* (Re)define links between variables and rules.
VARIABLE ATTRIBUTE
    VARIABLES=recbart3  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_recbart3_' ")
    /VARIABLES=catscan  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_catscan_' ")
    /VARIABLES=doa  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_doa_'"+
 " ")
    /VARIABLES=gender  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_gender_' ")
    /VARIABLES=dhosp  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_dhosp_'"+
 " ")
    /VARIABLES=angina  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_angina_' ")
    /VARIABLES=smoker  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_smoker_' ")
    /VARIABLES=af  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_af_' ")
    /VARIABLES=tia  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_tia_'"+
 " ")
    /VARIABLES=anticlot  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[3]'"+
 ",OutcomeVar='@0to3Categorical_anticlot_' ")
    /VARIABLES=agecat  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_agecat_' ")
    /VARIABLES=obesity  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_obesity_' ")
    /VARIABLES=barthel1  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[9]',OutcomeVar='@0to100by5_barthel1_'"+
 " ")
    /VARIABLES=clotsolv  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[3]'"+
 ",OutcomeVar='@0to3Categorical_clotsolv_' ")
    /VARIABLES=active  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_active_' ")
    /VARIABLES=barthel2  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[9]',OutcomeVar='@0to100by5_barthel2_'"+
 " ")
    /VARIABLES=barthel3  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[9]',OutcomeVar='@0to100by5_barthel3_'"+
 " ")
    /VARIABLES=age  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[5]'"+
 ",OutcomeVar='Nonnegativeinteger_age_' ")
    /VARIABLES=rankin0  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[8]'"+
 ",OutcomeVar='@0to5Categorical_rankin0_' ")
    /VARIABLES=rankin1  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[8]'"+
 ",OutcomeVar='@0to5Categorical_rankin1_' ")
    /VARIABLES=hospsize  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[7]'"+
 ",OutcomeVar='@1to3Categorical_hospsize_' ")
    /VARIABLES=rankin2  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[8]'"+
 ",OutcomeVar='@0to5Categorical_rankin2_' ")
    /VARIABLES=cost  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[6]'"+
 ",OutcomeVar='Nonnegativenumber_cost_' ")
    /VARIABLES=los_rehab  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[5]'"+
 ",OutcomeVar='Nonnegativeinteger_los_rehab_' ")
    /VARIABLES=result  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_result_' ")
    /VARIABLES=mi  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_mi_' ")
    /VARIABLES=rankin3  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[8]'"+
 ",OutcomeVar='@0to5Categorical_rankin3_' ")
    /VARIABLES=surgery  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[2]'"+
 ",OutcomeVar='@0to2Categorical_surgery_' ")
    /VARIABLES=bp  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[2]',OutcomeVar='@0to2Categorical_bp_'"+
 " ")
    /VARIABLES=diabetes  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_diabetes_' ")
    /VARIABLES=recbart1  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_recbart1_' ")
    /VARIABLES=time  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[5]'"+
 ",OutcomeVar='Nonnegativeinteger_time_' ")
    /VARIABLES=recbart2  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[4]'"+
 ",OutcomeVar='@1to4Categorical_recbart2_' ")
    /VARIABLES=rehab  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[3]'"+
 ",OutcomeVar='@0to3Categorical_rehab_' ")
    /VARIABLES=nitro  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]',OutcomeVar='@0to1Dichotomy_nitro_'"+
 " ")
    /VARIABLES=choles  ATTRIBUTE=
      $VD.SRuleRef[1]("Rule='$VD.SRule[1]'"+
 ",OutcomeVar='@0to1Dichotomy_choles_' ") .
* 0 to 3 Categorical.
COMPUTE @0to3Categorical_anticlot_ = NOT(ANY(VALUE(anticlot), 0, 1, 2, 3) OR
  (MISSING(anticlot) AND NOT(SYSMIS(anticlot)))) OR SYSMIS(anticlot).
COMPUTE @0to3Categorical_rehab_ = NOT(ANY(VALUE(rehab), 0, 1, 2, 3) OR
  (MISSING(rehab) AND NOT(SYSMIS(rehab)))) OR SYSMIS(rehab).
COMPUTE @0to3Categorical_clotsolv_ = NOT(ANY(VALUE(clotsolv), 0, 1, 2, 3) OR
  (MISSING(clotsolv) AND NOT(SYSMIS(clotsolv)))) OR SYSMIS(clotsolv).
* 1 to 3 Categorical.
COMPUTE @1to3Categorical_hospsize_ = NOT(ANY(VALUE(hospsize), 1, 2, 3) OR
  (MISSING(hospsize) AND NOT(SYSMIS(hospsize)))) OR SYSMIS(hospsize).
* 0 to 1 Dichotomy.
DO REPEAT #OV=@0to1Dichotomy_obesity_ @0to1Dichotomy_dhosp_
  @0to1Dichotomy_tia_ @0to1Dichotomy_af_ @0to1Dichotomy_nitro_
  @0to1Dichotomy_smoker_ @0to1Dichotomy_active_ @0to1Dichotomy_doa_
  @0to1Dichotomy_mi_ @0to1Dichotomy_gender_ @0to1Dichotomy_catscan_
  @0to1Dichotomy_angina_ @0to1Dichotomy_diabetes_ @0to1Dichotomy_choles_
  /#IV=obesity dhosp tia af nitro smoker active doa mi gender catscan angina
  diabetes choles.
COMPUTE #OV=NOT(ANY(VALUE(#IV), 0, 1) OR (MISSING(#IV) AND NOT(SYSMIS(#IV))))
  OR SYSMIS(#IV).
END REPEAT.
* 0 to 100 by 5.
COMPUTE @0to100by5_barthel3_ = NOT(ANY(VALUE(barthel3), 0, 5, 10, 15, 20, 25,
  30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100) OR
  (MISSING(barthel3) AND NOT(SYSMIS(barthel3)))) OR SYSMIS(barthel3).
COMPUTE @0to100by5_barthel2_ = NOT(ANY(VALUE(barthel2), 0, 5, 10, 15, 20, 25,
  30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100) OR
  (MISSING(barthel2) AND NOT(SYSMIS(barthel2)))) OR SYSMIS(barthel2).
COMPUTE @0to100by5_barthel1_ = NOT(ANY(VALUE(barthel1), 0, 5, 10, 15, 20, 25,
  30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100) OR
  (MISSING(barthel1) AND NOT(SYSMIS(barthel1)))) OR SYSMIS(barthel1).
* 1 to 4 Categorical.
DO REPEAT #OV=@1to4Categorical_recbart3_ @1to4Categorical_recbart2_
  @1to4Categorical_recbart1_ @1to4Categorical_agecat_ @1to4Categorical_result_
  /#IV=recbart3 recbart2 recbart1 agecat result.
COMPUTE #OV=NOT(ANY(VALUE(#IV), 1, 2, 3, 4) OR (MISSING(#IV) AND
  NOT(SYSMIS(#IV)))) OR SYSMIS(#IV).
END REPEAT.
* 0 to 2 Categorical.
COMPUTE @0to2Categorical_bp_ = NOT(ANY(VALUE(bp), 0, 1, 2) OR (MISSING(bp)
  AND NOT(SYSMIS(bp)))) OR SYSMIS(bp).
COMPUTE @0to2Categorical_surgery_ = NOT(ANY(VALUE(surgery), 0, 1, 2) OR
  (MISSING(surgery) AND NOT(SYSMIS(surgery)))) OR SYSMIS(surgery).
* Nonnegative number.
COMPUTE Nonnegativenumber_cost_ = NOT(VALUE(cost)>=0 OR (MISSING(cost) AND
  NOT(SYSMIS(cost)))) OR SYSMIS(cost).
* 0 to 5 Categorical.
DO REPEAT #OV=@0to5Categorical_rankin3_ @0to5Categorical_rankin2_
  @0to5Categorical_rankin1_ @0to5Categorical_rankin0_
  /#IV=rankin3 rankin2 rankin1 rankin0.
COMPUTE #OV=NOT(ANY(VALUE(#IV), 0, 1, 2, 3, 4, 5) OR (MISSING(#IV) AND
  NOT(SYSMIS(#IV)))) OR SYSMIS(#IV).
END REPEAT.
* Nonnegative integer.
COMPUTE Nonnegativeinteger_los_rehab_ = NOT(VALUE(los_rehab)>=0 AND
  VALUE(los_rehab)=TRUNC(VALUE(los_rehab)) OR (MISSING(los_rehab) AND
  NOT(SYSMIS(los_rehab)))) OR SYSMIS(los_rehab).
COMPUTE Nonnegativeinteger_time_ = NOT(VALUE(time)>=0 AND
  VALUE(time)=TRUNC(VALUE(time)) OR (MISSING(time) AND NOT(SYSMIS(time)))) OR
  SYSMIS(time).
COMPUTE Nonnegativeinteger_age_ = NOT(VALUE(age)>=0 AND
  VALUE(age)=TRUNC(VALUE(age)) OR (MISSING(age) AND NOT(SYSMIS(age)))) OR
  SYSMIS(age).
* DiedTwice.
COMPUTE DiedTwice_ = (doa=1) & (dhosp=1).
* Mark rule outcome variables as such in SPSS data dictionary.
VARIABLE ATTRIBUTE
   VARIABLES=@0to3Categorical_anticlot_  TO DiedTwice_
   ATTRIBUTE=$VD.RuleOutcomeVar("Yes").
VARIABLE LABELS @1to4Categorical_recbart3_  '1 to 4 Categorical:Recoded'+
 ' Barthel index at 6 months'.
VARIABLE LABELS @0to1Dichotomy_catscan_  '0 to 1 Dichotomy:CAT scan result'.
VARIABLE LABELS @0to1Dichotomy_doa_  '0 to 1 Dichotomy:Dead on arrival'.
VARIABLE LABELS @0to1Dichotomy_gender_  '0 to 1 Dichotomy:Gender'.
VARIABLE LABELS @0to1Dichotomy_dhosp_  '0 to 1 Dichotomy:Died in hospital'.
VARIABLE LABELS @0to1Dichotomy_angina_  '0 to 1 Dichotomy:History of angina'.
VARIABLE LABELS @0to1Dichotomy_smoker_  '0 to 1 Dichotomy:Smoker'.
VARIABLE LABELS @0to1Dichotomy_af_  '0 to 1 Dichotomy:Atrial fibrillation'.
VARIABLE LABELS @0to1Dichotomy_tia_  '0 to 1 Dichotomy:History of transient'+
 ' ischemic attack'.
VARIABLE LABELS @0to3Categorical_anticlot_  '0 to 3 Categorical:Taking anti'+
 '-clotting drugs'.
VARIABLE LABELS @1to4Categorical_agecat_  '1 to 4 Categorical:Age category'.
VARIABLE LABELS @0to1Dichotomy_obesity_  '0 to 1 Dichotomy:Obesity'.
VARIABLE LABELS @0to100by5_barthel1_  '0 to 100 by 5:Barthel index at 1'+
 ' month'.
VARIABLE LABELS @0to3Categorical_clotsolv_  '0 to 3 Categorical:Clot'+
 '-dissolving drugs'.
VARIABLE LABELS @0to1Dichotomy_active_  '0 to 1 Dichotomy:Physically active'.
VARIABLE LABELS @0to100by5_barthel2_  '0 to 100 by 5:Barthel index at 3'+
 ' months'.
VARIABLE LABELS @0to100by5_barthel3_  '0 to 100 by 5:Barthel index at 6'+
 ' months'.
VARIABLE LABELS Nonnegativeinteger_age_  'Nonnegative integer:Age in years'.
VARIABLE LABELS @0to5Categorical_rankin0_  '0 to 5 Categorical:Initial Rankin'+
 ' score'.
VARIABLE LABELS @0to5Categorical_rankin1_  '0 to 5 Categorical:Rankin score'+
 ' at 1 month'.
VARIABLE LABELS @1to3Categorical_hospsize_  '1 to 3 Categorical:Hospital'+
 ' size'.
VARIABLE LABELS @0to5Categorical_rankin2_  '0 to 5 Categorical:Rankin score'+
 ' at 3 months'.
VARIABLE LABELS Nonnegativenumber_cost_  'Nonnegative number:Total treatment'+
 ' and rehabilitation costs in thousands'.
VARIABLE LABELS Nonnegativeinteger_los_rehab_  'Nonnegative integer:Length of'+
 ' stay for rehabilitation'.
VARIABLE LABELS @1to4Categorical_result_  '1 to 4 Categorical:Treatment'+
 ' result'.
VARIABLE LABELS @0to1Dichotomy_mi_  '0 to 1 Dichotomy:History of myocardial'+
 ' infarction'.
VARIABLE LABELS @0to5Categorical_rankin3_  '0 to 5 Categorical:Rankin score'+
 ' at 6 months'.
VARIABLE LABELS @0to2Categorical_surgery_  '0 to 2 Categorical:Post-event'+
 ' preventative surgery'.
VARIABLE LABELS @0to2Categorical_bp_  '0 to 2 Categorical:Blood pressure'.
VARIABLE LABELS @0to1Dichotomy_diabetes_  '0 to 1 Dichotomy:History of'+
 ' diabetes'.
VARIABLE LABELS @1to4Categorical_recbart1_  '1 to 4 Categorical:Recoded'+
 ' Barthel index at 1 month'.
VARIABLE LABELS Nonnegativeinteger_time_  'Nonnegative integer:Time to'+
 ' hospital'.
VARIABLE LABELS @1to4Categorical_recbart2_  '1 to 4 Categorical:Recoded'+
 ' Barthel index at 3 months'.
VARIABLE LABELS @0to3Categorical_rehab_  '0 to 3 Categorical:Post-event'+
 ' rehabilitation'.
VARIABLE LABELS @0to1Dichotomy_nitro_  '0 to 1 Dichotomy:Prescribed'+
 ' nitroglycerin'.
VARIABLE LABELS @0to1Dichotomy_choles_  '0 to 1 Dichotomy:Cholesterol'.
VARIABLE LABELS DiedTwice_  'DiedTwice:(doa=1) & (dhosp=1)'.
VALUE LABELS @0to3Categorical_anticlot_  TO DiedTwice_  1 'Invalid' 0
  'Valid'.
FORMAT @0to3Categorical_anticlot_  TO DiedTwice_  (F1.0).
VARIABLE WIDTH @0to3Categorical_anticlot_  TO DiedTwice_  (4).
VARIABLE LEVEL @0to3Categorical_anticlot_  TO DiedTwice_  (NOMINAL).
* Validate Data.
VALIDATEDATA
  VARIABLES=hospsize age agecat gender active obesity diabetes bp af smoker
  choles angina mi nitro anticlot tia time doa rankin0 catscan clotsolv dhosp
  result surgery rehab los_rehab cost rankin1 rankin2 rankin3 barthel1
  barthel2 barthel3 recbart1 recbart2 recbart3
  ID=hospid patid physid
  CROSSVARRULES=$VD.CRule[1]
 /VARCHECKS STATUS=ON PCTMISSING=70 PCTEQUAL=95 PCTUNEQUAL=90 CV=0.001
  STDDEV=0
 /IDCHECKS INCOMPLETE DUPLICATE
 /CASECHECKS REPORTEMPTY=YES SCOPE=ALLVARS
 /CASEREPORT DISPLAY=YES MINVIOLATIONS=1 CASELIMIT=FIRSTN(100)
 /RULESUMMARIES BYVARIABLE.
