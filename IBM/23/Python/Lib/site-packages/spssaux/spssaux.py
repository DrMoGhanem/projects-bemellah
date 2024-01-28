"""
a library of useful utility routines for working with the SPSS variable dictionary and other common tasks
Copyright (C) 2006, 2007, 2008, 2009 by SPSS Inc."""

#/***********************************************************************
# * Licensed Materials - Property of IBM 
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2013
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp. 
# ************************************************************************/

import spss
import random
import copy, sys, os.path, os
import ConfigParser
import re, operator
import codecs

# debugging
    # makes debug apply only to the current thread
#try:
    #import wingdbstub
    #if wingdbstub.debugger != None:
        #import time
        #wingdbstub.debugger.StopDebug()
        #time.sleep(1)
        #wingdbstub.debugger.StartDebug()
    #import thread
    #wingdbstub.debugger.SetDebugThreads({thread.get_ident(): 1}, default_policy=0)
    ## for V19 use
    ###    ###SpssClient._heartBeat(False)
#except:
    #pass

# All messages for this module are collected here for translation purposes.  Docstrings, however, are not.
# To translate, duplicate the message block and translate the later copy, maintaining the assignment syntax.
# The original can be commented out, but it will be replaced by the later version anyway, so this is not necessary.
# Maintaining the original English text will make it easier to update translations later.
# Place the translated block after all the English messages in order to facilitate checking for changes in the English text.

_msg1 = "An OMS subtype must be specified."
_msg2 = "Unequal number of dataset names and subtypes was specified."
_msg3 = "Invalid type specified"
_msg4 = "Invalid verify specified"
_msg5 = "cd must be an absolute path if used"
_msg6 = "filespec does not exist:"
_msg7 = "filespec is not of the specified type: "
_msg8 = "filespec does not exist or is not of the specified type: "
_msg9 = "getMissingValues2 requires at least SPSS 15"
_msg10 = "Variable not in this dictionary"
_msg11 = "start or end variable not in dictionary"
_msg12 = "A VariableDict is required if var is a string."
_msg13 = "Invalid variable type"
_msg14 = "Invalid variable measurement level or not a list"
_msg15 = "No variable values found"
_msg16 = "Invalid variable name."
_msg17 = "VariableDict pattern parameter specifies and invalid regular expression: "
_msg18 = """Error: Cannot set to original name.  File probably already exists.
        Opening under temporary name.  Original  name is\n"""
_msg19 = "Invalid variable or TO usage: "
_msg20 = "Invalid file type: %s"

#History
#    2005-10-3   tolerate extra group level in GetSHOW xml
#                         add GetProcessInstallDir
#    2005-10-6   add GetSPSSInstallDir
#    2005-10-27  fine tune GetDatasetInfo
#    2005-11-22  adjustments to VariableDict class for iterating and indexing
#    2005-12-01  allow variable names in VariableDict indexing and preserve creation order of variables
#    2006-01-13  provide for regular expression matches in in VariableDict creation and retrieving variable lists (Variables method)
#    2006-01-17  extend selection feature to include variable type and measurement level
#    2006-02-21  New functions getActiveDatasetName and CreateOutputDataset
#    2006-02-27  New method, Indexes, in VariableDict class, new function, isDateVariable,
#                and __int__ implemented for Variable class.  Added varsWithDuplicateLabels function
#                and to the VariableDict class, the variables property
#    2006-03-24 Add setters for Variable class properties
#    2006-03-28 Generalize createDatasetOutput to take a list of table subtypes
#    2006-03-30 Add range method to VariableDict class
#    2006-04-18 Added CreateFileHandle
#    2006-04-28 Added __str__ method to Variable object, returning the variable name
#    2006-06-29 Added datasetvisible parameter to createDatasetOutput function
#    2006-07-11  Added CreateAttribute and getSpssVersion functions and 
#                          implement __eq__,  __ ne__, and __hash__ for Variable class so sets of variables work
#                          Add dataset activate and close methods to VariableDict class.
#    2006-08-01 Changes to GetSPSSInstallDir and getSpssVersion to support SPSS 15
#    2006-08-14 Added getMissingValues2 for SPSS15
#    2006-08-22 Added GetSPSSMajorVersion
#    2006-10-09 Enhanced getValuesFromXmlWorkspace for tables without a row dimension or without a column dimension
#    2006-12-15  ValueLabelsTyped support for getting the labelled values according to the variable's type
#    2007-01-12  Added openDataFileFromUrl
#    2007-02-06 Handle value label for a blank in GetValueLabels function and property
#    2007-03-22 Standardize casing of function and class names and define aliases for old names
#    2007-04-24 Rename variables method of VariableDict to variablesf to avoid conflict with variables property
#    2007-06-20 Add expand method to VariableDict
#    2007-06-26 Bug fix for creating value labels
#    2007-09-10 Adjust _GetSPSSLocFromIni for SPSS 16 location
#    2007-09-27 Generalize OpenDataFile to handle Excel, SAS, and Stata files with all options
#    2007-10-03  Add u and truncatestring functions for Unicode support
#    2009-04-29 Add FileHandles class for SPSS file handle management
#    2009-06-05 Generalize GetSPSSInstallDir to look for paswstat.  Accept sequence tags in getOutputFrom...
#    2009-07-23 Bug fix for platform-specific location of site-packages
#    2009-08-19  Caseless option for VariableDict class
#    2009-08-31 Bug fix for handling multiple site-packages locations
#    2010-03-22 Workaround in hash, eq, ne operators for Unicode str problem
#    2010-10-19  Make setting value labels in VariableDict work with extended characters
#    2010-12-24 Adjust getMissingValues for change in Display Dict structure
#     2011-03-22 Update GetSPSSInstallDir for changes in executable names
#     2011-08-31 Make GetValueLabels work when olang is not English
#     2011-10-26 Make getSpssInstallDir work when Statistics drive mode
#    2013-03-15 Adapt _GetSPSSLocFromIni for longer version numbers
#    2013-12-14 New function, GetDatasetInfoEx

__author__  =  'spss, jkp'
__version__ =  '2.6.0'
version = __version__

# global variable tracebacklimit is used to save and restore traceback limit state
tracebacklimit = None

def getSpssVersion():
    """Return the SPSS version."""
    
    # This code is needed because the 14.0.x version of the spss module does not have an __version__ variable
    try:
        return spss.__version__
    except:
        try:
            sv = spss.Cursor
            sv = '14.0.1'
        except:
            sv = '14.0.0'
        return sv

ok1600 = int(getSpssVersion().split(".")[0]) >= 16
ok1800 = int(getSpssVersion().split(".")[0]) >= 18

def _GetVariableInfo(fn, vars=None):
    """_GetVariableInfo(vars) ->list of specified information.
    The result is -
        all variables if no argument is supplied
        a list of variables if a list of positions is supplied
        a one-item list if a single position is supplied
"""
    
    names = []
    if isinstance(vars, (list, tuple)):         #type(vars) is a sequence:
        names = copy.copy(vars)
    elif vars is None:
        names = [v for v in range(spss.GetVariableCount())]
    else:
        names = [vars]
    return [fn(v) for v in names]

def    createXmlOutput(cmd, omsid=None, subtype='', visible=False):
    """
    Create a tagged item in the XMLworkspace containing the output from an SPSS command.
    
        cmd is an SPSS command or sequence of commands.  
        omsid is the OMS identifier for the command whose output is to be captured.  
        (Other commands in the sequence will not be captured,  but all executions of the command 
        with this identifier will be in a single workspace object.)
        The omsid is not case sensitive.
        If omsid is not included, the value of cmd up to the first whitespace is used, except
        that any trailing period is removed.
        If subtype, which only applies to tables, is specified, only tables of that type are included.
        subtype can be a single subtype or a list of subtypes.  It is ignored for items other than tables.
        By default, the captured output is excluded from the Viewer, if visible is True, the output
        will be displayed.  Note that visibility only affects the output for the omsid command.

    Return value is a two-tuple consisting of the workspace tag by which to retrieve the output,
    which should be destroyed when no longer needed, and the last (maximum) error level of the request.  
    The error level will be zero if there were no SPSS errors.
    """
    tag = "S"+ str(random.uniform(0, 1))
    if omsid is None:
        omsid = cmd.split()[0]
        if omsid[-1] == ".": 
            omsid = omsid[0:-1]
    if cmd[-1] != ".":
        cmd += "."
    if subtype:
        if isinstance(subtype, (list, tuple)):
            subtype = " ".join(["'" + s + "'" for s in subtype])
        else:
            subtype = "'" + subtype + "'"
        subtype = " subtype=[" + subtype + "]"
    s = ["OMS /if commands='" + str(omsid) + "'" + subtype,
       " /DESTINATION " \
       + (not visible and "Viewer=no " or "") \
       + "format=oxml xmlworkspace='" + tag + "'",
       "/TAG = '" + tag +"'.",
    cmd,
    "OMSEND TAG='" + tag + "'."]
    ###print s     #debug
    try:
        spss.Submit(s)
    except:
        pass
    return (tag, spss.GetLastErrorLevel())

def    _XPathSelector(category, attrib):
    """Create XPath qualifier fragment from a category and value
    If category is a list, a sequence of nested predicates is constructed
    """
    if category:
        c = category
        if not isinstance(c, list):        #type(c) is not list:
            c = [c]
        return reduce(lambda x, y: x + '//category[@' + attrib + '="' + y + '"]', c,"")
    else:
        return "//category"


def    getValuesFromXmlWorkspace(tag, tableSubtype, rowCategory=None, rowAttrib="text",
        colCategory=None, colAttrib="text", cellAttrib="*", xpathExpr=False, hasRows=None, hasCols=None):
    """Return a list of 0 or more values from a table item in the XMLWorkspace and, optionally,
    return the xpath expression for the request.
    
    Note: If you are uncertain about how to specify these values, you can use
    pivottablestruct.displayTableStrucure from the SPSS Community site to see the category structure of a pivot table.

        tag is the XMLWorkspace identifier to check.  It can be a sequence as returned by createXmlOutput, in
        which case the first element is used.
        tableSubtype is the subtype of the table from which to retrieve data.  It is the
        OMS table type identifier.
        rowCategory is the optional row category value to fetch.  If omitted, all rows
        meeting the other criteria are returned.
        rowAttrib is the attrib to use with rowCategory.  It defaults to text but may
        be any type in the table row labels such as label or varName
        colCategory is the optional column category to fetch.  If omitted, all columns
        meeting the other criteria are returned.
        colAttrib is the attribute type for colCategory.  It defaults to text but may
        be any type in the column labels such as label or varName
        cellAttrib is the attribute type to return.  It defaults to all attributes, but it may usefully
        be specified as number, date, or text.
        Some tables have no row dimension: set hasRows=False to remove the row selector from the xpath expression
        Some tables have no column dimension: set hasCols=False to remove the column selector from the xpath expression
        If the xpath expression returns an empty list and neither hasRows nor hasCols was specified, it is retried without the row dimension
        If still empty, it is tried without the col dimension
        If xpathExpr is True, the returned result is a 2-tuple with the first element as
        the result and the second as the xpath expression.
    """
    
    if not isinstance(tag, basestring):
        tag = tag[0]
    hasr = hasRows != False
    hasc = hasCols != False
    xpathbase = """//pivotTable[@subType='%(tableSubtype)s']"""
    xpathrows = """//dimension[@axis='row']%(rowselector)s"""
    xpathcols = """//dimension[@axis='column']%(colselector)s"""
    xpathtail =  """/cell/@%(cellAttrib)s"""
    
    d = {"tableSubtype": tableSubtype,
           "rowselector": _XPathSelector(rowCategory,rowAttrib),
           "colselector": _XPathSelector(colCategory,colAttrib),
           "cellAttrib": cellAttrib}
    xpath = (xpathbase + (hasr and xpathrows or '') + (hasc and xpathcols or '') + xpathtail) % d    
    res = spss.EvaluateXPath(tag, "/outputTree", xpath)
    
    # if Xpath query got nothing and caller did not declare no rows or no cols
    # so find out whether the table has row or column axes and adjust accordingly
    if res == []  and hasRows is None and hasCols is None:
        if rowCategory is None:
            hasr =  spss.EvaluateXPath(tag, "/outputTree", (xpathbase + "//dimension[@axis='row']") %d ) != []
        if colCategory is None:
            hasc =  spss.EvaluateXPath(tag, "/outputTree", (xpathbase + "//dimension[@axis='column']") %d) != []
        if hasr or hasc:
            xpath2 = (xpathbase + (hasr and xpathrows or '') + (hasc and xpathcols or '') + xpathtail) % d
            if xpath != xpath2:
                xpath = xpath2
                res = spss.EvaluateXPath(tag, "/outputTree", xpath)

    if xpathExpr:
        return res, xpath
    else:
        return res

def createDatasetOutput(cmd, omsid=None,  subtype=None, visible=False, newdsn=None, datasetvisible=True):
    """
    Create a dataset containing the output from a selected table or list of tables of an SPSS command sequence.
    
        cmd is a single SPSS command or a sequence of commands.
        omsid is the OMS identifier for the command whose output is to be captured.
        (Other commands in the sequence will not be captured.)
        The omsid and subtypes are not case sensitive.
        If omsid is not included, the value of cmd up to the first whitespace is used, except
        that any trailing period is removed.  For this convention to work, do not use command abbreviations.
        subtype must be specified: only tables of those types are included.
        By default, the cmd output is excluded from the Viewer, if visible is True, the output
        will be displayed.
        By default, the dataset(s) created will be visible.  If datasetvisible is False, the datasets will be hidden.
        Random names are assigned by default to the new datasets.  newdsn can be used to specify a
        different name.  The number of items in newdsn must match the number of subtypes.
    
    Side effect: if the current active dataset does not have a name, it is assigned one in order to
    preserve it.

    Return value is a tuple of the names of the dataset created and the last (maximum) error level of
    the request. The error level will be zero if there were no SPSS errors.

    Example:
    tag, err = spssaux.createDatasetOutput("FREQUENCIES year/ntiles=4",
    subtype='statistics', visible=True, newdsn='freqs')
    print "output dsn:", tag, "error code:", err
    """
    if subtype is None:
        raise ValueError, _msg1
    subtype = _listify(subtype)
    if newdsn:
        newdsn = _listify(newdsn)
        if len(newdsn) != len(subtype):
            raise ValueError, _msg2
    tag = ["S" + str(random.uniform(0, 1)) + "x" for i in range(len(subtype))]  #used both for OMS and as the dataset name unless newdsn is given
    tagtherest = "S" + str(random.uniform(0, 1)) + "x"
    if not newdsn:
        newdsn = tag
    dsn = getActiveDatasetName()        #a name must be assigned if there isn't one already
    if not dsn:
        dsn = "D" + str(random.uniform(0, 1)) + 'x'
        spss.Submit("DATASET NAME " + dsn)
    if omsid is None:
        omsid = cmd[:cmd.find(" ")]
        if omsid[-1] == ".": 
            omsid = omsid[0:-1]
    if datasetvisible:
        dsv = ""
    else:
        dsv = " WINDOW=HIDDEN"
    for itag, idsn, isubtype in zip(tag, newdsn, subtype):                                    
        spss.Submit(["DATASET DECLARE " + idsn + dsv + ".",
        "OMS SELECT TABLES /IF COMMANDS='" + str(omsid) + "' SUBTYPE='" + isubtype + "'",
        " /DESTINATION " + (not visible and "Viewer=no " or "")   + " FORMAT=SAV OUTFILE='" + idsn + "'",
        "/TAG = '" + itag +"'."])
    if not visible:
        spss.Submit("OMS /DESTINATION VIEWER=NO/TAG='" + tagtherest + "'.")
    try:
        err = 0
        spss.Submit(cmd)
    except:
        err = spss.GetLastErrorLevel()
    spss.Submit("OMSEND TAG=['" + "' '".join(tag) + "'].")
    if not visible:
        spss.Submit("OMSEND TAG='" + tagtherest + "'.")
    spss.Submit("DATASET ACTIVATE " + dsn)
    newdsn.append(err)
    return newdsn

def getVariableNamesList(vars=None):
    "Return a list containing variable names.  vars is an index or a list of indexes"
    fn = spss.GetVariableName
    return _GetVariableInfo(fn, vars)

def getVariableFormatsList(vars=None):
    "Return a list containing variable formats.  vars is an index or a list of indexes"
    fn = spss.GetVariableFormat
    return _GetVariableInfo(fn, vars)

def getVariableLabelsList(vars=None):
    "Return a list containing variable labels.  vars is an index or a list of indexes"
    fn = spss.GetVariableLabel
    return _GetVariableInfo(fn, vars)

def getVariableMeasurementLevelsList(vars=None):
    "Return a list containing variable measurement levels.  vars is an index or a list of indexes"
    fn = spss.GetVariableMeasurementLevel
    return _GetVariableInfo(fn, vars)

def getVariableTypesList(vars=None):
    "Return a list containing variable types.  vars is an index or a list of indexes"
    fn = spss.GetVariableType
    return _GetVariableInfo(fn, vars)

# SHOW command output functions
def getShow(item, olang=None):
    """Return the output for "item" as a string, where item is a SHOW command keyword.
    
    Item must appear in the System Settings table. For the few items where there are multiple fields,
    the fields are separated with ";". An empty string will be returned for an invalid keyword.
    olang specifies the output language that should be set for the output, defaulting to current.
    An exception is raised if the olang is not available."""
    
    try:
        if not olang is None:
            spss.Submit(["PRESERVE.", "SET OLANG = " + olang + "."])
        

        tag, ignore = createXmlOutput("SHOW " + item + ".", "SHOW")
        
        # The xpath expression below is designed to work with all output languages
        result = ";".join(spss.EvaluateXPath(tag, '/',
        '//pivotTable[@subType="System Settings"]/dimension//category/dimension/category[2]/cell/@text'))
    finally:
        if not olang is None:
            spss.Submit("RESTORE")
        if sys.exc_info()[0] is None:
            spss.DeleteXPathHandle(tag)
    return result
    
# find the Process installation directory
def getProcessInstallDir(handle=None): 
    """Return the path to the spss executable or whatever directory the current process was launched
    from. If handle is specified, an SPSS FILE HANDLE for that location is created."""
    
    spssloc = os.path.dirname(sys.executable)
    if handle:
        if not isinstance(handle, basestring):
            raise TypeError("file handle must be a string")
        spss.Submit("FILE HANDLE " + handle + " /NAME='" + spssloc + "'.")
    return spssloc

# find the SPSS/PASW Statistics installation directory (works in both xd and dx modes)
def getSpssInstallDir(handle=None):
    """Return the path to the spss executable. If handle is specified, an SPSS FILE HANDLE for that
    location is created."""
    
    if not os.path.basename(sys.executable).lower().startswith(("spss", "paswstat", "startpy", "startx")):
        spssloc = _getSPSSLocFromIni()
    else:
        spssloc = os.path.dirname(sys.executable)
    if not spssloc:
        raise AttributeError("Cannot determine SPSS/PASW Statistics location")
    if handle:
        if not isinstance(handle, basestring):
            raise TypeError("file handle must be a string")
        spss.Submit("FILE HANDLE " + handle + " /NAME='" + spssloc + "'.")
    return spssloc

def createFileHandle(filespec, handlename, type=None, verify=None, cd="", subcommands=""):
    """Create an SPSS File Handle named handlename. 
    
        If type == "path", assume that filespec is a directory; 
        If type == "file", assume that it refers to a file (with an optional path)
        
        If verify == None, no validity check is made; 
        If verify == "full", check that the complete spec exists and has the type specified, if any.
        If verify == "path", check that the path is valid but succeed if the type is "file" and the path to the file exists even if the file does not).
        
        On failure, raise an exception.
        If filespec is or has a relative path, it will be evaluated against the process current working directory when verifying.  This might not be
        the SPSS Processor working directory.  Specify the working directory to be used for a relative path in the cd parameter,
        which must be an absolute path if used.
        subcommands can be specified as a string containing other parameters of the FILE HANDLE command such as /LRECL.
    """
    
    if not type in [None, "path", "file"]:
        raise ValueError, _msg3
    if not verify in [None, "full", "path"]:
        raise ValueError, _msg4
    if verify and not os.path.isabs(filespec):
        if cd != "" and not os.path.isabs(cd):
            raise Exception, _msg5
        filespec = os.path.join(cd, filespec)
        
    if verify == "full":
        if not os.path.exists(filespec):
            raise Exception, _msg6 + filespec
        if (type == "path" and not os.path.isdir(filespec)) or (type == "file" and not os.path.isfile(filespec)):
            raise Exception, _msg7 + filespec
    if verify == "path":
        if type == "file":
            dirname = os.path.dirname(filespec)
        else:
            dirname = filespec
        if not os.path.isdir(dirname):
            raise Exception, _msg8 + dirname
        
    cmd = "FILE HANDLE %(handlename)s /NAME '%(filespec)s' %(subcommands)s" % locals()
    spss.Submit(cmd)
    

# get Variable attributes for selected variable
def getAttributesDict(varname=None):
    """return a dictionary of attributes and their values for variable varname.
    
    If no varname is supplied, datafile attributes are returned instead.
    The attribute names are the keys.  For array attributes, the subscript is part of
    the name.  E.g., an array attribute might have the name "y[1]".
    """
    if varname:
        subcmd = "/variable=" + varname
        attnamespath = \
            "//pivotTable[@subType='Variable Attributes']/dimension/category/dimension/category/@text"
        attvaluespath = \
    "//pivotTable[@subType='Variable Attributes']/dimension/category/dimension/category/dimension/category/cell/@text"
    else:
        subcmd = ""
        attnamespath = \
            "//pivotTable[@subType='Datafile Attributes']/dimension/category/@text"
        attvaluespath = \
            "//pivotTable[@subType='Datafile Attributes']/dimension/category/dimension/category/cell/@text"
    
    tag, ignore = createXmlOutput("display attributes " + subcmd + ".", "File Information")
    
    attnames = spss.EvaluateXPath(tag, '/outputTree', attnamespath)
    attvalues = spss.EvaluateXPath(tag, '/outputTree', attvaluespath)
    spss.DeleteXPathHandle(tag)    
    return dict(zip(attnames, attvalues))

def getDatasetInfo(Info="Data"):
    """Return selected information on the current active dataset.  Value is empty if none.
    
        Info can be
            Data    name of the active file (empty if unnamed)
            Filter    filter variable or empty
            Weight    weight variable or empty
            SplitFile    comma-separated split variable(s) or empty
        If there is no active file but there IS a dataset name, the dataset name is returned.
        Except for Data, the form of the information returned depends on the SPSS Output Labels
        preference setting.
    """
    InfoTypes = {"data" : 0 , "filter" : -3, "weight" : -2, "splitfile" : -1}
    Info = Info.lower()
    if not Info in InfoTypes:
        raise ValueError
    
    tag = createXmlOutput("show dir")
    cf = spss.EvaluateXPath(tag[0], "/outputTree",
        "//pivotTable[@subType='Notes']/dimension[@axis='row']/group[1]/category/cell/@text|@label")
    #cf will have three entries if no active file; otherwise four or five after discarding possible case count
    spss.DeleteXPathHandle(tag[0])
    try:
        x = int(cf[-1])        # if last item is a number, it is the case count (hack)
        cf = cf[:-1]
    except: pass
    if Info == "data":
        if len(cf) >= 4:
            return cf[0].replace("\\", "/").rstrip()
        else:
            return ""    #no entry for file is present if there is no named active file
    else:
        item = cf[InfoTypes[Info]]
        if item.startswith("<"):
            return ""
        else:
            return item
        
def getDatasetInfoEx():
    """Return a dictionary of information on the current active dataset.
    
    Contents are (key, value):
        Data: datafile name
        Active Dataset: dataset name
        File Label: datafile label
        Filter: filter variable
        Weight: weight variable
        Split File: split file specification
        
    If an item is not in effect, its dictionary value is None.
    Key names are in English regardless of the OLANG setting.
    ** This function requires at least Statistics version 19. **
    """
    
    try:
        olang = "english"   # in case api fails
        olang = spss.GetSetting("OLANG")
        if olang.lower() != "english":
            spss.SetOutputLanguage("English")
        tag = createXmlOutput("show dir")
        items = spss.EvaluateXPath(tag[0], "/outputTree",
            """//pivotTable[@subType="Notes"]
            /dimension[@axis="row"]/group[@text="Input"]/category/@text""")
        values = spss.EvaluateXPath(tag[0], "/outputTree",
             """//pivotTable[@subType="Notes"]
             /dimension[@axis="row"]/group[@text="Input"]/category/cell/@text""")
        for i,v in enumerate(values):
            if v == "<none>":
                values[i] = None
        spss.DeleteXPathHandle(tag[0])
        result = dict(zip(items, values))
        for k in ["Data", "Active Dataset", "File Label"]:
            if not k in result:
                result[k] = None
    finally:
        if olang.lower != "english":
            spss.SetOutputLanguage(olang)
    return result

def getActiveDatasetName():
    """Return the dataset name for the active dataset or None if unnamed."""
    
    d = {"tag" : "S"+ str(random.uniform(0, 1)), "tag2" : "S"+ str(random.uniform(0, 1))}
    spss.Submit(
        """OMS /IF SUBTYPES='Datasets'/DESTINATION XMLWORKSPACE='%(tag)s' FORMAT=OXML VIEWER=NO/TAG='%(tag)s'.
        OMS /DESTINATION VIEWER=NO/TAG='%(tag2)s'.
        DATASET DISPLAY.
        OMSEND TAG=['%(tag)s' '%(tag2)s'].""" % d)
    dsn = spss.EvaluateXPath(d["tag"], "/", "//pivotTable/dimension//cell/footnote/../@text")
    spss.DeleteXPathHandle(d["tag"])
    if dsn[0].startswith("("):
        return None
    else:
        return dsn[0]

def    getValueLabels(varindex, matchtype=False):
    """Get the value labels for the variable with index varindex.  varindex may be an int or a Variable object.
    Returns a Python dictionary with values and labels.
    
        If matchtype is False (the default), all values are returned as strings.
        If matchtype is True, values are converted to doubles for numeric variables
    """
    varindex = int(varindex)
    vn = spss.GetVariableName(varindex)
    vt = spss.GetVariableType(varindex)
    xptail = vt == 0 and "@number" or "@string"
    
    tag, errlevel = createXmlOutput("DISPLAY DICTIONARY /VARIABLES=" + vn + ".", "File Information")
    if errlevel:
        raise Exception, spss.GetLastErrorMessage()
    
    ###spss.GetXmlUtf16(tag, filename="c:/temp/dis.xml")
    valpath = "pivotTable[@subType='Variable Values']/dimension/group/category/" + xptail
    ###labpath = "pivotTable[@subType='Variable Values']/dimension/group/category/@label"
    labpath = """//pivotTable[@subType='Variable Values']/dimension/group/category/dimension//cell/@text"""
    ###labpath = """//pivotTable[@subType='Variable Values']/dimension/group/category/dimension[@text='Label']//cell/@text"""
    vallist = spss.EvaluateXPath(tag, '/outputTree/command', valpath)
    if matchtype and vt == 0:
        vallist = [float(v) for v in vallist]
    lablist = spss.EvaluateXPath(tag, '/outputTree/command', labpath)
    spss.DeleteXPathHandle(tag)
    
    # if the variable type is string and there is a label for a blank value, there may be no string (or text) attribute for the
    # value.  If the label and value list lengths differ by one, assume a blank value occurs first
    if vt > 0 and len(vallist) - len(lablist) == -1:
        vallist.insert(0, " ")

    # there will be no variable values table if no labels are defined.
    return dict(zip(vallist, lablist))

def getMissingValues(varindex):
    """Return a string of the missing values for the variable with index varindex.
    
        varindex may be a number or a Variable object. The values are comma separated and are formatted
        according to the variable's format and, for range specifications, are expressed in a
        language-sensitive way. String codes are quoted. 
        
        If no missing values are defined, the returned string is empty. """
    
    # The queried table has a new column as of V18, role, inserted in the middle, which means
    # that the missing values column number is version dependent.
    # In addition, if there are no missing values, the missing value column is not produced.
    
    varindex = int(varindex)
    tag, ignore = createXmlOutput("DISPLAY DICTIONARY /VARIABLE=" + spss.GetVariableName(varindex) + ".",
        "File Information")
    result = spss.EvaluateXPath(tag, '/outputTree',
    "//pivotTable[@subType='Variable Information']/dimension/category/dimension/category/cell/@text")
    spss.DeleteXPathHandle(tag)
    if ok1800:   # extra column appears
        inc = 1
    else:
        inc = 0
    if len(result) == 8+ inc:
        return result[-1]
    else:
        return ""
        
    ###return len(result) and result[0] or ""

def getMissingValues2(varindex):
    """Return a 4-tuple of missing value codes for the variable with index varindex.
    varindex may be a number or a Variable object.
    This function requires SPSS 15.
    The first element of the tuple indicates the type of the following triple.
      0 = simple values
      1 = range
      2 = range plus one additional missing value
    Unused slots have value None"""
    try:
        return spss.GetVarMissingValues(int(varindex))
    except AttributeError:
        print _msg9
        raise

def openDataFile(filespec, datasetName=None, dataset=None, varlist=None, filetype='sav', **kwargs):
    """Open an SPSS, Excel, SAS, or Stata data file.
    
    filespec is required and is a string that identifies the file to open.
    datasetName is optional and specifies a dataset name to be assigned to the file,
    which allows the file to remain open and usable when another data file is opened.
    dataset is an alternative name for the datasetName parameter.  Only one should be used.
    
    filetype can be sav, xls, xlsm, xlsx, sas, or stata.
    
    Options for SAV:
    a single variable name or a list of variable
    names to be retained in the opened file.
    
    Options for Excel:
    assumedstrwidth.  Default 32767
    sheet: index or name.  Default: index
    sheetid: the sheet number.  Default: 1
    cellrange: FULL or RANGE.  Default: FULL
    rangespec: required if RANGE: No default.
    readnames: ON or OFF.  read names from first row.  Default: ON
    
    SAS:
    dset: dataset name within file.  Default: first dataset
    formats: a formats file to read.  Default: none
    
    Stata:
    No options.
    
    Parameters are not validated: if they are not valid, an SPSS error will be produced.
    """

    filetype = filetype.lower()
    filespec = _smartquote(filespec)
    
    if filetype == "sav":
        varlist = kwargs.get("varlist", " ")
        if varlist.strip():
            varlist = " /KEEP=" + (isinstance(varlist, basestring) and varlist or ' '.join(varlist))
        cmd = "GET FILE= %(filespec)s %(varlist)s"
        
    elif filetype in ['xls', 'xlsx', 'xlsm'] :    # Excel
        assumedstrwidth = kwargs.get("assumedstrwidth", 32767)
        sheet = kwargs.get("sheet", "INDEX")
        sheetid = kwargs.get("sheetid", 1)
        if isinstance(sheetid, basestring):
            sheetid = _smartquote(sheetid)
        cellrange= kwargs.get("cellrange", "FULL")
        rangespec = kwargs.get("rangespec", " ")
        if rangespec.strip():
            rangespec = '"' + rangespec + '"'
        readnames = kwargs.get("readnames", "ON")

        cmd = """GET DATA /TYPE= %(filetype)s /FILE=%(filespec)s /ASSUMEDSTRWIDTH=%(assumedstrwidth)d
        /SHEET=%(sheet)s %(sheetid)s /CELLRANGE=%(cellrange)s %(rangespec)s /READNAMES=%(readnames)s"""
        
    elif filetype == "sas":
        dset = kwargs.get("dset", " ")
        if dset.strip():
            dset = "DSET(" + _smartquote(dset) + ")"
        formats = kwargs.get("formats", " ")
        if formats.strip():
            formats = "/FORMATS=" + _smartquote(formats) 
        cmd = "GET SAS DATA=%(filespec)s %(dset)s %(formats)s"
        
    elif filetype == "stata":
        cmd = "GET STATA FILE=" + filespec
        
    else:
        raise ValueError, _msg20 % filetype
    
    kwargs.update(locals())
    cmd = cmd % kwargs

    spss.Submit(cmd)
    
    datasetName = datasetName or dataset
    if datasetName:
        spss.Submit("DATASET NAME " + str(datasetName))

def openDataFileFromUrl(url,  *args, **kwds):
    """Copy a data file from a location specified by a url and open it.
    
    url is the location from which to retrieve the file.
    The other arguments are identical to the openDataFile parameters.
    
    The file is restored to its original name if possible."""
    
    import urllib, os
    localfilename, headers = urllib.urlretrieve(url)
    unqname = urllib.unquote_plus(url)
    truefilename = os.path.split(unqname)[-1]
    localdir = "".join(os.path.split(localfilename)[:-1])
    newname = localdir + "/" + truefilename
    try:
        os.rename(localfilename, newname)
    except:
        print _msg18 + truefilename
        newname = localfilename
    openDataFile(newname, *args, **kwds)
    
def saveDataFile(filespec):
    """Save the active dataset as filespec.
    
    An SpssError exception will be raised if there is no active dataset."""
    
    # just for symmetry with openDataFile
    spss.Submit("SAVE OUTFILE='" + filespec + "'")

class Variable(object):
    """variable class that delegates to VariableDict to get properties dynamically based on index.
    If passing a Variable object to a function that takes only a variable index, use int(variable).
    Variable properties that are supported are
    VariableName (get)
    VariableIndex (get)
    VariableLabel (get, set)
    VariableLevel (get, set)
    VariableType (get)
    VariableFormat (get, set)
    ValueLabels (get, set by assigning a dictionary of values and labels)
    Attributes= (get, set)
    MissingValues (get, set by assigning a list of values.  For numeric, entry can include ranges, e.g., 99 thru high)
    MissingValues2(get)  returns 4-tuple.  Requires SPSS 15
"""
    def __init__(self, dict, index, indextype='VariableDict'):
        self.dict = dict
        if indextype == 'VariableDict':
            self.index = self.dict.vdict[index] #map from dict subscript to SPSS dict slot number
        elif indextype =='spss':
            self.index = index
        else:
            raise ValueError

    #  originally, repr displayed the variable index.  Changed to display variable name
    # To get the original behavior, uncomment the line below and comment out the one
    # following.
    def __repr__(self):
        #return str(self.index)
        return self.dict.VariableName(self.index)
    
    def __eq__(self, other):
        """Return True if self and other have the same variable name."""
        #return self.dict.VariableName(self.index) == other.dict.VariableName(other.index)
        #return str(self) == str(other)
        return self.__str__() == other.__str__()
    
    def __ne__(self, other):
        """Return True if self and other have different variable names"""
        #return str(self) != str(other)
        return self.__str__() != other.__str__()
    
    def __hash__(self):
        """Implement this function so that set operations will work as expected."""
    
        return hash(self.__str__())  # ought to be equivalent to line below
        ###return hash(str(self))
    
    def _VN(self):
        "returns the name of the variable"
        return self.dict.VariableName(self.index)
    def _VI(self):
        return self.dict.VariableIndex(self.index)
    def __int__(self):      #so int(variable) will work
        return self.dict.VariableIndex(self.index)
    def __str__(self):     #for str(variable)
        return self.dict.VariableName(self.index)
    def _VarL(self):
        return self.dict.VariableLabel(self.index)
    def _VarLSet(self, value):
        "sets the variable label.  value is the string to be used as the label"
        spss.Submit("VARIABLE LABELS " + spss.GetVariableName(self.index) + " " + _smartquote(value) )
    def _VarLevel(self):
        return self.dict.VariableLevel(self.index)
    def _VarLevelSet(self, value):
        "sets the measurement level for the variable.  value must be nominal, ordinal, or scale"
        spss.Submit("VARIABLE LEVEL " + spss.GetVariableName(self.index) + " (" + value + ").")
    def _VarType(self):
        return self.dict.VariableType(self.index)
    def _VarFmt(self):
        return self.dict.VariableFormat(self.index)
    def _VarFmtSet(self, value):
        "set the variable format. value is an SPSS format specification"
        spss.Submit("FORMAT " + spss.GetVariableName(self.index) + " (" + value + ").")
    def _ValLab(self):
        return self.dict.ValueLabels(self.index)
    def _ValLab2(self):
        return self.dict.ValueLabelsTyped(self.index)

    def _ValLabSet(self, vldict):
        """set the value labels for the variable.  vldict is a dictionary of values and their labels.
        Existing labels are replaced."""
        
        # must be very careful with unicode vs str here
        ###vllist = " ".join([_smartquote(str(k)) + " " + _smartquote(str(v)) for k, v in vldict.items()])
        vllist = " ".join([_usmartquote(k) + " " + _usmartquote(v) for k, v in vldict.items()])
        ###spss.Submit("VALUE LABELS " + spss.GetVariableName(self.index) + " " + vllist)
        spss.Submit("VALUE LABELS " + self.VariableName + " " + vllist)
    def _Attr(self):
        return self.dict.Attributes(self.index)
    def _AttrSet(self, attrdict):
        """set the attributes according to attrdict, using keys as names and values as values.  Unmentioned
        attributes are not affected."""
        attrlist = " ".join([k + "(" + _smartquote(str(v))+ ")" for k, v in attrdict.items()])
        spss.Submit("VARIABLE ATTRIBUTE VARIABLES=" +  spss.GetVariableName(self.index) + \
                    " ATTRIBUTE=" + attrlist)
    def _MV(self):
        return self.dict.MissingValues(self.index)
    def _MV2(self):
        return self.dict.MissingValues2(self.index)
    def _MVSet(self, mlist):
        """set the missing value(s) for the variable.  The low, high, and thru keywords are valid only for numeric variables."""
        
        if spss.GetVariableType(self.index) == 0:   #numeric
            mlist = " ".join([str(m) for m in mlist])
        else:
            mlist = " ".join([_smartquote(v) for v in mlist])
        spss.Submit("MISSING VALUES " + spss.GetVariableName(self.index) + " (" + mlist + ").")

    VariableName = property(_VN)
    VariableIndex = property(_VI)
    VariableLabel = property(_VarL, _VarLSet)
    VariableLevel = property(_VarLevel, _VarLevelSet)
    VariableType = property(_VarType)
    VariableFormat = property(_VarFmt, _VarFmtSet)
    ValueLabels = property(_ValLab, _ValLabSet)
    ValueLabelsTyped = property(_ValLab2)
    Attributes = property(_Attr, _AttrSet)
    MissingValues = property(_MV, _MVSet)
    MissingValues2 = property(_MV2)

class CasingDict(dict):
    """A dictionary class where the keys need not be case sensitive."""
    def __init__(self, contents=None, caseless=True):
        """Create a dictionary using the usual dictionary constructors but provide case-insensitive
        retrieval if caseless is True.  Keys returned maintain original case.
        If case insensitive, an extra dictionary carrying the original casing is generated.
        
        contents optionally supplies the dictionary contents as a regular dictionary or
        other dictionary initializer other than keyword arguments.
        ** keys must have a lower method. **
        caseless defaults to True, which makes retrieval case insensitive but returns the case-preserved key.
        If false, operates as a standard dictionary."""

        self.origcase = {}
        self.caseless = caseless
        if contents:
            # Doesn't do keyword args
            if isinstance(contents, dict):
                for k,v in contents.items():
                    k1 = k.lower()
                    if caseless:
                        dict.__setitem__(self, k1, v)
                        self.origcase[k1] = k
                    else:
                        dict.__setitem__(self, k, v)
            else:
                for k,v in contents:
                    k1 = k.lower()
                    if caseless:
                        dict.__setitem__(self, k1, v)
                        self.origcase[k1] = k
                    else:
                        dict.__setitem__(self, k, v)
                        
    def keys(self):
        "Return case-preserving keys if caseless==True else regular"
        if self.caseless:
            return self.origcase.values()
        else:
            return dict.keys(self)
    
    def items(self):
        """Return dictionary items with original-case keys if caseless=True"""
        
        if self.caseless:
            return [(self.origcase[k], self.__getitem__(k)) for k in self]
        else:
            return dict.items(self)

    def __getitem__(self, key):
        if self.caseless:
            key = key.lower()
        return dict.__getitem__(self,key)

    def __setitem__(self, key, value):
        if self.caseless:
            k1 = key.lower()
            dict.__setitem__(self, k1, value)
            self.origcase[k1] = key
        else:
            dict.__setitem__(self, key, value)

    def __contains__(self, key):
        if self.caseless:
            return dict.__contains__(self, key.lower())
        else:
            return dict.__contains__(self, key)

    def has_key(self, key):
        if self.caseless:
            return dict.has_key(self, key.lower())
        else:
            return dict.has_key(self, key)
        
    def get(self, key, def_val=None):
        if self.caseless:
            return dict.get(self, key.lower(), def_val)
        else:
            return dict.get(self, key, def_val)

    def setdefault(self, key, def_val=None):
        if self.caseless:
            return dict.setdefault(self, key.lower(), def_val)
        else:
            return dict.setdefault(self, key, def_val)

    def update(self, contents):
        for k,v in contents.items():
            if self.caseless:
                k1 = k.lower()
                dict.__setitem__(self, k1, v)
                self.origcase[k1] = k
            else:
                dict.__setitem__(self, k, v)

    def fromkeys(self, iterable, value=None):
        d = CasingDict(caseless = self.caseless)
        for k in iterable:
            if self.caseless:
                k1 = k.lower()
                dict.__setitem__(d, k1, value)
                d.origcase[k1] = k
            else:
                dict.__setitem__(d, k, value)
        return d
    
    def iteritems(self):
        if self.caseless:
            for k in self:
                yield (self.origcase[k], self[k])
        else:
            yield dict.iteritems(self)
    
    def iterkeys(self):
        if self.caseless:
            return self.origcase.itervalues()
        else:
            return dict.iterkeys(self)
                

    def pop(self, key, def_val=None):
        if self.caseless:
            k1 = key.lower()
            self.origcase.pop(k1)
            return dict.pop(self, k1, def_val)
        else:
            return dict.pop(self, key, def_val)
        
    def __delitem__(self, key):
        if self.caseless:
            k1 = key.lower()
            dict.__delitem__(self, k1)
            del self.origcase[k1]
        else:
            dict.__delitem__(self, key)

class VariableDict(object):
    """A Python dictionary indexed by variable name for use with the SPSS Variable Dictionary.
    
    The Python dictionary does not contain SPSS dictionary properties other than name and index.
    Other variable properties are retrieved dynamically when requested.

    Unlike the SPSS dictionary, variable names in this class are case sensitive (except for regular
    expression matches).
    
    If no argument is supplied, all variable names in the SPSS dictionary are indexed.
    If a list of names or indexes is supplied, only those variables are included.
    If pattern is supplied, the dictionary includes only the subset of variables with names
    matching the pattern.  The pattern is a regular expression that starts at the beginning of the name.
    Examples:
        r'age'  - any variables starting with age
        r'.*age'- any variable whose name contains age
        r'.*\d$' - any variable whose name ends in a digit
    Matches are case insensitive and pattern can be combined with namelists, in which case
    the match subsets the name list.
    If variableType ('numeric' or 'string') is specified, the dictionary is restricted to variables
    with that type.
    If variableLevel, which must be a list, ('nominal', 'ordinal', 'scale', 'unknown') is
    specified, only variables with any of those levels are included.
    These selection criteria can be combined.  They can also be used with
    the Variables method, which returns a list of variable names and the Indexes method, which
    returns a list of variable indexes in the SPSS dictionary.
    The class contains a property named variables (note lower case) that returns a list of all
    the variables in the object.
    
    If safe == True, each time a variable property is retrieved after the dictionary is created, the
    actual SPSS dictionary is checked to see if the index still refers to that variable, and KeyError
    is raised if it is not.

    The class includes iterator and subscripted access.
    Subscripts and iterative access go according to the variables in the object, but
    api access functions take SPSS dictionary slot numbers.  Subscripts can be variable names
    or numbers.
    
    See the Variable class for details on variable properties. Most properties and attributes can be
    retrieved, and those that are changeable can be changed by assigning to the property.
    
    This class includes methods for manipulating named datasets as well.
    """
    # The indexes in the Variable Dictionary refer to the index in the SPSS dictionary, not
    # the index within this class.  The keys are variable names, and the values are
    # SPSS dictionary slot numbers (which are needed for the spss dictionary apis).

    # The theory of this implementation is that if no variable list is given, the number
    # of variables may be very large and efficiency is important, but if a list is given,
    # the number of variables will rarely be very large, and efficiency is not critical.
    
    def __init__(self, namelist=None, safe=False, pattern=None, variableType=None, variableLevel=None, 
        dataset=None, caseless=False):
        """
        All arguments are optional.  All conditions on variables are ANDed together to determine what variables to include.
        
            namelist is a list of names or indexes.  Defaults to all variables.  It can also be a white-space-separated string of names or indexes.
            safe specifies whether or not check for whether variable names still correspond to slots when fetching properties.
            pattern is a regular expression used as a match on variable names
            variableType can be "numeric" or "string".
            variableLevel can be one or more of "nominal", "ordinal", "scale", and "unknown".
            dataset is the current name of the dataset.  Specifying it does NOT cause a name to be assigned.
            If caseless is True, variable references are not case sensitive, which implies some extra overhead.
        """
    
        match = makeVariableFilter(pattern, variableType, variableLevel)           
        allnames = [spss.GetVariableName(v) for v in range(spss.GetVariableCount())]
        self.keys = []
        namelist = _buildvarlist(namelist)  #convert a string of names into a sequence
        
        if namelist is None:   # selecting all variables
            #self.vdict = dict([(n.lower(), index) for index, n in enumerate(allnames) if match(index, n)])
            self.vdict = CasingDict([(n, index) for index, n in enumerate(allnames) if match(index, n)], caseless)
            if not match.noop: #build list only if subset
                self.keys = [index for index, name in enumerate(allnames) if self.vdict.get(name) is not None]
        elif isinstance(namelist[0], basestring):        #type(namelist[0]) is str:    # got list of names
            #self.vdict = dict([(n, index) for index, n in enumerate(allnames) if n in namelist and match(index, n)])
            if caseless:
                namelist = [v.lower() for v in namelist]
                self.vdict =CasingDict([(n, index) for index, n in enumerate(allnames) if n.lower() in namelist and match(index, n)], caseless)
            else:
                self.vdict =CasingDict([(n, index) for index, n in enumerate(allnames) if n in namelist and match(index, n)], caseless)
            for name in namelist:      # user order
                vnumber = self.vdict.get(name)  #no entry if failed match
                if vnumber is not None:
                    self.keys.append(vnumber)    #spss variable numbers
        else:                                # got list of indexes
            #self.vdict = dict([(n, index) for index, n in enumerate(allnames) if index in namelist and match(index, n)])
            self.vdict = CasingDict([(n, index) for index, n in enumerate(allnames) if index in namelist and match(index, n)], caseless)
            values = self.vdict.values()
            self.keys = [vnumber for vnumber in namelist if vnumber in values]        #spss variable numbers
        self.safe = safe
        self.numvars = len(self.vdict) 
        self.datasetname = dataset
            
    def __iter__(self):
        """generator to iterate over the variables in this dictionary.
        Returns an item with all the variable properties implemented in this class."""
        
        if self.numvars > 0 and not self.keys:
            for v in range(spss.GetVariableCount()):
                yield Variable(self, v, indextype='spss')
        else:
            for v in self.keys:
                yield Variable(self, v, indextype='spss')


    #subscripted access
    def __getitem__(self, index):
        if isinstance(index, basestring):
            try:
                return Variable(self, self.vdict[index], indextype='spss')
            except:
                raise ValueError, _msg10
        elif self.keys:
            return Variable(self, self.keys[index], indextype = 'spss')
        else:
            return Variable(self, index, indextype = 'spss')

    def __len__(self):
        return self.numvars
    
    def variableCount(self):
        "return the number of variables in this dictionary"
        return self.numvars
    
    #method renamed from variables to distinguish variables property from subset selection
    def variablesf(self, variableType=None, variableLevel=None, pattern=None):
        """return a list of the variables in this dictionary, optionally filtered by one or
        more of a type, level, or pattern specification."""
        
        match = makeVariableFilter(pattern, variableType, variableLevel)
        if match.noop:
            return self.vdict.keys()
        else:
            return [var for var in self.vdict.keys() if match(self.vdict[var], var)]
    #property - make complete variable list available as property
    variables = property(variablesf, None)
    
    def range(self, start=None, end=None, variableType=None, variableLevel=None, pattern=None):
        """return a list of variable names in this dictionary between start and end, inclusive in the order in this dictionary.
        
        start and end are variable names.  If either is omitted, the list extends to the first or last variable.
        variableType, variableLevel, and pattern can be used to filter the list.
        Omitting both returns all variables in dictionary order.
        If end precedes start, the returned list will be empty.
        Case is ignored in this function if this is a caseless dictionary.  The returned list is in true case."""
        
        match = makeVariableFilter(pattern, variableType, variableLevel)
        varlist = []
        if not start:
            start = self[0].VariableName
        if not end:
            end = self[self.numvars-1].VariableName
        if not (start in self.vdict and end in self.vdict):
            raise ValueError, _msg11
        fetching = False
        start = start.lower()
        end = end.lower()
        for v in self:
            vv = v.VariableName.lower()
            if vv == start:
                fetching = True
            if fetching and match(index=v.VariableIndex, name=v.VariableName):
                varlist.append(v.VariableName)
            if vv == end:
                break
        return varlist

    def expand(self, vlist):
        """return a validated variable list with TO and ALL expanded.
        
        vlist is the sequence or string of names to validate.  If a name is not found, a ValueError exception is raised with that name.
        An exception will also be raised for a malformed TO construct.
        The set of valid names consists of those in this VariableDict object.
        case is IGNORED here, unlike elsewhere in this class.
        The expanded list is returned in the case as given in the call or the lowercase names for expanded entries"""
        
        vlist = _buildvarlist(vlist)
        if vlist[0].lower() == "all":
            return self.variables
        # generate lower case variable list in SPSS dictionary order if not already available
        if not hasattr(self, "simplelist"):
            self.simplelist = [v.lower() for (v, l) in sorted(self.vdict.items(), key=operator.itemgetter(1))]
        resultlist = []
        try:
            for i, v in enumerate(vlist):
                if v.lower() in self.simplelist:
                    resultlist.append(v)
                elif v.lower() == "to":
                    start = self.simplelist.index(vlist[i-1].lower())+1
                    end = self.simplelist.index(vlist[i+1].lower())
                    if start > end:
                        continue
                    resultlist.extend(self.simplelist[start:end])
                else:
                    raise ValueError
        except:
            raise ValueError, _msg19 + v
        return resultlist
    
    def indexes(self, variableType=None, variableLevel=None, pattern=None):
        """return a list of the variable indexes in this dictionary, optionally filtered by one or
        more of a type, level, or pattern specification."""
        match = makeVariableFilter(pattern, variableType, variableLevel)
        if match.noop:
            return self.vdict.values()
        else:
            return [self.vdict[var] for var in self.vdict.keys() if match(self.vdict[var], var)]
        
    def variableIndex(self, id):
        "return the index in the SPSS dictionary of the variable with name or index id."
        # if varDict is safe, check that the named variable is still at the saved index value
        if isinstance(id, basestring):            #type(id) is str:
            res = self.vdict[id]
            if self.safe and id != spss.GetVariableName(res): 
                raise KeyError
        else:
            res = id
        
        return res

    def variableName(self, id=None):
        "return the name of the variable with name or index id."
        # admittedly pointless if id is in fact a name, but allows the class to support names and
        # indexes uniformly
        if id is None:
            return None
        return spss.GetVariableName(self.VariableIndex(id))

    def variableLabel(self, id):
        "return the label of the variable with name or index id."
        return spss.GetVariableLabel(self.VariableIndex(id))
        
    def variableLevel(self, id):
        "return the measurement level of the variable with name or index id."
        return spss.GetVariableMeasurementLevel(self.VariableIndex(id))

    def variableType(self, id):
        """return the type of the variable with name or index id.
        0 = numeric
        >0 = string of that length
        """
        return spss.GetVariableType(self.VariableIndex(id))
    
    def variableFormat(self, id):
        "return the format of the variable with name or index id."
        return spss.GetVariableFormat(self.VariableIndex(id))

    def valueLabels(self, id):
        "return the set of value labels of the variable with name or index id as a dictionary."
        return GetValueLabels(self.VariableIndex(id))
    
    def valueLabelsTyped(self, id):
        """return the set of value labels of the variable with name or index id as a dictionary.
        
        The values are converted to numbers for numeric variables"""
        return GetValueLabels(self.VariableIndex(id), matchtype=True)

    def attributes(self, id=None):
        """return a dictionary of attributes for variable or index id.  If id = None
        the datafile attributes are returned
        """
        return getAttributesDict(self.VariableName(id))

    def missingValues(self, id):
        "return a string listing the missing value codes for variable or index id"
        return getMissingValues(self.VariableIndex(id))
    
    def missingValues2(self, id):
        "return a 4-tuple of missing value codes for variable or index id"
        return getMissingValues2(id)
    
    def variableNamesFromLabel(self, label):
        """Return a list of variable names for variables that have as label the specified text.
        
        This may be useful when SPSS output returns a variable label when the name is neede.  For
        example, getSHOW('weight') returns the label of the weight variable.  Variable labels need
        not be unique, however.
        """
        return [name for (name, index) in self.vdict.items() if spss.GetVariableLabel(index) == label]
    
    def activate(self, window="ASIS"):
        """Activate this dataset.  T
        
        he datasetname must already have been specified.
        window can be specified as ASIS, the default, or FRONT to bring it to the front."""
        
        spss.Submit("DATASET ACTIVATE " + self.datasetname + " WINDOW="+window)
        
    def close(self):
        """Close the dataset."""
        spss.Submit("DATASET CLOSE " + self.datasetname)
        
    #VariableDict class
    VariableCount = variableCount
    Variables = variables
    Indexes = indexes
    VariableIndex = variableIndex
    VariableName = variableName
    VariableLabel = variableLabel
    VariableLevel = variableLevel
    VariableType = variableType
    VariableFormat = variableFormat
    ValueLabels = valueLabels
    ValueLabelsTyped = valueLabelsTyped
    Attributes = attributes
    MissingValues = missingValues
    MissingValues2 = missingValues2
    VariableNamesFromLabel = variableNamesFromLabel

def isDateVariable(var, varDict=None):
    """return True if var is an SPSS date variable.  
    
    That is, its format is any of
    DATE, ADATE, EDATE, JDATE, SDATE, QYR, MOYR, WKYR, or DATETIME.  These are the variables that
    can be converted to Python dates.  TIME, WKDAY, and MONTH
    formats cannot be converted to dates, because they do not represent a particular point in
    time and, hence, this function returns False for them.

    var may be an SPSS dictionary variable index, or a Variable reference from a VariableDict object.
    If a VariableDict object is supplied, var may be a string holding a variable name."""
    
    if isinstance(var, basestring):
        if varDict is None or not isinstance(varDict, VariableDict):
            raise Exception(_msg12)
        var = int(varDict[var])
    else:
        var = int(var)
    vfmt = spss.GetVariableFormat(var)
    return vfmt[:3] in ['DAT','ADA','EDA','JDA','SDA','QYR','MOY','WKY','DAT']

def makeVariableFilter(pattern=None, variableType=None, variableLevel=None):
    """Make a criterion closure function for selecting variables based on regular expressions over names,
    variable type, and variable level (a list).  
    
    Returns the function.  The indexes in this function refer to the SPSS dictionary."""

    if pattern:
        try:
            pat = re.compile(pattern, re.IGNORECASE)
        except:
            raise ValueError, _msg17 + pattern
    if variableType and not variableType in ['numeric', 'string']:
        raise ValueError, _msg13

    if variableLevel is not None:
        for vl in variableLevel:
            if not vl in ['nominal', 'ordinal', 'scale', 'unknown']:
                raise ValueError, _msg14

    def match(index=-1, name=None):
        """test closure.  name is the variable name, and index is the SPSS dictionary index.
        
        name is not required unless an re is used, and index is not required unless type or level is specified.
        noop attribute is True if match does nothing."""
        
        if variableType is not None:
            p = spss.GetVariableType(index)
            if (variableType == "numeric" and p > 0) or (variableType == "string" and p ==0):
                return False
        if variableLevel is not None:
            p = spss.GetVariableMeasurementLevel(index)
            if not p in variableLevel:
                return False
        if pattern and not pat.match(name):
            return False
        return True
    match.noop = pattern == None and variableType == None and variableLevel == None
    return match

def _getSPSSLocFromIni():
    "return None or the SPSS directory for the preferred SPSS version from the xd ini file."

    # Try to find the Python installation location and then the spssxdcfg.ini file
    # Use that to find the location of SPSS
    # This function is not needed in spss drives mode, but in xd, the
    # process executable will not indicate the SPSS location.
    # There are several variations in the location of the ini file in different SPSS versions
    # This code wil fail if Python not installed somewhere in .../Pythonxx (two or more x's)

    try:
        sitep = os.path.join(re.search(r".*python\d\d\d*", sys.executable, re.I).group(), "Lib","site-packages")
        try:
            spssdir = open(os.path.join(sitep, "spss.pth")).readline()[:-1]   # try to find specific spss dir via pth file
            spssdir = os.path.join(sitep, spssdir, "spss")
        except:
            spssdir = os.path.join(sitep, "spss")  # No pth file in oldest versions
        cfgfile = os.path.join(spssdir, "spssxdcfg.ini")
        cfg = ConfigParser.ConfigParser()
        cfg.read(os.path.join(spssdir, "spssxdcfg.ini"))
        return cfg.get("path", "spssxd_path")
    except:
        return None

def getVariableValues(varindex, missing=True):
    """Return a list of the values of the variable with index varindex as strings.  
    
    Raises exception if no nonsysmis values are found.
    If missing is True, user missing values are included; otherwise they are not.
    Note: if values are used to generate SPSS syntax and may contain quotes, be sure to handle
    them appropriately."""

    # spss module apis require simple int type    
    if isinstance(varindex, Variable): 
        varindex = varindex.VariableIndex

    varname = spss.GetVariableName(varindex)
    vartype = spss.GetVariableType(varindex)
    xptail, quot = vartype == 0 and ("@number", " ") or ("@string", "\"")
    if missing:
        xpath ="//pivotTable[@subType='Frequencies']/dimension/group//category/" + xptail
    else:
        xpath ="//pivotTable[@subType='Frequencies']/dimension/group/group//category/" + xptail

    tag, ignore = createXmlOutput("FREQUENCIES " + varname  +"/statistics none.")
    freqvalues = spss.EvaluateXPath(tag, '/outputTree',    xpath)
    spss.DeleteXPathHandle(tag)
    if len(freqvalues) == 0:
        raise Exception, _msg15
    return freqvalues                
    
# check value labels for uniqueness
def varsWithDuplicateLabels(vars):
    """Returns a dictionary where each SPSS variable with any duplicate value labels is the key,
    and the value for that key is the list of duplicates.  
    
    If a variable has no value labels, it has no duplicate values.
    vars can be an SPSS variable name (string), a list of names, or an spssaux VariableDict object.
    If a variable does not exist, an exception will be raised.  Variable names are not case
    sensitive.

    Example:
    vard = spssaux.VariableDict()
    d = spssaux.varsWithDuplicateLabels(vard)
    if d:
        print "Variables with Duplicate Value Labels"
        for var, values in d.items():
            print var, ":", values
    else:
        print "no duplicate value labels"
    """

    if isinstance(vars, VariableDict):
        vars = [v.VariableName for v in vars]
    elif isinstance(vars, basestring):
        vars = [vars]
    tag, err = createXmlOutput("DISPLAY DICT /VARIABLES = " + " ".join(vars),
        omsid='File Information')
    if err > 0:
        raise Exception, _msg16
    dupdict = {}
    #Xpath 1.0 does not include case conversion functions, so we have to match the actual Xpath names
    #Variables with no value labels do not show up in this table.
    xmlvarnames = spss.EvaluateXPath(tag, "/",
            "/outputTree/command/pivotTable[@subType='Variable Values']/dimension/group/@varName")  #get varnames w labels in XML case
    for v in xmlvarnames:
        valueLabels = spss.EvaluateXPath(tag, "/outputTree/command/pivotTable[@subType='Variable Values']",
        "dimension/group/category[@varName='%s']/@label" % v)
        d = _dups(valueLabels)
        if d:
            dupdict[v] = d

    spss.DeleteXPathHandle(tag)
    return dupdict

def _dups(vlist):
    """return a list of the values that occur more than once in the list vlist."""
    
    dupd = {}
    vdic = {}
    for v in vlist:
        if v in vdic:
            dupd[v] = None
        else:
            vdic[v] = None
    return list(dupd)


def _smartquote(s, qchar='"'):
    """ smartquote a string so that internal quotes are distinguished from surrounding
    quotes for SPSS and return that string with the surrounding quotes.  
    
    qchar is the character to use for surrounding quotes."""
    
    return qchar + s.replace(qchar, qchar+qchar) + qchar

def _usmartquote(s, qchar='"'):
    """ smartquote a string so that internal quotes are distinguished from surrounding
    quotes for SPSS and return that string with the surrounding quotes.
    if s is not text, convert to a string first but  not quoted
    
    qchar is the character to use for surrounding quotes."""
    if not isinstance(s, basestring):
        s = str(s)
        return s
    
    return qchar + s.replace(qchar, qchar+qchar) + qchar

def _listify(item):
    "Make item into a list but a string is a singleton"
    
    if isinstance(item, basestring):
        item = [item]
    else:
        item = list(item)
    return item

def createAttribute(varnames, attrname, attrvalue):
    """Create the scalar attribute attrname for the list of variables varnames with value attrvalue"""
    
    spss.Submit("VARIABLE ATTRIBUTE VARIABLES = " + varnames +\
                " ATTRIBUTE=" + attrname + "(" + _smartquote(str(attrvalue)) + ").")
    

def getSpssMajorVersion():
    "Return the major version number as an integer"
    
    return int(getSpssVersion().split(".")[0])

def _isseq(obj):
    """Return True if obj is a sequence, i.e., is iterable.
    
    Will be False if obj is a string or basic data type"""
    
    # differs from operator.isSequenceType() in being False for a string
    
    if isinstance(obj, basestring):
        return False
    else:
        try:
            iter(obj)
        except:
            return False
        return True
    
def deleteVars(varlist):
    """Delete the specified variables from the active dataset.
    
    varlist is a list of variable names to delete.
    If a variable in varlist does not exist, the delete is silently ignored."""
    
    # use a VariableDict object to silently eliminate variables that do not exist
    vard = VariableDict(namelist=varlist)
    if vard:
        spss.Submit("DELETE VARIABLES " + " ".join(vard.variables))
    
def _buildvarlist(arg):
    """return a list of (presumed) variable names or indexes.
    
    arg can be a sequence, including an spssaux VariableDict or a string of white-space or comma-separated names
    if arg is a string and its items can be converted to integers, the sequence is converted, but if any item cannot be
    converted, a list of strings is returned."""
    
    # sequences are not converted in order to preserve Variable objects
        
    if _isseq(arg) or arg is None or isinstance(arg, int):
        return arg
    else:
        arg = re.split("[ \t,\n]+", arg)
        try:
            numarg = [int(item) for item in arg if item != ""]  #if condition accounts for terminal blank
            return numarg
        except:
            return arg 
        
def getcleartblimit():
    """Save the traceback limit, if any, and suppress tracebacks"""

    global tracebacklimit
    try:
        tracebacklimit = sys.tracebacklimit
    except:
        tracebacklimit = None
    sys.tracebacklimit = 0
    
def restoretblimit():
    """Restore traceback limit to saved value, if any"""

    global tracebacklimit
    if tracebacklimit is None:
        if hasattr(sys, "tracebacklimit"):
            del sys.tracebacklimit
    else:
        sys.tracebacklimit = tracebacklimit
        
def u(txt):
    """Return txt as Unicode or unmodified according to the SPSS mode"""
    
    if not ok1600 or not isinstance(txt, str):
        return txt
    if spss.PyInvokeSpss.IsUTF8mode():
        if isinstance(txt, unicode):
            return txt
        else:
            return unicode(txt, "utf-8")
    else:
        return txt

ecutf8 = codecs.getencoder("utf_8")   # in Unicode mode, must figure var names in bytes of utf-8

def truncatestring(name, maxlength=64):
    """Return a name truncated to no more than maxlength BYTES.
    
    name is the candidate string
    maxlength is the maximum byte count allowed.  It must be a positive integer and defaults to 64,
    which is the maximum legal size for an SPSS variable name.
    
    If name is a (code page) string, truncation is straightforward.  If it is Unicode utf-8,
    the utf-8 byte representation must be used to figure this out but still truncate on a character
    boundary."""
    
    unicodemode = ok1600 and spss.PyInvokeSpss.IsUTF8mode()
    if not unicodemode:
        name =  name[:maxlength]
    else:
        newname = []
        nnlen = 0
        
        # In Unicode mode, length must be calculated in terms of utf-8 bytes
        for c in name:
            c8 = ecutf8(c)[0]   # one character in utf-8
            nnlen += len(c8)
            if nnlen <= maxlength:
                newname.append(c)
            else:
                break
        name = "".join(newname)
    # in 16.0.0, names cannot end in "_"
    #if name[-1] == "_":
    #    name = name[:-1]
    return name

class FileHandles(object):
    """manage and replace file handles in filespecs.
    
    For versions prior to 18, it will always be as if there are no handles defined as the necessary
    api is new in that version, but path separators will still be rationalized.
    """
    
    def __init__(self):
        """Get currently defined handles"""
        
        # If the api is available, make dictionary with handles in lower case and paths in canonical form, i.e.,
        # with the os-specific separator and no trailing separator
        # path separators are forced to the os setting
        if os.path.sep == "\\":
            ps = r"\\"
        else:
            ps = "/"
        try:
            self.fhdict = dict([(h.lower(), (re.sub(r"[\\/]", ps, spec.rstrip("\\/")), encoding))\
                for h, spec, encoding in spss.GetFileHandles()])
        except:
            self.fhdict = {}  # the api will fail prior to v 18
    
    def resolve(self, filespec):
        """Return filespec with file handle, if any, resolved to a regular filespec
        
        filespec is a file specification that may or may not start with a handle.
        The returned value will have os-specific path separators whether or not it
        contains a handle"""
        
        parts = re.split(r"[\\/]", filespec)
        # try to substitute the first part as if it is a handle
        parts[0] = self.fhdict.get(parts[0].lower(), (parts[0],))[0]
        return os.path.sep.join(parts)
    
    def getdef(self, handle):
        """Return duple of handle definition and encoding or None duple if not a handle
        
        handle is a possible file handle
        The return is (handle definition, encoding) or a None duple if this is not a known handle"""
        
        return self.fhdict.get(handle.lower(), (None, None))
    
    def createHandle(self, handle, spec, encoding=None):
        """Create a file handle and update the handle list accordingly
        
        handle is the name of the handle
        spec is the location specification, i.e., the /NAME value
        encoding optionally specifies the encoding according to the valid values in the FILE HANDLE syntax."""
        
        spec = re.sub(r"[\\/]", re.escape(os.path.sep), spec)   # clean up path separator
        cmd = """FILE HANDLE %(handle)s /NAME="%(spec)s" """ % locals()
        # Note the use of double quotes around the encoding name as there are some encodings that
        # contain a single quote in the name
        if encoding:
            cmd += ' /ENCODING="' + encoding + '"'
        spss.Submit(cmd)
        self.fhdict[handle.lower()] = (spec, encoding)


        

#aliases for original casing of names for compatibility
CreateXMLOutput = createXmlOutput
GetValuesFromXMLWorkspace = getValuesFromXmlWorkspace
CreateDatasetOutput = createDatasetOutput
GetVariableNamesList = getVariableNamesList
GetVariableFormatsList = getVariableFormatsList
GetVariableLabelsList = getVariableLabelsList
GetVariableMeasurementLevelsList = getVariableMeasurementLevelsList
GetVariableTypesList = getVariableTypesList
GetSHOW = getShow
GetProcessInstallDir = getProcessInstallDir
GetSPSSInstallDir = getSpssInstallDir
CreateFileHandle = createFileHandle
GetAttributesDict = getAttributesDict
GetDatasetInfo = getDatasetInfo
GetActiveDatasetName = getActiveDatasetName
GetValueLabels = getValueLabels
GetMissingValues = getMissingValues
GetMissingValues2 = getMissingValues2
OpenDataFile = openDataFile
OpenDataFileFromUrl = openDataFileFromUrl
SaveDataFile = saveDataFile

GetVariableValues = getVariableValues
VarsWithDuplicateLabels = varsWithDuplicateLabels
CreateAttribute = createAttribute
GetSPSSVersion = getSpssVersion
GetSPSSMajorVersion = getSpssMajorVersion
DeleteVars = deleteVars
