<%--
 Copyright (c) 2000, 2010 IBM Corporation and others.
 All rights reserved. This program and the accompanying materials 
 are made available under the terms of the Eclipse Public License v1.0
 which accompanies this distribution, and is available at
 http://www.eclipse.org/legal/epl-v10.html
 
 Contributors:
     IBM Corporation - initial API and implementation
--%>
<%@ include file="header.jsp"%>

<% 
	LayoutData data = new LayoutData(application,request, response);
	WebappPreferences prefs = data.getPrefs();
	AbstractView[] views = data.getViews();	
	// Read the scope parameter
	RequestScope.setScopeFromRequest(request, response);
%>	


<html lang="<%=ServletResources.getString("locale", request)%>">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">

<title><%=ServletResources.getString("Views", request)%></title>

<style type="text/css">

/* need this one for Mozilla */
HTML { 
	width:100%;
	height:100%;
	margin:0px;
	padding:0px;
	border:0px;
 }

BODY {
	margin:0px;
	padding:0px;
	/* Mozilla does not like width:100%, so we set height only */
	height:100%;
	position : relative;  // Needed for Safari
}

IFRAME {
	width:100%;
	height:100%;
	position : absolute;  // Needed for Safari
	top : 0px;
}

.hidden {
	visibility:hidden;
	width:0;
	height:0;
}

.visible {
	visibility:visible;
	width:100%;
	height:100%;
}

</style>
<script language="JavaScript" src="../<%=pluginVersion%>/advanced/views.js"></script>
<script language="Javascript">

var activityFiltering = <%=(new ActivitiesData(application, request, response)).isActivityFiltering()?"true":"false"%>;
var displayShowAllConfirmation = <%=prefs.isDontConfirmShowAll()?"false":"true"%>;

function confirmShowAll()
{
<%
if (data.isIE()){
%>
	var l = top.screenLeft + (top.document.body.clientWidth - w) / 2;
	var t = top.screenTop + (top.document.body.clientHeight - h) / 2;
<%
} else {
%>
	var l = top.screenX + (top.innerWidth - w) / 2;
	var t = top.screenY + (top.innerHeight - h) / 2;
<%
}
%>
	// move the dialog just a bit higher than the middle
	if (t-50 > 0) t = t-50;
	
	window.location="javascript://needModal";
	confirmShowAllDialog = window.open("confirmShowAll.jsp", "confirmShowAllDialog", "resizable=no,height="+h+",width="+w+",left="+l+",top="+t );
	confirmShowAllDialog.focus(); 
}

function selectScope() 
{
<%
if (data.isIE()){
%>
	var l = top.screenLeft + (top.document.body.clientWidth - w) / 2;
	var t = top.screenTop + (top.document.body.clientHeight - h) / 2;
<%
} else {
%>
	var l = top.screenX + (top.innerWidth - w) / 2;
	var t = top.screenY + (top.innerHeight - h) / 2;
<%
}
%>
	// move the dialog just a bit higher than the middle
	if (t-50 > 0) t = t-50;
	
	window.location="javascript://needModal";
	selectScopeDialog = window.open("selectScope.jsp", "selectScopeDialog", "resizable=no,height="+h+",width="+w+",left="+l+",top="+t );
	selectScopeDialog.focus(); 
}

</script>

</head>
   
<body dir="<%=direction%>" tabIndex="-1" onunload="closeConfirmShowAllDialog()" role="main" aria-label="<%=ServletResources.getString("Views", request)%>">
<h1 id="viewsTitle" style="display:none;"><%=ServletResources.getString("Views", request)%></h1>
<%
	for (int i=0; i<views.length; i++) 
	{
	    if (views[i].isVisible()) {
		    // normally we would hide the views first, but mozilla needs all iframes to be visible to load 
		    // other frames
		    String className =  data.getVisibleView().equals(views[i].getName()) ? "visible" : "hidden";
%>
 	<iframe role="region" aria-labelledby="viewsTitle" frameborder="0" 
 		    class="<%=className%>"  
 		    name="<%=views[i].getName()%>"
 		    title="<%=views[i].getFrameTitle(UrlUtil.getLocaleObj(request, null))%>"
 		    id="<%=views[i].getName()%>" 
 		    scrolling="no"
 		    src='<%="view.jsp?view="+views[i].getName()+(request.getQueryString()==null?"":("&"+UrlUtil.htmlEncode(request.getQueryString())))%>'>
 	</iframe> 
<%
        }
	}
%>	

</body>
</html>
