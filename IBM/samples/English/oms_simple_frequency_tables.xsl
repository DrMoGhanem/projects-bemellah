<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0" xmlns:oms="http://xml.spss.com/spss/oms">
  
<!--enclose everything in a template, starting at the root node-->
<xsl:template match="/">

<HTML>
<HEAD>
<TITLE>Modified Frequency Tables</TITLE>
</HEAD>
<BODY>
<!--Find all Frequency Tables-->
<xsl:for-each select="//oms:pivotTable[@subType='Frequencies']">
<xsl:for-each select="oms:dimension[@axis='row']">
 <h3>
  <xsl:value-of select="@text"/>
 </h3>
</xsl:for-each>
<!--create the HTML table-->
<table border="1">
 <tbody align="char" char="." charoff="1">
 <tr>
  <!--
  table header row; you could extract headings from 
  the XML but in this example we're using different header text
  -->
  <th>Category</th><th>Count</th><th>Percent</th>
 </tr>
 <!--find the columns of the pivot table-->
 <xsl:for-each select="descendant::oms:dimension[@axis='column']">
   <!--select only valid, skip missing-->
    <xsl:if test="ancestor::oms:group[@text='Valid']">
     <tr>
     <td>
       <xsl:choose>
        <xsl:when test="not((parent::*)[@text='Total'])">
         <xsl:value-of select="parent::*/@text"/>
        </xsl:when>
        <xsl:when test="((parent::*)[@text='Total'])">
         <b><xsl:value-of select="parent::*/@text"/></b>
        </xsl:when>
       </xsl:choose>
     </td>
     <td>
      <xsl:value-of select="oms:category[@text='Frequency']/oms:cell/@text"/>      
     </td>
     <td>
      <xsl:value-of select="oms:category[@text='Valid Percent']/oms:cell/@text"/>
     </td>
    </tr>
  </xsl:if>
  </xsl:for-each>
 </tbody>
</table>
<!--Don't forget possible footnotes for split files-->
<xsl:if test="descendant::*/oms:note">
<p><xsl:value-of select="descendant::*/oms:note/@text"/></p>
</xsl:if>
</xsl:for-each>
</BODY>
</HTML>
</xsl:template>
</xsl:stylesheet>
