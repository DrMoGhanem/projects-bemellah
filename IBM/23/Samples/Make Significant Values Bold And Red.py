#/***********************************************************************
# * IBM Confidential 
# *
# * OCO Source Materials
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2011
# *
# * The source code for this program is not published or otherwise divested of its trade secrets,
# * irrespective of what has been deposited with the U.S. Copyright Office.
# ************************************************************************/

import SpssClient

""" This example finds a column labelled "Significance" in selected
    pivot tables, and changes the color of values less than 0.05
    in that column to red.  It can be applied to all pivot tables
    by changing

"""
### TODO: This part will migrate into its own module SpssClientAux.py
### and will be imported from Lib/site-packages.
###
### Please scroll to the end to see how this is applied.

class OutputItemTypeEnum(object):
    itemType = {}
    #itemType[0] = SpssClient.OutputItemType.UNKNOWN
    itemType[1] = SpssClient.OutputItemType.CHART
    itemType[2] = SpssClient.OutputItemType.HEAD
    itemType[3] = SpssClient.OutputItemType.LOG
    itemType[4] = SpssClient.OutputItemType.NOTE
    itemType[5] = SpssClient.OutputItemType.PIVOT
    itemType[6] = SpssClient.OutputItemType.ROOT
    itemType[7] = SpssClient.OutputItemType.TEXT
    itemType[8] = SpssClient.OutputItemType.WARNING
    itemType[9] = SpssClient.OutputItemType.TITLE
    itemType[11] = SpssClient.OutputItemType.PAGETITLE
    itemType[13] = SpssClient.OutputItemType.TREEMODEL
    itemType[14] = SpssClient.OutputItemType.GENERIC
    #itemType["UNKNOWN"] = itemType[0]
    itemType["CHART"] = itemType[1]
    itemType["HEAD"] = itemType[2]
    itemType["LOG"] = itemType[3]
    itemType["NOTE"] = itemType[4]
    itemType["PIVOT"] = itemType[5]
    itemType["ROOT"] = itemType[6]
    itemType["TEXT"] = itemType[7]
    itemType["WARNING"] = itemType[8]
    itemType["TITLE"] = itemType[9]
    itemType["PAGETITLE"] = itemType[11]
    itemType["TREEMODEL"] = itemType[13]
    itemType["GENERIC"] = itemType[14]

    def __getitem__(self, key):
        return self.itemType[key]

    def get(self, key, default=None):
        return self.itemType.get(key, default)

class SpssItems(object):
    OutputItemType = OutputItemTypeEnum()
    def __init__(self, outputDoc=None, selected=False):
        if outputDoc:
            self.outputDoc = outputDoc
        else:
            self.outputDoc = SpssClient.GetDesignatedOutputDoc()
        self.items = self.outputDoc.GetOutputItems()
        self.__itemType = []
        self.__selected = selected

    def __iter__(self):
        if self.__selected:
            for index in xrange(self.items.Size()):
                item = self.items.GetItemAt(index)
                if item.IsSelected():
                    yield item
        else:
            for index in xrange(self.items.Size()):
                item = self.items.GetItemAt(index)
                yield item

class SpssItemsTyped(SpssItems):
    def __init__(self,  itemType=[], outputDoc=None, selected=False):
        super(SpssItemsTyped, self).__init__(outputDoc=outputDoc, selected=selected)
        if isinstance(itemType, (list, tuple)):
            itemTypes = itemType
        else:
            itemTypes = [itemType]
        itemTypes = [SpssItems.OutputItemType.get(it, None) for it in itemTypes]
        itemTypes = [it for it in itemTypes if it]
        self.__itemType = itemTypes

    def __iter__(self):
        for item in super(SpssItemsTyped, self).__iter__():
            if item.GetType() in self.__itemType:
                 typedItem = item.GetSpecificType()
                 yield typedItem
        
class PivotTables(SpssItemsTyped):
    """ Convenience Class, equivalent to:
            SpssItemsTyped("PIVOT")
    """
    def __init__(self, outputDoc=None, selected=False):
        super(PivotTables, self).__init__(itemType="PIVOT", outputDoc=outputDoc, selected=selected)

class WarningTables(SpssItemsTyped):
    """ Convenience Class, equivalent to:
            SpssItemsTyped("WARNING")
    """
    def __init__(self, outputDoc=None, selected=False):
        super(WarningTables, self).__init__(itemType="WARNING", outputDoc=outputDoc, selected=selected)                

class TextStyleEnum(object):
    TextStyle = {}
    TextStyle['Regular'] = SpssClient.SpssTextStyleTypes.SpssTSRegular
    TextStyle['Bold'] = SpssClient.SpssTextStyleTypes.SpssTSBold
    TextStyle['Italic'] = SpssClient.SpssTextStyleTypes.SpssTSItalic
    TextStyle['BoldItalic'] = SpssClient.SpssTextStyleTypes.SpssTSBoldItalic
    TextStyle[0] = TextStyle['Regular']
    TextStyle[1] = TextStyle['Bold']
    TextStyle[2] = TextStyle['Italic']
    TextStyle[3] = TextStyle['BoldItalic']
    
    def __getitem__(self, key):
        return self.TextStyle[key]

    def get(self, key, default=None):
        return self.TextStyle.get(key, default)
    
def RGB(r,g,b):
    """Assumes red, green, blue values are integers in range(256)"""
    return r + 256*g + 65536*b

def FindColumn(pivotTable, label):
    """Really FindFirstColumn with the given label"""
    try:
        colLabels = pivotTable.ColumnLabelArray()
        rows = colLabels.GetNumRows()
        cols = colLabels.GetNumColumns()
        for i in xrange(rows):
            for j in xrange(cols):
                if colLabels.GetValueAt(i, j) == label:
                    return j
    except:
        return None
    return None

### TODO: do other useful things
            
try:
    SpssClient.StartClient()
    TS = TextStyleEnum()
    # change selected=False to apply to all pivot tables
    for pivotTable in PivotTables(selected=True):
        sigColumn = FindColumn(pivotTable, "Sig.")
        if sigColumn is not None:
            data = pivotTable.DataCellArray()
            rows = data.GetNumRows()
            for i in xrange(rows):
                try:
                     cellValue = data.GetValueAt(i,sigColumn)
                     value = float(cellValue)
                     if value >= 0.0 and value <= 0.05:
                         data.SetTextColorAt(i,sigColumn, RGB(255,0,0))
                         data.SetTextStyleAt(i,sigColumn, TS["Bold"])
                except Exception, e:
                    #print e
                    pass
except Exception, e:
        print e
finally:
    SpssClient.StopClient()
