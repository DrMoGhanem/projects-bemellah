@REM ************************************************************************
@REM Licensed Materials - Property of IBM 
@REM
@REM IBM SPSS Products: Statistics Common
@REM
@REM (C) Copyright IBM Corp. 1989, 2013
@REM
@REM US Government Users Restricted Rights - Use, duplication or disclosure
@REM restricted by GSA ADP Schedule Contract with IBM Corp. 
@REM ************************************************************************
@SETLOCAL & PUSHD & SET RET=
@set SPSS_HOME=%~sdp0
@set PATH=%SPSS_HOME%\JRE\bin;%PATH%
@echo off
@for /f "tokens=* delims=" %%i in ('java -jar "%SPSS_HOME%\"pythoncfg.jar showpython') do set PYTHONHOME=%%i
@set PYTHONPATH=%SPSS_HOME%\Python\Lib\site-packages;%PYTHONPATH%
@set PATH=%PYTHONHOME%;%PATH%
@echo on
@call "%PYTHONHOME%\python" %*
@POPD & ENDLOCAL & SET RET=%RET%
