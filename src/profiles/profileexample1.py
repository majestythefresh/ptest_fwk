#!/usr/bin/env python3
#==============================================================================
#title           : profileexample1.py
#description     : Example profile file. It contains data collection with test
#                  names and order of execution..
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Profile to test bla bla 1
"""

profile_def = {
    'type' : 'profile',
    'name' : 'profileexample1',
    'descp': 'Profile to test bla bla 1',
    'tests' : {
        1 : { 'name' : 'testexample1', 'descp' : 'Test to cover bla bla 1'},
        2 : { 'name' : 'testexample2', 'descp' : 'Test to cover bla bla 2'}
        }
    }
