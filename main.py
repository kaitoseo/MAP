#!/usr/bin/env python

from map import MAP
import glob
for name in glob.glob('*.csv'):
    MAP().zscore(name)
    MAP().ranking(name,'fructose')
#MAP().finalize('result')
