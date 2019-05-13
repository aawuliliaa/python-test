#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from core.main import run

if __name__ == '__main__':
    run()
