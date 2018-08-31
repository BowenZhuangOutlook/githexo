```
import os
import sys

if len(sys.argv)!=2:
	print 'Usage: search.py <string>'
	exit()

def search(name, flist, path='.'):
	for x in os.listdir(path):		
		y = os.path.join(path, x)
		if os.path.isdir(y):
			search(name, flist, y)
		elif os.path.isfile(y) and x.find(name)!=-1:
			print y
			flist.append(y)

flist = []
search(sys.argv[1], flist)
print flist
```

```
>>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']
```
