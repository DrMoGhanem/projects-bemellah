<?xml version="1.0" encoding="UTF-8"?>
<!-- ***************************************************************** -->
<!--                                                                   -->
<!-- Licensed Materials - Property of IBM                              -->
<!--                                                                   -->
<!-- IBM SPSS Products: Statistics Common                              -->
<!--                                                                   -->
<!-- (C) Copyright IBM Corp. 1989, 2014                                -->
<!--                                                                   -->
<!-- US Government Users Restricted Rights - Use, duplication or       -->
<!-- disclosure restricted by GSA ADP Schedule Contract with IBM       -->
<!-- Corp.                                                             -->
<!--                                                                   -->
<!-- ***************************************************************** -->



<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:xalan="http://xml.apache.org/xalan" exclude-result-prefixes="xalan">
    <xsl:output method="xml" indent="no" encoding="UTF-8"/>
    <!--**************************************************************************************-->
    <xsl:template match="/SPSS/Transformation">
        <PMML version="3.2">
            <Header copyright="Copyright(c) SPSS Inc. 1989-2008. All rights reserved.">
                <Application name="Statistics" version="17.0"/>
            </Header>
            <xsl:variable name="funcs">
                <xsl:call-template name="DefineFunc">
                    <xsl:with-param name="funclist" select="./Compute//Function"/>
                    <xsl:with-param name="funcdef" select="./None"/>
                </xsl:call-template>
            </xsl:variable>
            <xsl:call-template name="doCommands">
                <xsl:with-param name="commands" select="./*"/>
                <xsl:with-param name="datavars" select="./empty"/>
                <xsl:with-param name="transvars" select="./empty"/>
                <xsl:with-param name="funcs" select="xalan:nodeset($funcs)/*"/>
            </xsl:call-template>
        </PMML>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="doCommands">
        <xsl:param name="commands"/>
        <xsl:param name="datavars"/>
        <xsl:param name="transvars"/>
        <xsl:param name="funcs"/>
        <!-- 
<xsl:message>
<xsl:text>In name=doCommands0</xsl:text>
<xsl:text>  commandscount=</xsl:text>
<xsl:value-of select="count(commands)"/>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars)"/>
<xsl:text>  datavarsfirstname=</xsl:text>
<xsl:value-of select="$datavars/@name"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:value-of select="count($transvars)"/>
<xsl:text>  transvarsfirstname=</xsl:text>
<xsl:value-of select="$transvars/@name"/>
</xsl:message>
-->
        <xsl:choose>
            <xsl:when test="count($commands) &lt; 1">
                <DataDictionary>
                    <xsl:copy-of select="$datavars"/>
                </DataDictionary>
                <TransformationDictionary>
                    <xsl:copy-of select="$funcs"/>
                    <xsl:copy-of select="$transvars"/>
                </TransformationDictionary>
            </xsl:when>
            <xsl:otherwise>
                <!-- 
<xsl:message>
<xsl:text>In name=doCommands1</xsl:text>
<xsl:text>  varname=</xsl:text>
<xsl:value-of select="$commands[position()=1]/Expression//Variable/@VarName"/>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars)"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:value-of select="count($transvars)"/>
</xsl:message>
-->
                <xsl:variable name="datavars0">
                    <xsl:choose>
                        <xsl:when test="name($commands) = 'Recode'">
                            <xsl:call-template name="doVariables">
                                <xsl:with-param name="vars"
                                    select="$commands[position()=1]/FromVarList/Variable"/>
                                <xsl:with-param name="datavars" select="$datavars"/>
                                <xsl:with-param name="transvars" select="$transvars"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="name($commands) = 'Compute'">
                            <xsl:call-template name="doVariables">
                                <xsl:with-param name="vars"
                                    select="$commands[position()=1]/Expression//Variable"/>
                                <xsl:with-param name="datavars" select="$datavars"/>
                                <xsl:with-param name="transvars" select="$transvars"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:copy-of select="$datavars"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>
                <xsl:variable name="datavars1" select="xalan:nodeset($datavars0)"/>
                <!-- 
<xsl:message>
<xsl:text>In name=doCommands2</xsl:text>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars1/*)"/>
<xsl:text>  datavarsfirstname=</xsl:text>
<xsl:value-of select="$datavars1/*/@name"/>
</xsl:message>
-->
                <xsl:variable name="transvars0">
                    <xsl:copy-of select="$transvars"/>
                    <xsl:if test="name($commands) = 'Recode' or name($commands) = 'Compute'">
                        <xsl:apply-templates select="$commands[position()=1]">
                            <xsl:with-param name="datavars" select="$datavars1/*"/>
                            <xsl:with-param name="transvars" select="$transvars"/>
                        </xsl:apply-templates>
                    </xsl:if>
                </xsl:variable>
                <xsl:variable name="transvars1" select="xalan:nodeset($transvars0)"/>
                <!-- 
<xsl:message>
<xsl:text>In name=doCommands3</xsl:text>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars1/*)"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:value-of select="count($transvars1/*)"/>
<xsl:text>  transvars1name=</xsl:text>
<xsl:value-of select="$transvars1/*[position()=1]/@name"/>
</xsl:message>
-->
                <xsl:call-template name="doCommands">
                    <xsl:with-param name="commands" select="$commands[position() &gt; 1]"/>
                    <xsl:with-param name="datavars" select="$datavars1/*"/>
                    <xsl:with-param name="transvars" select="$transvars1/*"/>
                    <xsl:with-param name="funcs" select="$funcs"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="doVariables">
        <xsl:param name="vars"/>
        <xsl:param name="datavars"/>
        <xsl:param name="transvars"/>
        <xsl:choose>
            <xsl:when test="count($vars) &gt; 0">
                <xsl:variable name="datavar">
                    <DataField>
                        <xsl:call-template name="Variable">
                            <xsl:with-param name="curnode" select="$vars[position() = 1]"/>
                            <xsl:with-param name="datavars" select="$datavars"/>
                            <xsl:with-param name="transvars" select="$transvars"/>
                        </xsl:call-template>
                    </DataField>
                </xsl:variable>
                <xsl:variable name="datavar0" select="xalan:nodeset($datavar)"/>
                <xsl:variable name="datavars0">
                    <xsl:copy-of select="$datavars"/>
                    <xsl:if test="$datavar0/*/@name">
                        <xsl:copy-of select="$datavar"/>
                    </xsl:if>
                </xsl:variable>
                <xsl:variable name="datavars1" select="xalan:nodeset($datavars0)"/>
                <!-- 
<xsl:message>
<xsl:text>In doVariables1 </xsl:text>
<xsl:text>  varscount=</xsl:text>
<xsl:value-of select="count($vars)"/>
<xsl:text>  firstname=</xsl:text>
<xsl:value-of select="$vars/@VarName"/>
<xsl:text>  datavarname=</xsl:text>
<xsl:value-of select="$datavar0/*/@name"/>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars1/*)"/>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars)"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:value-of select="count($transvars)"/>
</xsl:message>
-->
                <xsl:call-template name="doVariables">
                    <xsl:with-param name="vars" select="$vars[position() &gt; 1]"/>
                    <xsl:with-param name="datavars" select="$datavars1/*"/>
                    <xsl:with-param name="transvars" select="$transvars"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:copy-of select="$datavars"/>
                <!-- 
<xsl:message>
<xsl:text>In doVariables2 </xsl:text>
<xsl:text>  varscount=</xsl:text>
<xsl:value-of select="count($vars)"/>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars)"/>
<xsl:text>  datavarsfirstname=</xsl:text>
<xsl:value-of select="name($datavars)"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:value-of select="count($transvars)"/>
</xsl:message>
-->
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--Recode  begin ************************************************************************-->
    <!--**************************************************************************************-->
    <xsl:template name="StringValues">
        <xsl:param name="newvalues"/>
        <xsl:param name="leftvalues"/>
        <xsl:param name="hasmissing" select="false()"/>
        <!-- 
<xsl:message>
<xsl:text>  In StringValues1  </xsl:text>
<xsl:text>  newvalues count= </xsl:text><xsl:value-of select="count($newvalues)"/>
<xsl:text>  leftvalues count= </xsl:text><xsl:value-of select="count($leftvalues)"/>
<xsl:text>  leftvalues firstname= </xsl:text><xsl:value-of select="name($leftvalues)"/>
<xsl:text>  leftvalues extname= </xsl:text><xsl:value-of select="$leftvalues/@name"/>
<xsl:text>  hasmissing= </xsl:text><xsl:value-of select="$hasmissing"/>
</xsl:message>
        -->
        <xsl:choose>
            <xsl:when test="count($leftvalues) &gt; 0">
                <xsl:choose>
                    <xsl:when test="name($leftvalues) = 'row'">
                        <!-- 
                            <xsl:message>
                            <xsl:text>  In StringValues2  </xsl:text>
                            </xsl:message>
                        -->
                        <xsl:variable name="newvalues1">
                            <xsl:copy-of select="$newvalues"/>
                            <xsl:copy-of select="$leftvalues[position()=1]"/>
                        </xsl:variable>
                        <xsl:variable name="newnodes" select="xalan:nodeset($newvalues1)"/>
                        <xsl:call-template name="StringValues">
                            <xsl:with-param name="newvalues" select="$newnodes/*"/>
                            <xsl:with-param name="leftvalues" select="$leftvalues[position()&gt;
                                1]"/>
                            <xsl:with-param name="hasmissing" select="$hasmissing"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="($leftvalues[position()=1]/@name='mapElseTo')">
                        <!-- 
<xsl:message>
<xsl:text>  In StringValues3  </xsl:text>
<xsl:text>  name=</xsl:text><xsl:value-of select="$leftvalues[position()=1]/@name"/>
<xsl:text>  firstflag=</xsl:text> <xsl:value-of select="($leftvalues[position()=1]/@name='mapElseTo')"/>
<xsl:text>  secondflag=</xsl:text> <xsl:value-of select=" ($leftvalues[position()=1]/@name='recodeElseCopy')"/>
<xsl:text>  flag=</xsl:text> <xsl:value-of select="($leftvalues[position()=1]/@name='mapElseTo')  or ($leftvalues[position()=1]/@name='recodeElseCopy')"/>
</xsl:message>
                        -->
                        <xsl:copy-of select="$newvalues"/>
                        <xsl:if test="$hasmissing = false()">
                            <Extension extender="spss.com" name="mapMissingTo">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="$leftvalues[position()=1]/@value"/>
                                </xsl:attribute>
                            </Extension>
                            <!-- 
                            <Extension extender="spss.com" name="mapSysmisTo">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="$leftvalues[position()=1]/@value"/>
                                </xsl:attribute>
                            </Extension>
                            -->
                        </xsl:if>
                        <xsl:copy-of select="$leftvalues[position()=1]"/>
                    </xsl:when>
                    <xsl:when test="($leftvalues[position()=1]/@name='recodeElseCopy') or
                        ($leftvalues[position()=1]/@name='recodeElseSysmis')">
                        <!-- 
                            <xsl:message>
                            <xsl:text>  In StringValues3  </xsl:text>
                            <xsl:text>  name=</xsl:text><xsl:value-of select="$leftvalues[position()=1]/@name"/>
                            <xsl:text>  firstflag=</xsl:text> <xsl:value-of select="($leftvalues[position()=1]/@name='mapElseTo')"/>
                            <xsl:text>  secondflag=</xsl:text> <xsl:value-of select=" ($leftvalues[position()=1]/@name='recodeElseCopy')"/>
                            <xsl:text>  flag=</xsl:text> <xsl:value-of select="($leftvalues[position()=1]/@name='mapElseTo')  or ($leftvalues[position()=1]/@name='recodeElseCopy')"/>
                            </xsl:message>
                        -->
                        <xsl:copy-of select="$newvalues"/>
                        <xsl:copy-of select="$leftvalues[position()=1]"/>
                    </xsl:when>
                    <xsl:when test="$leftvalues[position()=1]/@name = 'mapMissingTo' ">
                        <!-- 
                            <xsl:message>
                            <xsl:text>  In StringValues4  </xsl:text>
                            </xsl:message>
                        -->
                        <xsl:variable name="newvalues1">
                            <xsl:copy-of select="$newvalues"/>
                            <xsl:if test="$hasmissing=false()">
                                <xsl:copy-of select="$leftvalues[position()=1]"/>
                                <!-- 
                                <Extension extender="spss.com" name="mapSysmisTo">
                                    <xsl:attribute name="value">
                                        <xsl:value-of select="$leftvalues[position()=1]/@value"/>
                                    </xsl:attribute>
                                </Extension>
                                -->
                            </xsl:if>
                        </xsl:variable>
                        <xsl:variable name="newnodes" select="xalan:nodeset($newvalues1)"/>
                        <!-- 
                            <xsl:message>
                            <xsl:text>  In StringValues5  </xsl:text>
                            </xsl:message>
                        -->
                        <xsl:call-template name="StringValues">
                            <xsl:with-param name="newvalues" select="$newnodes/*"/>
                            <xsl:with-param name="leftvalues" select="$leftvalues[position()
                                &gt; 1]"/>
                            <xsl:with-param name="hasmissing" select="true()"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="($leftvalues[position()=1]/@name = 'recodeMissingCopy') or
                        ($leftvalues[position()=1]/@name = 'recodeMissingSysmis') ">
                        <!-- 
<xsl:message>
<xsl:text>  In StringValues4  </xsl:text>
</xsl:message>
-->
                        <xsl:variable name="newvalues1">
                            <xsl:copy-of select="$newvalues"/>
                            <xsl:if test="$hasmissing=false()">
                                <xsl:copy-of select="$leftvalues[position()=1]"/>
                            </xsl:if>
                        </xsl:variable>
                        <xsl:variable name="newnodes" select="xalan:nodeset($newvalues1)"/>
                        <!-- 
<xsl:message>
<xsl:text>  In StringValues5  </xsl:text>
</xsl:message>
-->
                        <xsl:call-template name="StringValues">
                            <xsl:with-param name="newvalues" select="$newnodes/*"/>
                            <xsl:with-param name="leftvalues" select="$leftvalues[position()
                                &gt; 1]"/>
                            <xsl:with-param name="hasmissing" select="true()"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <!-- 
<xsl:message>
<xsl:text>  In StringValues7  </xsl:text>
</xsl:message>
                        -->
                        <xsl:variable name="newvalues1">
                            <xsl:copy-of select="$newvalues"/>
                            <xsl:copy-of select="$leftvalues[position()=1]"/>
                        </xsl:variable>
                        <xsl:variable name="newnodes" select="xalan:nodeset($newvalues1)"/>
                        <xsl:call-template name="StringValues">
                            <xsl:with-param name="newvalues" select="$newnodes/*"/>
                            <xsl:with-param name="leftvalues" select="$leftvalues[position()
                                &gt; 1]"/>
                            <xsl:with-param name="hasmissing" select="$hasmissing"/>
                        </xsl:call-template>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:copy-of select="$newvalues"/>
            </xsl:otherwise>
        </xsl:choose>
        <!-- 
<xsl:message>
<xsl:text>  In StringValues10  </xsl:text>
</xsl:message>
-->
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template match="Recode">
        <xsl:param name="datavars"/>
        <xsl:param name="transvars"/>
        <xsl:call-template name="RecodeOne">
            <xsl:with-param name="lefttarget" select="./IntoVarList/Variable"/>
            <xsl:with-param name="datavars" select="$datavars"/>
            <xsl:with-param name="transvars" select="$transvars"/>
        </xsl:call-template>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="RecodeOne">
        <xsl:param name="lefttarget"/>
        <xsl:param name="datavars"/>
        <xsl:param name="transvars"/>
        <xsl:variable name="pos" select="count(./IntoVarList/Variable)-count($lefttarget)+1"/>
        <xsl:variable name="target" select="./IntoVarList/Variable[position()=$pos]"/>
        <xsl:variable name="source" select="./FromVarList/Variable[position()=$pos]"/>
        <xsl:choose>
            <xsl:when test="$target">
                <xsl:variable name="upSourceValue"
                    select="translate($source/@VarName,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                <xsl:variable name="upTargetValue"
                    select="translate($target/@VarName,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                <xsl:if test="$upSourceValue = $upTargetValue">
                    <xsl:message terminate="yes">
                        <xsl:text>CVT_ReVarsErr:</xsl:text>
                        <xsl:value-of select="$source/@VarName"/>
                    </xsl:message>
                </xsl:if>
            </xsl:when>
            <xsl:otherwise>
                <xsl:message terminate="yes">
                    <xsl:text>CVT_ConvertErr:</xsl:text>
                    <xsl:value-of select="$source/@VarName"/>
                </xsl:message>
            </xsl:otherwise>
        </xsl:choose>
        <!--  
<xsl:message>
<xsl:text>In Recode0 </xsl:text>
<xsl:text>  lefttarget pos=</xsl:text><xsl:value-of select="$pos"/>
<xsl:text>  lefttarget count=</xsl:text><xsl:value-of select="count($lefttarget)"/>
</xsl:message>
-->
        <DerivedField>
            <!-- 
<xsl:message>
<xsl:text>In Recode1 </xsl:text>
<xsl:text>  curnodename=</xsl:text><xsl:value-of select="name()"/>
<xsl:text>  datavarscount=</xsl:text><xsl:value-of select="count($datavars)"/>
<xsl:text>  transvarscount=</xsl:text><xsl:value-of select="count($transvars)"/>
</xsl:message>
-->
            <xsl:call-template name="Variable">
                <xsl:with-param name="curnode" select="$target"/>
                <xsl:with-param name="datavars" select="$datavars"/>
                <xsl:with-param name="transvarsa" select="$transvars"/>
                <xsl:with-param name="type">derived</xsl:with-param>
            </xsl:call-template>
            <!-- 
<xsl:message>
<xsl:text>In Recode2 </xsl:text>
<xsl:text>  curnodename=</xsl:text><xsl:value-of select="name()"/>
<xsl:text>  datavarscount=</xsl:text><xsl:value-of select="count($datavars)"/>
<xsl:text>  transvarscount=</xsl:text><xsl:value-of select="count($transvars)"/>
</xsl:message>
-->
            <xsl:choose>
                <xsl:when test="$source/@datatype ='string'">
                    <!-- Notice: same code in 2 places.  -->
                    <xsl:variable name="output">
                        <xsl:text>c</xsl:text>
                        <xsl:value-of select="translate($target/@VarName, '#', '__' )"/>
                    </xsl:variable>
                    <xsl:variable name="input">
                        <xsl:text>c</xsl:text>
                        <xsl:value-of select="translate($source/@VarName, '#', '__' )"/>
                    </xsl:variable>
                    <xsl:variable name="values1">
                        <!-- 
<xsl:message>
<xsl:text>In name=Recode3</xsl:text>
<xsl:text>  sourcecount=</xsl:text><xsl:value-of select="count(./RecodeValue/ValueList/*)"/>
<xsl:text>  input=</xsl:text><xsl:value-of select="$input"/>
<xsl:text>  output=</xsl:text><xsl:value-of select="$output"/>
</xsl:message>
-->
                        <xsl:call-template name="RecodeString">
                            <xsl:with-param name="input" select="$input"/>
                            <xsl:with-param name="output" select="$output"/>
                            <xsl:with-param name="sources" select="./RecodeValue/ValueList/*"/>
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="valuesnode1" select="xalan:nodeset($values1)"/>
                    <xsl:variable name="values">
                        <xsl:call-template name="StringValues">
                            <xsl:with-param name="leftvalues" select="$valuesnode1/*"/>
                            <xsl:with-param name="newvalues" select="$valuesnode1/None"/>
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="valuesnode" select="xalan:nodeset($values)"/>
                    <MapValues>
                        <xsl:attribute name="outputColumn">
                            <xsl:value-of select="$output"/>
                        </xsl:attribute>
                        <!-- add mapMissingTo and defaultValue attribute  here -->
                        <xsl:if test="$valuesnode/Extension[@name = 'mapElseTo']">
                            <xsl:attribute name="defaultValue">
                                <xsl:value-of select="$valuesnode/Extension[@name =
                                    'mapElseTo']/@value"/>
                            </xsl:attribute>
                        </xsl:if>
                        <xsl:if test="$valuesnode/Extension[@name = 'mapMissingTo']">
                            <xsl:variable name="ttt" select="$valuesnode/Extension[@name =
                                'mapMissingTo']/@value"/>
                            <xsl:attribute name="mapMissingTo">
                                <xsl:value-of select="$ttt"/>
                            </xsl:attribute>
                        </xsl:if>
                        <xsl:copy-of select="$valuesnode/Extension[@name != 'mapElseTo' and
                            @name   !='mapMissingTo']"/>
                        <FieldColumnPair>
                            <xsl:attribute name="field">
                                <xsl:value-of select="$source/@VarName"/>
                            </xsl:attribute>
                            <xsl:attribute name="column">
                                <xsl:value-of select="$input"/>
                            </xsl:attribute>
                        </FieldColumnPair>

                        <xsl:if test="$valuesnode/row">
                            <InlineTable>
                                <xsl:copy-of select="$valuesnode/row"/>
                            </InlineTable>
                        </xsl:if>
                    </MapValues>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:variable name="intervals">
                        <xsl:variable name="nodes">
                            <xsl:call-template name="RecodeValue">
                                <xsl:with-param name="sources" select="./RecodeValue/ValueList/*"/>
                            </xsl:call-template>
                            <xsl:variable name="test1"
                                select="translate($source/@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                                'abcdefghijklmnopqrstuvwxyz')"/>
                            <xsl:variable name="test2"
                                select="$datavars[translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                                'abcdefghijklmnopqrstuvwxyz')=$test1]"/>
                            <xsl:copy-of select="$test2"/>
                        </xsl:variable>
                        <xsl:variable name="nodelist" select="xalan:nodeset($nodes)"/>
                        <xsl:choose>
                            <xsl:when test="function-available('xalan:intervals')">
                                <!-- 
<xsl:copy-of select="$nodelist/Extension"/>
-->
                                <xsl:copy-of select="xalan:intervals($nodelist/*)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:copy-of select="$nodes"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="intervalnodes" select="xalan:nodeset($intervals)"/>
                    <Discretize>
                        <xsl:attribute name="field">
                            <xsl:value-of select="$source/@VarName"/>
                        </xsl:attribute>
                        <xsl:if test="$intervalnodes/Extension[@name = 'mapElseTo']">
                            <xsl:attribute name="defaultValue">
                                <xsl:value-of select="$intervalnodes/Extension[@name =
                                    'mapElseTo']/@value"/>
                            </xsl:attribute>
                        </xsl:if>
                        <xsl:if test="$intervalnodes/Extension[@name = 'mapMissingTo']">
                            <xsl:attribute name="mapMissingTo">
                                <xsl:value-of select="$intervalnodes/Extension[@name =
                                    'mapMissingTo']/@value"/>
                            </xsl:attribute>
                        </xsl:if>
                        <xsl:choose>
                            <xsl:when test="$intervalnodes/DiscretizeBin">
                                <xsl:copy-of select="$intervalnodes/Extension[@name != 'mapElseTo'
                                    and @name         !='mapMissingTo']"/>
                                <xsl:copy-of select="$intervalnodes/DiscretizeBin"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:variable name="extensions"
                                    select="$intervalnodes/Extension[@name != 'mapElseTo' and
                                    @name!='mapMissingTo']"/>
                                <xsl:variable name="elses" select="$extensions[@name =
                                    'recodeElseCopy' or @name='recodeElseSysmis']"/>
                                <xsl:variable name="lefts" select="$extensions[@name !=
                                    'recodeElseCopy' and @name != 'recodeElseSysmis']"/>

                                <xsl:choose>
                                    <xsl:when test="$lefts">
                                        <xsl:copy-of select="$elses"/>
                                        <xsl:for-each select="$lefts">
                                            <DiscretizeBin binValue="">
                                                <Extension extender="spss.com">
                                                  <xsl:attribute name="name">
                                                  <xsl:value-of select="./@name"/>
                                                  </xsl:attribute>
                                                  <xsl:if test="./@value">
                                                  <xsl:attribute name="value">
                                                  <xsl:value-of select="./@value"/>
                                                  </xsl:attribute>
                                                  </xsl:if>
                                                </Extension>
                                                <xsl:choose>
                                                  <xsl:when test="./Interval">
                                                  <xsl:copy-of select="./Interval"/>
                                                  </xsl:when>
                                                  <xsl:otherwise>
                                                  <Interval closure="closedClosed"/>
                                                  </xsl:otherwise>
                                                </xsl:choose>
                                            </DiscretizeBin>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:when test="$elses">
                                        <DiscretizeBin binValue="">
                                            <Extension extender="spss.com">
                                                <xsl:attribute name="name">
                                                  <xsl:value-of
                                                  select="$elses[position()=1]/@name"/>
                                                </xsl:attribute>
                                            </Extension>
                                            <Interval closure="closedClosed"/>
                                        </DiscretizeBin>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <DiscretizeBin binValue="">
                                            <Interval closure="closedClosed"/>
                                        </DiscretizeBin>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:otherwise>
                        </xsl:choose>
                    </Discretize>
                </xsl:otherwise>
            </xsl:choose>
        </DerivedField>
        <xsl:if test="count($lefttarget) &gt; 1">
            <xsl:call-template name="RecodeOne">
                <xsl:with-param name="lefttarget" select="$lefttarget[position() &gt; 1]"/>
                <xsl:with-param name="datavars" select="$datavars"/>
                <xsl:with-param name="transvars" select="$transvars"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="RecodeString">
        <xsl:param name="input"/>
        <xsl:param name="output"/>
        <xsl:param name="sources"/>
        <!-- 
<xsl:message>
<xsl:text>In name=RecodeString0</xsl:text>
<xsl:text>  sourcecount=</xsl:text><xsl:value-of select="count($sources)"/>
<xsl:text>  input=</xsl:text><xsl:value-of select="$input"/>
<xsl:text>  output=</xsl:text><xsl:value-of select="$output"/>
</xsl:message>
-->
        <xsl:if test="$sources[name()='CONVERT']">
            <xsl:message terminate="yes">
                <xsl:text>CVT_ConvertErr:</xsl:text>
            </xsl:message>
        </xsl:if>
        <xsl:for-each select="$sources">
            <!-- 
<xsl:sort order="descending" select="name()" data-type="text"/>
<xsl:sort order="descending" data-type="text" select="name(../../Target/*)"/>
-->
            <!-- 
<xsl:message>
<xsl:text>In name=RecodeString</xsl:text>
<xsl:text>  sourcecount=</xsl:text><xsl:value-of select="count($sources)"/>
<xsl:text>  curname=</xsl:text><xsl:value-of select="name()"/>
<xsl:text>  curvalue=</xsl:text><xsl:value-of select="./@Value"/>
</xsl:message>
-->
            <xsl:choose>
                <xsl:when test=" name() = 'Constant'">
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <row>
                                <xsl:element name="{$input}">
                                    <xsl:value-of select="./@Value"/>
                                </xsl:element>
                                <xsl:element name="{$output}">
                                    <xsl:value-of select="./@Value"/>
                                </xsl:element>
                            </row>
                        </xsl:when>
                        <xsl:when test="../../Target/Constant">
                            <row>
                                <xsl:element name="{$input}">
                                    <xsl:value-of select="./@Value"/>
                                </xsl:element>
                                <xsl:element name="{$output}">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:element>
                            </row>
                        </xsl:when>
                        <xsl:when test="../../Target/SYSMIS">
                            <Extension extender="spss.com" name="recodeTargetSysmis">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="./@Value"/>
                                </xsl:attribute>
                            </Extension>
                        </xsl:when>
                        <xsl:otherwise/>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test=" name() = 'ELSE'">
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <Extension extender="spss.com" name="recodeElseCopy"/>
                        </xsl:when>
                        <xsl:when test="../../Target/Constant">
                            <Extension extender="spss.com" name="mapElseTo">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:attribute>
                            </Extension>
                        </xsl:when>
                        <xsl:when test="../../Target/SYSMIS">
                            <Extension extender="spss.com" name="recodeElseSysmis"/>
                        </xsl:when>
                        <xsl:otherwise/>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test=" name() = 'MISSING'">
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <Extension extender="spss.com" name="recodeMissingCopy"/>
                        </xsl:when>
                        <xsl:when test="../../Target/Constant">
                            <Extension extender="spss.com" name="mapMissingTo">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:attribute>
                            </Extension>
                        </xsl:when>
                        <xsl:when test="../../Target/SYSMIS">
                            <Extension extender="spss.com" name="recodeMissingSysmis"/>
                        </xsl:when>
                        <xsl:otherwise/>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test=" name() = 'SYSMIS'">
                    <!-- syntax error-->
                </xsl:when>
                <xsl:when test=" name() = 'CONVERT'">
                    <!-- Error -->
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <!--Recode  end   ************************************************************************-->
    <xsl:template name="RecodeValue">
        <xsl:param name="sources"/>
        <xsl:for-each select="$sources">
            <!-- 
<xsl:sort order="descending" select="name()" data-type="text"/>
<xsl:sort order="descending" data-type="text" select="name(../../Target/*)"/>
-->
            <!-- 
<xsl:message>
<xsl:text>In name=RecodeValue</xsl:text>
<xsl:text>  sourcecount=</xsl:text><xsl:value-of select="count($sources)"/>
<xsl:text>  curname=</xsl:text><xsl:value-of select="name()"/>
<xsl:text>  curvalue=</xsl:text><xsl:value-of select="./@Value"/>
</xsl:message>
-->
            <xsl:choose>
                <xsl:when test="name() = 'BetweenValue'">
                    <xsl:variable name="intervalvar">
                        <Interval>
                            <xsl:attribute name="closure">
                                <xsl:text>closedClosed</xsl:text>
                            </xsl:attribute>
                            <xsl:variable name="upLoValue"
                                select="translate(./LoValue/@Value,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                            <xsl:if test="starts-with($upLoValue, 'LO') = false">
                                <xsl:attribute name="leftMargin">
                                    <xsl:value-of select="./LoValue/@Value"/>
                                </xsl:attribute>
                            </xsl:if>
                            <xsl:variable name="upHiValue"
                                select="translate(./HiValue/@Value,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                            <xsl:if test="starts-with(./HiValue/@Value, 'HI') = false">
                                <xsl:attribute name="rightMargin">
                                    <xsl:value-of select="./HiValue/@Value"/>
                                </xsl:attribute>
                            </xsl:if>
                        </Interval>
                    </xsl:variable>
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <Extension extender="spss.com" name="recodeIntervalCopy">
                                <xsl:copy-of select="$intervalvar"/>
                            </Extension>
                        </xsl:when>
                        <xsl:when test="../../Target/SYSMIS">
                            <Extension extender="spss.com" name="recodeTargetSysmis">
                                <xsl:copy-of select="$intervalvar"/>
                            </Extension>
                        </xsl:when>
                        <xsl:otherwise>
                            <DiscretizeBin>
                                <xsl:attribute name="binValue">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:attribute>
                                <xsl:copy-of select="$intervalvar"/>
                            </DiscretizeBin>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test=" name() = 'Constant'">
                    <xsl:variable name="intervalvar">
                        <Interval>
                            <xsl:attribute name="closure">
                                <xsl:text>closedClosed</xsl:text>
                            </xsl:attribute>
                            <xsl:attribute name="leftMargin">
                                <xsl:value-of select="./@Value"/>
                            </xsl:attribute>
                            <xsl:attribute name="rightMargin">
                                <xsl:value-of select="./@Value"/>
                            </xsl:attribute>
                        </Interval>
                    </xsl:variable>
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <Extension extender="spss.com" name="recodeIntervalCopy">
                                <xsl:copy-of select="$intervalvar"/>
                            </Extension>
                        </xsl:when>
                        <xsl:when test="../../Target/SYSMIS">
                            <Extension extender="spss.com" name="recodeTargetSysmis">
                                <xsl:copy-of select="$intervalvar"/>
                            </Extension>
                        </xsl:when>
                        <xsl:otherwise>
                            <DiscretizeBin>
                                <xsl:attribute name="binValue">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:attribute>
                                <xsl:copy-of select="$intervalvar"/>
                            </DiscretizeBin>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test=" name() = 'ELSE'">
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <Extension extender="spss.com" name="recodeElseCopy"/>
                        </xsl:when>
                        <xsl:when test="../../Target/SYSMIS">
                            <Extension extender="spss.com" name="recodeElseSysmis"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <Extension extender="spss.com" name="mapElseTo">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:attribute>
                            </Extension>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test=" name() = 'MISSING'">
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <Extension extender="spss.com" name="recodeMissingCopy"/>
                        </xsl:when>
                        <xsl:when test="../../Target/SYSMIS">
                            <Extension extender="spss.com" name="recodeMissingSysmis"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <!-- 
<xsl:message>
<xsl:text>In name=RecodeValue1</xsl:text>
<xsl:text>  mapMissingTo=</xsl:text><xsl:value-of select="../../Target/Constant/@Value"/>
</xsl:message>
-->
                            <Extension extender="spss.com" name="mapMissingTo">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:attribute>
                            </Extension>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test=" name() = 'SYSMIS'">
                    <xsl:choose>
                        <xsl:when test="../../Target/COPY">
                            <Extension extender="spss.com" name="recodeSysmisCopy"/>
                        </xsl:when>
                        <xsl:otherwise>
<!--                            <Extension extender="spss.com" name="mapSysmisTo">
                                <xsl:attribute name="value">
                                    <xsl:value-of select="../../Target/Constant/@Value"/>
                                </xsl:attribute>
                            </Extension>-->
                            <xsl:attribute name="mapMissingTo">
                                <xsl:value-of select="../../Target/Constant/@Value"/>
                            </xsl:attribute>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <!--Recode  end   ************************************************************************-->
    <!--**************************************************************************************-->
    <!--Compute begin ************************************************************************-->
    <!--**************************************************************************************-->
    <xsl:template match="Compute">
        <xsl:param name="datavars"/>
        <xsl:param name="transvars"/>
        <!-- 
<xsl:message>
<xsl:text>In Compute</xsl:text>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars)"/>
<xsl:text>  datavarsname=</xsl:text>
<xsl:value-of select="$datavars[position()=1]/@name"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:value-of select="count($transvars)"/>
</xsl:message>
-->
        <xsl:call-template name="equation">
            <xsl:with-param name="nodes" select="./*"/>
            <xsl:with-param name="datavars" select="$datavars"/>
            <xsl:with-param name="transvars" select="$transvars"/>
        </xsl:call-template>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="equation">
        <xsl:param name="nodes"/>
        <xsl:param name="datavars"/>
        <xsl:param name="transvars"/>
        <xsl:if test="count($nodes) &gt; 1">
            <DerivedField>
                <!-- 
<xsl:message>
<xsl:text>In equation</xsl:text>
<xsl:text>  nodescount</xsl:text>
<xsl:value-of select="count($nodes)"/>
<xsl:text>  firstVarname=</xsl:text>
<xsl:value-of select="$nodes[position()=1]/@VarName"/>
<xsl:text>  firstNodename=</xsl:text>
<xsl:value-of select="name($nodes)"/>
<xsl:value-of select="count($datavars)"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:value-of select="count($transvars)"/>
<xsl:text>  datavarscount=</xsl:text>
</xsl:message>
-->
                <xsl:call-template name="Variable">
                    <xsl:with-param name="curnode" select="$nodes[position()=1]"/>
                    <xsl:with-param name="datavars" select="$datavars"/>
                    <xsl:with-param name="transvars" select="$transvars"/>
                    <xsl:with-param name="type">derived</xsl:with-param>
                </xsl:call-template>
                <xsl:variable name="nodescount" select="count(./*)"/>
                <xsl:call-template name="parseExpression">
                    <xsl:with-param name="nodes" select="./Expression/*"/>
                </xsl:call-template>
            </DerivedField>
        </xsl:if>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="parseExpression">
        <xsl:param name="nodes"/>
        <xsl:variable name="new">
            <xsl:for-each select="$nodes">
                <xsl:choose>
                    <xsl:when test="name() = 'Variable'">
                        <FieldRef>
                            <xsl:attribute name="field">
                                <xsl:value-of select="./@VarName"/>
                            </xsl:attribute>
                        </FieldRef>
                    </xsl:when>
                    <xsl:when test="name() = 'Constant'">
                        <Constant>
                            <xsl:attribute name="dataType">
                                <xsl:call-template name="mapdataType">
                                    <xsl:with-param name="type" select="./@datatype"/>
                                </xsl:call-template>
                            </xsl:attribute>
                            <xsl:value-of select="./@Value"/>
                        </Constant>
                    </xsl:when>
                    <xsl:when test="name() = 'StackOperator' and ./@Name='(' ">
                        <xsl:text/>
                    </xsl:when>
                    <xsl:when test="name() = 'StackOperator' and ./@Name='=' ">
                        <xsl:text/>
                    </xsl:when>
                    <xsl:when test="name() = 'doOperator' and ./@opcode=27">
                        <xsl:text/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:copy-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:variable>
        <xsl:variable name="newnodes" select="xalan:nodeset($new)"/>
        <xsl:call-template name="expression">
            <xsl:with-param name="nodes" select="$newnodes/*"/>
        </xsl:call-template>
    </xsl:template>
    <!--**************************************************************************************-->
    <!-- do parse -->
    <xsl:template name="expression">
        <xsl:param name="nodes"/>
        <xsl:variable name="pos">
            <xsl:call-template name="findFirstDo">
                <xsl:with-param name="nodes" select="$nodes"/>
            </xsl:call-template>
        </xsl:variable>
        <!-- 
<xsl:message>
<xsl:text>In expression </xsl:text>
<xsl:text> countnode=</xsl:text>
<xsl:copy-of select="count($nodes)"/>
<xsl:text> firstnodename=</xsl:text>
<xsl:copy-of select="name($nodes)"/>
<xsl:text> pos=</xsl:text>
<xsl:copy-of select="$pos"/>
</xsl:message>
-->
        <xsl:choose>
            <xsl:when test="number($pos) &gt; 0">
                <xsl:variable name="new">
                    <xsl:call-template name="dealFirstDo">
                        <xsl:with-param name="nodes" select="$nodes"/>
                        <xsl:with-param name="pos" select="$pos"/>
                    </xsl:call-template>
                </xsl:variable>
                <!-- xalan extend function -->
                <xsl:variable name="newnodes" select="xalan:nodeset($new)"/>
                <xsl:call-template name="expression">
                    <xsl:with-param name="nodes" select="$newnodes/*"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:copy-of select="$nodes"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="findFirstDo">
        <xsl:param name="nodes"/>
        <xsl:variable name="result">
            <xsl:for-each select="$nodes">
                <xsl:if test="name() = 'doOperator' or name() = 'FunctionCall'">
                    <xsl:value-of select="position()"/>
                    <xsl:text>firststop</xsl:text>
                </xsl:if>
            </xsl:for-each>
            <xsl:text>0firststop</xsl:text>
        </xsl:variable>
        <!-- 
<xsl:message>
<xsl:copy-of select="$result"/>
</xsl:message>
-->
        <xsl:copy-of select="substring-before($result,'firststop')"/>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="dealFirstDo">
        <xsl:param name="nodes"/>
        <xsl:param name="pos"/>
        <xsl:variable name="opcode">
            <xsl:value-of select="$nodes[position() = number($pos)]/@opcode"/>
        </xsl:variable>
        <xsl:variable name="funcnode" select="$nodes[position() = number($pos)-2]"/>
        <xsl:variable name="funcname">
            <xsl:choose>
                <xsl:when test="number($opcode)=22">
                    <xsl:text>,</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="mapFuncName">
                        <xsl:with-param name="funcname" select="$funcnode/@Name"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <!-- 
<xsl:message>
<xsl:text>In recursion </xsl:text>
<xsl:text> opcode=</xsl:text>
<xsl:copy-of select="$opcode"/>
<xsl:text> funcname=</xsl:text>
<xsl:value-of select="$funcname"/>
<xsl:text> nodename=</xsl:text>
<xsl:copy-of select="name($funcnode)"/>
<xsl:text> pos=</xsl:text>
<xsl:copy-of select="$pos"/>
</xsl:message>
-->
        <xsl:choose>
            <!-- function call -->
            <xsl:when test="$opcode = 21">
                <xsl:copy-of select="$nodes[position() &lt; number($pos)-2] "/>
                <Apply>
                    <xsl:attribute name="function">
                        <xsl:value-of select="$funcname"/>
                    </xsl:attribute>
                    <xsl:call-template name="parseExpression">
                        <xsl:with-param name="nodes" select="$nodes[position() = number($pos)-1]/*"
                        />
                    </xsl:call-template>
                </Apply>
            </xsl:when>
            <!-- menus -->
            <xsl:when test="$opcode = 33">
                <xsl:copy-of select="$nodes[position() &lt; number($pos)-2] "/>
		<xsl:if test="($nodes[position() = number($pos)-2])/@Name ='-'">
		        <xsl:choose>
		            <xsl:when test="($nodes[position() = number($pos)-1])[name()='Constant']">
			        <Constant dataType="double">
				    <xsl:value-of select="-($nodes[position() = number($pos)-1])"/>
			        </Constant>
		            </xsl:when>
		            <xsl:otherwise> 		
                                <Apply function="*">
                                    <Constant dataType="double">-1</Constant>
                                    <xsl:copy-of select="$nodes[position() = number($pos)-1]"/>
                                </Apply>
		            </xsl:otherwise>
		        </xsl:choose>
		</xsl:if>
            </xsl:when>
            <!-- commas -->
            <xsl:when test="$opcode = 22">
                <xsl:copy-of select="$nodes[position() &lt; number($pos)-2] "/>
                <xsl:copy-of select="$nodes[position() = number($pos)-1]"/>
            </xsl:when>
			<!-- Special process for comparsion operator -->
			<xsl:when test="$opcode &lt; 7 and name($funcnode) = 'StackOperator'">
				<xsl:copy-of select="$nodes[position() &lt; number($pos)-3] "/>
                <Apply function="if">
					<Apply>
						<xsl:attribute name="function">
							<xsl:value-of select="$funcname"/>
						</xsl:attribute>
						<xsl:copy-of select="$nodes[position() = number($pos)-3]"/>
						<xsl:copy-of select="$nodes[position() = number($pos)-1]"/>
					</Apply>
                <Constant dataType="double">1</Constant> 
                <Constant dataType="double">0</Constant> 
				</Apply>
			</xsl:when>				
            <!-- other operator -->
            <xsl:when test="name($funcnode) = 'StackOperator'">
                <xsl:copy-of select="$nodes[position() &lt; number($pos)-3] "/>
                <Apply>
                    <xsl:attribute name="function">
                        <xsl:value-of select="$funcname"/>
                    </xsl:attribute>
                    <xsl:copy-of select="$nodes[position() = number($pos)-3]"/>
                    <xsl:copy-of select="$nodes[position() = number($pos)-1]"/>
                </Apply>
            </xsl:when>
            <xsl:otherwise>
                <xsl:message>Error to find opcode.</xsl:message>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:copy-of select="$nodes[position() > number($pos)] "/>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="mapFuncName">
        <xsl:param name="funcname"/>
        <xsl:variable name="lowname"
            select="translate($funcname,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
        <xsl:choose>
            <xsl:when test="$lowname = '+'">
                <xsl:text>+</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = '-'">
                <xsl:text>-</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = '*'">
                <xsl:text>*</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = '/'">
                <xsl:text>/</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = '**'">
                <xsl:text>pow</xsl:text>
            </xsl:when>
			<!-- ECM00141616 required. Add new link funcion/-->
            <xsl:when test="$lowname = 'and'">
                <xsl:text>and</xsl:text>
            </xsl:when>	
            <xsl:when test="$lowname = 'not'">
                <xsl:text>not</xsl:text>
            </xsl:when>	
            <xsl:when test="$lowname = 'or'">
                <xsl:text>or</xsl:text>
            </xsl:when>	
            <xsl:when test="$lowname = 'equal'">
                <xsl:text>equal</xsl:text>
            </xsl:when>	
 			<xsl:when test="$lowname = 'eq'">
                <xsl:text>equal</xsl:text>
            </xsl:when>
			<xsl:when test="$lowname = 'notequal'">
                <xsl:text>notEqual</xsl:text>
            </xsl:when>	
 			<xsl:when test="$lowname = 'ne'">
                <xsl:text>notEqual</xsl:text>
            </xsl:when>	
			<xsl:when test="$lowname = 'lessthan'">
                <xsl:text>lessThan</xsl:text>
            </xsl:when>		
 			<xsl:when test="$lowname = 'lt'">
                <xsl:text>lessThan</xsl:text>
            </xsl:when>	
			<xsl:when test="$lowname = 'greaterthan'">
                <xsl:text>greaterThan</xsl:text>
            </xsl:when>		
 			<xsl:when test="$lowname = 'gt'">
                <xsl:text>greaterThan</xsl:text>
            </xsl:when>	
			<xsl:when test="$lowname = 'greaterorequal'">
                <xsl:text>greaterOrEqual</xsl:text>
            </xsl:when>				
 			<xsl:when test="$lowname = 'ge'">
                <xsl:text>greaterOrEqual</xsl:text>
            </xsl:when>	
			<xsl:when test="$lowname = 'lessorequal'">
                <xsl:text>lessOrEqual</xsl:text>
            </xsl:when>	
			<xsl:when test="$lowname = 'le'">
                <xsl:text>lessOrEqual</xsl:text>
            </xsl:when>			
            <xsl:when test="$lowname = 'missing'">
                <xsl:text>isMissing</xsl:text>
            </xsl:when>					
 			
            <!-- comma is just to seperate parameters of function 
<xsl:when test="$lowname = ','">
<xsl:text>,</xsl:text>
</xsl:when>
-->
            <xsl:when test="$lowname = 'abs'">
                <xsl:text>abs</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'lg10'">
                <xsl:text>log10</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'exp'">
                <xsl:text>exp</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'ln'">
                <xsl:text>ln</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'rnd'">
                <xsl:text>round</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'pow'">
                <xsl:text>pow</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'sqrt'">
                <xsl:text>sqrt</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'max'">
                <xsl:text>max</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'min'">
                <xsl:text>min</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'mean'">
                <xsl:text>avg</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'sum'">
                <xsl:text>sum</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'upcase'">
                <xsl:text>uppercase</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.upcase'">
	        <xsl:text>uppercase</xsl:text>
            </xsl:when>
            <!-- 
<xsl:when test="$lowname = 'eq'">
<xsl:text>=</xsl:text>
</xsl:when>
<xsl:when test="$lowname = 'ne' or $funcname = '¬ =' or $funcname = '&lt;&gt;'">
<xsl:text>~=</xsl:text>
</xsl:when>
<xsl:when test="$lowname = 'lt'">
<xsl:text>&lt;</xsl:text>
</xsl:when>
<xsl:when test="$lowname = 'le'">
<xsl:text>&lt;=</xsl:text>
</xsl:when>
<xsl:when test="$lowname = 'gt'">
<xsl:text>></xsl:text>
</xsl:when>
<xsl:when test="$lowname = 'ge'">
<xsl:text>threshold</xsl:text>
</xsl:when>
-->
            <xsl:when test="$lowname = 'mod'">
                <xsl:text>mod</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'cdf.normal'">
                <xsl:text>cdf.normal</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'cdfnorm'">
                <xsl:text>cdfnorm</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'trunc'">
                <xsl:text>floor</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.trunc'">
	        <xsl:text>floor</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'idf.normal'">
                <xsl:text>idf.normal</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'sysmis'">
                <xsl:text>sysmis</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'value'">
                <xsl:text>value</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'pdf.normal'">
                <xsl:text>pdf.normal</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'sd'">
                <xsl:text>sd</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'variance'">
                <xsl:text>variance</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'concat'">
                <xsl:text>concat</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.concat'">
	        <xsl:text>concat</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'length'">
                <xsl:text>length</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.length'">
	        <xsl:text>length</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'lower'">
                <xsl:text>lower</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.lower'">
	        <xsl:text>lower</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'ltrim'">
                <xsl:text>ltrim</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.ltrim'">
	        <xsl:text>ltrim</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'rtrim'">
                <xsl:text>rtrim</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.rtrim'">
	        <xsl:text>rtrim</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'substr'">
                <xsl:text>substr</xsl:text>
            </xsl:when>
            <xsl:when test="$lowname = 'char.substr'">
	        <xsl:text>substr</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:message terminate="yes">
                    <xsl:text>CVT_FuncErr:</xsl:text>
                    <xsl:value-of select="$lowname"/>
                </xsl:message>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="DefineFunc">
        <xsl:param name="funclist"/>
        <xsl:param name="funcdef"/>
        <xsl:choose>
            <xsl:when test="count($funclist) &gt; 0">
                <xsl:variable name="funcdef0">
                    <xsl:copy-of select="$funcdef"/>
                    <xsl:variable name="lowname"
                        select="translate($funclist[position()=1]/@Name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
                    <xsl:choose>
                        <xsl:when test="$funcdef[@name = $lowname]"/>
                        <xsl:otherwise>
                            <xsl:choose>
<!--                                <xsl:when test="$lowname = 'mean'">
                                     Y=mean(x1, x2,……)
xi: double 
Return: double 
Note: This function requires two or more arguments.

                                    <DefineFunction name="mean" dataType="double"
                                        optype="continuous">
                                        <ParameterField name="xi" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="mean"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>-->
<!--                                <xsl:when test="$lowname = 'mod'">
                                     Y=Mod(x1,x2) x1 and x2: double; but x2 not equal to 0

                                    <DefineFunction name="mod" dataType="double" optype="continuous">
                                        <ParameterField name="x1" dataType="double"
                                            optype="continuous"/>
                                        <ParameterField name="x2" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="mod"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>-->
								<!-- Update mod DefineFunction as Svetlana suggestion to follow ADP change-->
								<xsl:when test="$lowname = 'mod'">
									<DefineFunction name="mod" dataType="integer" optype="continuous">
										<ParameterField name="A" /> 
										<ParameterField name="B" /> 
										<Apply function="-">
											<FieldRef field="A" /> 
											<Apply function="*">
												<FieldRef field="B" /> 
												<Apply function="floor">
													<Apply function="/">
														<FieldRef field="A" /> 
														<FieldRef field="B" /> 
													</Apply>
												</Apply>
											</Apply>
										</Apply>
									</DefineFunction>							
								</xsl:when>
                                <xsl:when test="$lowname = 'cdf.normal'">
                                    <!-- Y=Cdfnorm(x) x: double  Return: double
-->
                                    <DefineFunction name="cdf.normal" dataType="double"
                                        optype="continuous">
                                        <ParameterField name="x1" dataType="double"
                                            optype="continuous"/>
                                        <ParameterField name="x2" dataType="double"
                                            optype="continuous"/>
                                        <ParameterField name="x3" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="cdf.normal"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'cdfnorm'">
                                    <!-- Y=Cdfnorm(x) x: double  Return: double
-->
                                    <DefineFunction name="cdfnorm" dataType="double"
                                        optype="continuous">
                                        <ParameterField name="x" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="cdfnorm"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
<!--                                <xsl:when test="$lowname = 'trunc'">
                                     Y=Trunc(x) x: double; Return: integer

                                    <DefineFunction name="trunc" dataType="integer"
                                        optype="continuous">
                                        <ParameterField name="x" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="trunc"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>-->
                                <xsl:when test="$lowname = 'idf.normal'">
                                    <!-- Y=ldf.Normal(x1,x2,x3)
x1, x2 and x3: double
Return: double
-->
                                    <DefineFunction name="idf.normal" dataType="double"
                                        optype="continuous">
                                        <ParameterField name="x1" dataType="double"
                                            optype="continuous"/>
                                        <ParameterField name="x2" dataType="double"
                                            optype="continuous"/>
                                        <ParameterField name="x3" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="idf.normal"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'sysmis'">
                                    <!-- Y=Sysmis(x)
x: name of numeric variable
Return: Logical ????
-->
                                    <DefineFunction name="sysmis" dataType="integer"
                                        optype="continuous">
                                        <ParameterField name="x" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="sysmis"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'value'">
                                    <!-- Y=Value(variable name)
Return: double or string	????
-->
                                    <DefineFunction name="value" dataType="double"
                                        optype="continuous">
                                        <ParameterField name="x" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="value"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'pdf.normal'">
                                    <!-- Y=Pdf.Normal(x1,x2,x3)
x1,x2 and x3: double
Return: double
-->
                                    <DefineFunction name="pdf.normal" dataType="double"
                                        optype="continuous">
                                        <ParameterField name="x1" dataType="double"
                                            optype="continuous"/>
                                        <ParameterField name="x2" dataType="double"
                                            optype="continuous"/>
                                        <ParameterField name="x3" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="pdf.normal"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'sd'">
                                    <!-- Y=Sd(x1, x2,……)
xi: double 
Return: double 
Note: This function requires two or more arguments.
-->
                                    <DefineFunction name="sd" dataType="double" optype="continuous">
                                        <ParameterField name="xi" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="sd"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'variance'">
                                    <!-- Y=Variance(x1, x2,……)
xi: double 
Return: double 
Note: This function requires two or more arguments.
-->
                                    <DefineFunction name="variance" dataType="double"
                                        optype="continuous">
                                        <ParameterField name="xi" dataType="double"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="variance"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'concat'">
                                    <!-- Y=Concat(x1, x2,……)
xi: string 
Return: string
Note: This function requires two or more arguments.
-->
                                    <DefineFunction name="concat" dataType="string"
                                        optype="categorical">
                                        <ParameterField name="xi" dataType="string"
                                            optype="categorical"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="concat"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'length'">
                                    <!-- 
Y=Length(x)
x: string
return: double
-->
                                    <DefineFunction name="length" dataType="integer"
                                        optype="continuous">
                                        <ParameterField name="x" dataType="string"
                                            optype="categorical"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="length"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'lower'">
                                    <!-- Y=lower(x)
x: string
Return: string
-->
                                    <DefineFunction name="lower" dataType="string"
                                        optype="categorical">
                                        <ParameterField name="x" dataType="string"
                                            optype="categorical"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="lower"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'ltrim'">
                                    <!-- Y=Ltrim(x)
x: string
Return: string
-->
                                    <DefineFunction name="ltrim" dataType="string"
                                        optype="categorical">
                                        <ParameterField name="x" dataType="string"
                                            optype="categorical"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="ltrim"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'rtrim'">
                                    <!--Y=Rtrim(x)
x: string
Return: string
-->
                                    <DefineFunction name="rtrim" dataType="string"
                                        optype="categorical">
                                        <ParameterField name="x" dataType="string"
                                            optype="categorical"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="rtrim"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:when test="$lowname = 'substr'">
                                    <!--Y=Substr(x1,x2)
X1: string
X2: integer 
Return: string ,and if x2 GT length of x1 ,return empty string
-->
                                    <DefineFunction name="substr" dataType="string"
                                        optype="categorical">
                                        <ParameterField name="x1" dataType="string"
                                            optype="categorical"/>
                                        <ParameterField name="x2" dataType="integer"
                                            optype="continuous"/>
                                        <Apply function="dummyfunction">
                                            <Extension extender="spss.com"
                                                name="transformationFunction" value="substr"/>
                                        </Apply>
                                    </DefineFunction>
                                </xsl:when>
                                <xsl:otherwise/>
                            </xsl:choose>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>
                <xsl:call-template name="DefineFunc">
                    <xsl:with-param name="funclist" select="$funclist[position() &gt; 1]"/>
                    <xsl:with-param name="funcdef" select="xalan:nodeset($funcdef0)/*"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:copy-of select="$funcdef"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--Compute end   ************************************************************************-->
    <!--**************************************************************************************-->
    <!--Variable begin************************************************************************-->
    <!--**************************************************************************************-->
    <xsl:template name="mapdataType">
        <xsl:param name="type"/>
        <xsl:choose>
            <xsl:when test="$type = 'number'">
                <xsl:text>double</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>string</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="mapoptype">
        <xsl:param name="type"/>
        <xsl:choose>
            <xsl:when test="$type = 1">
                <xsl:text>categorical</xsl:text>
            </xsl:when>
            <xsl:when test="$type = 2">
                <xsl:text>ordinal</xsl:text>
            </xsl:when>
            <xsl:when test="$type = 3">
                <xsl:text>continuous</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>continuous</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="findVariable">
        <xsl:param name="curvar"/>
        <xsl:param name="vars"/>
        <!-- 
<xsl:message>
<xsl:text>In name=findVariable</xsl:text>
<xsl:text>  varscount=</xsl:text>
<xsl:if test="$vars">
<xsl:value-of select="count($vars)"/>
</xsl:if>
<xsl:text>  curvarname=</xsl:text>
<xsl:value-of select="$curvar/@VarName"/>
<xsl:text>  vars1name=</xsl:text>
<xsl:if test="$vars">
<xsl:value-of select="$vars[position()=1]/@name"/>
</xsl:if>
</xsl:message>
-->
        <xsl:choose>
            <xsl:when test="$vars">
                <xsl:choose>
                    <xsl:when test="$vars[translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        'abcdefghijklmnopqrstuvwxyz')=translate($curvar/@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        'abcdefghijklmnopqrstuvwxyz')]">
                        <xsl:text>true</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>false</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>false</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="Variable">
        <xsl:param name="curnode"/>
        <xsl:param name="datavars"/>
        <xsl:param name="transvars"/>
        <xsl:param name="type"/>
        <!-- 
<xsl:message>
<xsl:text>In name=Variable1</xsl:text>
<xsl:text>  varname=</xsl:text>
<xsl:value-of select="$curnode/@VarName"/>
<xsl:text>  datavarscount=</xsl:text>
<xsl:value-of select="count($datavars)"/>
<xsl:text>  transvarscount=</xsl:text>
<xsl:if test="$transvars">
<xsl:value-of select="count($transvars)"/>
</xsl:if>
</xsl:message>
-->
        <xsl:variable name="findindata">
            <xsl:call-template name="findVariable">
                <xsl:with-param name="curvar" select="$curnode"/>
                <xsl:with-param name="vars" select="$datavars"/>
            </xsl:call-template>
        </xsl:variable>
        <!-- 
<xsl:message>
<xsl:text>In name=Variable1.1</xsl:text>
<xsl:text>  varname=</xsl:text>
<xsl:value-of select="$curnode/@VarName"/>
<xsl:text>  findindata=</xsl:text>
<xsl:value-of select="$findindata"/>
</xsl:message>
-->
        <xsl:variable name="findintrans">
            <xsl:call-template name="findVariable">
                <xsl:with-param name="curvar" select="$curnode"/>
                <xsl:with-param name="vars" select="$transvars"/>
            </xsl:call-template>
        </xsl:variable>
        <!-- 
<xsl:message>
<xsl:text>In name=Variable2</xsl:text>
<xsl:text>  varname=</xsl:text>
<xsl:value-of select="$curnode/@VarName"/>
<xsl:text>  findindata=</xsl:text>
<xsl:value-of select="$findindata"/>
<xsl:text>  findintrans=</xsl:text>
<xsl:value-of select="$findintrans"/>
</xsl:message>
-->
        <xsl:variable name="varname">
            <xsl:value-of select="$curnode/@VarName"/>
        </xsl:variable>
        <xsl:variable name="isfind">
            <xsl:choose>
                <xsl:when test="name() = 'Transformation' and $findindata = 'true' and $findintrans
                    = 'true'">
                    <xsl:text>true</xsl:text>
                    <xsl:message terminate="yes">
                        <!-- 
<xsl:text>DataField varname( </xsl:text>
<xsl:value-of select="$varname"/>
<xsl:text> ) is same with another DataField  and  DerivedField varnames.</xsl:text>
-->
                        <xsl:text>CVT_ReVarsErr:</xsl:text>
                        <xsl:value-of select="$varname"/>
                    </xsl:message>
                </xsl:when>
                <xsl:when test="name() = 'Transformation' and $findindata = 'true'">
                    <xsl:text>true</xsl:text>
                    <!-- 
<xsl:message>
<xsl:text>WARNING: DataField varname( </xsl:text>
<xsl:value-of select="$varname"/>
<xsl:text> ) is same with another DataField varname.</xsl:text>
</xsl:message>
-->
                </xsl:when>
                <xsl:when test="name() = 'Transformation' and $findintrans = 'true'">
                    <xsl:text>true</xsl:text>
                    <!-- 
<xsl:message>
<xsl:text>WARNING: DataField varname( </xsl:text>
<xsl:value-of select="$varname"/>
<xsl:text> ) is same with another DerivedField varname.</xsl:text>
</xsl:message>
-->
                </xsl:when>
                <xsl:when test="$findindata = 'true' and $findintrans = 'true'">
                    <xsl:text>true</xsl:text>
                    <xsl:message terminate="yes">
                        <!--
<xsl:text>DerivedField varname( </xsl:text>
<xsl:value-of select="$varname"/>
<xsl:text> ) is same with another DataField and  DerivedField varnames.</xsl:text>
-->
                        <xsl:text>CVT_ReVarsErr:</xsl:text>
                        <xsl:value-of select="$varname"/>
                    </xsl:message>
                </xsl:when>
                <xsl:when test="$findindata = 'true'">
                    <xsl:text>true</xsl:text>
                    <xsl:message terminate="yes">
                        <!--
<xsl:text>DerivedField varname( </xsl:text>
<xsl:value-of select="$varname"/>
<xsl:text> ) is same with another DataField varname.</xsl:text>
-->
                        <xsl:text>CVT_ReVarsErr:</xsl:text>
                        <xsl:value-of select="$varname"/>
                    </xsl:message>
                </xsl:when>
                <xsl:when test="$findintrans = 'true'">
                    <xsl:text>true</xsl:text>
                    <xsl:message terminate="yes">
                        <!--
<xsl:text>DerivedField varname( </xsl:text>
<xsl:value-of select="$varname"/>
<xsl:text> ) is same with another DerivedField varname.</xsl:text>
-->
                        <xsl:text>CVT_ReVarsErr:</xsl:text>
                        <xsl:value-of select="$varname"/>
                    </xsl:message>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>false</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:if test="$isfind = 'false'">
            <xsl:attribute name="name">
                <xsl:value-of select="$varname"/>
            </xsl:attribute>
            <xsl:attribute name="dataType">
                <xsl:call-template name="mapdataType">
                    <xsl:with-param name="type" select="$curnode/@datatype"/>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:attribute name="optype">
                <xsl:call-template name="mapoptype">
                    <xsl:with-param name="type" select="$curnode/@optype"/>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:variable name="nodes1"
                select="/SPSS/Transformation/VariableLabels[translate(@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'abcdefghijklmnopqrstuvwxyz')=translate($varname,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'abcdefghijklmnopqrstuvwxyz')]"/>
            <xsl:choose>
                <xsl:when test="$nodes1">
                    <xsl:attribute name="displayName">
                        <xsl:value-of select="$nodes1[position()=count($nodes1)]/@Label"/>
                    </xsl:attribute>
                </xsl:when>
                <xsl:when test="$curnode/@Label">
                    <xsl:attribute name="displayName">
                        <xsl:value-of select="$curnode/@Label"/>
                    </xsl:attribute>
                </xsl:when>
            </xsl:choose>
            <xsl:variable name="nodes2"
                select="/SPSS/Transformation/VariableLevel/Variable[translate(@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'abcdefghijklmnopqrstuvwxyz')=translate($varname,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                'abcdefghijklmnopqrstuvwxyz')]"/>
            <!-- 
<xsl:message>
<xsl:text>Variable10</xsl:text>
<xsl:text>nodes2 count=</xsl:text><xsl:value-of select="count($nodes2)"/>
</xsl:message>
<xsl:variable name="nodes21"
select="/SPSS/Transformation/VariableLevel/Variable[@VarName=$varname] or $curnode"/>
<xsl:message>
<xsl:text>Variable11</xsl:text>
<xsl:text>nodes21 count=</xsl:text><xsl:value-of select="count($nodes21)"/>
</xsl:message>
            -->
            <xsl:variable name="curoptype">
                <xsl:choose>
                    <xsl:when test="$nodes2">
                        <xsl:call-template name="mapoptype">
                            <xsl:with-param name="type"
                                select="$nodes2[position()=count($nodes2)]/@optype"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="$curnode/@optype">
                        <xsl:call-template name="mapoptype">
                            <xsl:with-param name="type" select="$curnode/@optype"/>
                        </xsl:call-template>
                    </xsl:when>
                </xsl:choose>
            </xsl:variable>
            <xsl:attribute name="optype">
                <xsl:value-of select="$curoptype"/>
            </xsl:attribute>
            <xsl:if test="$curnode/StringLength">
                <Extension extender="spss.com" name="stringLength">
                    <xsl:attribute name="value">
                        <xsl:value-of select="$curnode/StringLength/@length"/>
                    </xsl:attribute>
                </Extension>
            </xsl:if>
            <xsl:variable name="missingvalues">
                <xsl:variable name="nodes3"
                    select="/SPSS/Transformation/MissingValues/VariableList/Variable[translate(@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                    'abcdefghijklmnopqrstuvwxyz')=translate($varname,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                    'abcdefghijklmnopqrstuvwxyz')]/../.."/>
                <xsl:choose>
                    <xsl:when test="$nodes3">
                        <xsl:call-template name="MissingValues">
                            <xsl:with-param name="node" select="$nodes3[position()=count($nodes3)]"/>
                            <xsl:with-param name="type" select="$type"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="$curnode/MissingValues">
                        <xsl:call-template name="MissingValues">
                            <xsl:with-param name="node" select="$curnode/MissingValues"/>
                            <xsl:with-param name="type" select="$type"/>
                        </xsl:call-template>
                    </xsl:when>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="missingvaluesnode" select="xalan:nodeset($missingvalues)"/>
            <xsl:variable name="valuelabels">
                <xsl:variable name="nodes4a"
                    select="/SPSS/Transformation/ValueLabels/VariableList/Variable[translate(@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                    'abcdefghijklmnopqrstuvwxyz')=translate($varname,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                    'abcdefghijklmnopqrstuvwxyz')]/../.."/>
                <xsl:variable name="nodes4b"
                    select="/SPSS/Transformation/AddValueLabels/VariableList/Variable[translate(@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                    'abcdefghijklmnopqrstuvwxyz')=translate($varname,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                    'abcdefghijklmnopqrstuvwxyz')]/../.."/>
                <xsl:choose>
                    <xsl:when test="$nodes4a">
                        <xsl:variable name="nodes4">
                            <xsl:copy-of select="$nodes4a[position()=count($nodes4a)]/*"/>
                            <xsl:copy-of select="$nodes4b/*"/>
                        </xsl:variable>
                        <xsl:variable name="nodes4nodes" select="xalan:nodeset($nodes4)"/>
                        <xsl:call-template name="ValueLabels">
                            <xsl:with-param name="nodes" select="$nodes4nodes/*"/>
                            <xsl:with-param name="name" select="$varname"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="$curnode/ValueLabels">
                        <xsl:variable name="nodes4">
                            <xsl:copy-of select="$curnode/ValueLabels/*"/>
                            <xsl:copy-of select="$nodes4b/*"/>
                        </xsl:variable>
                        <xsl:variable name="nodes4nodes" select="xalan:nodeset($nodes4)"/>
                        <xsl:call-template name="ValueLabels">
                            <xsl:with-param name="nodes" select="$nodes4nodes/*"/>
                            <xsl:with-param name="name" select="$varname"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:call-template name="ValueLabels">
                            <xsl:with-param name="nodes" select="$nodes4b/*"/>
                            <xsl:with-param name="name" select="$varname"/>
                        </xsl:call-template>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="valuelabelsnode" select="xalan:nodeset($valuelabels)"/>
            <xsl:variable name="parsedlist">
                <xsl:call-template name="ParseValues">
                    <xsl:with-param name="missings" select="$missingvaluesnode/*"/>
                    <xsl:with-param name="labels" select="$valuelabelsnode/*"/>
                </xsl:call-template>
            </xsl:variable>
            <xsl:variable name="parsedlistnode" select="xalan:nodeset($parsedlist)"/>
            <xsl:choose>
                <xsl:when test="$curoptype='continuous'">
                    <xsl:copy-of select="$parsedlistnode/Extension"/>
                    <xsl:copy-of select="$parsedlistnode/Value[@property='missing']"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy-of select="$parsedlistnode/*"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="ParseValues">
        <xsl:param name="missings"/>
        <xsl:param name="labels"/>
        <xsl:for-each select="$missings">
            <xsl:choose>
                <xsl:when test="name()='Value'">
                    <Value property="missing">
                        <xsl:attribute name="value">
                            <xsl:value-of select="./@value"/>
                        </xsl:attribute>
                        <xsl:variable name="display">
                            <xsl:choose>
                                <xsl:when test="$labels[name()='Value' and @value=./@value]">
                                    <xsl:value-of select="$labels[name()='Value' and
                                        @value=./@value]/@displayValue"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="./@displayValue"/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:variable>
                        <xsl:if test="$display!=''">
                            <xsl:attribute name="displayValue">
                                <xsl:copy-of select="$display"/>
                            </xsl:attribute>
                        </xsl:if>
                    </Value>
                </xsl:when>
                <xsl:when test="name()='Extension' and ./@name='MissingValues'">
                    <Extension extender="spss.com" name="MissingValues">
                        <xsl:for-each select="./*">
                            <xsl:choose>
                                <xsl:when test="name()='Value'">
                                    <xsl:variable name="value" select="./@value"/>
                                    <Value>
                                        <xsl:attribute name="value">
                                            <xsl:value-of select="./@value"/>
                                        </xsl:attribute>
                                        <xsl:variable name="display">
                                            <xsl:choose>
                                                <xsl:when test="$labels[name()='Value' and
                                                  @value=$value]">
                                                  <xsl:value-of select="$labels[name()='Value' and
                                                  @value=$value]/@displayValue"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                  <xsl:value-of select="./@displayValue"/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:variable>
                                        <xsl:if test="$display!=''">
                                            <xsl:attribute name="displayValue">
                                                <xsl:copy-of select="$display"/>
                                            </xsl:attribute>
                                        </xsl:if>
                                    </Value>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:copy-of select="."/>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:for-each>
                    </Extension>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
        <xsl:for-each select="$labels">
            <xsl:choose>
                <xsl:when test="name()='Value'">
                    <xsl:variable name="value" select="./@value"/>
                    <xsl:choose>
                        <xsl:when test="$missings[name()='Value' and @value=$value]"/>
                        <xsl:when test="$missings[name()='Extension']/Value[@value = $value]"/>
                        <xsl:otherwise>
                            <xsl:copy-of select="."/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="ValueLabels">
        <xsl:param name="nodes"/>
        <xsl:param name="name"/>
        <!-- 
<xsl:message>
<xsl:text>  ValueLabels1</xsl:text>
<xsl:text>  Name=</xsl:text>
<xsl:value-of select="$name"/>
<xsl:text>  nodes count=</xsl:text>
<xsl:value-of select="count($nodes)"/>
</xsl:message>
-->
        <xsl:if test="count($nodes) &gt; 0">
            <xsl:choose>
                <xsl:when test="name($nodes)='ValueList'">
                    <xsl:for-each select="$nodes[position()=1]/VarValue">
                        <Value>
                            <xsl:attribute name="value">
                                <xsl:value-of select="./@Value"/>
                            </xsl:attribute>
                            <xsl:attribute name="displayValue">
                                <xsl:value-of select="./@Label"/>
                            </xsl:attribute>
                        </Value>
                    </xsl:for-each>
                    <xsl:call-template name="ValueLabels">
                        <xsl:with-param name="nodes" select="$nodes[position() &gt; 1]"/>
                        <xsl:with-param name="name" select="$name"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:when test="name($nodes)='VariableList'">
                    <xsl:choose>
                        <xsl:when
                            test="$nodes[position()=1]/Variable[translate(@VarName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                            'abcdefghijklmnopqrstuvwxyz')=translate($name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                            'abcdefghijklmnopqrstuvwxyz')]">
                            <xsl:call-template name="ValueLabels">
                                <xsl:with-param name="nodes" select="$nodes[position() &gt; 1]"/>
                                <xsl:with-param name="name" select="$name"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:call-template name="ValueLabels">
                                <xsl:with-param name="nodes" select="$nodes[position() &gt; 2]"/>
                                <xsl:with-param name="name" select="$name"/>
                            </xsl:call-template>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="ValueLabels">
                        <xsl:with-param name="nodes" select="$nodes[position() &gt; 1]"/>
                        <xsl:with-param name="name" select="$name"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    <!--**************************************************************************************-->
    <xsl:template name="MissingValues">
        <xsl:param name="node"/>
        <xsl:param name="type"/>
        <!-- 
<xsl:message>
<xsl:text>In MissingValues1</xsl:text>
<xsl:value-of select="$type"/>
</xsl:message>
-->
        <xsl:if test="$node/ValueList/*">
            <xsl:choose>
                <xsl:when test="$type='derived'">
                    <Extension extender="spss.com" name="MissingValues">
                        <xsl:for-each select="$node/ValueList/*">
                            <xsl:choose>
                                <xsl:when test="name()='Constant'">
                                    <Value>
                                        <xsl:attribute name="value">
                                            <xsl:value-of select="./@Value"/>
                                        </xsl:attribute>
                                    </Value>
                                </xsl:when>
                                <xsl:when test="name()='BetweenValue'">
                                    <Interval closure="closedClosed">
                                        <xsl:variable name="upLoValue"
                                            select="translate(./LoValue/@Value,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                                        <xsl:if test="starts-with($upLoValue, 'LO') = false">
                                            <xsl:attribute name="leftMargin">
                                                <xsl:value-of select="./LoValue/@Value"/>
                                            </xsl:attribute>
                                        </xsl:if>
                                        <xsl:variable name="upHiValue"
                                            select="translate(./HiValue/@Value,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                                        <xsl:if test="starts-with(./HiValue/@Value, 'HI') = false">
                                            <xsl:attribute name="rightMargin">
                                                <xsl:value-of select="./HiValue/@Value"/>
                                            </xsl:attribute>
                                        </xsl:if>
                                    </Interval>
                                </xsl:when>
                            </xsl:choose>
                        </xsl:for-each>
                    </Extension>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:for-each select="$node/ValueList/*">
                        <xsl:sort select="name()"/>
                        <xsl:choose>
                            <xsl:when test="name()='Constant'">
                                <Value property="missing">
                                    <xsl:attribute name="value">
                                        <xsl:value-of select="./@Value"/>
                                    </xsl:attribute>
                                </Value>
                            </xsl:when>
                            <xsl:when test="name()='BetweenValue'">
                                <Extension extender="spss.com" name="invalidRangeLower">
                                    <xsl:variable name="upLoValue"
                                        select="translate(./LoValue/@Value,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                                    <xsl:choose>
                                        <xsl:when test="starts-with($upLoValue, 'LO') = false">
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="./LoValue/@Value"/>
                                            </xsl:attribute>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="LOWEST"/>
                                            </xsl:attribute>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </Extension>
                                <Extension extender="spss.com" name="invalidRangeUpper">
                                    <xsl:variable name="upHiValue"
                                        select="translate(./HiValue/@Value,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
                                    <xsl:choose>
                                        <xsl:when test="starts-with(./HiValue/@Value, 'HI') = false">
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="./HiValue/@Value"/>
                                            </xsl:attribute>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:attribute name="value">
                                                <xsl:value-of select="HIGHEST"/>
                                            </xsl:attribute>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </Extension>
                            </xsl:when>
                        </xsl:choose>
                    </xsl:for-each>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    <!--Variable end  ************************************************************************-->
</xsl:stylesheet>
