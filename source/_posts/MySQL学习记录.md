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
