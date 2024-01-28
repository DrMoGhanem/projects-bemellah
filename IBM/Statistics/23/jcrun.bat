@REM ************************************************************************
@REM IBM Confidential
@REM
@REM OCO Source Materials
@REM
@REM IBM SPSS Products: Statistics Common
@REM
@REM (C) Copyright IBM Corp. 1989, 2015
@REM
@REM The source code for this program is not published or otherwise divested of its trade secrets, 
@REM irrespective of what has been deposited with the U.S. Copyright Office.
@REM ************************************************************************

@SETLOCAL & SET RET=

@ECHO OFF

@REM the installation directory
SET INSTALLDIR=%~sdp0

@REM set the PATH to include the common directory
SET COMMONDIR=%INSTALLDIR%common\
SET PATH=%COMMONDIR%ext\bin\spss.common\;%COMMONDIR%thirdparty\;%PATH%

@REM set the PATH to include the installation directory
SET PATH=%INSTALLDIR%;%PATH%

PUSHD %INSTALLDIR%

%INSTALLDIR%JRE\bin\java.exe -ea -Dsun.java2d.d3d=false -Xshareclasses:name=statistics_%u -Xshareclasses:nonfatal -Xscmx32M -Xdisableexplicitgc -Xms32M -Xmx768M -Dcom.sun.media.jai.disableMediaLib=true -Dswing.aatext=false -Djava.library.path=%INSTALLDIR%;%INSTALLDIR%JRE\bin -Dapplication.home=%INSTALLDIR% -Dcom.ibm.jsse2.disableSSLv3=false -Dstatistics.home=%INSTALLDIR% -Dstd_deployment.home=%INSTALLDIR% -DsaveXml=true -classpath "%INSTALLDIR%*;%INSTALLDIR%common\ext\lib\spss.common\*;%INSTALLDIR%as\lib\*;%INSTALLDIR%as\3rdparty\*" com.spss.java_client.core.common.Driver %*

:end

@POPD & ENDLOCAL & SET RET=%RET%
