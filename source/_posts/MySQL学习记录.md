---
title: MySQL学习记录
date: 2018-08-01 13:41:22
tags:
---

# MySQL学习记录

##  Communication Protocols
|Protocol|Type of Connections|Support OS|
| - | :-:|
|TCP/IP|Local,remote|ALL|
|Unix socket file|Local|Unix only|
|Named pipe|Local|Windows only|
|Shared memory|Local|Windows only|

* TCP/IP connections are supported by any MySQL server unless the seriver is started with the --skip-networking option
* Unix socket file are supported by all Unix servers
* Named-pipe connections are supported only on windows and only if you use one of the servers that has -nt in its name.However, named piped are disable by default. To enable named-pipe connections,you must start the -nt server with the --enable-named-pipe option
* Shared-memory connections are supported by all Windows servers, but are disabled by default. To enable shared-memory connections, you must start the server with the --shared-memory option.

The different connection methods are not all equally efficient:
* In many Windows configurations, communication via named pipes is much slower than using TCP/IP. You should use named pipes only when you choose to disable TCP/IP (using the --skip-networking startup parameter) or when you can confirm that named pipes actually are faster for your particular setup.
* On Unix, a Unix socket file connection provides better performance than a TCP/IP connection.
* On any platform, an ODBC connection made via MySQL Connector/ODBC is slower than a connection established directly using the native C client library. This is because ODBC is layered on top of the C library, which adds overhead
* On any platform, a JDBC connection made via MySQL Connector/J is likely to be roughly about the same speed as a connection established using the native C client library.

## The SQL Parser and Storage Engine Tiers
The server executes each statement using a two-tier processing model:
* The upper tier includes the SQL parser and optimizer. The server parses each statement to see what kind of request it is, then uses its optimizer to determine how most efficiently to execute the statement. However, this tier does not interact directly with tables named by the statement.
* The lower tier comprises a set of storage engines. The server uses a modular architecture: Each storage engine is a software module to be used for managing tables of a particular type. The storage engine associated with a table directly accesses it to store or retrieve data. MyISAM, MEMORY, and InnoDB are some of the available engines. The use of this modular approach allows storage engines to be easily selected for inclusion in the server at configuration time. New engines also can be added relatively easily.


## How MySQL Uses Disk Space
The MySQL server's data directory to store all the following:
* Database directories. Each database corresponds to single directory under the data directory, regardless of what types of tables you create in the database.
* Table format file (.frm files) that contain a description of table structure. Every table have its ower .frm file,
 located in the appropriate database directory. This is true no matter which storage engine mananges the table.
* Data and index files are created of each table by some storege engines and placed in the appropriate database directory.
* The InnoDB storage engine has its own tablespace and log files.The tablespace contains data and index information for all InnoDB tables, as well as the undo logs that are needed if a transaction must be rolled back. The log files record information about committed transactions and are used to ensure that no data loss occurs. By default, the tablespace and log files are located in the data directory. The default tablespace file is named ibdata1 and the default log files are named ib_logfile0 and ib_logfile1. (It is also possible to configure InnoDB to use one tablespace file per table. In this case, InnoDB creates the tablespace file for a given table in the table's database directory.)
* Server log files and status files. These files contain information about the statements that the server has been processing. Logs are used for replication and data recovery, to obtain information for use in optimizing query performance, and to determine whether operational problems are occurring


## How MySQL Uses Memory
* Thread handlers. The server is multi-threaded, and a thread is like a small process running inside the server. For each client that connects, the server allocates a thread to it to handle the connection. For performance reasons, the server maintains a small cache of thread handlers. If the cache is not full when a client disconnects, the thread is placed in the cache for later reuse. If the cache is not empty when a client connects, a thread from the cache is reused to handle the connection. Thread handler reuse avoids the overhead of repeated handler setup and teardown.
* The server uses several buffers (caches) to hold information in memory for the purpose of avoiding disk access when possible:
  * Grant table buffers. The grant tables store information about MySQL user accounts and the privileges they have. The server loads a copy of the grant tables into memory for fast access-control checking. Client access is checked for every query, so looking up privilege information in memory rather than from the grant tables on disk results in a significant reduction of disk access overhead.
  * A key buffer holds index blocks for MyISAM tables. By caching index blocks in memory, the server often can avoid reading index contents repeatedly from disk for index-based retrievals and other index-related operations such as sorts
  * The table cache holds descriptors for open tables. For frequently used tables, keeping the descriptors in the cache avoids having to open the tables again and again
  * The server supports a query cache that speeds up processing of queries that are issued repeatedly
  * The host cache holds the results of hostname resolution lookups. These results are cached to minimize the number of calls to the hostname resolver
  * The InnoDB storage engine logs information about current transactions in a memory buffer. When a transaction commits, the log buffer is flushed to the InnoDB log files, providing a record on disk that can be used to recommit the transaction if it is lost due to a crash. If the transaction rolls back instead, the flush to disk need not be done at all
* The MEMORY storage engine creates tables that are held in memory. These tables are very fast because no transfer between disk and memory need be done to access their contents
* The server might create internal temporary tables in memory during the course of query processing. If the size of such a table exceeds the value of the tmp_table_size system variable, the server converts it to a MyISAM-format table on disk and increments its Created_tmp_disk_tables status variable
* The server maintains several buffers for each client connection. One is used as a communications buffer for exchanging information with the client. Other buffers are maintained per client for reading tables and for performing join and sort operations.

## Windows MySQL distributions include several servers
* mysqld is the standard server. It includes both the MyISAM and InnoDB storage engines
* mysqld-nt is like mysqld, but includes support for named pipes on NT-based systems such as Windows NT, 2000, XP, and 2003.
* mysqld-max and mysql-max-nt are like mysqld and mysql-nt, but with extra features such as support for additional storage engines that are not included in the non-max servers.
* mysqld-debug contains support for debugging. Normally, you don't choose this server for production use because it has a larger runtime image and uses more memory.

## Choosing a Server Startup/Shutdown Method on Unix
* You can invoke mysqld manually. This is usually not done except for debugging purposes. If you invoke the server this way, error messages go to the terminal by default rather than to the error log.
* mysqld_safe is a shell script that invokes mysqld. The script sets up the error log, and then launches mysqld and monitors it. If mysqld terminates abnormally, mysqld_safe restarts it.
* mysql.server is a shell script that invokes mysqld_safe. It's used as a wrapper around mysqld_safe for systems such as Linux and Solaris that use System V run-level directories. Typically, this script is renamed to mysql when it is installed in a run-level directory.
* mysqld_multi is a Perl script intended to make it easier to manage multiple servers on a single host. It can start or stop servers, or report on whether servers are running.
* The mysqladmin program has a shutdown command. It connects to the server as a client and can shut down local or remote servers.
* The mysql.server script can shut down the local server when invoked with an argument of stop
* The mysqld_multi script has a stop command and can shut down any of the servers that it manages. It does so by invoking mysqladmin

**note:** mysqld_safe has no server shutdown capability. You can use mysqladmin shutdown instead. Note that if you forcibly terminate mysqld by using the kill -9 command to send it a signal, mysqld_safe will detect that mysqld terminated abnormally and will restart it. You can work around this by killing mysqld_safe first and then mysqld, but it's better to use mysqladmin shutdown, which initiates a normal (clean) server shutdown.

## Log and status Files
* The general query log records all statements that the server receives from clients. use --log or --log=file_name
* The binary log records statements that modify data. use --log-bin or --log-bin=file_name . wen can use mysqlbinlog utility dump bin log context.
* The slow query log contains a record of queries that take a long time to execute. use --log-slow-queries or --log-slow-queries=file_name.we can use mysqldumpslow utility analysis slow query.
* The Error Log. Alert log file
* Status Files. PID file


## Client Programs for DBA Work
* mysql is a general-purpose command-line client for sending SQL statements to the server, including those of an administrative nature.
* mysqladmin is an administrative command-line client that helps you manage the server.
* mysqlimport provides a command-line interface to the LOAD DATA INFILE statement. It is used to load data files into tables without having to issue LOAD DATA INFILE statements yourself. mysqlimport can load files located on the client host or on the server host. It can load tables managed by local or remote servers.
* mysqldump is a command-line client for dumping the contents of databases and tables. It's useful for making backups or for copying databases to other machines.

### mysqladmin
The mysqladmin command-line client is designed specifically for administrative operations. Its capabilities include those in the following list:
* "Ping" the server to see whether it's running and accepting client connections
* Shut down the server
* Create and drop databases
* Display server configuration and version information
* Display or reset server status variables
* Set passwords
* Reload the grant tables
* Flush the log files or various server caches
* Start or stop replication slave servers
* Display information about client connections or kill connections

### mysqldump
* Table contents dumped to data files can be dumped only on the server host, so when using mysqldump this way, it's best to invoke it on the server host.
* When using mysqldump to produce SQL-format dump files, the server transfers table contents to mysqldump, which writes the dump file locally on the client host. SQL-format dumps can be generated for tables managed by local or remote servers.

## Client Program Limitations
* mysqladmin can create or drop databases, but it has no capabilities for creating or dropping individual tables or indexes. It can change passwords, but cannot create or delete user accounts. The mysql and MySQL Administrator programs can perform all of these operations
* mysqlimport loads data files, so it can load data files produced by mysqldump. However, mysqldump also can produce SQL-format dump files containing INSERT statements, and mysqlimport cannot load those files. Thus, mysqlimport is only a partial complement to mysqldump. To process dump files containing SQL statements, use mysql instead.
* With one exception, none of the client programs can start the server. Normally, you invoke the server directly or by using a startup script, or you can arrange to have the operating system invoke the server as part of its system startup procedure
* None of the clients discussed in this chapter can shut down the server except mysqladmin and MySQL Administrator. mysqladmin shuts down the server by using a special non-SQL capability of the client/server protocol. If you use an account that has the SHUTDOWN privilege, it can shut down local or remote servers. MySQL Administrator can shut down a local MySQL server on Windows if the server is configured to run as a Windows service

## Choosing Data Types for Character Columns
1. If stored string values all have the same length, use a fixed-length type rather than a variable-length type. To store values that are always 32 characters long, CHAR(32) requires 32 characters each, whereas VARCHAR(32) requires 32 characters each, plus an extra byte to store the length. In this case, VARCHAR requires one byte more per value than CHAR.  --> compare CHAR and VARCHAR , when fixed-length type.
2. On the other hand, if stored string values vary in length, a variable-length data type takes less space. If values range from 0 to 32 characters with an average of about 16 characters, CHAR(32) values require 32 characters, whereas VARCHAR(32) requires 16 characters plus one byte on average. Here, VARCHAR requires only about half as much storage as CHAR. --> compare CHAR and VARCHAR, when vary length type.
3. For multi-byte character sets that have variable-length encoding, a variable-length data type may be appropriate even if stored values always have the same number of characters. The utf8 character set uses one to three bytes per characters. For fixed-length data types, three bytes per character must always be allocated to allow for the possibility that every character will require the "widest" encoding. Thus, CHAR(32) requires 96 bytes, even if most stored values contain 32 single-byte characters. For variable-length data types, only as much storage is allocated as required. In a VARCHAR(32) column, a 32-character string that consists entirely of three-byte characters requires 96 bytes plus a length byte, whereas it requires only 32 bytes plus a length byte if the string consists entirely of single-byte characters. --> compare CHAR and VARCHAR, when multi-byte character sets,e.g utf8 vs ucs2
4. If you have a choice between multi-byte character sets, choose the one for which the most commonly used characters take less space. For example, the utf8 and utc2 character sets both can be used for storing Unicode data. In utf8, characters take from one to three bytes, but most non-accented Latin characters take one byte. In ucs2, every character takes two bytes. Therefore, if the majority of your characters are non-accented characters, you'll likely achieve a space savings by using utf8 rather than ucs2. This assumes the use of a variable-length data type such as VARCHAR(n). If you use a fixed-length type such as CHAR(n), stored values require n x 3 bytes for utf8 and only n x 2 bytes for ucs2, regardless of the particular characters in stored values. --> we need to know how many bytes the character takes. e.g utf-8 take one to three bytes, then ucs2 take two types.
