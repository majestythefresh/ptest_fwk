#!/usr/bin/env python3
#==============================================================================
#title           : common_lib.py
#description     : Common library file to create classes or methods to
#                  no overload functions inside framework.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Common library file to create classes or methods to and
no overload functions inside framework.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import sys_lib as SYS
from lib import proc_lib as PROCLIB
from lib import log_lib as LOG
from config import config as CFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import importlib
import datetime
import os

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#Strings
CMN_MOD_PROFILE = 'src.profiles.%s'
CMN_MOD_TEST = 'src.tests.%s.%s'
CMN_TD_NOTVALID = 'Definition type is not valid'
CMN_DEF_NOTFOUND = '[\'%s\'] %s not found'
CMN_DEF_MODNOTFOUND = 'Module Not Found Error:'

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args, test_def, test_ctrl, log, globals_def):
    """
    Main function.
    Entry point for single command exec and Executor for Test Definition

    type: sys.argv
    @param: args - argument list (method, mode, instance number)

    type: test_def
    @param: test_def - test definition structure

    type: Logging
    @param: log - log object

    type: globals[]
    @param: globals_def list of methods in package

    rtype: number
    @return: 1 for args error, 0 otherwise
    """

    if len(args) < 5:
        return 1

    method = args[1]
    #Call function sending properties to TestCase Decorator Class
    globals_def[method](args, test_def, test_ctrl, log)

    return 0


#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

def getDefinition(type_def, name):
    """
    Get static Definiton for profile or test as declared in test lib.

    type: str
    @param: type_def - type of definition [ test | profile ]

    type: str
    @param: name - of definition

    rtype: dictionary
    @return: definition structure
    """

    dft = []

    try:
        if type_def == CFG.SW_TD_PROFILE:
            profile_pkg = importlib.import_module(CMN_MOD_PROFILE % name)
            dft = profile_pkg.profile_def
        elif type_def == CFG.SW_TD_TEST:
            test_pkg = importlib.import_module(CMN_MOD_TEST % (name, name))
            dft = test_pkg.test_def
        else:
            print (CMN_TD_NOTVALID)
            return
    except ImportError as e:
        if type_def == CFG.SW_TD_PROFILE:
            pathfile = '%s/%s.py' % (CFG.SW_PROF_PATH, name)
        else:
            pathfile = '%s/%s/%s.py' % (CFG.SW_TEST_PATH, name, name)
        if os.path.exists(pathfile):
            print(CMN_DEF_MODNOTFOUND,e)
        else:
            print(CMN_DEF_NOTFOUND % (name, type_def))

    return dft

#==============================================================================

def getMethodAttr(method, order, tdef):
    """
    Get Method/Testcase attributes.

    type: str
    @param: mode - mode name

    type: test_def
    @param: tdef - test definition structure

    rtype: dictionary
    @return: structure with method attributes
    """

    test_name = tdef['name']
    for k, v in tdef['test_cases'].items():
        if method == v['name'] and int(k) == int(order):
            order = k
            method_name = v['name']
            descp = v['descp']
            mode = v['mode']
            concurrency_inst = v['concurrency_inst']
            prot_flag = v['protected']
            if 'args' in v:
                user_args = v['args']
            else:
                user_args = ''
            break

    return ({
            'order' : order ,
            'testname' : test_name,
            'methodname' : method_name,
            'descp' : descp ,
            'mode' : mode,
            'cinst' : concurrency_inst,
            'protected' : prot_flag,
            'user_args' : user_args
            })

#==============================================================================

def isTestAbleToRun(tdef, usermode):
    """
    Is a test able to run in a specific user mode?.

    type: str
    @param: tdef - test definition structure

    type: str
    @param: usermode - user mode

    rtype: boolean
    @return: True if is able to run, False otherwise
    """


    for k, v in tdef['usermodes'].items():
        if k == usermode and v == 1:
            return True

    return False

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

#...
