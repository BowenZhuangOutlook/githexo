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
