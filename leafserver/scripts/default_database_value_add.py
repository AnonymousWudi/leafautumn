#!/usr/bin/env python
# coding=utf-8

import os
import sys

pro_dir = os.getcwd()
print pro_dir
sys.path.append(pro_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'leafautumn.settings'

from models import Subject


def add_default_subjects():

    return True


if __name__ == '__main__':
    add_default_subjects()
