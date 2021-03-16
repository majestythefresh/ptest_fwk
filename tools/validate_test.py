#!/usr/bin/env python3
#==============================================================================
#title           : validate_test.py
#description     : Command to validate a ID Test Folder results.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Command to validate a ID Test Folder results.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from config import config as CFG
from lib import sys_lib as SYS
from tools.toolslib import tools_lib as TOOLIB
from tools.toolsconfig import tools_config as TOOLCFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import os
import sys
import re
import getopt
import json

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class ValidateTest(object):
    """
    Class to validate sha 256 hash from test id folder
    """

    def __init__(self, test_folder_path):
        """
        Constructor

        type: string
        @param: test_folder_path - full path of test id folder to backup
        """

        self.test_folder = test_folder_path

    #==========================================================================

    def validate(self):
        """
        Validate results from a Test ID folder
        """

        test_paths = self.test_folder.split('/')
        test_id = test_paths[len(test_paths)-1]
        pathfile = '%s/%s.json' % (self.test_folder, test_id)
        if not os.path.exists(self.test_folder):
            return SYS.EXIT_ERROR, TOOLCFG.VALTEST_NOFILE % self.test_folder

        #Get current checksum
        try:
            cmd = 'find %s -type f ! -name "%s.json" -exec shasum -a 256 {} \; | shasum -a 256' % (self.test_folder, test_id)
            rout = SYS.execPlainCommand(cmd)

            #Get checksum in json log
            json_file = open(pathfile,'r')
        except FileNotFoundError:
            print (TOOLCFG.VALTEST_NOFILE % pathfile)
            SYS.exitTC(SYS.EXIT_ERROR)

        test_results = json.load(json_file)
        try:
            if rout == test_results['sha256sum']:
                return SYS.EXIT_NO_ERROR, TOOLCFG.VALTEST_VALID % (test_id, rout, test_results['sha256sum'])
            else:
                return SYS.EXIT_ERROR, TOOLCFG.VALTEST_NOVALID % (test_id, rout, test_results['sha256sum'])
        except KeyError:
            return SYS.EXIT_ERROR, TOOLCFG.VALTEST_ERROR

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """

    try:
        opts, argmts = getopt.getopt(args[1:], 'ht', ['help', 'testfolder='])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_VALTEST_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    test_id_folder = ''
    for option, value in opts:
        if option in ('--testfolder'):
            test_id_folder = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_VALTEST_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not test_id_folder:
        print(TOOLCFG.VALTEST_MSG_1)
        TOOLIB.MENU_VALTEST_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    vtest = ValidateTest(test_id_folder)
    rc, rout = vtest.validate()
    print(rout)
    SYS.exitTC(rc)


if __name__ == "__main__":
    main(sys.argv)
