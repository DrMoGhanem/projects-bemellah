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
	TocData data = new TocData(application,request, response);
	WebappPreferences prefs = data.getPrefs();
%>

<html lang="<%=ServletResources.getString("locale", request)%>">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title><%=ServletResources.getString("Content", request)%></title>

<base target="ContentViewFrame">
</head>


<body dir="<%=direction%>" bgcolor="<%=prefs.getBasicViewBackground()%>" role="navigation">
<h1 id="_tocViewTitle" style="display:none;"><%=ServletResources.getString("Content", request)%></h1>
<table role="region" aria-labelledby="_tocViewTitle" border="0" cellpadding="0" cellspacing="0">
<%
	for (int toc=0; toc<data.getTocCount(); toc++) {
		boolean isSelected =data.getSelectedToc() != -1 &&
					   data.getTocHref(data.getSelectedToc()).equals(data.getTocHref(toc));
		//if(!data.isEnabled(toc) && !isSelected){
			// do not show
		//	continue;
		//}
		String icon = isSelected ?
						"../" + pluginVersion + "/basic/" + prefs.getImagesDirectory()+"/toc_open.gif" :
							"../" + pluginVersion + "/basic/" + prefs.getImagesDirectory()+"/toc_closed.gif";
		String alt = isSelected ?
						ServletResources.getString("bookOpen", request) :
						ServletResources.getString("bookClosed", request) ;
%>
	<tr>
		<td align='<%=isRTL?"right":"left"%>' nowrap>
<%
		if(isSelected){
%>
			<b><img src="<%=icon%>" alt="<%=alt%>" title="<%=alt%>"><a href="<%=data.getTocDescriptionTopic(toc)%>" target="ContentViewFrame">&nbsp;<%=data.getTocLabel(toc)%></a></b>
<%
		}else{
%>
			<b><img src="<%=icon%>" alt="<%=alt%>" title="<%=alt%>"><a href="<%="tocView.jsp?toc="+data.getTocHref(toc)%>" target='_self'>&nbsp;<%=data.getTocLabel(toc)%></a></b>
<%
		}
%>
		</td>
	</tr>
<%
		// Only generate the selected toc
		if (isSelected) {
%>		
	<tr>
		<td align='<%=isRTL?"right":"left"%>' nowrap>			
<%
			data.generateBasicToc(toc, out);
%>			
		</td>
	</tr>
<%
		}
	}
%>		
</table>
</body>
</html>
