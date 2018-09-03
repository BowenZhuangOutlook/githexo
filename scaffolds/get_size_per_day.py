#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import datetime


def get_size_per_day(path):
    result = {}
    for filename in os.listdir(path):
        filename = os.path.join(path, filename)
        info = os.stat(filename)
        date = datetime.datetime.fromtimestamp(info.st_ctime).strftime("%Y-%m-%d")
        size = (info.st_size / 1024 / 1024)
        result[date] = result.get(date, 0) + size
    for key in result.keys():
        print("%s size is %s Mb" % (key, result[key]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("option error")
        print("get_size_per_day /opt")
        sys.exit()
    print("options:", sys.argv[1])
    get_size_per_day(sys.argv[1])
