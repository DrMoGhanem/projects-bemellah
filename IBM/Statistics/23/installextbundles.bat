@REM /***********************************************************************
@REM * Licensed Materials - Property of IBM 
@REM *
@REM * IBM SPSS Products: Statistics Common
@REM *
@REM * (C) Copyright IBM Corp. 1989, 2014
@REM *
@REM * US Government Users Restricted Rights - Use, duplication or disclosure
@REM * restricted by GSA ADP Schedule Contract with IBM Corp. 
@REM ************************************************************************/

@SETLOCAL & PUSHD & SET RET=

@ECHO OFF

@REM the installation directory
SET INSTALLDIR=%~sdp0

@REM set the PATH to include the common directory
SET COMMONDIR=%INSTALLDIR%common\
SET PATH=%COMMONDIR%ext\bin\spss.common\;%PATH%

@REM set the PATH to include the installation directory
SET PATH=%INSTALLDIR%;%PATH%

@REM set the JAVAEXECUTABLE to be either java.exe or javaw.exe(don't show command window)
IF "%1"=="-silent" (
    SET JAVAEXECUTABLE=javaw.exe
) ELSE (
    SET JAVAEXECUTABLE=java.exe
)

%INSTALLDIR%JRE\bin\%JAVAEXECUTABLE% -ea -XX:NewSize=4M -XX:NewRatio=2 -Xms32M -Xmx1024M -Dcom.sun.media.jai.disableMediaLib=true -Dswing.aatext=false -Djava.library.path=%INSTALLDIR%;%INSTALLDIR%JRE\bin\ -Dapplication.home=%INSTALLDIR% -Dstatistics.home=%INSTALLDIR% -Dstd_deployment.home=%INSTALLDIR% -classpath "%INSTALLDIR%*;%COMMONDIR%ext\lib\spss.common\*" com.spss.java_client.installextbundles.Installer %*

:end

@POPD & ENDLOCAL & SET RET=%RET%
