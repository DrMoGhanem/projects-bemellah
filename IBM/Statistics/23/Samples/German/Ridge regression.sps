preserve.
set printback=off.
define ridgereg (enter=!charend('/')
                /dep = !charend('/')
                /start=!default(0) !charend('/')
                /stop=!default(1) !charend('/')
                /inc=!default(.05) !charend('/')
                /k=!default(999) !charend('/') 
                /debug=!DEFAULT ('N')!charend('/')  ).

preserve.
!IF ( !DEBUG !EQ 'N') !THEN
set printback=off mprint off.                                                   
!ELSE
set printback on mprint on.
!IFEND .
SET mxloops=200.

*---------------------------------------------------------------------------.
* Save original active file to give back after macro is done.
*---------------------------------------------------------------------------.
!IF (!DEBUG !EQ 'N') !THEN 
SET RESULTS ON.
DO IF $CASENUM=1.
PRINT / "NOTE: ALL OUTPUT INCLUDING ERROR MESSAGES HAVE BEEN TEMPORARILY" 
      / "SUPPRESSED. IF YOU EXPERIENCE UNUSUAL BEHAVIOR, RERUN THIS" 
      / "MACRO WITH AN ADDITIONAL ARGUMENT /DEBUG='Y'."  
      / "BEFORE DOING THIS YOU SHOULD RESTORE YOUR DATA FILE."
      / "THIS WILL FACILITATE FURTHER DIAGNOSIS OF ANY PROBLEMS.".
END IF.
!IFEND .

save outfile='rr__tmp1.sav'.

*---------------------------------------------------------------------------.
* Use CORRELATIONS to create the correlation matrix.
*---------------------------------------------------------------------------.

* DEFAULT:  SET RESULTS AND ERRORS OFF TO SUPPRESS CORRELATION PIVOT TABLE *.
!IF (!DEBUG='N') !THEN
set results off errors off.
!IFEND 

correlations variables=!dep !enter /missing=listwise/matrix out(*).
set errors on results listing .

*---------------------------------------------------------------------------.
* Enter MATRIX.
*---------------------------------------------------------------------------.

matrix.

*---------------------------------------------------------------------------.
* Initialize k, increment, and  number of iterations. If k was not
* specified, it is 999 and looping will occur. Otherwise, just the one
* value of k will be used for estimation.
*---------------------------------------------------------------------------.

do if (!k=999).
. compute k=!start.
. compute inc=!inc.
. compute iter=trunc((!stop - !start ) / !inc ) + 1.
. do if (iter <= 0).
.   compute iter = 1.
. end if.
else.
. compute k=!k.
. compute inc=0.
. compute iter=1.
end if.

*---------------------------------------------------------------------------.
* Get data from working matrix file.
*---------------------------------------------------------------------------.

get x/file=*/names=varname/variable=!dep !enter.

*---------------------------------------------------------------------------.
* Third row of matrix input is the vector of Ns. Use this to compute number
* of variables.
*---------------------------------------------------------------------------.

compute n=x(3,1).
compute nv=ncol(x)-1.

*---------------------------------------------------------------------------.   
* Get variable names.
*---------------------------------------------------------------------------.

compute varname=varname(2:(nv+1)).

*---------------------------------------------------------------------------.
* Get X'X matrix (or R, matrix of predictor correlations) from input data
* Also get X'Y, or correlations of predictors with dependent variable.
*---------------------------------------------------------------------------.

compute xpx=x(5:(nv+4),2:(nv+1)).
compute xy=t(x(4,2:(nv+1))).

*---------------------------------------------------------------------------.
* Initialize the keep matrix for saving results, and the names vector.
*---------------------------------------------------------------------------.

compute keep=make(iter,nv+2,-999).
compute varnam2={'K','RSQ',varname}.

*---------------------------------------------------------------------------.
* Compute means and standard deviations. Means are in the first row of x and
* standard deviations are in the second row. Now that all of x has been
* appropriately stored, release x to maximize available memory.
*---------------------------------------------------------------------------.

compute xmean=x(1,2:(nv+1)).
compute ybar=x(1,1).
compute std=t(x(2,2:(nv+1))).
compute sy=x(2,1).
release x.

*---------------------------------------------------------------------------.
* Start loop over values of k, computing standardized regression
* coefficients and squared multiple correlations. Store results
*---------------------------------------------------------------------------.

loop l=1 to iter.
. compute b = inv(xpx+(k &* ident(nv,nv)))*xy.
. compute rsq= 2* t(b)*xy - t(b)*xpx*b.
. compute keep(l,1)=k.
. compute keep(l,2)=rsq.
. compute keep(l,3:(nv+2))=t(b).
. compute k=k+inc.
end loop.

*---------------------------------------------------------------------------.
* If we are to print out estimation results, compute needed pieces and
* print out header and ANOVA table.
*---------------------------------------------------------------------------.

do if (!k <> 999).
.!let !rrtitle=!concat('****** Ridge Regression with k = ',!k).
.!let !rrtitle=!quote(!concat(!rrtitle,' ****** ')).
. compute sst=(n-1) * sy **2.
. compute sse=sst * ( 1 - 2* t(b)*xy + t(b)*xpx*b).
. compute ssr = sst - sse.
. compute s=sqrt( sse / (n-nv-1) ).
. print /title=!rrtitle /space=newpage.
. print {sqrt(rsq);rsq;rsq-nv*(1-rsq)/(n-nv-1);s}
 /rlabel='Mult R' 'RSquare' 'Adj RSquare' 'SE'
 /title=' '.
. compute anova={nv,ssr,ssr/(nv);n-nv-1,sse,sse/(n-nv-1)}.
. compute f=ssr/sse * (n-nv-1)/(nv).
. print anova
   /clabels='df' 'SS','MS'
   /rlabel='Regress' 'Residual'
   /title='         ANOVA table'
   /format=f9.3.
.  compute test=ssr/sse * (n-nv-1)/nv.
.  compute sigf=1 - fcdf(test,nv,n-nv-1).
.  print {test,sigf} /clabels='F value' 'Sig F'/title=' '.

*---------------------------------------------------------------------------.
* Calculate raw coefficients from standardized ones, compute standard errors
* of coefficients, and an intercept term with standard error. Then print
* out similar to REGRESSION output.
*---------------------------------------------------------------------------

. compute beta={b;0}.
. compute b= ( b &/ std ) * sy.
. compute intercpt=ybar-t(b)*t(xmean).
. compute b={b;intercpt}.
. compute xpx=(sse/(sst*(n-nv-1)))*inv(xpx+(k &* ident(nv,nv)))*xpx*
                                 inv(xpx+(k &* ident(nv,nv))).
. compute xpx=(sy*sy)*(mdiag(1 &/ std)*xpx*mdiag(1 &/ std)).
. compute seb=sqrt(diag(xpx)).
. compute seb0=sqrt( (sse)/(n*(n-nv-1)) + xmean*xpx*t(xmean)).
. compute seb={seb;seb0}.
. compute rnms={varname,'Constant'}.
. compute ratio=b &/ seb.
. compute bvec={b,seb,beta,ratio}.
. print bvec/title='--------------Variables in the Equation----------------'
  /rnames=rnms /clabels='B' 'SE(B)' 'Beta' 'B/SE(B)'.
. print /space=newpage.
end if.

*---------------------------------------------------------------------------.
* Save kept results into file. The number of cases in the file will be
* equal to the number of values of k for which results were produced. This
* will be simply 1 if k was specified.
*---------------------------------------------------------------------------.

save keep /outfile='rr__tmp2.sav' /names=varnam2.

*---------------------------------------------------------------------------.
* Finished with MATRIX part of job.
*---------------------------------------------------------------------------.

end matrix.

*---------------------------------------------------------------------------.
* If doing ridge trace, get saved file and produce table and plots.
*---------------------------------------------------------------------------.

!if (!k = 999) !then

get file='rr__tmp2.sav'.
print formats k rsq (f6.5) !enter (f8.6).
report format=list automatic
 /vars=k rsq !enter
 /title=center 'R-SQUARE AND BETA COEFFICIENTS FOR ESTIMATED VALUES OF K'.

graph
  /title = 'RIDGE TRACE'
  /footnote = 'K'
  /scatterplot(overlay) k with !enter.

graph
  /title = 'R-SQUARE VS. K'
  /scatterplot k with rsq.

!ifend.

*---------------------------------------------------------------------------.
* Get back original data set and restore original settings.
*---------------------------------------------------------------------------.

get file=rr__tmp1.sav.
restore.
!enddefine.
restore.
