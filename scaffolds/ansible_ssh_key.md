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
