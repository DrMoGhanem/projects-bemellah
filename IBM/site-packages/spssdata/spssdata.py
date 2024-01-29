"This module manages SPSS database functions at a higher level than the SPSS module"

#Licensed Materials - Property of IBM
#IBM SPSS Products: Statistics General
#(c) Copyright IBM Corp. 2005, 2011
#US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

# All messages for this module are collected here for translation purposes.  Docstrings, however, are not.
# To translate, duplicate the message block and translate the later copy, maintaining the assignment syntax.
# The original can be commented out, but it will be replaced by the later version anyway, so this is not necessary.
# Maintaining the original English text will make it easier to update translations later.
# Place the translated block after all the English messages in order to facilitate checking for changes in the English text.

_msg1 = "Warning: this module requires at least spssaux version "
_msg2 = "Measurement level must be nominal, ordinal, or scale"
_msg3 = "Variable format type  is invalid: "
_msg4 = "attrib parameter must be a dictionary or similar object type"
_msg5 = "Invalid accessType: "
_msg6 = "Cannot access data because active dataset is empty"
_msg7 = "accessType n cannot be combined with indexes or cvtDates"
_msg8 = "Indexes and cvtDates arguments must be a sequence of variable names or numbers or a VariableDict: "
_msg9 = "cvtDates must be subset of the index list"
_msg10 = "w,  a, and n data access require at least SPSS 15"
_msg11 = "convertUserMissing = False requires at least SPSS 15.0"
_msg12 = "makemvchecker cannot be used until dictionary is committed"
_msg13 = "Missing value checking requires at least SPSS 15"
_msg14 = "append is only available for accessType='w' and 'n'"
_msg15 = "casevalues is only available for accessType='w'"
_msg16 = "setvalue is only available for accessType w"
_msg17 = "appendvalue is only available for accessType='a'"
_msg18 = "Invalid variable name, variable index, or variable value specified: "
_msg19 = "CommitCase is only available for accessTypes a and w"
_msg20 = "Only three missing values can be defined for a variable."
_msg21 = "Invalid missing value range specification"
_msg22 = "IsStartSplit is only available for accessType = 'r' or 'w'"
_msg23 = "Cannot check for missing values.  makemvchecker must be called first."
_msg24 = "ismissing: The specified variable name or index is not in the cursor"
_msg25 = "fetchone cannot be used with accessType: "
_msg26 = "Only one VariableDict can be used in the index list"
_msg27 = "A cursor request specified an undefined variable"
_msg28 = "Unconvertible datetime value"
_msg29 = "date specification must include at least (yyyy, mm, dd) but not more than six parts"


# copyright(c) SPSS Inc, 2005
# history
# 2005-oct-19 initial version
# 2005-nov-04 integrate optional date conversion into fetching
# 2006-feb-25 make cvtDates work when index is zero
# 2006-mar-28 Dataset class, dataset parameter in Spssdata class
#2006-aug-14  Add ismissing to test for missing value.  Requires SPSS 15 structure for mvs
#2006-aug-28 Add support for write and append cursors for SPSS 15
#2006-sep-22 Adjustments for write cursor
#2006-sep-25 Add methods for append cursor
#2006-oct-10 Allow Spssdata to accept string lists of indexes
#2006-oct-20 Implement Spssdata convertUserMissing parameter
#2006-nov-01 Add accessType='n' to Spssdata class to allow creating new datasets from scratch
#2006-nov-09 Validate THRU missing value specification
#2008-feb-11 Spssdata class now obeys contexthandler so it can be used in a with statement
#2008-jun-27 Generalize yrmodasec to allow time portions

__author__  =  'spss'
__version__ =  '2.2.0'

import spss, spssaux, namedtuple
import datetime

minver = [2, 0, 1]
if [int(v) for v in spssaux.__version__.split(".")] < minver:
    raise ImportError, _msg1 + ".".join([str(item) for item in minver])

spssver = [int(v) for v in spssaux.GetSPSSVersion().split(".")]
ok1500 = spssver >= [15, 0, 0]
ok1501 = spssver >= [15, 0, 1]
ok1600 = spssver >= [16,0,0]


if ok1500:
    spsslow, spsshigh = spss.GetSPSSLowHigh()

def vdef(vname, vtype=None, vlabel=None, vmeasurelevel=None, vfmt=None, valuelabels=None, missingvalues=None, attrib=None):
    """helper function for defining new variables when Spssdata cursor has accessType='w'.
    
    Returns a tuple of all the variable attributes, making it easy to supply only nondefault values.
    The tuple is of the form expected by Spssdata.commit.
    The variable may be appened more than once with subsets of properties in each append.  They will be merged, with
    the last one winning in case of conflicts.
    
    vname is the variable name.  It is the only required parameter.
    vtype is the numerical type code, default is numeric (0) if nothing is specified before the dictionary is committed.
    vlabel is the variable label, if any.
    vmeasurelevel = 'nominal','ordinal' or 'scale'.  Default is SPSS default according to type.
    vfmt = variable format as a sequence of type, width, optional decimals.  See varfmts list below for types.
    valuelabels is a dictionary of values and labels.
    missingvalues is a user missing value specification tuple.
    It can be a 4-tuple matching the definition for spss.GetVarMissingValues, or it can be a list of up to three
    missing values or it can include "THRU" in the list to indicate a range, and, optionally a third value.
    Examples: [9, "THRU", 99], [99,98,97], [9, "THRU", 99]
    Ranges are only available for numeric variables.
    If used, the range specification must precede the singleton missing value: [99, 999, "THRU", 9999] is invalid.
    attrib is a dictionary of attributes and their values
    """
    try:
        if vmeasurelevel:
            ml = ['nominal', 'ordinal', 'scale'].index(vmeasurelevel) + 2
        else:
            ml = None
    except:
        raise AttributeError, _msg2
    try:
        if vfmt:
            fmtspec = [varfmts[vfmt[0].upper()]]
            fmtspec.extend(vfmt[1:])
            if len(fmtspec) < 3:
                fmtspec.append(None)
            vfmt = fmtspec
    except:
        raise KeyError, _msg3 + str(vfmt[0])
    if attrib and not spssaux._isseq(attrib):
        raise AttributeError, _msg4
    return (vname, vtype, vlabel, ml, vfmt, valuelabels, missingvalues, attrib)

varfmts = dict(
    [("A",1),
    ("AHEX",2),
    ("COMMA",3),
    ("DOLLAR",4),
    ("F",5),
    ("N",16),
    ("E",17),
    ("DATE",20),
    ("TIME",21),
    ("DATETIME",22),
    ("ADATE",23),
    ("JDATE",24),
    ("DTIME",25),
    ("MONTH",26),
    ("MOYR",27),
    ("QYR",28),
    ("WKYR",29),
    ("PCT",30),
    ("DOT",31),
    ("CCA",32),
    ("CCB",33),
    ("CCC",34),
    ("CCD",35),
    ("CCE",36),
    ("EDATE",37),
    ("SDATE",38)])

# format numbers where decimals can be specified
vardecimalsallowed = set([3,4,5,16,17,21, 22,25,30,31,32,33,34,35,36])
# for reverse lookups when creating data definitions via syntax
varfmtsrev = dict([(v, k) for k, v in varfmts.iteritems()])

varlevels = {2: "Nominal", 3: "Ordinal", 4: "Scale"}


def _fmtmap(fmt, width, decimals=0):
    """convert a format specification into an SPSS format spec, which is returned.
    
    fmt is a format type code in varfmts.
    width is the field width.
    decimal is the number of decimals (gnored for non-numeric formats)."""
    
    res = varfmtsrev[fmt] + str(width)
    if fmt in vardecimalsallowed and not decimals is None:
        res += "." + str(decimals)
    return res

class Spssdata(object):
    """Spssdata manages the active SPSS dataset retrievals at a higher level than
    in the spss module.
    
    Spssdata can be used as a context handler supporting the with statement available with Python 2.5.
    Example:
    from __future__ import with_statement
    import spss, spssdata
    with spssdata.Spssdata(indexes=[0]) as curs:
      for case in curs:
        print case
      z = case[0]/0
  
  This usage ensures that the cursor is properly closed at the end of the with whether an exception occurs (forced in this example), or not.
  """
    def __init__(self, indexes=(), names=True, cvtDates=(), dataset=None, omitmissing=False, convertUserMissing=True,
                 accessType='r', maxaddbuffer=80):
        """Create new cursor to active data.  
        
        Indexes can be a sequence of variable names or index numbers or omitted or () or "ALL" for
        all. Indexes can also be a string of names or index numbers separated by white space and/or
        commas. The index entries must all be the same type. Invalid variable names or out of range
        numbers will raise an exception either in the constructor when cases are fetched.
        
        names == True causes NamedTuples to be produced.  If false, standard tuples are returned.
        If names, the items in the index list must not contain any duplicates.
        If omitmissing is True (requires at least SPSS 15), then any case where any of the selected variables
        is user or system missing is not returned.  If missing values need to be checked but the cases returned
        anyway, use method makemvchecker to create a checking function and call it on the case with the ismissing method.
        For example,
          curs = spssdata.Spssdata(indexes=['mpg','year','accel'], convertUserMissing=False)
          curs.makemvchecker()
          curs.ismissing("year", 0)
          or
          curs.ismissing(1, 0)
          would return True if 0 is defined as a missing value for variable "year"
          Method hasmissing can be used to check the entire variable list at once.
          
        This module also contains a function ismissing (not part of this class) that can be used independently of the cursor.
        
        If convertUserMissing is True, user missing values are converted to None.
        
        If convertUserMissing is False and this is at least SPSS 15, user missing values are returned
        as is. If this is version 14, an exception is raised. convertUserMissing is irrelevant, of
        course, if omitmissing is True.
        
        If some of the variables retrieved are SPSS date/time variables they can be
        converted to Python datetime objects by listing them in cvtDates.  Otherwise
        the values are the SPSS datetime values.
        cvtDates accepts the same types of values as indexes, but an empty sequence means convert
        no dates, and "ALL" refers to all the variables in indexes.
        cvtDates should be a subset of indexes.
        If dataset is specified, that name is activated before creating the cursor.  If the current dataset
        has no name, it will be lost when the new one is activated.  The dataset parameter cannot be used between
        spss.StartProcedure and spss.EndProcedure
        accessType can be 'r', 'w', or 'a' for read (the default), write, or append access.  w and a require at least SPSS 15.
        
        For accessType w, use append to define a new variable, commitdict to commit the dictionary
        and start setting values, and casevalues to set the new values. Use CClose to close the
        cursor.
        
        For accessType a, use appendvalues to set the values of variables in a new case and
        CommitCase to finish that case. Use CClose to end the appends.
        
        If accessType='w' or will be 'w' within the current procedure and it is SPSS 15.0.1 or later,
        maxaddbuffer can be specified to allocate space for new variables. It will be added to the space
        required by appended variables with at least room for ten more numeric variables (on a future
        pass). If the new variables are appended on the first pass, there is no need to specify this
        parameter.
        
        To create an entirely new dataset (which will automatically close the active dataset if it
        does not have a dataset name), set accessType='n'. This will create the dataset definition
        using syntax and then change to append mode for adding the cases. """

        if not accessType in ["r", "w", "a", "n"]:
            raise ValueError, _msg5 + str(accessType)
        if accessType != 'n' and spss.GetVariableCount() == 0:
            raise ValueError, _msg6
        if accessType == 'n' and (indexes or cvtDates):
            raise ValueError, _msg7
        indexes = spssaux._buildvarlist(indexes)
        cvtDates = spssaux._buildvarlist(cvtDates)
        self.maxaddbuffer = maxaddbuffer
        self.calledalloc = False  # some functions can be used only once with a given cursor
        self.omitmissing = omitmissing
        self.mvdata = []  # for use in checking for missing data
        self.accessType = accessType
        self.convertUserMissing = convertUserMissing
        if accessType in ['a', 'n']:
            self.omitmissing = False
            self.convertUserMissing = False
        self.newvars = []  #for new variable specifications in w mode
        self.cvtDateIndexes = []
        self.namelist = []
        self.first = True
        self.isendsplit = None   #split status is undefined until a case has been read.
        self.unicodemode = ok1600 and spss.PyInvokeSpss.IsUTF8mode()
        if self.unicodemode:
            self.unistr = unicode
        else:
            self.unistr = str
        
        if dataset and self.accessType != 'n':
            spss.Submit("DATASET ACTIVATE " + self.unistr(dataset))        
        for item in indexes, cvtDates:  # never executed for accessType='n'           
            if not spssaux._isseq(item):  #for clearer diagnosis of common errors
                raise TypeError, _msg8 +self.unistr( item)
        if not accessType == 'n':  # cannot use until variables are defined if new dataset
            self.indexes, self.namelist = _getIndexInfo(list(indexes), datelist=False)
            self.numvars = len(self.indexes)
        if cvtDates:
            self.cvtDateIndexes = _getIndexInfo(list(cvtDates), datelist=True)
            if cvtDates[0] == "ALL":
                self.cvtDateIndexes = [item for item in self.cvtDateIndexes if item in self.indexes]
            if not set(self.cvtDateIndexes).issubset(self.indexes):
                raise TypeError, _msg9

        #make date index list refer to positions in projected tuple of SPSS variables if there is a projection
        if cvtDates:
            self.cvtDateIndexes = [self.indexes.index(item) for item in self.cvtDateIndexes]

        if names:
            self.rettype = namedtuple.MakeNamedTuple('namedTuple', self.namelist)
        else:
            self.rettype = tuple
        if self.accessType == 'r':
            self.cur = spss.Cursor(self.indexes)
        elif not ok1500:
            raise AttributeError, _msg10
        elif accessType != 'n':
            self.cur = spss.Cursor(self.indexes, self.accessType)
        if self.omitmissing:
            self.makemvchecker()
        if accessType == "a":
            self.vartypes = [spss.GetVariableType(i) for i in self.indexes]
        if accessType not in ['n', 'a'] and not self.convertUserMissing:
            if not ok1500:
                raise ValueError, _msg11
            self.cur.SetUserMissingInclude(True) # do not convert user missing values to None

    def __enter__(self):
        """initialization for with statement"""
        return self
        
    def __exit__(self, type, value, tb):
        """cleanup for use with with statement"""
        self.CClose()
        return False

    def getvarindex(self, varname):
        """return index number for varname in current cursor.
        
        varname is the case-matching variable name.
        The return value is an index suitable for use with spss module functions.
        A ValueError exception is raised if the variable is not in the cursor."""
        
        return self.indexes[self.namelist.index(varname)]
    
    def makemvchecker(self):
        """Prepare missing list for checking variables in the cursor for user and system missing values"""
        
        if self.accessType == 'n':
            raise ValueError, _msg12
        # side effect is building a dict for quicker access to missing value information via ismissing method
        self.vardict = {}
        try:
            for cindex, i in enumerate(self.indexes):
                val = spss.GetVarMissingValues(i)
                trimval = []
                for i in range(len(val)):
                    if isinstance(val[i], basestring):
                        trimval.append(val[i].rstrip())
                    else:
                        trimval.append(val[i])
                self.mvdata.append(tuple(trimval))
                self.vardict[self.namelist[cindex]] = cindex
        except AttributeError:
            print _msg13
            raise
    
    def append(self, variablespec):
        """Append a specification for a new variable consisting of a tuple as defined in function vdef above.
        
        If a variable is appended more than once, the properties are merged.  The last ones win.
        The variable order will be based on the first mention of the name.
        This is only allowed with accessType='w'
        """
        if not self.accessType in ['w', 'n']:
            raise TypeError, _msg14
        
        if not spssaux._isseq(variablespec):
            variablespec = [variablespec]
        self.newvars.append(list(variablespec))            

    def commitdict(self):
        """Create any specified new variable definitions.
        
        Order the variables by earliest mention, but use the last mention of properties.
        Note that case matters even though SPSS itself does not care.
        
        If vdef was used to create the variable properties, the property set will always be full size.
        Short sequences could be appended directly, in which case the item order is expected to be
        the same as in vdef, and property assignment stops when it runs out of items.
        This is only allowed with accessType='w'"""
        
        if not self.accessType in ['w', 'n']:
            raise TypeError, "commitdict is only available for accessType='w' and 'n'"
        if self.newvars:
            names = [] ; types = [] 
            for item in self.newvars:
                try:
                    if item[4][0] < 3 and item[1] is None:  #A formats imply string type
                        item[1] = int(item[4][1])
                except:
                    pass
                if len(item) == 1:
                    item.append(0)
                elif item[1] is None:
                    item[1] = 0
                try:
                    index = names.index(item[0])
                    types[index] =  item[1]
                except:    # first mention of variable
                    names.append(item[0])
                    types.append(item[1])
                    
            #  Automatic allocation can only address the first pass of added variables
            #  The buffer needs 8 bytes per numeric variable and length rounded up to a multiple of 8 for string variables
            if not self.calledalloc:
                bufferalloc = 0
                for t in types:
                    if t == 0:  #numeric
                        bufferalloc += 8
                    else:
                        bufferalloc += int((t+7)//8)*8
                self._bufferalloc(bufferalloc)
            self._SetVarNameAndType(names, types)


            for item in self.newvars:
                try:
                    if item[2]:  # variable label
                        self._SetVarLabel(item[0], item[2])
                    if item[3]:
                        self._SetVarMeasureLevel(item[0], item[3])
                    if item[4]:  # variable format
                        width = item[4][1] or item[1] # strings might not have a width in the format spec
                        decimals = None
                        if len(item[4]) > 2:
                            decimals = item[4][2]
                        self._SetVarFormat(item[0], item[4][0], width, decimals)
                    if item[5]:   # value labels
                        self._SetVarValueLabels(item[0], item[1], item[5])
                    if item[6]:  # missing values
                        self._SetVarMissingValues(item[0], item[1], item[6])
                    if item[7]:   #attributes
                        self._SetVarAttributes(item[0], item[7])
                except IndexError:   #allow list of attributes to be incomplete
                    pass
            self._CommitDictionary()
            
    def casevalues(self, valuelist):
        """Assign values to new variables in current case and commit it.
        
        With a write cursor, valuelist is a sequence of values, one for each new variable in the order appended.  
        If the list is shorter than the number of variables the extra variables will be sysmis.  Excess values will raise an exception."""
        
        # A user could have a write cursor but not have created new variables on the first pass, but buffer allocation must happen
        # anyway, so it is called here even though it would seem not to be needed.
        
        if self.accessType != 'w':
            raise TypeError, _msg15
        else:
            self._bufferalloc()
        
        for i, v in enumerate(valuelist):
            if len(self.newvars[i]) == 1 or not self.newvars[i][1] :   #numeric (0 or None)
                if not v is None:
                    v = float(v)
                self.cur.SetValueNumeric(self.newvars[i][0], v)
            else:
                if self.unicodemode:
                    v = unicode(v)
                self.cur.SetValueChar(self.newvars[i][0], self.unistr(v))
        self.cur.CommitCase()
        
    def setvalue(self, var, value):
        """Set the value of a variable for the current case with accessType w.  Case must be explicitly commited if this method is used.
        
        var is the name of the new value whose value is to be set.
        value is the value to set.
        ValueError will be raised if var is not a new variable name or the value type is inappropriate."""
        
        if not self.accessType == 'w':
            raise ValueError, _msg16
        index = [varspec[0] for varspec in  self.newvars].index(var)
        if len(self.newvars[index]) == 1 or not self.newvars[index][1]:  #numeric variable
            if not value is None:
                value = float(value)
            self.cur.SetValueNumeric(var, value)
        else:
            self.cur.SetValueChar(var, self.unistr(value))

        
    def appendvalue(self, var, value):
        """Append a value in the current new case for the specified variable.
        
        var is the variable name or variable index in the SPSS dictionary (as used in the constructor).
        value is the value to assign to the case.
        call CommitCase on the cursor to add the case to the dataset.
        If varname/varindex is not in the current cursor, an exception will be raised.
        """
        if self.accessType != 'a':
            raise ValueError, _msg17
        
        try:
            spssindex = int(var)
            var = self.namelist[self.indexes.index(spssindex)]  #convert SPSS index to name
        except:  #not numeric, assume it is a name
            pass
        try:
            if self.vartypes[self.namelist.index(var)] == 0:  #numeric
                self.cur.SetValueNumeric(var, value)
            else:
                self.cur.SetValueChar(var, value)
        except:
            raise ValueError, _msg18 + str(var)
        
    def CommitCase(self):
        """Commit the current case.
        
        This api is only intended for use with accessType append or with write after setting the case values."""
        
        # simply a passthrough to lower-level method
        if self.accessType == 'r':
            raise TypeError, _msg19
        else:
            self._bufferalloc()
        self.cur.CommitCase()

    def CClose(self):
        "Close the cursor after commiting cases"
        if self.accessType == 'a':
            try:
                self.cur.EndChanges()
            except:
                pass
        self.cur.close()
        del self.cur

    def _SetVarNameAndType(self, names, types):
        """Create variables with specified names and types.
        
        names is a sequence of names and types is a corresponding sequence of types.
        With a write cursor, use the Cursor.  With a new cursor, use syntax."""
        
        if self.accessType == 'w':
            self.cur.SetVarNameAndType(names, types)
        else:
            cmd = []
            for name, vtype in zip(names, types):
                if vtype == 0:
                    vt = "F8.2"
                else:
                    vt = "A" + str(vtype)
                cmd.append(name + " (" + vt + ")" )
            spss.Submit("DATA LIST NOTABLE/" + " ".join(cmd))
            self.indexes, self.namelist = _getIndexInfo([], datelist=False) #fetch all variables
            self.numvars = len(self.indexes)

    def _SetVarLabel(self, name, label):
        if self.accessType == 'w':
            self.cur.SetVarLabel(name, label)
        else:
            spss.Submit("VARIABLE LABEL " + name + " " + spssaux._smartquote(label))
            
    def _SetVarMeasureLevel(self, name, level):
        if self.accessType == 'w':
            self.cur.SetVarMeasureLevel(name, level)
        else:
            spss.Submit("VARIABLE LEVEL " + name + " (" + varlevels[level] + ")")
            
    def _SetVarFormat(self, name, fmt, width, decimals):
        if self.accessType == 'w':
            self.cur.SetVarFormat(name, fmt, width, decimals)
        else:
            spss.Submit("FORMATS " + name + "(" + _fmtmap(fmt, width, decimals) +")")
    
    def _SetVarValueLabels(self, name, vtype, labels):
        if self.accessType == 'w':
            for value, label in labels.iteritems():
                if not vtype:  #numeric (code of 0 or None)
                    self.cur.SetVarNValueLabel(name, float(value), str(label))
                else:
                    self.cur.SetVarCValueLabel(name, str(value), str(label))
        else:
            cmd = []
            for value, label in labels.iteritems():
                cmd.append(vtype and spssaux._smartquote(str(value)) or str(value) + " " + spssaux._smartquote(label))
            spss.Submit("VALUE LABELS " + name + " " + " ".join(cmd))

    def _SetVarMissingValues(self, name, vtype, mvtuple):
        if len(mvtuple) > 4:
            raise ValueError, _msg20
        # if variable is numeric, look for THRU to indicate a range spec
        # alternatively, if THRU is not present and the tuple is full length (4), assume type code is included.  Otherwise prefix with type 0
        # if variable is string and first element is not integer, prefix with type 0
        
        if vtype == 0:  #numeric?
            try:
                thruindex = list(mvtuple).index("THRU")   # range mv's?
                if thruindex != 1:
                    raise IndexError
                mvtuple = mvtuple[:thruindex] + mvtuple[thruindex+1:]
                mvtuple = (len(mvtuple) < 3 and 1 or 2,) + tuple(mvtuple)
            except IndexError:
                raise ValueError, _msg21
            except:
                if len(mvtuple) < 4:
                    mvtuple = (0,) + tuple(mvtuple)
        else:
            if not isinstance(mvtuple[0], int):
                mvtuple = (0,) + tuple(mvtuple)

        if self.accessType == 'w':
            mvtuple = tuple(mvtuple) + (None, None, None)  #user spec could be short
            if vtype == 0:
                self.cur.SetVarNMissingValues(name, mvtuple[0], mvtuple[1], mvtuple[2], mvtuple[3])
            else:
                self.cur.SetVarCMissingValues(name, mvtuple[1], mvtuple[2], mvtuple[3])
        else:
            if vtype == 0:
                mvspec = []
                for i in range(1, len(mvtuple)):
                    if mvtuple[i] == spsslow:
                        mvspec.append("LOWEST")
                    elif mvtuple[i] == spsshigh:
                        mvspec.append("HIGHEST")
                    elif not mvtuple[i] is None:
                        mvspec.append(str(mvtuple[i]))
                if mvtuple[0] > 0:  # range spec (only applies to numeric variables)
                    mvspec = " ".join(mvspec[:1] + ["THRU"] + mvspec[1:])
                else:
                    mvspec = " ".join(mvspec)
            else:
                mvspec = " ".join([spssaux._smartquote(item) for item in mvtuple[1:] if item is not None])
            if mvspec:
                spss.Submit("MISSING VALUES " + name + " (" + mvspec + ")")
                
    def _SetVarAttributes(self, name, attrs):
        if self.accessType == 'w':
            for key, value in attrs.iteritems():
                self.cur.SetVarAttributes(name, key, value, 0)
        else:
            cmd = []
            for key, value in attrs.iteritems():
                cmd.append(key + "(" + spssaux._smartquote(value) + ")")
            spss.Submit("VARIABLE ATTRIBUTE VARIABLES = " + name + " ATTRIBUTE = " + " ".join(cmd))
            
    def _CommitDictionary(self):
        if self.accessType == 'w':
            self.cur.CommitDictionary()
        else:
            self.accessType = 'a'
            self.cur = spss.Cursor(self.indexes, self.accessType)
            self.vartypes = [spss.GetVariableType(i) for i in self.indexes]
            
    def _dateconverter(self, row):
        """convert any values in row specified in cvtDates to Python date values."""
        if not self.cvtDateIndexes:
            return row
        if isinstance(row[self.cvtDateIndexes[0]], datetime.datetime):  #already converted?
            return row
        row = list(row)
        for index in self.cvtDateIndexes:
            row[index] = CvtSpssDatetime(row[index])
        return tuple(row)
            
    
    def fetchone(self):
        """Return the next case from the active dataset.  If omitmissing, return the next case without missing data.
        Note that missing data can cause EOFError to be raised.  Iterators will want to trap this.
        
        If split files is active, IsStartSplit can be called to determine a split boundary."""
        
        self._bufferalloc()
        if not self.accessType in ['r', 'w']:
            raise AttributeError, "fetchone cannot be used with accessType " + self.accessType
        if self.first:
            self.isendsplit = ok1500 and True  # split tracking only available in SPSS 15+
            self.first = False
        else:
            self.isendsplit = False
        while True:
            row = self.cur.fetchone()
            if row is None and ok1500 and self.cur.IsEndSplit():
                self.isendsplit = True
                row = self.cur.fetchone()   # in case split file processing is active
            if row is None:
                raise EOFError
            if self.omitmissing and self.hasmissing(row):
                continue
            return self.rettype(self._dateconverter(row))  # makes named or plain tuple
        
    def IsStartSplit(self):
        """Return True or False according to whether the cursor has crossed a split boundary.
        
        If no cases have been read or fetchall is used, the state is indeterminate, and None is returned.
        This function always returns False prior to SPSS 15 as the underlying support was introduced in that release."""
        
        if not self.accessType in ['r', 'w']:
            raise AttributeError, _msg22
        return ok1500 and self.isendsplit
        
    
    def hasmissing(self, row):
        """Return True if any variable value in current row is user or system missing"""
        
        if self.mvdata == []:
            raise AttributeError, _msg23
        for i in range(self.numvars):
            if ismissing(row[i], self.mvdata[i]):
                return True
        return False
    
    def ismissing(self, var, value):
        """Return True or False according to whether value is a missing value for the variable var in the current cursor.
        
        var is a variable name or index in the cursor.
        value is the value to check.
        makemvchecker must have been called on the cursor in order to use this method."""
        if self.mvdata == []:
            raise AttributeError, _msg23
        try:
            if isinstance(var, basestring):
                var = self.vardict[var]  # convert name to index
            return ismissing(value, self.mvdata[var])
        except:
            raise ValueError, _msg24
    
    def __iter__(self):
        """generator to iterate over all remaining cases in the active dataset."""
        while True:
            try:
                row = self.fetchone()
            except EOFError:
                raise StopIteration
            if not row:
                raise StopIteration
            else:
                yield self.rettype(self._dateconverter(row))
                
    def __del__(self):
        """make sure cursor is closed when the object is deleted."""
        try:
            self.CClose()
        except:
            pass

    def fetchall(self):
        """Fetch all rows of data.  Return a list of tuples or named tuples.
        Omit cases with missing data if constructor specified omitmissing.
        
        If split files is active, fetchall returns all cases in the current split only.  IsStartSplit can be
        used to monitor splits."""
        
        if not self.accessType in ['r', 'w']:
            raise AttributeError, _msg25 + self.accessType
        self.first = False
        self._bufferalloc()
        rows = self.cur.fetchall()
        self.isendsplit = ok1500 and self.cur.IsEndSplit()
        if self.rettype != tuple or self.omitmissing or self.cvtDateIndexes:
            rows = [self.rettype(self._dateconverter(row)) for row in rows if not (self.omitmissing and self.hasmissing(row))]
        return rows
        

    def close(self):
        self.cur.close()
        del self.cur

    def restart(self):
        """Reset the open cursor to the same set of variables for another data pass.
        
        In append mode, any appended cases are committed before the reset."""
        
        if self.accessType == 'a':
            try:
                self.cur.EndChanges()
            except:
                pass
        self.cur.reset()
        self.newvars = []  # any previously added variables are now old
        self.first = True
        self.isendsplit = None

    def varnames(self):
        """Return a list of the variable names being fetched for the cursor."""
        
        return self.namelist
    
    def _bufferalloc(self, extra=0):
        """Ensure that buffer for new variables has been set if in write mode.
        
        self.maxaddbuffer is padding.  extra specifies a known amount to which the padding is added.
        This call will fail prior to 15.0.1 because the api is undefined."""
        # AllocNewVarsBuffer can only be called once for a cursor
        # Call is a no-op except in w mode
        
        try:
            if self.accessType == 'w' and not self.calledalloc:
                self.calledalloc = True
                self.cur.AllocNewVarsBuffer(self.maxaddbuffer+extra)
        except AttributeError:  #api undefined in this version
            pass

def ismissing(value, missingtuple):
    """Return True or False according to whether value is either user or system missing according to the 3 or 4-tuple missingtuple.
    
    missingtuple corresponds to what is returned by GetVarMissingValues or the spssaux Variable class MissingValues2 property"""
    
    #string variables return only a 3-tuple, so must check from the end.  Strings do not support range mv's
    #string values arrive with trailing blanks, but missing values do not.


    stringmv = isinstance(value, basestring)
    if stringmv:
        value = value.rstrip()
    if value is None or value in missingtuple[-3:]:
        return True
    if missingtuple[0] == 0 or stringmv:
        return False
    return missingtuple[1] <= value <= missingtuple[2]
    

def _getIndexInfo(indexes, datelist):
    """Return a duple of a list of variable indexes and a list of variable names.
    
    indexes is a sequence of SPSS dictionary slot numbers, variable names, or a single VariableDict object.
    If indexes is empty or "ALL", all the variables are retrieved.
    If datelist, then only SPSS date variables are included, and no variable name list is returned."""

    namelist = []
    if not indexes or indexes[0] == "ALL":
        indexes = range(spss.GetVariableCount())
    numrequestedvars = len(indexes)

    if isinstance(indexes[0], basestring):      #list of names
        #namelist = list(copy.copy(indexes))
        vdict = spssaux.VariableDict(list(indexes))
        indexes = [int(v) for v in vdict]
    elif isinstance(indexes[0], spssaux.VariableDict):
        if len(indexes) > 1:
            raise ValueError, _msg26
        namelist = [v.VariableName for v in indexes[0]]
        indexes = [int(v) for v in indexes[0]]
        
    if not namelist:
        namelist = [spss.GetVariableName(int(i)) for i in indexes]
    if len(indexes) < numrequestedvars:
        raise ValueError, _msg27
    if datelist:
        indexes = filter(spssaux.isDateVariable, indexes)  # restrict to date variables

    if datelist:
        return indexes
    else:
        return (indexes, namelist)
    
class Dataset(object):
    """Simple class for managing dataset operations.  The constructor takes a string as the dataset name"""
    
    def __init__(self, dsname):
        self.dsname = dsname
    def __str__(self):   # for unaware users of the object
        return self.dsname
    def name(self):
        spss.Submit("DATASET NAME " + self.dsname)
    def activate(self):
        spss.Submit("DATASET ACTIVATE " + self.dsname)
    def declare(self):
        spss.Submit("DATASET DECLARE " + self.dsname)
    def close(self):
        spss.Submit("DATASET CLOSE " + self.dsname)

def CvtSpssDatetime(dt):
    """Return a Python datetime object from an SPSS datetime value.
    
    Note that SPSS day of week and month of year values cannot be converted."""

    if not dt:
        return None
    if dt < 86400:
        raise ValueError, _msg28

    #t = dt//86400   # date part
    #time = dt % 86400
    t, time = divmod(dt, 86400)
    j = t + 578041
    y = (4*j-1)//146097
    j = (4*j) -1 - (146097*y)
    d = j//4
    j = (4*d+3)//1461
    d = (4*d) + 3 -(1461*j)
    d = (d+4)//4
    m = (5*d-3)//153
    d = (5*d) - 3 - (153*m)
    d = (d+5)//5
    y = 100*y + j
    if (m < 10):
        m = m + 3
    else:
        m = m - 9
        y = y + 1
        
    itime = int(time)
    hr, itime = divmod(itime, 60*60)
    minute, itime = divmod(itime, 60)
    return datetime.datetime(int(y), int(m), int(d), int(hr), int(minute), int(itime), int((time-int(time))*10**6))
    
def yrmodasec(ymd):
    """Compute SPSS internal date value from four digit year, month, and day and optional time.
    
    ymd is a sequence of numbers in that order.  The numbers will be truncated to integers.
    If there are 4, 5, or 6 parts to the tuple, they are assumed to be h, m, and s and are not
    truncated.  The omitted parts are considered to be zero.
    The result is equivalent to the SPSS subroutine yrmoda result converted to seconds
    except that hms is an extension."""
    
    if not 3 <= len(ymd) <= 6:
        raise ValueError, _msg29
    year = int(ymd[0])
    month = int(ymd[1])
    day = int(ymd[2])
    
    if year < 1582 or month < 1 or month > 13 or day < 0 or day > 31:
        raise ValueError, ("Invalid date value: %d %d %d") % (year, month, day)
    yrmo = year * 365 + (year+3)//4 - (year+99)//100 + (year + 399)//400 \
         + 3055 *(month+2)//100 - 578192
    if month > 2:
        yrmo -= 2
        if (year%4 == 0 and (year%100 != 0 or year%400 ==0)):
            yrmo += 1
    ret = (yrmo + day) * 86400   #24 * 60 * 60
    # allow for h, hm, or hms
    for i in range(3, len(ymd)):
        ret += ymd[i] * 60**(5-i)
    return ret

