#!/usr/bin/env python3
#==============================================================================
#title           : remove_profile.py
#description     : Command to delete a profile definition and template
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Command to delete a profile definition and template
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

class DeleteProfile(object):
    """
    Class to Delete a profile
    """

    def __init__(self, profile_name):
        """
        Constructor

        type: string
        @param: profile_name - name/id of profile
        """

        self.profile_name = profile_name

    #==========================================================================

    def delete(self):
        """
        Delete files
        """

        #Delete profile file
        pathfile = '%s/%s.py' % (CFG.SW_PROF_PATH, self.profile_name)
        templatefile = '%s/%s.csv' % (CFG.SW_TEMP_PROF_PATH, self.profile_name)
        templatefilejson = '%s/%s.json' % (CFG.SW_TEMP_PROF_PATH, self.profile_name)

        if os.path.exists(pathfile):
            os.remove(pathfile)
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
        opts, argmts = getopt.getopt(args[1:], 'ht', ['help', 'profile='])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_DELETEPROFILE_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    profile_name = ''
    for option, value in opts:
        if option in ('--profile'):
            profile_name = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_DELETEPROFILE_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not profile_name:
        print(TOOLCFG.DELPROF_MSG_5)
        TOOLIB.MENU_DELETEPROFILE_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    test = DeleteProfile(profile_name)
    rc, rout = test.delete()

    message = TOOLCFG.DELPROF_MSG_1
    if rc:
        message = TOOLCFG.DELPROF_MSG_2

    print(message)
    print(rout)
    SYS.exitTC(rc)


if __name__ == "__main__":
    main(sys.argv)
