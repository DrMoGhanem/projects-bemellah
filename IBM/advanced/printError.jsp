<%--
 Copyright (c) 2009, 2010 IBM Corporation and others.
 All rights reserved. This program and the accompanying materials 
 are made available under the terms of the Eclipse Public License v1.0
 which accompanies this distribution, and is available at
 http://www.eclipse.org/legal/epl-v10.html
 
 Contributors:
     IBM Corporation - initial API and implementation
--%>
<%@ include file="header.jsp"%>
<%
	String msg = (String)request.getAttribute("msg");
%>

<html lang="<%=ServletResources.getString("locale", request)%>">
<head>
<title><%=ServletResources.getString("error", request)%></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="-1">
<link rel="stylesheet" href="../<%=pluginVersion%>/advanced/printAlert.css" charset="utf-8" type="text/css">

<script language="JavaScript">

function onloadHandler() {
	sizeButtons();
}

function sizeButtons() {
	var minWidth=60;

	if(document.getElementById("ok").offsetWidth < minWidth){
		document.getElementById("ok").style.width = minWidth+"px";
	}
}

</script>

</head>

<body role="main" dir='<%=direction%>' onload="onloadHandler()">
<h1 id="printErrorTitle" style="display:none;"><%=ServletResources.getString("error", request)%></h1>
<p>&nbsp;</p>
<div align="center" role="region" aria-labelledby="printErrorTitle">
<div class="printAlertDiv">
	<table role="presentation" align="center" width="400" cellpadding="10" cellspacing="0">
		<tr>
			<td class="caption"><span style="font-weight:bold;"><%=ServletResources.getString("error", request)%></span></td>
		</tr>
		<tr>
			<td height="50" class="message">
			<p><%=ServletResources.getString(msg, request)%></p>
			</td>
		</tr>
		<tr>
			<td class="button">
			<div align="center">
				<button id="ok" onClick="top.close()" role="button"><%=ServletResources.getString("OK", request)%></button>
            </div>
			</td>
		</tr>
	</table>
</div>
</div>
</body>
</html>