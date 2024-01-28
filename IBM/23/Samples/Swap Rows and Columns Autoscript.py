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
SpssClient.StartClient()

objSpssScriptContext = SpssClient.GetScriptContext()
if objSpssScriptContext:
	objSpssOutputItem = objSpssScriptContext.GetOutputItem()
else:
	objSpssOutputDoc = SpssClient.GetDesignatedOutputDoc()
	objSpssOutputItem = objSpssOutputDoc.GetCurrentItem()

if objSpssOutputItem.GetType() == SpssClient.OutputItemType.PIVOT:	
    objSpssPivotTable = objSpssOutputItem.GetSpecificType()
    objSpssPivotMgr = objSpssPivotTable.PivotManager()
    objSpssPivotMgr.TransposeRowsWithColumns()
else:
    pass
    
SpssClient.StopClient()
