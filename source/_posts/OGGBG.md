---
title: GoldenGate Big Data 实验
date: 2018-07-19 23:10:40
toc: true
description: GoldenGate Big Data to Redshift/Flat file/Flume/Kafka 测试实验
categories: 
- 技术
tags: 
- OGG
- GoldenGate
---

# GoldenGate Big Data 实验
---

## Install GoldenGate Big Data
1. Request Install JDK 8 on OS
2. Configure Variables on OS
```
export JAVA_HOME=/usr/java/jdk1.8.0_121 
export JRE_HOME=/usr/java/jdk1.8.0_121/jre
export CLASSPATH=$JAVA_HOME/lib:$JRE_HOME/lib:./
export GG_HOME=/data/oggbg
export LD_LIBRARY_PATH=$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/jre/lib/amd64/server:$JAVA_HOME/jre/lib/amd64:$GG_HOME:$GG_HOME/lib
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/lib:$PATH:$GG_HOME
```
3. Installation Steps
	* Create an installation directory that has no spaces in its name. Then extract the ZIP file into this new installation directory. For example:
```
Shell> mkdir installation_directory 
Shell> cp path/to/installation_zip installation_directory 
Shell> cd installation_directory 
Shell> unzip installation_zip 
Shell> tar -xf installation_tar
```
	* Stay on the installation directory and bring up GGSCI to create the remaining subdirectories in the installation location
```
Shell> ggsci 
GGSCI> CREATE SUBDIRS
```
	* Create a Manager parameter file:
```
GGSCI> EDIT PARAM MGR 
PORT 7809
DYNAMICPORTLIST 7810-7909
```
	* Go to GGSCI, start the Manager, and check to see that it is running:
```
GGSCI>START MGR 
GGSCI>INFO MGR
```

## Source Extract Configure
1. Configure Capture Extract Process and Pump Extract Process
	* Capture Extract Process Parameter
**Name:** `egaehio.prm`
```
extract EGAEHIO 
statoptions reportfetch
reportcount 15 minutes, rate
encrypttrail AES128
dynamicresolution 
useridalias ggadmin
logallsupcols
updaterecordformat compact
tranlogoptions includeregionid
dboptions allowunusedcolumn
GETTRUNCATES
exttrail ./dirdat/ga
table EHTEMP.OGG_HADOOP_TEST;
table EHTEMP.EMPLOYEES;
```
	* Pump Extract Process Parameter
**Name:** `pga_ga.prm`
```
extract PGA_GA
passthru
dynamicresolution
reportcount 15 minutes, rate
rmthost sjdevbigdtcon01, mgrport 7809, encrypt AES128
rmttrail ./dirdat/ga
table EHTEMP.OGG_HADOOP_TEST;
table EHTEMP.EMPLOYEES;
```
2. Second, Start Capture and Pump Extract Process
	* command
```
 >ggsci
 >dblogin useridalias ggadmin
 >add trandata EHTEMP.OGG_HADOOP_TEST 
 >add trandata EHTEMP.EMPLOYEES 
 >register extract egaehio database
 >add extract egaehio, integrated tranlog, begin now
 >add exttrail ./dirdat/ga, extract egaehio, megabytes 1000
 >add extract pga_ga, exttrailsource ./dirdat/ga begin now
 >add rmttrail ./dirdat/ga, extract pga_ga, megabytes 1000
 >start extract egaehio
 >start extract pga_ga
```

## GoldenGate Replicate to Redshift
1. Create Table on Redshift
```
DROP TABLE IF EXISTS employees CASCADE;
commit;
CREATE TABLE employees
(
 employee_id     bigint         NOT NULL,
 first_name      varchar(20),
 last_name       varchar(25),
 email           varchar(25),
 phone_number    varchar(20),
 hire_date       date,
 job_id          varchar(10),
 salary          numeric(8,2),
 commission_pct  numeric(2,2),
 manager_id      bigint,
 department_id   bigint
);
commit;
ALTER TABLE employees
 ADD CONSTRAINT pk_employees
 PRIMARY KEY (employee_id);
commit;
```
2. Init Load Data
**On Source**
	* Get SCN Filter Value
```
select current_scn from v$databasse;
```
	* Configure init Extract Process and Generate init trail file
**Name:** `iegared.prm`
```
sourceistable
useridalias ggadmin
RMTHOST sjdevbigdtcon01, MGRPORT 7809
RMTFILE ./dirdat/iegared, MEGABYTES 2, PURGE
table EHTEMP.EMPLOYEES,SQLPREDICATE 'AS OF SCN 61896071442';
```
	**Exec Below Command**
```
./extract paramfile dirprm/iegared.prm reportfile dirrpt/iegared.rpt
```
 **On OGG Big Data Server**
	* Configure Redshift JDBC Parameter
**Name:** `jdbc_redshift.props`
```
gg.handlerlist=jdbcwriter
gg.handler.jdbcwriter.type=jdbc
#Handler properties for Redshift database target
gg.handler.jdbcwriter.DriverClass=com.amazon.redshift.jdbc.Driver
gg.handler.jdbcwriter.connectionURL=jdbc:redshift://10.16.9.81:5439/dev
gg.handler.jdbcwriter.userName=redadmin
gg.handler.jdbcwriter.password=xxxxxxxx
gg.classpath=/data/oggbg/jlib/RedshiftJDBC42-1.2.10.1009.jar
goldengate.userexit.timestamp=utc
goldengate.userexit.writers=javawriter
javawriter.stats.display=TRUE
javawriter.stats.full=TRUE
gg.log=log4j
gg.log.level=INFO
gg.report.time=30sec
javawriter.bootoptions=-Xmx512m -Xms32m -Djava.class.path=.:ggjava/ggjava.jar:./dirprm
```
	* Configure init Replicat Process.
**Name:** `irbigrd.prm`
```
specialrun
end runtime
EXTFILE ./dirdat/iegared
DDL include all
TARGETDB LIBFILE libggjava.so SET property=dirprm/jdbc_redshift.props
REPORTCOUNT EVERY 1 MINUTES, RATE
GROUPTRANSOPS 10000
MAP EHTEMP.EMPLOYEES, TARGET public.EMPLOYEES;
```
	**Exec Below Command**
```
./replicat paramfile dirprm/irbigrd.prm reportfile dirrpt/irbigrd.rpt
```
3. Configure Replicat Process
**Name:** `rjdbcrd.prm`
```
REPLICAT rjdbcrd
DDL include all
DISCARDFILE ./dircrd/redshift.dsc
TARGETDB LIBFILE libggjava.so SET property=dirprm/jdbc_redshift.props
REPORTCOUNT EVERY 1 MINUTES, RATE
GROUPTRANSOPS 1000
MAP EHTEMP.EMPLOYEES, TARGET public.employees;
```
	**Exec Below Command**
```
>ggsci
>add replicat rjdbcrd, exttrail ./dirdat/ga
>start replicat rjdbcrd AFTERCSN 61896071442
```

## GoldenGate Replicate to Flat file
Oracle GoldenGate for Flat File outputs transactional data captured by Oracle GoldenGate to rolling flat files to be consumed by a third party product.Oracle GoldenGate for Flat File is implemented as a user exit provided as a shared library (.so or .dll) that integrates into the Oracle GoldenGate Extract process.
The user exit supports two modes of output:
● DSV . Delimiter Separated Values (commas are an example)
● LDV . Length Delimited Values

It can output data:
● All to one file
● One file per table
● One file per operation code

1. Download GoldenGate Application Adapter
Copy `flatfilewriter.so` library to $OGG_HOME On OGG Big Data Server
2. Generate Table Define file
**Name:** `egadef.prm`
```
defsfile ./dirdef/fflue.def, PURGE
useridalias ggadmin
table EHTEMP.OGG_HADOOP_TEST;
table EHTEMP.EMPLOYEES;
```
	**Exec Below Command**
```
./defgen paramfile ./dirprm/egadef.prm
scp dirdef/fflue.def RemoteHost
```
3. Configure Flat Handler Parameter
**Name:** `ffue.properties`
```
#------------------------
#LOGGING OPTIONS
#------------------------
goldengate.log.logname=ffwriter
goldengate.log.level=INFO
goldengate.log.modules=LOGMALLOC
goldengate.log.level.LOGMALLOC=ERROR
goldengate.log.tostdout=false
goldengate.log.tofile=true
#------------------------
#FLAT FILE WRITER OPTIONS
#------------------------
goldengate.flatfilewriter.writers=dsvwriter
goldengate.userexit.chkptprefix=ffwriter_
#------------------------
# dsvwriter options
#------------------------
dsvwriter.mode=DSV
dsvwriter.rawchars=false
dsvwriter.includebefores=false
dsvwriter.includecolnames=false
dsvwriter.omitvalues=false
dsvwriter.diffsonly=false
dsvwriter.omitplaceholders=false
#dsvwriter.files.onepertable=false
dsvwriter.files.prefix=csv
dsvwriter.files.data.rootdir=./dirout
dsvwriter.files.data.ext=_data.dsv
dsvwriter.files.data.tmpext=_data.dsv.temp
dsvwriter.files.data.rollover.time=10
#dsvwriter.files.data.rollover.size=
dsvwriter.files.data.norecords.timeout=10
dsvwriter.files.control.use=true
dsvwriter.files.control.ext=_data.control
dsvwriter.files.control.rootdir=./dirout
dsvwriter.dsv.nullindicator.chars=<NULL>
dsvwriter.dsv.fielddelim.chars=|
dsvwriter.dsv.linedelim.chars=\n
dsvwriter.dsv.quotes.chars="
dsvwriter.dsv.quotes.escaped.chars=""
dsvwriter.metacols=position,txind,opcode,timestamp,schema,table
dsvwriter.metacols.txind.fixedlen=1
dsvwriter.metacols.txind.begin.chars=B
dsvwriter.metacols.txind.middle.chars=M
dsvwriter.metacols.txind.end.chars=E
dsvwriter.files.formatstring=pump_%s_%t_%d_%05n
#------------------------
# ldvwriter options
#------------------------
ldvwriter.mode=LDV
ldvwriter.rawchars=true
ldvwriter.includebefores=false
ldvwriter.includecolnames=false
ldvwriter.files.onepertable=false
ldvwriter.files.data.rootdir=./dirout
ldvwriter.files.data.ext=.data
ldvwriter.files.data.tmpext=.temp
ldvwriter.files.data.rollover.time=10
ldvwriter.files.data.norecords.timeout=10
ldvwriter.files.control.use=true
ldvwriter.files.control.ext=.ctrl
ldvwriter.files.control.rootdir=./dirout
ldvwriter.metacols=position,timestamp,@TOKEN-RBA,@TOKEN-POS,opcode,txind,schema,table
ldvwriter.metacols.TOKEN-RBA.fixedlen=10
ldvwriter.metacols.TOKEN-POS.fixedlen=10
ldvwriter.metacols.timestamp.fixedlen=26
ldvwriter.metacols.schema.fixedjustify=right
ldvwriter.metacols.schema.fixedpadchar.chars=Y
ldvwriter.metacols.opcode.fixedlen=1
ldvwriter.metacols.opcode.insert.chars=I
ldvwriter.metacols.opcode.update.chars=U
ldvwriter.metacols.opcode.delete.chars=D
ldvwriter.metacols.txind.fixedlen=1
ldvwriter.metacols.txind.begin.chars=B
ldvwriter.metacols.txind.middle.chars=M
ldvwriter.metacols.txind.end.chars=E
ldvwriter.metacols.txind.whole.chars=W
ldvwriter.ldv.vals.missing.chars=M
ldvwriter.ldv.vals.present.chars=P
ldvwriter.ldv.vals.null.chars=N
ldvwriter.ldv.lengths.record.mode=binary
ldvwriter.ldv.lengths.record.length=4
ldvwriter.ldv.lengths.field.mode=binary
ldvwriter.ldv.lengths.field.length=2
ldvwriter.files.rolloveronshutdown=false
ldvwriter.statistics.toreportfile=false
ldvwriter.statistics.period=onrollover
ldvwriter.statistics.tosummaryfile=true
ldvwriter.statistics.overall=true
ldvwriter.statistics.summary.fileformat=schema,table,schemaandtable,total,gctimestamp,ctimestamp
ldvwriter.statistics.summary.delimiter.chars=|
ldvwriter.statistics.summary.eol.chars=\n
ldvwriter.metacols.position.format=dec
ldvwriter.writebuffer.size=36863
```
4. Configure Flat Extract Process On OGG Big Data Server
**Name:** `ffue.prm`
```
Extract ffue
CUserExit flatfilewriter.so CUSEREXIT PassThru IncludeUpdateBefores, PARAMS "dirprm/ffue.properties"
SourceDefs dirsql/fflue.def
table EHTEMP.OGG_HADOOP_TEST;
table EHTEMP.EMPLOYEES;
```
5. Init Load Data
	* Get SCN Filter Value On Source
```
select current_scn from v$databasse;
```
	* Configure init extract process on source
**Name:** `iegaffl.prm`
```
sourceistable
useridalias ggadmin
RMTHOST sjdevbigdtcon01, MGRPORT 7809
RMTFILE ./dirdat/fi000000000, MEGABYTES 2, PURGE
table EHTEMP.OGG_HADOOP_TEST,SQLPREDICATE 'AS OF SCN 61896417495';
table EHTEMP.EMPLOYEES,SQLPREDICATE 'AS OF SCN 61896417495';
```
	**Exec Below Command On Source**
```
./extract paramfile dirprm/iegaffl.prm reportfile dirrpt/iegaffl.rpt
```
	**Exec Below Command On OGG Big Data Server**
```
ggsci> add extract ffue, extTrailSource dirdat/fi
ggsci> info ffue
ggsci> start extract ffue
```
6. Start Replicat Data Process
**Exec Below Command On OGG Big Data Server**
```
ggsci> stop extract ffue
ggsci> delete extract ffue
ggsci> add extract ffue, extTrailSource dirdat/ga
ggsci> start extract ffue AFTERCSN 61896417495
```

## GoldenGate Replicate to Flume
### Flume Configure and Start
### OGG Big Data Replicat to Flume
## GoldenGate Replicate to Kafka
### Kafka Configure and Start
### OGG Big Data Replicat to Kafka