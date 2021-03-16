#!/usr/bin/env python3
#==============================================================================
#title           : remove_test.py
#description     : Command to delete a test definition and template
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Command to delete a test definition and template
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from config import config as CFG
from lib import sys_lib as SYS
from tools.toolslib import tools_lib as TOOLIB
from tools.toolsconfig import tools_config as TOOLCFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import os
import shutil
import getopt

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class DeleteTest(object):
    """
    Class to Delete a test
    """

    def __init__(self, test_name):
        """
        Constructor

        type: string
        @param: test_name - name/id of test
        """

        self.test_name = test_name

    #==========================================================================

    def delete(self):
        """
        Delete files
        """

        #Delete test file
        pathfile = '%s/%s' % (CFG.SW_TEST_PATH, self.test_name)
        templatefile = '%s/%s.csv' % (CFG.SW_TEMP_TEST_PATH, self.test_name)
        templatefilejson = '%s/%s.json' % (CFG.SW_TEMP_TEST_PATH, self.test_name)

        if os.path.exists(pathfile):
            shutil.rmtree(pathfile)
            if os.path.exists(templatefile): os.remove(templatefile)
            if os.path.exists(templatefilejson): os.remove(templatefilejson)
        else:
            return 1, TOOLCFG.DELPROF_MSG_3 % pathfile

        return 0, TOOLCFG.DELPROF_MSG_4 % pathfile


#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """

    try:
        opts, argmts = getopt.getopt(args[1:], 'ht', ['help', 'test='])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_DELETETEST_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    test_name = ''
    for option, value in opts:
        if option in ('--test'):
            test_name = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_DELETETEST_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not test_name:
        print(TOOLCFG.DELPROF_MSG_5)
        TOOLIB.MENU_DELETETEST_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    test = DeleteTest(test_name)
    rc, rout = test.delete()

    message = TOOLCFG.DELTEST_MSG_1
    if rc:
        message = TOOLCFG.DELTEST_MSG_2

    print(message)
    print(rout)
    SYS.exitTC(rc)


if __name__ == "__main__":
    main(sys.argv)
