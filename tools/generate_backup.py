#!/usr/bin/env python3
#==============================================================================
#title           : generate_backup.py
#description     : Command to generate compressed file for an ID Test.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Command to generate compressed file for an ID Test.
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

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class GenTestBackup(object):
    """
    Class to generate a backup from test id
    """

    def __init__(self, test_folder, backup_folder):
        """
        Constructor

        type: string
        @param: test_folder - full path of test folder

        type: string
        @param: backup_folder - full path for backup file
        """

        self.test_id_folder = test_folder
        self.backup_folder = backup_folder

    #==========================================================================

    def generateBackup(self):
        """
        Generate compressed file
        """

        test_paths = self.test_id_folder.split('/')
        test_id = test_paths[len(test_paths)-1]

        backup_tar = '%s/%s.tar' % (self.backup_folder, test_id)

        if not os.path.exists(self.test_id_folder):
            return SYS.RC_ERROR, TOOLCFG.GENB_MSG_5 % self.test_id_folder

        if not os.path.exists(self.backup_folder):
            return SYS.RC_ERROR, TOOLCFG.GENB_MSG_6 % self.backup_folder

        if os.path.exists(backup_tar):
            return SYS.RC_ERROR, TOOLCFG.GENB_MSG_1 % backup_tar

        cmd = ['tar','-cvf', backup_tar, self.test_id_folder]
        rc, rout = SYS.execCommand(cmd, None, 1)

        if rc:
            SYS.execCommand(['rm', backup_tar])
        else:
            print(TOOLCFG.GENB_MSG_3 % backup_tar)

        return rc, rout

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """

    try:
        opts, argmts = getopt.getopt(args[1:], 'htb', ['help', 'testfolder=', 'backupfolder='])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_GENBACK_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    test_dir = ''
    backup_dir = ''
    for option, value in opts:
        if option in ('--testfolder'):
            test_dir = value
        elif option in ('--backupfolder'):
            backup_dir = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_GENBACK_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not test_dir or not backup_dir:
        print(TOOLCFG.GENB_MSG_2)
        TOOLIB.MENU_GENBACK_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    genB = GenTestBackup(test_dir, backup_dir)
    rc, rout = genB.generateBackup()
    message=''
    if rc:
        message=TOOLCFG.GENB_MSG_4

    print(message)
    print(rout)
    SYS.exitTC(rc)


if __name__ == "__main__":
    main(sys.argv)
