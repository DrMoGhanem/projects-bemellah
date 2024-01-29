#/***********************************************************************
# * Licensed Materials - Property of IBM 
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2014
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp. 
# ************************************************************************/

#!/usr/bin/python

"""
A python interface to the XD API
"""

#Copyright (C) 2008 by SPSS Inc.

import os,sys
from errMsg import errTable
from errMsg import StrError
from os.path import exists
import ConfigParser

def __GetSpssXdPath():
    config = ConfigParser.ConfigParser()
    # Read spssxd config file
    spssxdcfg = os.sep.join([__path__[0],"spssxdcfg.ini"])
    assert exists(spssxdcfg)
    config.read(spssxdcfg)
    return config.get('path','spssxd_path')

def __GetSpssDxVersion():
    spssxd_path = __GetSpssXdPath()
    if sys.platform == 'win32':
        spssdxcfg = os.sep.join([spssxd_path, "spssdxcfg.ini"])
    else:
        spssdxcfg = os.sep.join([spssxd_path + "/bin", "spssdxcfg.ini"])
    assert exists(spssdxcfg)

    config = ConfigParser.ConfigParser()
    # Read spssdxcfg.ini file
    config.read(spssdxcfg)
    ver = config.get('version','SpssdxVersion')
    return ver

def __VersionCheck():
    # Read spssxd(Plug-In) version
    from version import version as spssxd_version
    # Read spssdx(SPSS) version
    spssdx_version = __GetSpssDxVersion()

    # Only the first 2 digits in version are used
    tmpList = spssxd_version.split('.')
    spssxd_version = '.'.join(tmpList[:2])
    tmpList = spssdx_version.split('.')
    spssdx_version = '.'.join(tmpList[:2])
    assert spssdx_version == spssxd_version

def __PutEnv(key,value,sep=":"):
    if not os.environ.has_key(key):
        os.environ[key] = value
    else:
        os.environ[key] = sep.join([value,os.environ[key]])

def __SetSpssEnv():
    # Define platform
    if sys.platform == "win32":
        platform = "win32"
    else:
        platform = "unSupported"

    spss_home = __GetSpssXdPath()

    # Export the LC_ALL environment variable if it is not set
    #if not os.environ.has_key("LC_ALL"):
    #    os.environ["LC_ALL"] = "en_US"

    # Set SPSS_HOME
    os.environ["SPSS_HOME"] = spss_home
    #Set LANGUAGE
    if os.getenv("LANGUAGE") is None:
        os.environ["LANGUAGE"] = "English"

    if platform == 'win32':
        __PutEnv("path",spss_home,";")
        return
    # Set TMP path
    if os.environ.has_key("SPSSTMPDIR"):
        os.environ["TMPDIR"]=os.getenv("SPSSTMPDIR")
    elif not os.environ.has_key("TMPDIR"):
        __PutEnv("TMPDIR","/tmp")
    else:
        pass
        
    if sys.platform.lower().find('aix') > -1:
        if os.environ.has_key("LIBPATH"):
            __PutEnv("LIBPATH", "/usr/lib:/lib")

def __GetLanguage():
    import locale
    
    lang = "en"
    spss_olang = os.getenv("LANGUAGE")

    if("SChinese" == spss_olang):
        lang = "zh_CN"
    elif( "TChinese" == spss_olang):
        lang = "zh_TW"
    elif( "German" == spss_olang):
        lang = "de"
    elif( "Spanish" == spss_olang):
        lang = "es"
    elif( "French" == spss_olang):
        lang = "fr"
    elif( "Italian" == spss_olang):
        lang = "it"
    elif( "Japanese" == spss_olang):
        lang = "ja"
    elif( "Korean" == spss_olang):
        lang = "ko"
    elif( "Polish" == spss_olang):
        lang = "pl"
    elif( "Russian" == spss_olang):
        lang = "ru"
    elif("English" == spss_olang):
        lang = "en"
    elif("BPortugu" == spss_olang):
        lang = "pt_BR"

    return lang

def __findLocalizedErrfile(language):
    rootPath = __path__[0]
    #rootPath = __GetSpssXdPath()
    langPath = os.sep.join([rootPath, "lang", language])
    fileName = "spsspy.properties"
    errfile = os.sep.join([langPath, fileName])
    if not exists(errfile):
        language = "en"
        langPath = os.sep.join([rootPath,"lang", language])
        errfile = os.sep.join([langPath, fileName])
        print "Can not find localized error message file. Using default spsspy.properties for English."
    if not exists(errfile):
        raise StrError("Can not find error message file.")

    return errfile

def __SetErrorMessage():
    """Read the error messages from spsspy.properties file,
    and initial global object 'errTable' with the error messages.
    """
    # read error messages from messages.err file
    language = __GetLanguage()    
    errfile = __findLocalizedErrfile(language)
    
    
    fp = open(errfile,"r")
    errLines = fp.readlines()
    fp.close()
    sep = ("[", "]", "=")
    # initial global object 'errTable' with error messages
    for errLine in errLines:
        errLine = errLine.strip()
        if errLine.startswith("#"):
            continue 
        if not errLine.startswith(sep[0]):
            continue
        errType = errLine.split(sep[0])[1].split(sep[1])[0].strip().lower()
        other = errLine.split(sep[0])[1].split(sep[1])[1][1:]
        errLevel = other.split(sep[2])[0].strip()
        errMsg = other.split(sep[2])[1].strip()
        if errTable.has_key(errType):
            errTable[errType][errLevel] = errMsg
        else:
            errTable[errType] = {errLevel:errMsg}

def GetDefaultPlugInVersion():
    return __GetInstalledPlugInVersions()[0]

def __GetInstalledPlugInVersions():
    import ConfigParser
    xdconfig = ConfigParser.ConfigParser()
    xdcfgfile = os.path.join(__path__[0], 'spssxdcfg.ini')
    assert os.path.exists(xdcfgfile)
    xdconfig.read(xdcfgfile)
    versionmajor = xdconfig.get('version','SpssxdVersionMajor')
    fixpack = xdconfig.get('version','SpssxdFixPack')
    version = 'spss' + versionmajor + fixpack
    return [version,]

def ShowInstalledPlugInVersions():
    installedList = __GetInstalledPlugInVersions()
    print "Installed versions of the IBM SPSS Statistics-Python Integration Plug-in:"

    for (i,x) in enumerate(installedList):
        print str(i) + ":   ", x
    #return installedList
    
def __SetPlugInVersion(defaultVersion):
    if isinstance(defaultVersion,int):
        version = 'spss' + str(defaultVersion)
    elif isinstance(defaultVersion,str):
        version = defaultVersion.lower()
    else:
        raise StrError("Expected a string or integer.")

    oldlist = __GetInstalledPlugInVersions()
    if not version in oldlist:
        raise StrError("There is no plug in installed with the given version.")
       
    return version

def SetDefaultPlugInVersion(defaultVersion):    
    version = __SetPlugInVersion(defaultVersion)
    #in case the client is connected to a remote server
    return

__VersionCheck()
__SetSpssEnv()
__SetErrorMessage()

from spssutil import extrapath
extrapath()
from spssutil import SetPythonPath
SetPythonPath(__path__[0])

from spss import *
from cursors import *
from pivotTable import *
from procedure import *
from dataStep import *

__all__ = spss.__all__ + cursors.__all__ + procedure.__all__ + pivotTable.__all__ + dataStep.__all__

import version
__version__ = version.version