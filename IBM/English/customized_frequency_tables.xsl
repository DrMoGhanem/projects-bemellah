<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="1.0" xmlns:oms="http://xml.spss.com/spss/oms">
<!--
Modified version of simple_frequency_tables.xsl that:
1. Rounds decimal values to integers.
2. Always shows both variable names and labels.
3. Always shows both values and value labels.
5. Doesn't rely on any localized text.
-->
  
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
  <xsl:call-template name="showVarInfo"/>
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
   <!--select only valid, skip missing;
   Missing don't have a third (or fourth) category;
   alternative w/ localized text: ancestor::group[@text='Valid']-->
   <xsl:if test="oms:category[3]">
    <tr>
     <td>
       <xsl:choose>
        <!--if it has a varName, then it's not a total;
        Alternative w/ localized text: not((parent::*)[@text='Total'])-->
        <xsl:when test="parent::*/@varName">
         <xsl:call-template name="showValueInfo"/>
        </xsl:when>
        <xsl:when test="not(parent::*/@varName)">
          <b><xsl:value-of select="parent::*/@text"/></b>
        </xsl:when>
       </xsl:choose>
     </td>
     <td>
      <!--get value of Frequency column, which is first statistics column;
      alternative w/ localized text: category[@text='Frequency']/cell/@number-->
      <xsl:apply-templates select="oms:category[1]/oms:cell/@number"/>
     </td>
     <td>
      <!--get value of Valid Percent column, which is third stats column;
      alternative w/ localized text: category[@text='Valid Percent']/cell/@number-->
      <xsl:apply-templates select="oms:category[3]/oms:cell/@number"/>
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

<!--round decimal cell values to integers-->
<xsl:template match="@number">
  <xsl:value-of select="format-number(.,'#')"/>
</xsl:template>

<!--display both variable names and labels-->
<xsl:template name="showVarInfo">
 <p>
 <xsl:text>Variable Name: </xsl:text>
 <xsl:value-of select="@varName"/>
 </p>
 <xsl:if test="@label">
  <p>
   <xsl:text>Variable Label: </xsl:text>
   <xsl:value-of select="@label"/>
  </p>
 </xsl:if>
</xsl:template>

<!--display both values and value labels-->
<xsl:template name="showValueInfo">
 <xsl:choose>
 <!--Numeric vars have a number attribute,
  string vars have a string attribute -->
  <xsl:when test="parent::*/@number">
   <xsl:value-of select="parent::*/@number"/>
  </xsl:when>
  <xsl:when test="parent::*/@string">
   <xsl:value-of select="parent::*/@string"/>
  </xsl:when>
 </xsl:choose>
 <xsl:if test="parent::*/@label">
   <xsl:text>: </xsl:text>
   <xsl:value-of select="parent::*/@label"/>
 </xsl:if>
</xsl:template>


</xsl:stylesheet>
