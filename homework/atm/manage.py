#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os,sys

from auth.login import welcome

base_dir = os.path.dirname(os.path.abspath(__file__))

#print(base_dir)
sys.path.append(base_dir)


def main():
    welcome()


if __name__ == '__main__':

    main()

