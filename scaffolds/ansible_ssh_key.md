# Ansible ssh 配置操作
ansible MY*:\!MYDEV -m copy -a 'src=ssh_key.sh dest=/home/bowenz/ssh_key.sh mode=0777' -u bowenz -k
ansible MY*:\!MYDEV -m copy -a 'src=id_rsa.pub dest=/home/bowenz/id_rsa.pub mode=0777' -u bowenz -k
ansible MY*:\!MYDEV -m shell -a '/home/bowenz/ssh_key.sh ' -u bowenz -k

ansible MY* -m ping -u mysql


ansible MG*:\!MGDEV -m copy -a 'src=ssh_key.sh dest=/home/bowenz/ssh_key.sh mode=0777' -u bowenz -k
ansible MG*:\!MGDEV -m copy -a 'src=id_rsa.pub dest=/home/bowenz/id_rsa.pub mode=0777' -u bowenz -k
ansible MG*:\!MGDEV -m shell -a '/home/bowenz/ssh_key.sh ' -u bowenz -k


ansible MG*:MMS -m ping -u mongod

ansible localhost -m debug -a 'var=groups.keys()'

QAPROXY
CMPROXY
PRPROXY
IPROXY

#!/bin/bash

sudo su - <<EOF
 cd /home/oracle/.ssh
 cat /home/bowenz/id_rsa.pub >> authorized_keys
EOF


ansible *PROXY -m copy -a 'src=ssh_key.sh dest=/home/bowenz/ssh_key.sh mode=0777' -u bowenz -k
ansible *PROXY -m copy -a 'src=id_rsa.pub dest=/home/bowenz/id_rsa.pub mode=0777' -u bowenz -k
ansible *PROXY -m shell -a '/home/bowenz/ssh_key.sh ' -u bowenz -k

ansible *PROXY -m ping -u oracle


tail -f /var/log/secure
chmod g-w /home/mysql
chmod 700 /home/mysql/.ssh
chmod 600 /home/mysql/.ssh/authorized_keys


-rw------- 1 mysql mysql  397 Aug  9 02:32 authorized_keys
-rw------- 1 mysql mysql 1675 Aug  9 02:25 id_rsa
-r-------- 1 mysql mysql  420 Aug  9 02:25 id_rsa.pub
-rw-r--r-- 1 mysql mysql 8859 Aug  9 00:32 known_hosts

-rw------- 1 mysql mysql 3319 Aug  9 02:19 authorized_keys
-rw------- 1 mysql mysql 1679 Mar 22  2013 id_rsa
-r-------- 1 mysql mysql  399 Mar 22  2013 id_rsa.pub
-rw-r--r-- 1 mysql mysql 6452 Feb 22 18:46 known_hosts


chmod 600 authorized_keys
chmod 600 id_rsa
chmod 400 id_rsa.pub
chmod 644 known_hosts



Ansible common operation reference

#get ansible inventory group name
ansible localhost -m debug -a 'var=groups.keys()'
#get ansible host list by group name
ansible MGDEV --list-host
#get MG* host list except MGDEV contain host
ansible MG*:\!MGDEV --list-host
#for mysql,please execute a similar command  
ansible MYDEV -m ping -u mysql
#for mongod,please execute a similar command  
ansible MYDEV -m ping -u mongod
#for oracle/proxy,please execute a similar command  
ansible MYDEV -m ping -u oracle
#get information
ansible CDWPROD -m shell -a 'free -g' -u oracle
#copy file to remote host
ansible MYDEV -m copy -a 'src=dbjobfunctions dest=/u01/app/mysql/script/dbjob/dbjobfunctions mode=0777' -u mysql
#execute remote script
ansible MYDEV -m shell -a '/home/mysql/work/bowenz/mv_dbjobfunc.sh ' -u mysql
#get remote file detail information: actime/ctime/mtime，md5，uid，gid
ansible MYDEV -m stat -a "path=/etc/my.cnf" -u mysql
#tar remote server folder
ansible PROD:CDWPROD:RRSPROD -m shell -a 'cd /u01/app/oracle/report && zip -r /tmp/baseline.zip baseline' -u oracle
#get remote server files or folder
ansible PROD:CDWPROD:RRSPROD -m fetch -a 'src=/tmp/baseline.zip dest=/home/oracle/work/bowenz/baseline/{{ inventory_hostname }}/ flat=yes' -u oracle
#batch get files from remote server
---
- hosts: '{{ hosts }}'
  tasks:
  - name: find compare baseline files
    find:
     paths: /u01/app/oracle/report
     patterns: compare_baseline*
     recurse: no
    register: file_2_fetch
  - name: pull compare files from remote node
    fetch:
     src: "{{ item.path }}"
     dest: /home/oracle/work/bowenz/compare_baseline/{{ inventory_hostname }}/
     flat: yes
    with_items: "{{ file_2_fetch.files }}"

ansible-playbook pull.yml --extra-vars "hosts=abprdb01" -v -u oracle
#execute localhost script on remote node
ansible MYDEV -m script -a '/home/mysql/get.sh' -u mysql

###get baseline for company
ansible PROD:CDWPROD:RRSPROD -m shell -a 'cd /u01/app/oracle/report/ && zip -r /tmp/baseline.zip baseline' -u oracle
ansible PROD:CDWPROD:RRSPROD -m fetch -a 'src=/tmp/baseline.zip dest=/home/oracle/work/bowenz/baseline/{{ inventory_hostname }}/ flat=yes' -u oracle
ansible MGPROD -m shell -a 'cd /home/mongod/report/ && zip -r /tmp/baseline.zip baseline' -u mongod
ansible MGPROD -m fetch -a 'src=/tmp/baseline.zip dest=/home/oracle/work/bowenz/baseline/{{ inventory_hostname }}/ flat=yes' -u mongod


## get pmm server status
ansible MYDEV -m copy -a 'src=check_pmm.sh dest=/home/bowenz/check_pmm.sh mode=0777' -u bowenz -k
ansible MYDEV -m shell -a '/home/bowenz/check_pmm.sh' -u bowenz -k 
