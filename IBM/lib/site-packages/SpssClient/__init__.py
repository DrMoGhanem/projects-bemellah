#/***********************************************************************
# * IBM Confidential 
# *
# * OCO Source Materials
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2013
# *
# * The source code for this program is not published or otherwise divested of its trade secrets,
# * irrespective of what has been deposited with the U.S. Copyright Office.
# ************************************************************************/

"""
A python wrapper to SpssClient Module
Required to add the SPSS_HOME to PATH system variable
"""

#Copyright (C) 2007 by SPSS Inc.

import atexit,sys
import platform
import os
from os.path import exists
import ConfigParser
import spss

spssclient_home = spss.__GetSpssXdPath()
os.environ["SPSS_HOME"] = spssclient_home

if (sys.platform[:3].lower() == "win"):
    jvmlibpath = os.sep.join([spssclient_home, "JRE", "bin", "client"])
    tempPath = os.pathsep.join([spssclient_home, jvmlibpath, os.getenv("PATH")])
    os.environ["PATH"] = tempPath
    
elif ("linux" in sys.platform.lower()):
    try:
        if not spssclient_home.endswith(os.sep):
            spssclient_home += os.sep
        if spssclient_home.endswith('bin/'):
            spssclient_home = spssclient_home[:-4]
        import ctypes
        try:
            ctypes.CDLL(spssclient_home+'JRE/bin/j9vm/libjvm.so')
        except:
            ctypes.CDLL(spssclient_home+'bin/JRE/bin/j9vm/libjvm.so')
        ctypes.CDLL(spssclient_home+'lib/libJCAdaptor.so')
        ctypes.CDLL(spssclient_home+'lib/libPythonTransport.so')
        ctypes.CDLL(spssclient_home+'lib/libSpssClientProxy.so')

        jvmlibpath = os.sep.join([spssclient_home, "JRE"])
        if not exists(jvmlibpath):
            jvmlibpath = os.sep.join([spssclient_home, "bin"])
        spsslibpath = os.sep.join([spssclient_home, "lib"])
        tempPath = os.pathsep.join([spssclient_home, jvmlibpath, spsslibpath, os.getenv("LD_LIBRARY_PATH")])
        os.environ["LD_LIBRARY_PATH"] = tempPath
    except:
        pass
    
elif ("darwin" in sys.platform.lower()):
    jvmlibpath = os.sep.join([spssclient_home, "bin"])
    spsslibpath = os.sep.join([spssclient_home, "lib"])
    tempPath = os.pathsep.join([spssclient_home, jvmlibpath, spsslibpath, os.getenv("DYLD_LIBRARY_PATH")])
    os.environ["DYLD_LIBRARY_PATH"] = tempPath

def GetDefaultJCVersion():
    return __GetInstalledJCVersions()  


def __GetInstalledJCVersions():
    # Read spssclientcfg.ini file
    pthfile = os.sep.join([__path__[0], "spssclientcfg.ini"])
    assert exists(pthfile)
    fp = open(pthfile,'r')
    version = ''
    for line in fp.readlines():
        if(line.find('major') != -1):
            ver = line[line.find('=')+1:][:-1]
            version = 'SpssClient%s0' %ver
    fp.close()
    return version
    
def SetDefaultJCVersion(defaultVersion):
    if isinstance(defaultVersion,int):
        spss.__SetPlugInVersion('spss' + str(defaultVersion))
    else:
        modulename = defaultVersion[:-3]
        version = defaultVersion[-3:]
        if modulename == "SpssClient":
            modulename = "spss"
        spss.__SetPlugInVersion(modulename + version)

def __DisableExitInFrontendAndBackendPython():
    None


from _SpssClient import *
__local__ = locals()
if (os.getenv("FRONTEND_RUN_AUTO") == "True") | (os.getenv("BACKEND_PYTHON_SCRIPT") == "True"):
    Exit = __DisableExitInFrontendAndBackendPython

def _heartBeat(status = None):
    """Get or Set the heart beat status."""
    if status == None:
        return _SpssClient._getHeartBeat()
    else:
        return _SpssClient._setHeartBeat(status)

import threading
import time

class HeartbeatThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.isalive = True
    def stopHeartbeat(self):
        try:
            self.isalive = False
        except Exception:
            pass
    def setProxy(self,p):
        self.proxy = p
    def setLock(self, l):
        self.lock = l
    def setSession(self, idstr):
        self.sessionid = idstr
    def run(self):
        while(self.isalive):
            self.lock.acquire()
            try:
                arg = {'session_id':self.sessionid}
                self.proxy.sendHeartBeat(arg) 
            except Exception:
                return
            finally:
                self.lock.release()
            time.sleep(15)

def getHeartbeat():
    _objHeartbeatThread = HeartbeatThread()
    _objHeartbeatThread.setDaemon(True)
    return _objHeartbeatThread

def _stopSpssClient():
    _SpssClient.StopClient()

atexit.register(_stopSpssClient)

import spss

class sessionMgr(object):
    _inst = None
    _count = 0
    def __new__(clas):
        if not clas._inst:
            clas._inst = super(sessionMgr, clas).__new__(clas)
        return clas._inst
    def getCount(clas):
        return clas._count
    def setCount(clas,c):
        if c >= 0:
            clas._count = c

def getSessionMgr():
    return sessionMgr()

def StartClient():
    sm = getSessionMgr()
    sm.setCount(sm.getCount() + 1)
    return _SpssClient.StartClient()

def StopClient():
    sm = getSessionMgr()
    if spss.GetNestState():
        if sm.getCount() == 1:
            _SpssClient.StopClient()
    else:
        _SpssClient.StopClient()
    sm.setCount(sm.getCount() - 1)


def __raiseJCAdaptorException(eCode, eMsg, eCause):
    raise JCAdaptorException(eCode, eMsg, eCause)
    
def __raiseSpssClientException(eCode, eMsg, eCause):
    raise SpssClientException(eCode, eMsg, eCause)

class JCAdaptorException(Exception):
    def __init__(self, eCode, eMsg, eCause):
        self.args = (eCode, eMsg.decode('utf-8'), eCause.decode('utf-8'))
        
    def __str__(self):
        return "(%s, '%s', '%s')" % (self.args[0], self.args[1], self.args[2])
            
class SpssClientException(Exception):
    def __init__(self, eCode, eMsg, eCause):
        self.args = (eCode, eMsg.decode('utf-8'), eCause.decode('utf-8'))
        
    def __str__(self):
        return "(%s, '%s', '%s')" % (self.args[0], self.args[1], self.args[2])
        
import types

class ChartExportFormat(object):
    values = {}
    bmp = None
    emf = None
    eps = None
    jpg = None
    png = None
    tiff = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'bmp'
        elif self.numerator == 1:
            self.name = 'emf'
        elif self.numerator == 2:
            self.name = 'eps'
        elif self.numerator == 3:
            self.name = 'jpg'
        elif self.numerator == 4:
            self.name = 'png'
        elif self.numerator == 5:
            self.name = 'tiff'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.ChartExportFormat.bmp'
        elif self.numerator == 1:
            return 'SpssClient.ChartExportFormat.emf'
        elif self.numerator == 2:
            return 'SpssClient.ChartExportFormat.eps'
        elif self.numerator == 3:
            return 'SpssClient.ChartExportFormat.jpg'
        elif self.numerator == 4:
            return 'SpssClient.ChartExportFormat.png'
        elif self.numerator == 5:
            return 'SpssClient.ChartExportFormat.tiff'

ChartExportFormat.bmp = ChartExportFormat(0)
ChartExportFormat.emf = ChartExportFormat(1)
ChartExportFormat.eps = ChartExportFormat(2)
ChartExportFormat.jpg = ChartExportFormat(3)
ChartExportFormat.png = ChartExportFormat(4)
ChartExportFormat.tiff = ChartExportFormat(5)

ChartExportFormat.values.update({0:ChartExportFormat.bmp})
ChartExportFormat.values.update({1:ChartExportFormat.emf})
ChartExportFormat.values.update({2:ChartExportFormat.eps})
ChartExportFormat.values.update({3:ChartExportFormat.jpg})
ChartExportFormat.values.update({4:ChartExportFormat.png})
ChartExportFormat.values.update({5:ChartExportFormat.tiff})

class DocExportFormat(object):
    values = {}
    SpssFormatHtml = None
    SpssFormatText = None
    SpssFormatXls = None
    SpssFormatDoc = None
    SpssFormatPpt = None
    SpssFormatPdf = None
    SpssFormatXlsx = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssFormatHtml'
        elif self.numerator == 1:
            self.name = 'SpssFormatText'
        elif self.numerator == 2:
            self.name = 'SpssFormatXls'
        elif self.numerator == 3:
            self.name = 'SpssFormatDoc'
        elif self.numerator == 4:
            self.name = 'SpssFormatPpt'
        elif self.numerator == 5:
            self.name = 'SpssFormatPdf'
        elif self.numerator == 6:
            self.name = 'SpssFormatXlsx'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.DocExportFormat.SpssFormatHtml'
        elif self.numerator == 1:
            return 'SpssClient.DocExportFormat.SpssFormatText'
        elif self.numerator == 2:
            return 'SpssClient.DocExportFormat.SpssFormatXls'
        elif self.numerator == 3:
            return 'SpssClient.DocExportFormat.SpssFormatDoc'
        elif self.numerator == 4:
            return 'SpssClient.DocExportFormat.SpssFormatPpt'
        elif self.numerator == 5:
            return 'SpssClient.DocExportFormat.SpssFormatPdf'
        elif self.numerator == 6:
            return "SpssClient.DocExportFormat.SpssFormatXlsx"

DocExportFormat.SpssFormatHtml = DocExportFormat(0)
DocExportFormat.SpssFormatText = DocExportFormat(1)
DocExportFormat.SpssFormatXls = DocExportFormat(2)
DocExportFormat.SpssFormatDoc = DocExportFormat(3)
DocExportFormat.SpssFormatPpt = DocExportFormat(4)
DocExportFormat.SpssFormatPdf = DocExportFormat(5)
DocExportFormat.SpssFormatXlsx = DocExportFormat(6)

DocExportFormat.values.update({0:DocExportFormat.SpssFormatHtml})
DocExportFormat.values.update({1:DocExportFormat.SpssFormatText})
DocExportFormat.values.update({2:DocExportFormat.SpssFormatXls})
DocExportFormat.values.update({3:DocExportFormat.SpssFormatDoc})
DocExportFormat.values.update({4:DocExportFormat.SpssFormatPpt})
DocExportFormat.values.update({5:DocExportFormat.SpssFormatPdf})
DocExportFormat.values.update({6:DocExportFormat.SpssFormatXlsx})

class DocExportOption(object):
    values = {}
    ExcelSheetNames = None
    ExcelStartingCell = None
    ExcelOperationOptions = None
    ExcelLocationOptions = None
    WideTablesOptions = None
    ItemsPageHeight = None
    ItemsPageWidth = None
    ItemsTopMargin = None
    ItemsBottomMargin = None
    ItemsRightMargin = None
    ItemsLeftMargin = None
    ItemsMeasurementUnits = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'ExcelSheetNames'
        elif self.numerator == 1:
            self.name = 'ExcelStartingCell'
        elif self.numerator == 2:
            self.name = 'ExcelOperationOptions'
        elif self.numerator == 3:
            self.name = 'ExcelLocationOptions'
        elif self.numerator == 4:
            self.name = 'WideTablesOptions'
        elif self.numerator == 6:
            self.name = 'ItemsPageHeight'
        elif self.numerator == 7:
            self.name = 'ItemsPageWidth'
        elif self.numerator == 8:
            self.name = 'ItemsTopMargin'
        elif self.numerator == 9:
            self.name = 'ItemsBottomMargin'
        elif self.numerator == 10:
            self.name = 'ItemsRightMargin'
        elif self.numerator == 11:
            self.name = 'ItemsLeftMargin'
        elif self.numerator == 12:
            self.name = 'ItemsMeasurementUnits'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.DocExportOption.ExcelSheetNames'
        elif self.numerator == 1:
            return 'SpssClient.DocExportOption.ExcelStartingCell'
        elif self.numerator == 2:
            return 'SpssClient.DocExportOption.ExcelOperationOptions'
        elif self.numerator == 3:
            return 'SpssClient.DocExportOption.ExcelLocationOptions'
        elif self.numerator == 4:
            return 'SpssClient.DocExportOption.WideTablesOptions'
        elif self.numerator == 6:
            return 'SpssClient.DocExportOption.ItemsPageHeight'
        elif self.numerator == 7:
            return 'SpssClient.DocExportOption.ItemsPageWidth'
        elif self.numerator == 8:
            return 'SpssClient.DocExportOption.ItemsTopMargin'
        elif self.numerator == 9:
            return 'SpssClient.DocExportOption.ItemsBottomMargin'
        elif self.numerator == 10:
            return 'SpssClient.DocExportOption.ItemsRightMargin'
        elif self.numerator == 11:
            return 'SpssClient.DocExportOption.ItemsLeftMargin'
        elif self.numerator == 12:
            return 'SpssClient.DocExportOption.ItemsMeasurementUnits'

DocExportOption.ExcelSheetNames = DocExportOption(0)
DocExportOption.ExcelStartingCell = DocExportOption(1)
DocExportOption.ExcelOperationOptions = DocExportOption(2)
DocExportOption.ExcelLocationOptions = DocExportOption(3)
DocExportOption.WideTablesOptions = DocExportOption(4)
DocExportOption.ItemsPageHeight = DocExportOption(6)
DocExportOption.ItemsPageWidth = DocExportOption(7)
DocExportOption.ItemsTopMargin = DocExportOption(8)
DocExportOption.ItemsBottomMargin = DocExportOption(9)
DocExportOption.ItemsRightMargin = DocExportOption(10)
DocExportOption.ItemsLeftMargin = DocExportOption(11)
DocExportOption.ItemsMeasurementUnits = DocExportOption(12)

DocExportOption.values.update({0:DocExportOption.ExcelSheetNames})
DocExportOption.values.update({1:DocExportOption.ExcelStartingCell})
DocExportOption.values.update({2:DocExportOption.ExcelOperationOptions})
DocExportOption.values.update({3:DocExportOption.ExcelLocationOptions})
DocExportOption.values.update({4:DocExportOption.WideTablesOptions})
DocExportOption.values.update({6:DocExportOption.ItemsPageHeight})
DocExportOption.values.update({7:DocExportOption.ItemsPageWidth})
DocExportOption.values.update({8:DocExportOption.ItemsTopMargin})
DocExportOption.values.update({9:DocExportOption.ItemsBottomMargin})
DocExportOption.values.update({10:DocExportOption.ItemsRightMargin})
DocExportOption.values.update({11:DocExportOption.ItemsLeftMargin})
DocExportOption.values.update({12:DocExportOption.ItemsMeasurementUnits})


class ExportOptions(object):
    values = {}
    ObjectsToExport = None
    DocExportType = None
    DocFilePath = None
    GraphExportType = None
    GraphFilePath = None
    XLSLayers = None
    XLSFootnotes = None
    XLSLocation = None
    HTMLayers = None
    HTMFootnotes = None
    WordRTFLayers = None
    WordRTFFootnotes = None
    TXTPlainTabsOrSpaces = None
    TXTPlainColumnWidthType = None
    TXTPlainNoOfChars = None
    TXTPlainRowBorderChar = None
    TXTPlainColBorderChar = None
    TxtPlainLayersInPivotTable = None
    TXTPlainFootnoteCaption = None
    TXTPlainInsertPageBreak = None
    TXTUTF8TabsOrSpaces = None
    TXTUTF8ColumnWidthType = None
    TXTUTF8NoOfChars = None
    TXTUTF8RowBorderChar = None
    TXTUTF8ColBorderChar = None
    TxtUTF8LayersInPivotTable = None
    TXTUTF8FootnoteCaption = None
    TXTUTF8InsertPageBreak = None
    TXTUTF16TabsOrSpaces = None
    TXTUTF16ColumnWidthType = None
    TXTUTF16NoOfChars = None
    TXTUTF16RowBorderChar = None
    TXTUTF16ColBorderChar = None
    TxtUTF16LayersInPivotTable = None
    TXTUTF16FootnoteCaption = None
    TXTUTF16InsertPageBreak = None
    PDFEmbedBookmarks = None
    PDFEmbedFonts = None
    PDFLayers = None
    JPEGSize = None
    JPEGGreyScale = None
    BMPSize = None
    BMPCompressImage = None
    PNGSize = None
    PNGColorDepth = None
    TIFSize = None
    EPSSize = None
    EPSPercent = None
    EPSWidthPoints = None
    EPSPreviewImage = None
    EPSFont = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 1101:
            self.name = 'ObjectsToExport'
        elif self.numerator == 1102:
            self.name = 'DocExportType'
        elif self.numerator == 1103:
            self.name = 'DocFilePath'
        elif self.numerator == 1104:
            self.name = 'GraphExportType'
        elif self.numerator == 1105:
            self.name = 'GraphFilePath'
        elif self.numerator == 2101:
            self.name = 'XLSLayers'
        elif self.numerator == 2102:
            self.name = 'XLSFootnotes'
        elif self.numerator == 2103:
            self.name = 'XLSLocation'
        elif self.numerator == 2201:
            self.name = 'HTMLayers'
        elif self.numerator == 2202:
            self.name = 'HTMFootnotes'
        elif self.numerator == 2301:
            self.name = 'WordRTFLayers'
        elif self.numerator == 2302:
            self.name = 'WordRTFFootnotes'
        elif self.numerator == 2401:
            self.name = 'TXTPlainTabsOrSpaces'
        elif self.numerator == 2402:
            self.name = 'TXTPlainColumnWidthType'
        elif self.numerator == 2403:
            self.name = 'TXTPlainNoOfChars'
        elif self.numerator == 2404:
            self.name = 'TXTPlainRowBorderChar'
        elif self.numerator == 2405:
            self.name = 'TXTPlainColBorderChar'
        elif self.numerator == 2406:
            self.name = 'TxtPlainLayersInPivotTable'
        elif self.numerator == 2407:
            self.name = 'TXTPlainFootnoteCaption'
        elif self.numerator == 2408:
            self.name = 'TXTPlainInsertPageBreak'
        elif self.numerator == 2501:
            self.name = 'TXTUTF8TabsOrSpaces'
        elif self.numerator == 2502:
            self.name = 'TXTUTF8ColumnWidthType'
        elif self.numerator == 2503:
            self.name = 'TXTUTF8NoOfChars'
        elif self.numerator == 2504:
            self.name = 'TXTUTF8RowBorderChar'
        elif self.numerator == 2505:
            self.name = 'TXTUTF8ColBorderChar'
        elif self.numerator == 2506:
            self.name = 'TxtUTF8LayersInPivotTable'
        elif self.numerator == 2507:
            self.name = 'TXTUTF8FootnoteCaption'
        elif self.numerator == 2508:
            self.name = 'TXTUTF8InsertPageBreak'
        elif self.numerator == 2601:
            self.name = 'TXTUTF16TabsOrSpaces'
        elif self.numerator == 2602:
            self.name = 'TXTUTF16ColumnWidthType'
        elif self.numerator == 2603:
            self.name = 'TXTUTF16NoOfChars'
        elif self.numerator == 2604:
            self.name = 'TXTUTF16RowBorderChar'
        elif self.numerator == 2605:
            self.name = 'TXTUTF16ColBorderChar'
        elif self.numerator == 2606:
            self.name = 'TxtUTF16LayersInPivotTable'
        elif self.numerator == 2607:
            self.name = 'TXTUTF16FootnoteCaption'
        elif self.numerator == 2608:
            self.name = 'TXTUTF16InsertPageBreak'
        elif self.numerator == 2702:
            self.name = 'PDFEmbedBookmarks'
        elif self.numerator == 2703:
            self.name = 'PDFEmbedFonts'
        elif self.numerator == 2705:
            self.name = 'PDFLayers'
        elif self.numerator == 3101:
            self.name = 'JPEGSize'
        elif self.numerator == 3102:
            self.name = 'JPEGGreyScale'
        elif self.numerator == 3201:
            self.name = 'BMPSize'
        elif self.numerator == 3202:
            self.name = 'BMPCompressImage'
        elif self.numerator == 3301:
            self.name = 'PNGSize'
        elif self.numerator == 3302:
            self.name = 'PNGColorDepth'
        elif self.numerator == 3401:
            self.name = 'TIFSize'
        elif self.numerator == 3501:
            self.name = 'EPSSize'
        elif self.numerator == 3502:
            self.name = 'EPSPercent'
        elif self.numerator == 3503:
            self.name = 'EPSWidthPoints'
        elif self.numerator == 3504:
            self.name = 'EPSPreviewImage'
        elif self.numerator == 3505:
            self.name = 'EPSFont'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 1101:
            return 'SpssClient.ExportOptions.ObjectsToExport'
        elif self.numerator == 1102:
            return 'SpssClient.ExportOptions.DocExportType'
        elif self.numerator == 1103:
            return 'SpssClient.ExportOptions.DocFilePath'
        elif self.numerator == 1104:
            return 'SpssClient.ExportOptions.GraphExportType'
        elif self.numerator == 1105:
            return 'SpssClient.ExportOptions.GraphFilePath'
        elif self.numerator == 2101:
            return 'SpssClient.ExportOptions.XLSLayers'
        elif self.numerator == 2102:
            return 'SpssClient.ExportOptions.XLSFootnotes'
        elif self.numerator == 2103:
            return 'SpssClient.ExportOptions.XLSLocation'
        elif self.numerator == 2201:
            return 'SpssClient.ExportOptions.HTMLayers'
        elif self.numerator == 2202:
            return 'SpssClient.ExportOptions.HTMFootnotes'
        elif self.numerator == 2301:
            return 'SpssClient.ExportOptions.WordRTFLayers'
        elif self.numerator == 2302:
            return 'SpssClient.ExportOptions.WordRTFFootnotes'
        elif self.numerator == 2401:
            return 'SpssClient.ExportOptions.TXTPlainTabsOrSpaces'
        elif self.numerator == 2402:
            return 'SpssClient.ExportOptions.TXTPlainColumnWidthType'
        elif self.numerator == 2403:
            return 'SpssClient.ExportOptions.TXTPlainNoOfChars'
        elif self.numerator == 2404:
            return 'SpssClient.ExportOptions.TXTPlainRowBorderChar'
        elif self.numerator == 2405:
            return 'SpssClient.ExportOptions.TXTPlainColBorderChar'
        elif self.numerator == 2406:
            return 'SpssClient.ExportOptions.TxtPlainLayersInPivotTable'
        elif self.numerator == 2407:
            return 'SpssClient.ExportOptions.TXTPlainFootnoteCaption'
        elif self.numerator == 2408:
            return 'SpssClient.ExportOptions.TXTPlainInsertPageBreak'
        elif self.numerator == 2501:
            return 'SpssClient.ExportOptions.TXTUTF8TabsOrSpaces'
        elif self.numerator == 2502:
            return 'SpssClient.ExportOptions.TXTUTF8ColumnWidthType'
        elif self.numerator == 2503:
            return 'SpssClient.ExportOptions.TXTUTF8NoOfChars'
        elif self.numerator == 2504:
            return 'SpssClient.ExportOptions.TXTUTF8RowBorderChar'
        elif self.numerator == 2505:
            return 'SpssClient.ExportOptions.TXTUTF8ColBorderChar'
        elif self.numerator == 2506:
            return 'SpssClient.ExportOptions.TxtUTF8LayersInPivotTable'
        elif self.numerator == 2507:
            return 'SpssClient.ExportOptions.TXTUTF8FootnoteCaption'
        elif self.numerator == 2508:
            return 'SpssClient.ExportOptions.TXTUTF8InsertPageBreak'
        elif self.numerator == 2601:
            return 'SpssClient.ExportOptions.TXTUTF16TabsOrSpaces'
        elif self.numerator == 2602:
            return 'SpssClient.ExportOptions.TXTUTF16ColumnWidthType'
        elif self.numerator == 2603:
            return 'SpssClient.ExportOptions.TXTUTF16NoOfChars'
        elif self.numerator == 2604:
            return 'SpssClient.ExportOptions.TXTUTF16RowBorderChar'
        elif self.numerator == 2605:
            return 'SpssClient.ExportOptions.TXTUTF16ColBorderChar'
        elif self.numerator == 2606:
            return 'SpssClient.ExportOptions.TxtUTF16LayersInPivotTable'
        elif self.numerator == 2607:
            return 'SpssClient.ExportOptions.TXTUTF16FootnoteCaption'
        elif self.numerator == 2608:
            return 'SpssClient.ExportOptions.TXTUTF16InsertPageBreak'
        elif self.numerator == 2702:
            return 'SpssClient.ExportOptions.PDFEmbedBookmarks'
        elif self.numerator == 2703:
            return 'SpssClient.ExportOptions.PDFEmbedFonts'
        elif self.numerator == 2705:
            return 'SpssClient.ExportOptions.PDFLayers'
        elif self.numerator == 3101:
            return 'SpssClient.ExportOptions.JPEGSize'
        elif self.numerator == 3102:
            return 'SpssClient.ExportOptions.JPEGGreyScale'
        elif self.numerator == 3201:
            return 'SpssClient.ExportOptions.BMPSize'
        elif self.numerator == 3202:
            return 'SpssClient.ExportOptions.BMPCompressImage'
        elif self.numerator == 3301:
            return 'SpssClient.ExportOptions.PNGSize'
        elif self.numerator == 3302:
            return 'SpssClient.ExportOptions.PNGColorDepth'
        elif self.numerator == 3401:
            return 'SpssClient.ExportOptions.TIFSize'
        elif self.numerator == 3501:
            return 'SpssClient.ExportOptions.EPSSize'
        elif self.numerator == 3502:
            return 'SpssClient.ExportOptions.EPSPercent'
        elif self.numerator == 3503:
            return 'SpssClient.ExportOptions.EPSWidthPoints'
        elif self.numerator == 3504:
            return 'SpssClient.ExportOptions.EPSPreviewImage'
        elif self.numerator == 3505:
            return 'SpssClient.ExportOptions.EPSFont'

ExportOptions.ObjectsToExport = ExportOptions(1101)
ExportOptions.DocExportType = ExportOptions(1102)
ExportOptions.DocFilePath = ExportOptions(1103)
ExportOptions.GraphExportType = ExportOptions(1104)
ExportOptions.GraphFilePath = ExportOptions(1105)
ExportOptions.XLSLayers = ExportOptions(2101)
ExportOptions.XLSFootnotes = ExportOptions(2102)
ExportOptions.XLSLocation = ExportOptions(2103)
ExportOptions.HTMLayers = ExportOptions(2201)
ExportOptions.HTMFootnotes = ExportOptions(2202)
ExportOptions.WordRTFLayers = ExportOptions(2301)
ExportOptions.WordRTFFootnotes = ExportOptions(2302)
ExportOptions.TXTPlainTabsOrSpaces = ExportOptions(2401)
ExportOptions.TXTPlainColumnWidthType = ExportOptions(2402)
ExportOptions.TXTPlainNoOfChars = ExportOptions(2403)
ExportOptions.TXTPlainRowBorderChar = ExportOptions(2404)
ExportOptions.TXTPlainColBorderChar = ExportOptions(2405)
ExportOptions.TxtPlainLayersInPivotTable = ExportOptions(2406)
ExportOptions.TXTPlainFootnoteCaption = ExportOptions(2407)
ExportOptions.TXTPlainInsertPageBreak = ExportOptions(2408)
ExportOptions.TXTUTF8TabsOrSpaces = ExportOptions(2501)
ExportOptions.TXTUTF8ColumnWidthType = ExportOptions(2502)
ExportOptions.TXTUTF8NoOfChars = ExportOptions(2503)
ExportOptions.TXTUTF8RowBorderChar = ExportOptions(2504)
ExportOptions.TXTUTF8ColBorderChar = ExportOptions(2505)
ExportOptions.TxtUTF8LayersInPivotTable = ExportOptions(2506)
ExportOptions.TXTUTF8FootnoteCaption = ExportOptions(2507)
ExportOptions.TXTUTF8InsertPageBreak = ExportOptions(2508)
ExportOptions.TXTUTF16TabsOrSpaces = ExportOptions(2601)
ExportOptions.TXTUTF16ColumnWidthType = ExportOptions(2602)
ExportOptions.TXTUTF16NoOfChars = ExportOptions(2603)
ExportOptions.TXTUTF16RowBorderChar = ExportOptions(2604)
ExportOptions.TXTUTF16ColBorderChar = ExportOptions(2605)
ExportOptions.TxtUTF16LayersInPivotTable = ExportOptions(2606)
ExportOptions.TXTUTF16FootnoteCaption = ExportOptions(2607)
ExportOptions.TXTUTF16InsertPageBreak = ExportOptions(2608)
ExportOptions.PDFEmbedBookmarks = ExportOptions(2702)
ExportOptions.PDFEmbedFonts = ExportOptions(2703)
ExportOptions.PDFLayers = ExportOptions(2705)
ExportOptions.JPEGSize = ExportOptions(3101)
ExportOptions.JPEGGreyScale = ExportOptions(3102)
ExportOptions.BMPSize = ExportOptions(3201)
ExportOptions.BMPCompressImage = ExportOptions(3202)
ExportOptions.PNGSize = ExportOptions(3301)
ExportOptions.PNGColorDepth = ExportOptions(3302)
ExportOptions.TIFSize = ExportOptions(3401)
ExportOptions.EPSSize = ExportOptions(3501)
ExportOptions.EPSPercent = ExportOptions(3502)
ExportOptions.EPSWidthPoints = ExportOptions(3503)
ExportOptions.EPSPreviewImage = ExportOptions(3504)
ExportOptions.EPSFont = ExportOptions(3505)

ExportOptions.values.update({1101:ExportOptions.ObjectsToExport})
ExportOptions.values.update({1102:ExportOptions.DocExportType})
ExportOptions.values.update({1103:ExportOptions.DocFilePath})
ExportOptions.values.update({1104:ExportOptions.GraphExportType})
ExportOptions.values.update({1105:ExportOptions.GraphFilePath})
ExportOptions.values.update({2101:ExportOptions.XLSLayers})
ExportOptions.values.update({2102:ExportOptions.XLSFootnotes})
ExportOptions.values.update({2103:ExportOptions.XLSLocation})
ExportOptions.values.update({2201:ExportOptions.HTMLayers})
ExportOptions.values.update({2202:ExportOptions.HTMFootnotes})
ExportOptions.values.update({2301:ExportOptions.WordRTFLayers})
ExportOptions.values.update({2302:ExportOptions.WordRTFFootnotes})
ExportOptions.values.update({2401:ExportOptions.TXTPlainTabsOrSpaces})
ExportOptions.values.update({2402:ExportOptions.TXTPlainColumnWidthType})
ExportOptions.values.update({2403:ExportOptions.TXTPlainNoOfChars})
ExportOptions.values.update({2404:ExportOptions.TXTPlainRowBorderChar})
ExportOptions.values.update({2405:ExportOptions.TXTPlainColBorderChar})
ExportOptions.values.update({2406:ExportOptions.TxtPlainLayersInPivotTable})
ExportOptions.values.update({2407:ExportOptions.TXTPlainFootnoteCaption})
ExportOptions.values.update({2408:ExportOptions.TXTPlainInsertPageBreak})
ExportOptions.values.update({2501:ExportOptions.TXTUTF8TabsOrSpaces})
ExportOptions.values.update({2502:ExportOptions.TXTUTF8ColumnWidthType})
ExportOptions.values.update({2503:ExportOptions.TXTUTF8NoOfChars})
ExportOptions.values.update({2504:ExportOptions.TXTUTF8RowBorderChar})
ExportOptions.values.update({2505:ExportOptions.TXTUTF8ColBorderChar})
ExportOptions.values.update({2506:ExportOptions.TxtUTF8LayersInPivotTable})
ExportOptions.values.update({2507:ExportOptions.TXTUTF8FootnoteCaption})
ExportOptions.values.update({2508:ExportOptions.TXTUTF8InsertPageBreak})
ExportOptions.values.update({2601:ExportOptions.TXTUTF16TabsOrSpaces})
ExportOptions.values.update({2602:ExportOptions.TXTUTF16ColumnWidthType})
ExportOptions.values.update({2603:ExportOptions.TXTUTF16NoOfChars})
ExportOptions.values.update({2604:ExportOptions.TXTUTF16RowBorderChar})
ExportOptions.values.update({2605:ExportOptions.TXTUTF16ColBorderChar})
ExportOptions.values.update({2606:ExportOptions.TxtUTF16LayersInPivotTable})
ExportOptions.values.update({2607:ExportOptions.TXTUTF16FootnoteCaption})
ExportOptions.values.update({2608:ExportOptions.TXTUTF16InsertPageBreak})
ExportOptions.values.update({2702:ExportOptions.PDFEmbedBookmarks})
ExportOptions.values.update({2703:ExportOptions.PDFEmbedFonts})
ExportOptions.values.update({2705:ExportOptions.PDFLayers})
ExportOptions.values.update({3101:ExportOptions.JPEGSize})
ExportOptions.values.update({3102:ExportOptions.JPEGGreyScale})
ExportOptions.values.update({3201:ExportOptions.BMPSize})
ExportOptions.values.update({3202:ExportOptions.BMPCompressImage})
ExportOptions.values.update({3301:ExportOptions.PNGSize})
ExportOptions.values.update({3302:ExportOptions.PNGColorDepth})
ExportOptions.values.update({3401:ExportOptions.TIFSize})
ExportOptions.values.update({3501:ExportOptions.EPSSize})
ExportOptions.values.update({3502:ExportOptions.EPSPercent})
ExportOptions.values.update({3503:ExportOptions.EPSWidthPoints})
ExportOptions.values.update({3504:ExportOptions.EPSPreviewImage})
ExportOptions.values.update({3505:ExportOptions.EPSFont})


class LicenseOption(object):
    values = {}
    BASE = None
    TABLES = None
    PRO_STATS = None
    ADVANCED_STATS = None
    OLD_TRENDS = None
    CYTEL = None
    MARKET_RESEARCH = None
    MISSING_VALUES = None
    CONJOINT = None
    MAPX = None
    CUSTOM_TABLES = None
    COMPLEX_SAMPLE = None
    TREEVIEW = None
    VALIDATEDATA = None
    PROGRAMMABILITY = None
    ADVANCED_VISUALIZATION = None
    TRENDS = None
    PES = None
    NEURAL_NETWORK = None
    RFM = None
    BOOTSTRAPPING = None
    EXTENDED_BASE = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'BASE'
        elif self.numerator == 1:
            self.name = 'TABLES'
        elif self.numerator == 2:
            self.name = 'PRO_STATS'
        elif self.numerator == 3:
            self.name = 'ADVANCED_STATS'
        elif self.numerator == 4:
            self.name = 'OLD_TRENDS'
        elif self.numerator == 5:
            self.name = 'CYTEL'
        elif self.numerator == 6:
            self.name = 'MARKET_RESEARCH'
        elif self.numerator == 7:
            self.name = 'MISSING_VALUES'
        elif self.numerator == 8:
            self.name = 'CONJOINT'
        elif self.numerator == 9:
            self.name = 'MAPX'
        elif self.numerator == 10:
            self.name = 'CUSTOM_TABLES'
        elif self.numerator == 11:
            self.name = 'COMPLEX_SAMPLE'
        elif self.numerator == 12:
            self.name = 'TREEVIEW'
        elif self.numerator == 13:
            self.name = 'VALIDATEDATA'
        elif self.numerator == 14:
            self.name = 'PROGRAMMABILITY'
        elif self.numerator == 15:
            self.name = 'ADVANCED_VISUALIZATION'
        elif self.numerator == 16:
            self.name = 'TRENDS'
        elif self.numerator == 17:
            self.name = 'PES'
        elif self.numerator == 18:
            self.name = 'NEURAL_NETWORK'
        elif self.numerator == 19:
            self.name = 'RFM'
        elif self.numerator == 20:
            self.name = 'BOOTSTRAPPING'
        elif self.numerator == 21:
            self.name = 'EXTENDED_BASE'
         

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.LicenseOption.BASE'
        elif self.numerator == 1:
            return 'SpssClient.LicenseOption.TABLES'
        elif self.numerator == 2:
            return 'SpssClient.LicenseOption.PRO_STATS'
        elif self.numerator == 3:
            return 'SpssClient.LicenseOption.ADVANCED_STATS'
        elif self.numerator == 4:
            return 'SpssClient.LicenseOption.OLD_TRENDS'
        elif self.numerator == 5:
            return 'SpssClient.LicenseOption.CYTEL'
        elif self.numerator == 6:
            return 'SpssClient.LicenseOption.MARKET_RESEARCH'
        elif self.numerator == 7:
            return 'SpssClient.LicenseOption.MISSING_VALUES'
        elif self.numerator == 8:
            return 'SpssClient.LicenseOption.CONJOINT'
        elif self.numerator == 9:
            return 'SpssClient.LicenseOption.MAPX'
        elif self.numerator == 10:
            return 'SpssClient.LicenseOption.CUSTOM_TABLES'
        elif self.numerator == 11:
            return 'SpssClient.LicenseOption.COMPLEX_SAMPLE'
        elif self.numerator == 12:
            return 'SpssClient.LicenseOption.TREEVIEW'
        elif self.numerator == 13:
            return 'SpssClient.LicenseOption.VALIDATEDATA'
        elif self.numerator == 14:
            return 'SpssClient.LicenseOption.PROGRAMMABILITY'
        elif self.numerator == 15:
            return 'SpssClient.LicenseOption.ADVANCED_VISUALIZATION'
        elif self.numerator == 16:
            return 'SpssClient.LicenseOption.TRENDS'
        elif self.numerator == 17:
            return 'SpssClient.LicenseOption.PES'
        elif self.numerator == 18:
            return 'SpssClient.LicenseOption.NEURAL_NETWORK'
        elif self.numerator == 19:
            return 'SpssClient.LicenseOption.RFM'
        elif self.numerator == 20:
            return 'SpssClient.LicenseOption.BOOTSTRAPPING'
        elif self.numerator == 21:
            return 'SpssClient.LicenseOption.EXTENDED_BASE'

LicenseOption.BASE = LicenseOption(0)
LicenseOption.TABLES = LicenseOption(1)
LicenseOption.PRO_STATS = LicenseOption(2)
LicenseOption.ADVANCED_STATS = LicenseOption(3)
LicenseOption.OLD_TRENDS = LicenseOption(4)
LicenseOption.CYTEL = LicenseOption(5)
LicenseOption.MARKET_RESEARCH = LicenseOption(6)
LicenseOption.MISSING_VALUES = LicenseOption(7)
LicenseOption.CONJOINT = LicenseOption(8)
LicenseOption.MAPX = LicenseOption(9)
LicenseOption.CUSTOM_TABLES = LicenseOption(10)
LicenseOption.COMPLEX_SAMPLE = LicenseOption(11)
LicenseOption.TREEVIEW = LicenseOption(12)
LicenseOption.VALIDATEDATA = LicenseOption(13)
LicenseOption.PROGRAMMABILITY = LicenseOption(14)
LicenseOption.ADVANCED_VISUALIZATION = LicenseOption(15)
LicenseOption.TRENDS = LicenseOption(16)
LicenseOption.PES = LicenseOption(17)
LicenseOption.NEURAL_NETWORK = LicenseOption(18)
LicenseOption.RFM = LicenseOption(19)
LicenseOption.BOOTSTRAPPING = LicenseOption(20)
LicenseOption.EXTENDED_BASE = LicenseOption(21)

LicenseOption.values.update({0:LicenseOption.BASE})
LicenseOption.values.update({1:LicenseOption.TABLES})
LicenseOption.values.update({2:LicenseOption.PRO_STATS})
LicenseOption.values.update({3:LicenseOption.ADVANCED_STATS})
LicenseOption.values.update({4:LicenseOption.OLD_TRENDS})
LicenseOption.values.update({5:LicenseOption.CYTEL})
LicenseOption.values.update({6:LicenseOption.MARKET_RESEARCH})
LicenseOption.values.update({7:LicenseOption.MISSING_VALUES})
LicenseOption.values.update({8:LicenseOption.CONJOINT})
LicenseOption.values.update({9:LicenseOption.MAPX})
LicenseOption.values.update({10:LicenseOption.CUSTOM_TABLES})
LicenseOption.values.update({11:LicenseOption.COMPLEX_SAMPLE})
LicenseOption.values.update({12:LicenseOption.TREEVIEW})
LicenseOption.values.update({13:LicenseOption.VALIDATEDATA})
LicenseOption.values.update({14:LicenseOption.PROGRAMMABILITY})
LicenseOption.values.update({15:LicenseOption.ADVANCED_VISUALIZATION})
LicenseOption.values.update({16:LicenseOption.TRENDS})
LicenseOption.values.update({17:LicenseOption.PES})
LicenseOption.values.update({18:LicenseOption.NEURAL_NETWORK})
LicenseOption.values.update({19:LicenseOption.RFM})
LicenseOption.values.update({20:LicenseOption.BOOTSTRAPPING})
LicenseOption.values.update({21:LicenseOption.EXTENDED_BASE})

class OutputItemAlignment(object):
    values = {}
    Left = None 
    Center = None
    Right = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'Left'
        if self.numerator == 1:
            self.name = 'Center'
        if self.numerator == 2:
            self.name = 'Right'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.OutputItemAlignment.Left'
        if self.numerator == 1:
            return 'SpssClient.OutputItemAlignment.Center'
        if self.numerator == 2:
            return 'SpssClient.OutputItemAlignment.Right'

OutputItemAlignment.Left = OutputItemAlignment(0)
OutputItemAlignment.Center = OutputItemAlignment(1)
OutputItemAlignment.Right = OutputItemAlignment(2)

OutputItemAlignment.values.update({0:OutputItemAlignment.Left})
OutputItemAlignment.values.update({1:OutputItemAlignment.Center})
OutputItemAlignment.values.update({2:OutputItemAlignment.Right})

class OutputItemType(object):
    values = {}
    UNKNOWN = None
    CHART = None
    HEAD = None
    LOG = None
    NOTE = None
    PIVOT = None
    ROOT = None
    TEXT = None
    WARNING = None
    TITLE = None
    IGRAPH = None
    PAGETITLE = None
    TREEMODEL = None
    GENERIC = None
    MODEL = None
    GRAPHBOARD = None
    IMAGE = None
    LIGHTNOTE = None
    LIGHTPIVOT = None
    LIGHTWARNING = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'UNKNOWN'
        if self.numerator == 1:
            self.name = 'CHART'
        if self.numerator == 2:
            self.name = 'HEAD'
        if self.numerator == 3:
            self.name = 'LOG'
        if self.numerator == 4:
            self.name = 'NOTE'
        if self.numerator == 5:
            self.name = 'PIVOT'
        if self.numerator == 6:
            self.name = 'ROOT'
        if self.numerator == 7:
            self.name = 'TEXT'
        if self.numerator == 8:
            self.name = 'WARNING'
        if self.numerator == 9:
            self.name = 'TITLE'
        if self.numerator == 10:
            self.name = 'IGRAPH'
        if self.numerator == 11:
            self.name = 'PAGETITLE'
        if self.numerator == 13:
            self.name = 'TREEMODEL'
        if self.numerator == 14:
            self.name = 'GENERIC'
        if self.numerator == 15:
            self.name = 'MODEL'
        if self.numerator == 16:
            self.name = 'GRAPHBOARD'
        if self.numerator == 17:
            self.name = 'IMAGE'
        if self.numerator == 18:
            self.name = 'LIGHTNOTE'
        if self.numerator == 19:
            self.name = 'LIGHTPIVOT'
        if self.numerator == 20:
            self.name = 'LIGHTWARNING'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.OutputItemType.UNKNOWN'
        if self.numerator == 1:
            return 'SpssClient.OutputItemType.CHART'
        if self.numerator == 2:
            return 'SpssClient.OutputItemType.HEAD'
        if self.numerator == 3:
            return 'SpssClient.OutputItemType.LOG'
        if self.numerator == 4:
            return 'SpssClient.OutputItemType.NOTE'
        if self.numerator == 5:
            return 'SpssClient.OutputItemType.PIVOT'
        if self.numerator == 6:
            return 'SpssClient.OutputItemType.ROOT'
        if self.numerator == 7:
            return 'SpssClient.OutputItemType.TEXT'
        if self.numerator == 8:
            return 'SpssClient.OutputItemType.WARNING'
        if self.numerator == 9:
            return 'SpssClient.OutputItemType.TITLE'
        if self.numerator == 10:
            return 'SpssClient.OutputItemType.IGRAPH'
        if self.numerator == 11:
            return 'SpssClient.OutputItemType.PAGETITLE'
        if self.numerator == 13:
            return 'SpssClient.OutputItemType.TREEMODEL'
        if self.numerator == 14:
            return 'SpssClient.OutputItemType.GENERIC'
        if self.numerator == 15:
            return 'SpssClient.OutputItemType.MODEL'
        if self.numerator == 16:
            return 'SpssClient.OutputItemType.GRAPHBOARD'
        if self.numerator == 17:
            return 'SpssClient.OutputItemType.IMAGE'
        if self.numerator == 18:
            return 'SpssClient.OutputItemType.LIGHTNOTE'
        if self.numerator == 19:
            return 'SpssClient.OutputItemType.LIGHTPIVOT'
        if self.numerator == 20:
            return 'SpssClient.OutputItemType.LIGHTWARNING'

OutputItemType.UNKNOWN = OutputItemType(0)
OutputItemType.CHART = OutputItemType(1)
OutputItemType.HEAD = OutputItemType(2)
OutputItemType.LOG = OutputItemType(3)
OutputItemType.NOTE = OutputItemType(4)
OutputItemType.PIVOT = OutputItemType(5)
OutputItemType.ROOT = OutputItemType(6)
OutputItemType.TEXT = OutputItemType(7)
OutputItemType.WARNING = OutputItemType(8)
OutputItemType.TITLE = OutputItemType(9)
OutputItemType.IGRAPH = OutputItemType(10)
OutputItemType.PAGETITLE = OutputItemType(11)
OutputItemType.TREEMODEL = OutputItemType(13)
OutputItemType.GENERIC = OutputItemType(14)
OutputItemType.MODEL = OutputItemType(15)
OutputItemType.GRAPHBOARD = OutputItemType(16)
OutputItemType.IMAGE = OutputItemType(17)
OutputItemType.LIGHTNOTE = OutputItemType(18)
OutputItemType.LIGHTPIVOT = OutputItemType(19)
OutputItemType.LIGHTWARNING = OutputItemType(20)

OutputItemType.values.update({0:OutputItemType.UNKNOWN})
OutputItemType.values.update({1:OutputItemType.CHART})
OutputItemType.values.update({2:OutputItemType.HEAD})
OutputItemType.values.update({3:OutputItemType.LOG})
OutputItemType.values.update({4:OutputItemType.NOTE})
OutputItemType.values.update({5:OutputItemType.PIVOT})
OutputItemType.values.update({6:OutputItemType.ROOT})
OutputItemType.values.update({7:OutputItemType.TEXT})
OutputItemType.values.update({8:OutputItemType.WARNING})
OutputItemType.values.update({9:OutputItemType.TITLE})
OutputItemType.values.update({10:OutputItemType.IGRAPH})
OutputItemType.values.update({11:OutputItemType.PAGETITLE})
OutputItemType.values.update({13:OutputItemType.TREEMODEL})
OutputItemType.values.update({14:OutputItemType.GENERIC})
OutputItemType.values.update({15:OutputItemType.MODEL})
OutputItemType.values.update({16:OutputItemType.GRAPHBOARD})
OutputItemType.values.update({17:OutputItemType.IMAGE})
OutputItemType.values.update({18:OutputItemType.LIGHTNOTE})
OutputItemType.values.update({19:OutputItemType.LIGHTPIVOT})
OutputItemType.values.update({20:OutputItemType.LIGHTWARNING})

class PreferenceOptions(object):
    values = {}
    VariableListDisplay = None
    VariableListSort = None
    MeasurementSystem = None
    Language = None
    AutoRaise = None
    OutputScroll = None
    OutputSound = None
    OutputSoundFile = None
    ScientificNotation = None
    LookFeel = None
    OpenSyntaxAtStartup = None
    OnlyOneDataset = None
    DigitGrouping = None
    OXMLVersion = None
    OutputAttributes = None
    TitleFont = None
    TitleFontSize = None
    TitleFontBold = None
    TitleFontItalic = None
    TitleFontUnderline = None
    TitleFontColor = None
    PageTitleFont = None
    PageTitleFontSize = None
    PageTitleFontBold = None
    PageTitleFontItalic = None
    PageTitleFontUnderline = None
    PageTitleFontColor = None
    TextOutputFont = None
    TextOutputFontSize = None
    TextOutputFontBold = None
    TextOutputFontItalic = None
    TextOutputFontUnderline = None
    TextOutputFontColor = None
    DisplayCommandsLog = None
    LogContents = None
    WarningsContents = None
    WarningsJustification = None
    NotesContents = None
    NotesJustification = None
    TitleContents = None
    TitleJustification = None
    PageTitleContents = None
    PageTitleJustification = None
    PivotTableContents = None
    PivotTableJustification = None
    ChartContents = None
    ChartJustification = None
    TextOutputContents = None
    TreeModelContents = None
    GenericJustification = None
    DisplayModelViewer = None
    Orientation = None
    BottomMargin = None
    LeftMargin = None
    RightMargin = None
    TopMargin = None
    TransformationMergeOptions = None
    RandomNumberGenerator = None
    DisplayFormatWidth = None
    DisplayFormatDecimal = None
    ReadingExternalData = None
    CenturyRangeValue = None
    CenturyRangeBeginYear = None
    RndTruncNumericValuesNumFuzzBits = None
    RecordSyntax = None
    RecordMode = None
    SessionJournalFile = None
    TempDir = None
    RecentFiles = None
    DataFiles = None
    OtherFiles = None
    SpecifiedAndLastFolder = None
    CustomOutputFormat = None
    AllValuesPrefix = None
    AllValuesSuffix = None
    NegativeValuesPrefix = None
    NegativeValuesSuffix = None
    DecimalSeparator = None
    OutlineVariables = None
    OutlineVariableValues = None
    PivotTableVariables = None
    PivotTableVariableValues = None
    OutputDisplay = None
    ChartTemplate = None
    ChartTemplateFile = None
    ChartAspectRatio = None
    ChartFont = None
    ChartFrameInner = None
    ChartFrameOuter = None
    GridLineScale = None
    GridLineCategory = None
    StyleCyclePref = None
    ColumnWidth = None
    EditingMode = None
    TableRender = None
    MIOutput = None
    MoreOptionKeys = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 101:
            self.name = 'VariableListDisplay'
        if self.numerator == 102:
            self.name = 'VariableListSort'
        if self.numerator == 103:
            self.name = 'MeasurementSystem'
        if self.numerator == 104:
            self.name = 'Language'
        if self.numerator == 105:
            self.name = 'AutoRaise'
        if self.numerator == 106:
            self.name = 'OutputScroll'
        if self.numerator == 107:
            self.name = 'OutputSound'
        if self.numerator == 108:
            self.name = 'OutputSoundFile'
        if self.numerator == 109:
            self.name = 'ScientificNotation'
        if self.numerator == 110:
            self.name = 'LookFeel'
        if self.numerator == 111:
            self.name = 'OpenSyntaxAtStartup'
        if self.numerator == 112:
            self.name = 'OnlyOneDataset'
        if self.numerator == 113:
            self.name = 'DigitGrouping'
        if self.numerator == 114:
            self.name = 'OXMLVersion'
        if self.numerator == 115:
            self.name = 'OutputAttributes'
        if self.numerator == 201:
            self.name = 'TitleFont'
        if self.numerator == 202:
            self.name = 'TitleFontSize'
        if self.numerator == 203:
            self.name = 'TitleFontBold'
        if self.numerator == 204:
            self.name = 'TitleFontItalic'
        if self.numerator == 205:
            self.name = 'TitleFontUnderline'
        if self.numerator == 206:
            self.name = 'TitleFontColor'
        if self.numerator == 207:
            self.name = 'PageTitleFont'
        if self.numerator == 208:
            self.name = 'PageTitleFontSize'
        if self.numerator == 209:
            self.name = 'PageTitleFontBold'
        if self.numerator == 210:
            self.name = 'PageTitleFontItalic'
        if self.numerator == 211:
            self.name = 'PageTitleFontUnderline'
        if self.numerator == 212:
            self.name = 'PageTitleFontColor'
        if self.numerator == 213:
            self.name = 'TextOutputFont'
        if self.numerator == 214:
            self.name = 'TextOutputFontSize'
        if self.numerator == 215:
            self.name = 'TextOutputFontBold'
        if self.numerator == 216:
            self.name = 'TextOutputFontItalic'
        if self.numerator == 217:
            self.name = 'TextOutputFontUnderline'
        if self.numerator == 218:
            self.name = 'TextOutputFontColor'
        if self.numerator == 219:
            self.name = 'DisplayCommandsLog'
        if self.numerator == 220:
            self.name = 'LogContents'
        if self.numerator == 221:
            self.name = 'WarningsContents'
        if self.numerator == 222:
            self.name = 'WarningsJustification'
        if self.numerator == 223:
            self.name = 'NotesContents'
        if self.numerator == 224:
            self.name = 'NotesJustification'
        if self.numerator == 225:
            self.name = 'TitleContents'
        if self.numerator == 226:
            self.name = 'TitleJustification'
        if self.numerator == 227:
            self.name = 'PageTitleContents'
        if self.numerator == 228:
            self.name = 'PageTitleJustification'
        if self.numerator == 229:
            self.name = 'PivotTableContents'
        if self.numerator == 230:
            self.name = 'PivotTableJustification'
        if self.numerator == 231:
            self.name = 'ChartContents'
        if self.numerator == 232:
            self.name = 'ChartJustification'
        if self.numerator == 233:
            self.name = 'TextOutputContents'
        if self.numerator == 234:
            self.name = 'TreeModelContents'
        if self.numerator == 235:
            self.name = 'GenericJustification'
        if self.numerator == 236:
            self.name = 'DisplayModelViewer'
        if self.numerator == 237:
            self.name = 'Orientation'
        if self.numerator == 238:
            self.name = 'BottomMargin'
        if self.numerator == 239:
            self.name = 'LeftMargin'
        if self.numerator == 240:
            self.name = 'RightMargin'
        if self.numerator == 241:
            self.name = 'TopMargin'
        if self.numerator == 301:
            self.name = 'TransformationMergeOptions'
        if self.numerator == 302:
            self.name = 'RandomNumberGenerator'
        if self.numerator == 303:
            self.name = 'DisplayFormatWidth'
        if self.numerator == 304:
            self.name = 'DisplayFormatDecimal'
        if self.numerator == 305:
            self.name = 'ReadingExternalData'
        if self.numerator == 306:
            self.name = 'CenturyRangeValue'
        if self.numerator == 307:
            self.name = 'CenturyRangeBeginYear'
        if self.numerator == 308:
            self.name = 'RndTruncNumericValuesNumFuzzBits'
        if self.numerator == 801:
            self.name = 'RecordSyntax'
        if self.numerator == 802:
            self.name = 'RecordMode'
        if self.numerator == 803:
            self.name = 'SessionJournalFile'
        if self.numerator == 804:
            self.name = 'TempDir'
        if self.numerator == 805:
            self.name = 'RecentFiles'
        if self.numerator == 806:
            self.name = 'DataFiles'
        if self.numerator == 807:
            self.name = 'OtherFiles'
        if self.numerator == 808:
            self.name = 'SpecifiedAndLastFolder'
        if self.numerator == 401:
            self.name = 'CustomOutputFormat'
        if self.numerator == 402:
            self.name = 'AllValuesPrefix'
        if self.numerator == 403:
            self.name = 'AllValuesSuffix'
        if self.numerator == 404:
            self.name = 'NegativeValuesPrefix'
        if self.numerator == 405:
            self.name = 'NegativeValuesSuffix'
        if self.numerator == 406:
            self.name = 'DecimalSeparator'
        if self.numerator == 501:
            self.name = 'OutlineVariables'
        if self.numerator == 502:
            self.name = 'OutlineVariableValues'
        if self.numerator == 503:
            self.name = 'PivotTableVariables'
        if self.numerator == 504:
            self.name = 'PivotTableVariableValues'
        if self.numerator == 505:
            self.name = 'OutputDisplay'
        if self.numerator == 601:
            self.name = 'ChartTemplate'
        if self.numerator == 602:
            self.name = 'ChartTemplateFile'
        if self.numerator == 603:
            self.name = 'ChartAspectRatio'
        if self.numerator == 604:
            self.name = 'ChartFont'
        if self.numerator == 605:
            self.name = 'ChartFrameInner'
        if self.numerator == 606:
            self.name = 'ChartFrameOuter'
        if self.numerator == 607:
            self.name = 'GridLineScale'
        if self.numerator == 608:
            self.name = 'GridLineCategory'
        if self.numerator == 609:
            self.name = 'StyleCyclePref'
        if self.numerator == 701:
            self.name = 'ColumnWidth'
        if self.numerator == 702:
            self.name = 'EditingMode'
        if self.numerator == 703:
            self.name = 'TableRender'
        if self.numerator == 901:
            self.name = 'MIOutput'
        if self.numerator == 1000:
            self.name = 'MoreOptionKeys'
        

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 101:
            return 'SpssClient.PreferenceOptions.VariableListDisplay'
        if self.numerator == 102:
            return 'SpssClient.PreferenceOptions.VariableListSort'
        if self.numerator == 103:
            return 'SpssClient.PreferenceOptions.MeasurementSystem'
        if self.numerator == 104:
            return 'SpssClient.PreferenceOptions.Language'
        if self.numerator == 105:
            return 'SpssClient.PreferenceOptions.AutoRaise'
        if self.numerator == 106:
            return 'SpssClient.PreferenceOptions.OutputScroll'
        if self.numerator == 107:
            return 'SpssClient.PreferenceOptions.OutputSound'
        if self.numerator == 108:
            return 'SpssClient.PreferenceOptions.OutputSoundFile'
        if self.numerator == 109:
            return 'SpssClient.PreferenceOptions.ScientificNotation'
        if self.numerator == 110:
            return 'SpssClient.PreferenceOptions.LookFeel'
        if self.numerator == 111:
            return 'SpssClient.PreferenceOptions.OpenSyntaxAtStartup'
        if self.numerator == 112:
            return 'SpssClient.PreferenceOptions.OnlyOneDataset'
        if self.numerator == 113:
            return 'SpssClient.PreferenceOptions.DigitGrouping'
        if self.numerator == 114:
            return 'SpssClient.PreferenceOptions.OXMLVersion'
        if self.numerator == 115:
            return 'SpssClient.PreferenceOptions.OutputAttributes'
        if self.numerator == 201:
            return 'SpssClient.PreferenceOptions.TitleFont'
        if self.numerator == 202:
            return 'SpssClient.PreferenceOptions.TitleFontSize'
        if self.numerator == 203:
            return 'SpssClient.PreferenceOptions.TitleFontBold'
        if self.numerator == 204:
            return 'SpssClient.PreferenceOptions.TitleFontItalic'
        if self.numerator == 205:
            return 'SpssClient.PreferenceOptions.TitleFontUnderline'
        if self.numerator == 206:
            return 'SpssClient.PreferenceOptions.TitleFontColor'
        if self.numerator == 207:
            return 'SpssClient.PreferenceOptions.PageTitleFont'
        if self.numerator == 208:
            return 'SpssClient.PreferenceOptions.PageTitleFontSize'
        if self.numerator == 209:
            return 'SpssClient.PreferenceOptions.PageTitleFontBold'
        if self.numerator == 210:
            return 'SpssClient.PreferenceOptions.PageTitleFontItalic'
        if self.numerator == 211:
            return 'SpssClient.PreferenceOptions.PageTitleFontUnderline'
        if self.numerator == 212:
            return 'SpssClient.PreferenceOptions.PageTitleFontColor'
        if self.numerator == 213:
            return 'SpssClient.PreferenceOptions.TextOutputFont'
        if self.numerator == 214:
            return 'SpssClient.PreferenceOptions.TextOutputFontSize'
        if self.numerator == 215:
            return 'SpssClient.PreferenceOptions.TextOutputFontBold'
        if self.numerator == 216:
            return 'SpssClient.PreferenceOptions.TextOutputFontItalic'
        if self.numerator == 217:
            return 'SpssClient.PreferenceOptions.TextOutputFontUnderline'
        if self.numerator == 218:
            return 'SpssClient.PreferenceOptions.TextOutputFontColor'
        if self.numerator == 219:
            return 'SpssClient.PreferenceOptions.DisplayCommandsLog'
        if self.numerator == 220:
            return 'SpssClient.PreferenceOptions.LogContents'
        if self.numerator == 221:
            return 'SpssClient.PreferenceOptions.WarningsContents'
        if self.numerator == 222:
            return 'SpssClient.PreferenceOptions.WarningsJustification'
        if self.numerator == 223:
            return 'SpssClient.PreferenceOptions.NotesContents'
        if self.numerator == 224:
            return 'SpssClient.PreferenceOptions.NotesJustification'
        if self.numerator == 225:
            return 'SpssClient.PreferenceOptions.TitleContents'
        if self.numerator == 226:
            return 'SpssClient.PreferenceOptions.TitleJustification'
        if self.numerator == 227:
            return 'SpssClient.PreferenceOptions.PageTitleContents'
        if self.numerator == 228:
            return 'SpssClient.PreferenceOptions.PageTitleJustification'
        if self.numerator == 229:
            return 'SpssClient.PreferenceOptions.PivotTableContents'
        if self.numerator == 230:
            return 'SpssClient.PreferenceOptions.PivotTableJustification'
        if self.numerator == 231:
            return 'SpssClient.PreferenceOptions.ChartContents'
        if self.numerator == 232:
            return 'SpssClient.PreferenceOptions.ChartJustification'
        if self.numerator == 233:
            return 'SpssClient.PreferenceOptions.TextOutputContents'
        if self.numerator == 234:
            return 'SpssClient.PreferenceOptions.TreeModelContents'
        if self.numerator == 235:
            return 'SpssClient.PreferenceOptions.GenericJustification'
        if self.numerator == 236:
            return 'SpssClient.PreferenceOptions.DisplayModelViewer'
        if self.numerator == 237:
            return 'SpssClient.PreferenceOptions.Orientation'
        if self.numerator == 238:
            return 'SpssClient.PreferenceOptions.BottomMargin'
        if self.numerator == 239:
            return 'SpssClient.PreferenceOptions.LeftMargin'
        if self.numerator == 240:
            return 'SpssClient.PreferenceOptions.RightMargin'
        if self.numerator == 241:
            return 'SpssClient.PreferenceOptions.TopMargin'
        if self.numerator == 301:
            return 'SpssClient.PreferenceOptions.TransformationMergeOptions'
        if self.numerator == 302:
            return 'SpssClient.PreferenceOptions.RandomNumberGenerator'
        if self.numerator == 303:
            return 'SpssClient.PreferenceOptions.DisplayFormatWidth'
        if self.numerator == 304:
            return 'SpssClient.PreferenceOptions.DisplayFormatDecimal'
        if self.numerator == 305:
            return 'SpssClient.PreferenceOptions.ReadingExternalData'
        if self.numerator == 306:
            return 'SpssClient.PreferenceOptions.CenturyRangeValue'
        if self.numerator == 307:
            return 'SpssClient.PreferenceOptions.CenturyRangeBeginYear'
        if self.numerator == 308:
            return 'SpssClient.PreferenceOptions.RndTruncNumericValuesNumFuzzBits'
        if self.numerator == 801:
            return 'SpssClient.PreferenceOptions.RecordSyntax'
        if self.numerator == 802:
            return 'SpssClient.PreferenceOptions.RecordMode'
        if self.numerator == 803:
            return 'SpssClient.PreferenceOptions.SessionJournalFile'
        if self.numerator == 804:
            return 'SpssClient.PreferenceOptions.TempDir'
        if self.numerator == 805:
            return 'SpssClient.PreferenceOptions.RecentFiles'
        if self.numerator == 806:
            return 'SpssClient.PreferenceOptions.DataFiles'
        if self.numerator == 807:
            return 'SpssClient.PreferenceOptions.OtherFiles'
        if self.numerator == 808:
            return 'SpssClient.PreferenceOptions.SpecifiedAndLastFolder'
        if self.numerator == 401:
            return 'SpssClient.PreferenceOptions.CustomOutputFormat'
        if self.numerator == 402:
            return 'SpssClient.PreferenceOptions.AllValuesPrefix'
        if self.numerator == 403:
            return 'SpssClient.PreferenceOptions.AllValuesSuffix'
        if self.numerator == 404:
            return 'SpssClient.PreferenceOptions.NegativeValuesPrefix'
        if self.numerator == 405:
            return 'SpssClient.PreferenceOptions.NegativeValuesSuffix'
        if self.numerator == 406:
            return 'SpssClient.PreferenceOptions.DecimalSeparator'
        if self.numerator == 501:
            return 'SpssClient.PreferenceOptions.OutlineVariables'
        if self.numerator == 502:
            return 'SpssClient.PreferenceOptions.OutlineVariableValues'
        if self.numerator == 503:
            return 'SpssClient.PreferenceOptions.PivotTableVariables'
        if self.numerator == 504:
            return 'SpssClient.PreferenceOptions.PivotTableVariableValues'
        if self.numerator == 505:
            return 'SpssClient.PreferenceOptions.OutputDisplay'
        if self.numerator == 601:
            return 'SpssClient.PreferenceOptions.ChartTemplate'
        if self.numerator == 602:
            return 'SpssClient.PreferenceOptions.ChartTemplateFile'
        if self.numerator == 603:
            return 'SpssClient.PreferenceOptions.ChartAspectRatio'
        if self.numerator == 604:
            return 'SpssClient.PreferenceOptions.ChartFont'
        if self.numerator == 605:
            return 'SpssClient.PreferenceOptions.ChartFrameInner'
        if self.numerator == 606:
            return 'SpssClient.PreferenceOptions.ChartFrameOuter'
        if self.numerator == 607:
            return 'SpssClient.PreferenceOptions.GridLineScale'
        if self.numerator == 608:
            return 'SpssClient.PreferenceOptions.GridLineCategory'
        if self.numerator == 609:
            return 'SpssClient.PreferenceOptions.StyleCyclePref'
        if self.numerator == 701:
            return 'SpssClient.PreferenceOptions.ColumnWidth'
        if self.numerator == 702:
            return 'SpssClient.PreferenceOptions.EditingMode'
        if self.numerator == 703:
            return 'SpssClient.PreferenceOptions.TableRender'
        if self.numerator == 901:
            return 'SpssClient.PreferenceOptions.MIOutput'
        if self.numerator == 1000:
            return 'SpssClient.PreferenceOptions.MoreOptionKeys'

PreferenceOptions.VariableListDisplay = PreferenceOptions(101)
PreferenceOptions.VariableListSort = PreferenceOptions(102)
PreferenceOptions.MeasurementSystem = PreferenceOptions(103)
PreferenceOptions.Language = PreferenceOptions(104)
PreferenceOptions.AutoRaise = PreferenceOptions(105)
PreferenceOptions.OutputScroll = PreferenceOptions(106)
PreferenceOptions.OutputSound = PreferenceOptions(107)
PreferenceOptions.OutputSoundFile = PreferenceOptions(108)
PreferenceOptions.ScientificNotation = PreferenceOptions(109)
PreferenceOptions.LookFeel = PreferenceOptions(110)
PreferenceOptions.OpenSyntaxAtStartup = PreferenceOptions(111)
PreferenceOptions.OnlyOneDataset = PreferenceOptions(112)
PreferenceOptions.DigitGrouping = PreferenceOptions(113)
PreferenceOptions.OXMLVersion = PreferenceOptions(114)
PreferenceOptions.OutputAttributes = PreferenceOptions(115)
PreferenceOptions.TitleFont = PreferenceOptions(201)
PreferenceOptions.TitleFontSize = PreferenceOptions(202)
PreferenceOptions.TitleFontBold = PreferenceOptions(203)
PreferenceOptions.TitleFontItalic = PreferenceOptions(204)
PreferenceOptions.TitleFontUnderline = PreferenceOptions(205)
PreferenceOptions.TitleFontColor = PreferenceOptions(206)
PreferenceOptions.PageTitleFont = PreferenceOptions(207)
PreferenceOptions.PageTitleFontSize = PreferenceOptions(208)
PreferenceOptions.PageTitleFontBold = PreferenceOptions(209)
PreferenceOptions.PageTitleFontItalic = PreferenceOptions(210)
PreferenceOptions.PageTitleFontUnderline = PreferenceOptions(211)
PreferenceOptions.PageTitleFontColor = PreferenceOptions(212)
PreferenceOptions.TextOutputFont = PreferenceOptions(213)
PreferenceOptions.TextOutputFontSize = PreferenceOptions(214)
PreferenceOptions.TextOutputFontBold = PreferenceOptions(215)
PreferenceOptions.TextOutputFontItalic = PreferenceOptions(216)
PreferenceOptions.TextOutputFontUnderline = PreferenceOptions(217)
PreferenceOptions.TextOutputFontColor = PreferenceOptions(218)
PreferenceOptions.DisplayCommandsLog = PreferenceOptions(219)
PreferenceOptions.LogContents = PreferenceOptions(220)
PreferenceOptions.WarningsContents = PreferenceOptions(221)
PreferenceOptions.WarningsJustification = PreferenceOptions(222)
PreferenceOptions.NotesContents = PreferenceOptions(223)
PreferenceOptions.NotesJustification = PreferenceOptions(224)
PreferenceOptions.TitleContents = PreferenceOptions(225)
PreferenceOptions.TitleJustification = PreferenceOptions(226)
PreferenceOptions.PageTitleContents = PreferenceOptions(227)
PreferenceOptions.PageTitleJustification = PreferenceOptions(228)
PreferenceOptions.PivotTableContents = PreferenceOptions(229)
PreferenceOptions.PivotTableJustification = PreferenceOptions(230)
PreferenceOptions.ChartContents = PreferenceOptions(231)
PreferenceOptions.ChartJustification = PreferenceOptions(232)
PreferenceOptions.TextOutputContents = PreferenceOptions(233)
PreferenceOptions.TreeModelContents = PreferenceOptions(234)
PreferenceOptions.GenericJustification = PreferenceOptions(235)
PreferenceOptions.DisplayModelViewer = PreferenceOptions(236)
PreferenceOptions.Orientation = PreferenceOptions(237)
PreferenceOptions.BottomMargin = PreferenceOptions(238)
PreferenceOptions.LeftMargin = PreferenceOptions(239)
PreferenceOptions.RightMargin = PreferenceOptions(240)
PreferenceOptions.TopMargin = PreferenceOptions(241)
PreferenceOptions.TransformationMergeOptions = PreferenceOptions(301)
PreferenceOptions.RandomNumberGenerator = PreferenceOptions(302)
PreferenceOptions.DisplayFormatWidth = PreferenceOptions(303)
PreferenceOptions.DisplayFormatDecimal = PreferenceOptions(304)
PreferenceOptions.ReadingExternalData = PreferenceOptions(305)
PreferenceOptions.CenturyRangeValue = PreferenceOptions(306)
PreferenceOptions.CenturyRangeBeginYear = PreferenceOptions(307)
PreferenceOptions.RndTruncNumericValuesNumFuzzBits = PreferenceOptions(308)
PreferenceOptions.RecordSyntax = PreferenceOptions(801)
PreferenceOptions.RecordMode = PreferenceOptions(802)
PreferenceOptions.SessionJournalFile = PreferenceOptions(803)
PreferenceOptions.TempDir = PreferenceOptions(804)
PreferenceOptions.RecentFiles = PreferenceOptions(805)
PreferenceOptions.DataFiles = PreferenceOptions(806)
PreferenceOptions.OtherFiles = PreferenceOptions(807)
PreferenceOptions.SpecifiedAndLastFolder = PreferenceOptions(808)
PreferenceOptions.CustomOutputFormat = PreferenceOptions(401)
PreferenceOptions.AllValuesPrefix = PreferenceOptions(402)
PreferenceOptions.AllValuesSuffix = PreferenceOptions(403)
PreferenceOptions.NegativeValuesPrefix = PreferenceOptions(404)
PreferenceOptions.NegativeValuesSuffix = PreferenceOptions(405)
PreferenceOptions.DecimalSeparator = PreferenceOptions(406)
PreferenceOptions.OutlineVariables = PreferenceOptions(501)
PreferenceOptions.OutlineVariableValues = PreferenceOptions(502)
PreferenceOptions.PivotTableVariables = PreferenceOptions(503)
PreferenceOptions.PivotTableVariableValues = PreferenceOptions(504)
PreferenceOptions.OutputDisplay = PreferenceOptions(505)
PreferenceOptions.ChartTemplate = PreferenceOptions(601)
PreferenceOptions.ChartTemplateFile = PreferenceOptions(602)
PreferenceOptions.ChartAspectRatio = PreferenceOptions(603)
PreferenceOptions.ChartFont = PreferenceOptions(604)
PreferenceOptions.ChartFrameInner = PreferenceOptions(605)
PreferenceOptions.ChartFrameOuter = PreferenceOptions(606)
PreferenceOptions.GridLineScale = PreferenceOptions(607)
PreferenceOptions.GridLineCategory = PreferenceOptions(608)
PreferenceOptions.StyleCyclePref = PreferenceOptions(609)
PreferenceOptions.ColumnWidth = PreferenceOptions(701)
PreferenceOptions.EditingMode = PreferenceOptions(702)
PreferenceOptions.TableRender = PreferenceOptions(703)
PreferenceOptions.MIOutput = PreferenceOptions(901)
PreferenceOptions.MoreOptionKeys = PreferenceOptions(1000)

PreferenceOptions.values.update({101:PreferenceOptions.VariableListDisplay})
PreferenceOptions.values.update({102:PreferenceOptions.VariableListSort})
PreferenceOptions.values.update({103:PreferenceOptions.MeasurementSystem})
PreferenceOptions.values.update({104:PreferenceOptions.Language})
PreferenceOptions.values.update({105:PreferenceOptions.AutoRaise})
PreferenceOptions.values.update({106:PreferenceOptions.OutputScroll})
PreferenceOptions.values.update({107:PreferenceOptions.OutputSound})
PreferenceOptions.values.update({108:PreferenceOptions.OutputSoundFile})
PreferenceOptions.values.update({109:PreferenceOptions.ScientificNotation})
PreferenceOptions.values.update({110:PreferenceOptions.LookFeel})
PreferenceOptions.values.update({111:PreferenceOptions.OpenSyntaxAtStartup})
PreferenceOptions.values.update({112:PreferenceOptions.OnlyOneDataset})
PreferenceOptions.values.update({113:PreferenceOptions.DigitGrouping})
PreferenceOptions.values.update({114:PreferenceOptions.OXMLVersion})
PreferenceOptions.values.update({115:PreferenceOptions.OutputAttributes})
PreferenceOptions.values.update({201:PreferenceOptions.TitleFont})
PreferenceOptions.values.update({202:PreferenceOptions.TitleFontSize})
PreferenceOptions.values.update({203:PreferenceOptions.TitleFontBold})
PreferenceOptions.values.update({204:PreferenceOptions.TitleFontItalic})
PreferenceOptions.values.update({205:PreferenceOptions.TitleFontUnderline})
PreferenceOptions.values.update({206:PreferenceOptions.TitleFontColor})
PreferenceOptions.values.update({207:PreferenceOptions.PageTitleFont})
PreferenceOptions.values.update({208:PreferenceOptions.PageTitleFontSize})
PreferenceOptions.values.update({209:PreferenceOptions.PageTitleFontBold})
PreferenceOptions.values.update({210:PreferenceOptions.PageTitleFontItalic})
PreferenceOptions.values.update({211:PreferenceOptions.PageTitleFontUnderline})
PreferenceOptions.values.update({212:PreferenceOptions.PageTitleFontColor})
PreferenceOptions.values.update({213:PreferenceOptions.TextOutputFont})
PreferenceOptions.values.update({214:PreferenceOptions.TextOutputFontSize})
PreferenceOptions.values.update({215:PreferenceOptions.TextOutputFontBold})
PreferenceOptions.values.update({216:PreferenceOptions.TextOutputFontItalic})
PreferenceOptions.values.update({217:PreferenceOptions.TextOutputFontUnderline})
PreferenceOptions.values.update({218:PreferenceOptions.TextOutputFontColor})
PreferenceOptions.values.update({219:PreferenceOptions.DisplayCommandsLog})
PreferenceOptions.values.update({220:PreferenceOptions.LogContents})
PreferenceOptions.values.update({221:PreferenceOptions.WarningsContents})
PreferenceOptions.values.update({222:PreferenceOptions.WarningsJustification})
PreferenceOptions.values.update({223:PreferenceOptions.NotesContents})
PreferenceOptions.values.update({224:PreferenceOptions.NotesJustification})
PreferenceOptions.values.update({225:PreferenceOptions.TitleContents})
PreferenceOptions.values.update({226:PreferenceOptions.TitleJustification})
PreferenceOptions.values.update({227:PreferenceOptions.PageTitleContents})
PreferenceOptions.values.update({228:PreferenceOptions.PageTitleJustification})
PreferenceOptions.values.update({229:PreferenceOptions.PivotTableContents})
PreferenceOptions.values.update({230:PreferenceOptions.PivotTableJustification})
PreferenceOptions.values.update({231:PreferenceOptions.ChartContents})
PreferenceOptions.values.update({232:PreferenceOptions.ChartJustification})
PreferenceOptions.values.update({233:PreferenceOptions.TextOutputContents})
PreferenceOptions.values.update({234:PreferenceOptions.TreeModelContents})
PreferenceOptions.values.update({235:PreferenceOptions.GenericJustification})
PreferenceOptions.values.update({236:PreferenceOptions.DisplayModelViewer})
PreferenceOptions.values.update({237:PreferenceOptions.Orientation})
PreferenceOptions.values.update({238:PreferenceOptions.BottomMargin})
PreferenceOptions.values.update({239:PreferenceOptions.LeftMargin})
PreferenceOptions.values.update({240:PreferenceOptions.RightMargin})
PreferenceOptions.values.update({241:PreferenceOptions.TopMargin})
PreferenceOptions.values.update({301:PreferenceOptions.TransformationMergeOptions})
PreferenceOptions.values.update({302:PreferenceOptions.RandomNumberGenerator})
PreferenceOptions.values.update({303:PreferenceOptions.DisplayFormatWidth})
PreferenceOptions.values.update({304:PreferenceOptions.DisplayFormatDecimal})
PreferenceOptions.values.update({305:PreferenceOptions.ReadingExternalData})
PreferenceOptions.values.update({306:PreferenceOptions.CenturyRangeValue})
PreferenceOptions.values.update({307:PreferenceOptions.CenturyRangeBeginYear})
PreferenceOptions.values.update({308:PreferenceOptions.RndTruncNumericValuesNumFuzzBits})
PreferenceOptions.values.update({801:PreferenceOptions.RecordSyntax})
PreferenceOptions.values.update({802:PreferenceOptions.RecordMode})
PreferenceOptions.values.update({803:PreferenceOptions.SessionJournalFile})
PreferenceOptions.values.update({804:PreferenceOptions.TempDir})
PreferenceOptions.values.update({805:PreferenceOptions.RecentFiles})
PreferenceOptions.values.update({806:PreferenceOptions.DataFiles})
PreferenceOptions.values.update({807:PreferenceOptions.OtherFiles})
PreferenceOptions.values.update({808:PreferenceOptions.SpecifiedAndLastFolder})
PreferenceOptions.values.update({401:PreferenceOptions.CustomOutputFormat})
PreferenceOptions.values.update({402:PreferenceOptions.AllValuesPrefix})
PreferenceOptions.values.update({403:PreferenceOptions.AllValuesSuffix})
PreferenceOptions.values.update({404:PreferenceOptions.NegativeValuesPrefix})
PreferenceOptions.values.update({405:PreferenceOptions.NegativeValuesSuffix})
PreferenceOptions.values.update({406:PreferenceOptions.DecimalSeparator})
PreferenceOptions.values.update({501:PreferenceOptions.OutlineVariables})
PreferenceOptions.values.update({502:PreferenceOptions.OutlineVariableValues})
PreferenceOptions.values.update({503:PreferenceOptions.PivotTableVariables})
PreferenceOptions.values.update({504:PreferenceOptions.PivotTableVariableValues})
PreferenceOptions.values.update({505:PreferenceOptions.OutputDisplay})
PreferenceOptions.values.update({601:PreferenceOptions.ChartTemplate})
PreferenceOptions.values.update({602:PreferenceOptions.ChartTemplateFile})
PreferenceOptions.values.update({603:PreferenceOptions.ChartAspectRatio})
PreferenceOptions.values.update({604:PreferenceOptions.ChartFont})
PreferenceOptions.values.update({605:PreferenceOptions.ChartFrameInner})
PreferenceOptions.values.update({606:PreferenceOptions.ChartFrameOuter})
PreferenceOptions.values.update({607:PreferenceOptions.GridLineScale})
PreferenceOptions.values.update({608:PreferenceOptions.GridLineCategory})
PreferenceOptions.values.update({609:PreferenceOptions.StyleCyclePref})
PreferenceOptions.values.update({701:PreferenceOptions.ColumnWidth})
PreferenceOptions.values.update({702:PreferenceOptions.EditingMode})
PreferenceOptions.values.update({703:PreferenceOptions.TableRender})
PreferenceOptions.values.update({901:PreferenceOptions.MIOutput})
PreferenceOptions.values.update({1000:PreferenceOptions.MoreOptionKeys})

class PrintOptions(object):
    values = {}
    LeftMargin = None
    TopMargin = None
    RightMargin = None
    BottomMargin = None
    Orientation = None
    StartingPageNumber = None
    SpaceBetweenItems = None
    PrintedChartSize = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 1:
            self.name = 'LeftMargin'
        if self.numerator == 2:
            self.name = 'TopMargin'
        if self.numerator == 3:
            self.name = 'RightMargin'
        if self.numerator == 4:
            self.name = 'BottomMargin'
        if self.numerator == 5:
            self.name = 'Orientation'
        if self.numerator == 6:
            self.name = 'StartingPageNumber'
        if self.numerator == 7:
            self.name = 'SpaceBetweenItems'
        if self.numerator == 8:
            self.name = 'PrintedChartSize'
            
    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 1:
            return 'SpssClient.PrintOptions.LeftMargin'
        if self.numerator == 2:
            return 'SpssClient.PrintOptions.TopMargin'
        if self.numerator == 3:
            return 'SpssClient.PrintOptions.RightMargin'
        if self.numerator == 4:
            return 'SpssClient.PrintOptions.BottomMargin'
        if self.numerator == 5:
            return 'SpssClient.PrintOptions.Orientation'
        if self.numerator == 6:
            return 'SpssClient.PrintOptions.StartingPageNumber'
        if self.numerator == 7:
            return 'SpssClient.PrintOptions.SpaceBetweenItems'
        if self.numerator == 8:
            return 'SpssClient.PrintOptions.PrintedChartSize'

PrintOptions.LeftMargin = PrintOptions(1)
PrintOptions.TopMargin = PrintOptions(2)
PrintOptions.RightMargin = PrintOptions(3)
PrintOptions.BottomMargin = PrintOptions(4)
PrintOptions.Orientation = PrintOptions(5)
PrintOptions.StartingPageNumber = PrintOptions(6)
PrintOptions.SpaceBetweenItems = PrintOptions(7)
PrintOptions.PrintedChartSize = PrintOptions(8)

PrintOptions.values.update({1:PrintOptions.LeftMargin})
PrintOptions.values.update({2:PrintOptions.TopMargin})
PrintOptions.values.update({3:PrintOptions.RightMargin})
PrintOptions.values.update({4:PrintOptions.BottomMargin})
PrintOptions.values.update({5:PrintOptions.Orientation})
PrintOptions.values.update({6:PrintOptions.StartingPageNumber})
PrintOptions.values.update({7:PrintOptions.SpaceBetweenItems})
PrintOptions.values.update({8:PrintOptions.PrintedChartSize})

class SpssExportSubset(object):
    values = {}
    SpssAll = None
    SpssVisible = None
    SpssSelected = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssAll'
        if self.numerator == 1:
            self.name = 'SpssVisible'
        if self.numerator == 2:
            self.name = 'SpssSelected'
    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssExportSubset.SpssAll'
        if self.numerator == 1:
            return 'SpssClient.SpssExportSubset.SpssVisible'
        if self.numerator == 2:
            return 'SpssClient.SpssExportSubset.SpssSelected'

SpssExportSubset.SpssAll = SpssExportSubset(0)
SpssExportSubset.SpssVisible = SpssExportSubset(1)
SpssExportSubset.SpssSelected = SpssExportSubset(2)

SpssExportSubset.values.update({0:SpssExportSubset.SpssAll})
SpssExportSubset.values.update({1:SpssExportSubset.SpssVisible})
SpssExportSubset.values.update({2:SpssExportSubset.SpssSelected})

class SpssFootnoteMarkerTypes(object):
    values = {}
    SpssFtSuperscript = None
    SpssFtSubscript = None
    SpssFtAlphabetic = None
    SpssFtNumeric = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssFtSuperscript'
        if self.numerator == 1:
            self.name = 'SpssFtSubscript'
        if self.numerator == 2:
            self.name = 'SpssFtAlphabetic'
        if self.numerator == 3:
            self.name = 'SpssFtNumeric'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssFootnoteMarkerTypes.SpssFtSuperscript'
        if self.numerator == 1:
            return 'SpssClient.SpssFootnoteMarkerTypes.SpssFtSubscript'
        if self.numerator == 2:
            return 'SpssClient.SpssFootnoteMarkerTypes.SpssFtAlphabetic'
        if self.numerator == 3:
            return 'SpssClient.SpssFootnoteMarkerTypes.SpssFtNumeric'

SpssFootnoteMarkerTypes.SpssFtSuperscript = SpssFootnoteMarkerTypes(0)
SpssFootnoteMarkerTypes.SpssFtSubscript = SpssFootnoteMarkerTypes(1)
SpssFootnoteMarkerTypes.SpssFtAlphabetic = SpssFootnoteMarkerTypes(2)
SpssFootnoteMarkerTypes.SpssFtNumeric = SpssFootnoteMarkerTypes(3)

SpssFootnoteMarkerTypes.values.update({0:SpssFootnoteMarkerTypes.SpssFtSuperscript})
SpssFootnoteMarkerTypes.values.update({1:SpssFootnoteMarkerTypes.SpssFtSubscript})
SpssFootnoteMarkerTypes.values.update({2:SpssFootnoteMarkerTypes.SpssFtAlphabetic})                                       
SpssFootnoteMarkerTypes.values.update({3:SpssFootnoteMarkerTypes.SpssFtNumeric})        

class SpssGraphTypeInfo(object):
    values = {}
    spgrDot = None
    spgrRibbon = None
    spgrDropLine = None
    spgrSimple = None
    spgrStacked = None
    spgrPlotted = None
    spgrNone = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'spgrDot'
        if self.numerator == 1:
            self.name = 'spgrRibbon'
        if self.numerator == 2:
            self.name = 'spgrDropLine'
        if self.numerator == 3:
            self.name = 'spgrSimple'
        if self.numerator == 4:
            self.name = 'spgrStacked'
        if self.numerator == 5:
            self.name = 'spgrPlotted'
        if self.numerator == 6:
            self.name = 'spgrNone'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssGraphTypeInfo.spgrDot'
        if self.numerator == 1:
            return 'SpssClient.SpssGraphTypeInfo.spgrRibbon'
        if self.numerator == 2:
            return 'SpssClient.SpssGraphTypeInfo.spgrDropLine'
        if self.numerator == 3:
            return 'SpssClient.SpssGraphTypeInfo.spgrSimple'
        if self.numerator == 4:
            return 'SpssClient.SpssGraphTypeInfo.spgrStacked'
        if self.numerator == 5:
            return 'SpssClient.SpssGraphTypeInfo.spgrPlotted'
        if self.numerator == 6:
            return 'SpssClient.SpssGraphTypeInfo.spgrNone'

SpssGraphTypeInfo.spgrDot = SpssGraphTypeInfo(0)
SpssGraphTypeInfo.spgrRibbon = SpssGraphTypeInfo(1)
SpssGraphTypeInfo.spgrDropLine = SpssGraphTypeInfo(2)
SpssGraphTypeInfo.spgrSimple = SpssGraphTypeInfo(3)
SpssGraphTypeInfo.spgrStacked = SpssGraphTypeInfo(4)
SpssGraphTypeInfo.spgrPlotted = SpssGraphTypeInfo(5)
SpssGraphTypeInfo.spgrNone = SpssGraphTypeInfo(6)

SpssGraphTypeInfo.values.update({0:SpssGraphTypeInfo.spgrDot})
SpssGraphTypeInfo.values.update({1:SpssGraphTypeInfo.spgrRibbon})
SpssGraphTypeInfo.values.update({2:SpssGraphTypeInfo.spgrDropLine})
SpssGraphTypeInfo.values.update({3:SpssGraphTypeInfo.spgrSimple})
SpssGraphTypeInfo.values.update({4:SpssGraphTypeInfo.spgrStacked})
SpssGraphTypeInfo.values.update({5:SpssGraphTypeInfo.spgrPlotted})
SpssGraphTypeInfo.values.update({6:SpssGraphTypeInfo.spgrNone})

class SpssHAlignTypes(object):
    values = {}
    SpssHAlLeft = None
    SpssHAlRight = None
    SpssHAlCenter = None
    SpssHAlMixed = None
    SpssHAlDecimal = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssHAlLeft'
        if self.numerator == 1:
            self.name = 'SpssHAlRight'
        if self.numerator == 2:
            self.name = 'SpssHAlCenter'
        if self.numerator == 3:
            self.name = 'SpssHAlMixed'
        if self.numerator == 4:
            self.name = 'SpssHAlDecimal'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssHAlignTypes.SpssHAlLeft'
        if self.numerator == 1:
            return 'SpssClient.SpssHAlignTypes.SpssHAlRight'
        if self.numerator == 2:
            return 'SpssClient.SpssHAlignTypes.SpssHAlCenter'
        if self.numerator == 3:
            return 'SpssClient.SpssHAlignTypes.SpssHAlMixed'
        if self.numerator == 4:
            return 'SpssClient.SpssHAlignTypes.SpssHAlDecimal'

SpssHAlignTypes.SpssHAlLeft = SpssHAlignTypes(0)
SpssHAlignTypes.SpssHAlRight = SpssHAlignTypes(1)
SpssHAlignTypes.SpssHAlCenter = SpssHAlignTypes(2)
SpssHAlignTypes.SpssHAlMixed = SpssHAlignTypes(3)
SpssHAlignTypes.SpssHAlDecimal = SpssHAlignTypes(4)    

SpssHAlignTypes.values.update({0:SpssHAlignTypes.SpssHAlLeft})
SpssHAlignTypes.values.update({1:SpssHAlignTypes.SpssHAlRight})
SpssHAlignTypes.values.update({2:SpssHAlignTypes.SpssHAlCenter})
SpssHAlignTypes.values.update({3:SpssHAlignTypes.SpssHAlMixed})
SpssHAlignTypes.values.update({4:SpssHAlignTypes.SpssHAlDecimal}) 

class SpssIGraphElementType(object):
    values = {}
    SpssIGraphDotLine = None
    SpssIGraphBar = None
    SpssIGraphCloud = None
    SpssIGraphSmoother = None
    SpssIGraphPie = None
    SpssIGraphBoxPlot = None
    SpssIGraphAreaEl = None
    SpssIGraphRefLine = None
    SpssIGraphSpikeEl = None
    SpssIGraphHistogram = None
    SpssIGraphErrorBar = None
    SpssIGraphMean = None
    SpssIGraphRegression = None
    SpssIGraphUnknown = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssIGraphDotLine'
        if self.numerator == 1:
            self.name = 'SpssIGraphBar'
        if self.numerator == 2:
            self.name = 'SpssIGraphCloud'
        if self.numerator == 3:
            self.name = 'SpssIGraphSmoother'
        if self.numerator == 5:
            self.name = 'SpssIGraphPie'
        if self.numerator == 7:
            self.name = 'SpssIGraphBoxPlot'
        if self.numerator == 8:
            self.name = 'SpssIGraphAreaEl'
        if self.numerator == 9:
            self.name = 'SpssIGraphRefLine'
        if self.numerator == 10:
            self.name = 'SpssIGraphSpikeEl'
        if self.numerator == 14:
            self.name = 'SpssIGraphHistogram'
        if self.numerator == 15:
            self.name = 'SpssIGraphErrorBar'
        if self.numerator == 16:
            self.name = 'SpssIGraphMean'
        if self.numerator == 17:
            self.name = 'SpssIGraphRegression'
        if self.numerator == 18:
            self.name = 'SpssIGraphUnknown'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphDotLine'
        if self.numerator == 1:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphBar'
        if self.numerator == 2:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphCloud'
        if self.numerator == 3:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphSmoother'
        if self.numerator == 5:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphPie'
        if self.numerator == 7:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphBoxPlot'
        if self.numerator == 8:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphAreaEl'
        if self.numerator == 9:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphRefLine'
        if self.numerator == 10:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphSpikeEl'
        if self.numerator == 14:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphHistogram'
        if self.numerator == 15:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphErrorBar'
        if self.numerator == 16:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphMean'
        if self.numerator == 17:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphRegression'
        if self.numerator == 18:
            return 'SpssClient.SpssIGraphElementType.SpssIGraphUnknown' 

SpssIGraphElementType.SpssIGraphDotLine = SpssIGraphElementType(0)
SpssIGraphElementType.SpssIGraphBar = SpssIGraphElementType(1)
SpssIGraphElementType.SpssIGraphCloud = SpssIGraphElementType(2)
SpssIGraphElementType.SpssIGraphSmoother = SpssIGraphElementType(3)
SpssIGraphElementType.SpssIGraphPie = SpssIGraphElementType(5)
SpssIGraphElementType.SpssIGraphBoxPlot = SpssIGraphElementType(7)
SpssIGraphElementType.SpssIGraphAreaEl = SpssIGraphElementType(8)
SpssIGraphElementType.SpssIGraphRefLine = SpssIGraphElementType(9)
SpssIGraphElementType.SpssIGraphSpikeEl = SpssIGraphElementType(10)
SpssIGraphElementType.SpssIGraphHistogram = SpssIGraphElementType(14)
SpssIGraphElementType.SpssIGraphErrorBar = SpssIGraphElementType(15)
SpssIGraphElementType.SpssIGraphMean = SpssIGraphElementType(16)
SpssIGraphElementType.SpssIGraphRegression = SpssIGraphElementType(17)
SpssIGraphElementType.SpssIGraphUnknown = SpssIGraphElementType(18)

SpssIGraphElementType.values.update({0:SpssIGraphElementType.SpssIGraphDotLine})
SpssIGraphElementType.values.update({1:SpssIGraphElementType.SpssIGraphBar})
SpssIGraphElementType.values.update({2:SpssIGraphElementType.SpssIGraphCloud})
SpssIGraphElementType.values.update({3:SpssIGraphElementType.SpssIGraphSmoother})
SpssIGraphElementType.values.update({5:SpssIGraphElementType.SpssIGraphPie})
SpssIGraphElementType.values.update({7:SpssIGraphElementType.SpssIGraphBoxPlot})
SpssIGraphElementType.values.update({8:SpssIGraphElementType.SpssIGraphAreaEl})
SpssIGraphElementType.values.update({9:SpssIGraphElementType.SpssIGraphRefLine})
SpssIGraphElementType.values.update({10:SpssIGraphElementType.SpssIGraphSpikeEl})
SpssIGraphElementType.values.update({14:SpssIGraphElementType.SpssIGraphHistogram})
SpssIGraphElementType.values.update({15:SpssIGraphElementType.SpssIGraphErrorBar})
SpssIGraphElementType.values.update({16:SpssIGraphElementType.SpssIGraphMean})
SpssIGraphElementType.values.update({17:SpssIGraphElementType.SpssIGraphRegression})
SpssIGraphElementType.values.update({18:SpssIGraphElementType.SpssIGraphUnknown})

class SpssTextStyleTypes(object):
    values = {}
    SpssTSRegular = None
    SpssTSItalic = None
    SpssTSBold = None
    SpssTSBoldItalic = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssTSRegular'
        if self.numerator == 1:
            self.name = 'SpssTSItalic'
        if self.numerator == 2:
            self.name = 'SpssTSBold'
        if self.numerator == 3:
            self.name = 'SpssTSBoldItalic'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssTextStyleTypes.SpssTSRegular'
        if self.numerator == 1:
            return 'SpssClient.SpssTextStyleTypes.SpssTSItalic'
        if self.numerator == 2:
            return 'SpssClient.SpssTextStyleTypes.SpssTSBold'
        if self.numerator == 3:
            return 'SpssClient.SpssTextStyleTypes.SpssTSBoldItalic'

SpssTextStyleTypes.SpssTSRegular = SpssTextStyleTypes(0)
SpssTextStyleTypes.SpssTSItalic = SpssTextStyleTypes(1)
SpssTextStyleTypes.SpssTSBold = SpssTextStyleTypes(2)
SpssTextStyleTypes.SpssTSBoldItalic = SpssTextStyleTypes(3)

SpssTextStyleTypes.values.update({0:SpssTextStyleTypes.SpssTSRegular})
SpssTextStyleTypes.values.update({1:SpssTextStyleTypes.SpssTSItalic})
SpssTextStyleTypes.values.update({2:SpssTextStyleTypes.SpssTSBold})
SpssTextStyleTypes.values.update({3:SpssTextStyleTypes.SpssTSBoldItalic})

class SpssVAlignTypes(object):
    values = {}
    SpssVAlTop = None
    SpssVAlBottom = None
    SpssVAlCenter = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssVAlTop'
        if self.numerator == 1:
            self.name = 'SpssVAlBottom'
        if self.numerator == 2:
            self.name = 'SpssVAlCenter'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssVAlignTypes.SpssVAlTop'
        if self.numerator == 1:
            return 'SpssClient.SpssVAlignTypes.SpssVAlBottom'
        if self.numerator == 2:
            return 'SpssClient.SpssVAlignTypes.SpssVAlCenter'

SpssVAlignTypes.SpssVAlTop = SpssVAlignTypes(0)
SpssVAlignTypes.SpssVAlBottom = SpssVAlignTypes(1)
SpssVAlignTypes.SpssVAlCenter = SpssVAlignTypes(2)

SpssVAlignTypes.values.update({0:SpssVAlignTypes.SpssVAlTop})
SpssVAlignTypes.values.update({1:SpssVAlignTypes.SpssVAlBottom})
SpssVAlignTypes.values.update({2:SpssVAlignTypes.SpssVAlCenter})
    
class SpssWindowStates(object):
    values = {}
    SpssMinimized = None 
    SpssMaximized = None
    SpssNormal = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'SpssMinimized'
        if self.numerator == 1:
            self.name = 'SpssMaximized'
        if self.numerator == 2:
            self.name = 'SpssNormal'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.SpssWindowStates.SpssMinimized'
        if self.numerator == 1:
            return 'SpssClient.SpssWindowStates.SpssMaximized'
        if self.numerator == 2:
            return 'SpssClient.SpssWindowStates.SpssNormal'

SpssWindowStates.SpssMinimized = SpssWindowStates(0)
SpssWindowStates.SpssMaximized = SpssWindowStates(1)
SpssWindowStates.SpssNormal = SpssWindowStates(2)

SpssWindowStates.values.update({0:SpssWindowStates.SpssMinimized})
SpssWindowStates.values.update({1:SpssWindowStates.SpssMaximized})
SpssWindowStates.values.update({2:SpssWindowStates.SpssNormal})

class CopySpecialFormat(object):
    values = {}
    Text = None
    Rtf = None
    Image = None
    Biff = None
    Emf = None
    def __init__(self,enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'Text'
        if self.numerator == 1:
            self.name = 'Rtf'
        if self.numerator == 2:
            self.name = 'Image'
        if self.numerator == 3:
            self.name = 'Biff'
        if self.numerator == 4:
            self.name = 'Emf'
            
    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False
            
    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.CopySpecialFormat.Text'
        if self.numerator == 1:
            return 'SpssClient.CopySpecialFormat.Rtf'
        if self.numerator == 2:
            return 'SpssClient.CopySpecialFormat.Image'
        if self.numerator == 3:
            return 'SpssClient.CopySpecialFormat.Biff'
        if self.numerator == 4:
            return 'SpssClient.CopySpecialFormat.Emf'

CopySpecialFormat.Text = CopySpecialFormat(0)
CopySpecialFormat.Rtf = CopySpecialFormat(1)
CopySpecialFormat.Image = CopySpecialFormat(2)
CopySpecialFormat.Biff = CopySpecialFormat(3)
CopySpecialFormat.Emf = CopySpecialFormat(4)

CopySpecialFormat.values.update({0:CopySpecialFormat.Text})
CopySpecialFormat.values.update({1:CopySpecialFormat.Rtf})
CopySpecialFormat.values.update({2:CopySpecialFormat.Image})
CopySpecialFormat.values.update({3:CopySpecialFormat.Biff})
CopySpecialFormat.values.update({4:CopySpecialFormat.Emf})

class VarNamesDisplay(object):
    values = {}
    Names = None
    Labels = None
    Both = None
    def __init__(self, enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'Names'
        if self.numerator == 1:
            self.name = 'Labels'
        if self.numerator == 2:
            self.name = 'Both'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.VarNamesDisplay.Names'
        if self.numerator == 1:
            return 'SpssClient.VarNamesDisplay.Labels'
        if self.numerator == 2:
            return 'SpssClient.VarNamesDisplay.Both'

VarNamesDisplay.Names = VarNamesDisplay(0)
VarNamesDisplay.Labels = VarNamesDisplay(1)
VarNamesDisplay.Both = VarNamesDisplay(2)

VarNamesDisplay.values.update({0:VarNamesDisplay.Names})
VarNamesDisplay.values.update({1:VarNamesDisplay.Labels})
VarNamesDisplay.values.update({2:VarNamesDisplay.Both})

class VarValuesDisplay(object):
    values = {}
    Values = None
    Labels = None
    Both = None
    def __init__(self, enumValue):
        self.numerator = enumValue
        if self.numerator == 0:
            self.name = 'Values'
        if self.numerator == 1:
            self.name = 'Labels'
        if self.numerator == 2:
            self.name = 'Both'

    def __eq__(self,other):
        if type(other) == types.IntType and other == self.numerator:
            return True
        elif type(other) == type(self) and other.numerator == self.numerator:
            return True
        else:
            return False

    def __repr__(self):
        if self.numerator == 0:
            return 'SpssClient.VarValuesDisplay.Values'
        if self.numerator == 1:
            return 'SpssClient.VarValuesDisplay.Labels'
        if self.numerator == 2:
            return 'SpssClient.VarValuesDisplay.Both'

VarValuesDisplay.Values = VarValuesDisplay(0)
VarValuesDisplay.Labels = VarValuesDisplay(1)
VarValuesDisplay.Both = VarValuesDisplay(2)

VarValuesDisplay.values.update({0:VarValuesDisplay.Values})
VarValuesDisplay.values.update({1:VarValuesDisplay.Labels})
VarValuesDisplay.values.update({2:VarValuesDisplay.Both})
