@set INSTALLDIR=%~sdp0
@pushd %INSTALLDIR%
@%INSTALLDIR%JRE\bin\java.exe -Djava.library.path=. -jar licensecommute.jar
@popd
