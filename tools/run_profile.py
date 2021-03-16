#!/usr/bin/env python3
#==============================================================================
#title           : run_profile.py
#description     : Command to start running a profile
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Command to start running a profile
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from config import config as CFG
from lib import sys_lib as SYS
from tools.toolslib import tools_lib as TOOLIB
from tools.toolsconfig import tools_config as TOOLCFG
from src import executor

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import getopt
import sys

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

#...

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """

    try:
        opts, argmts = getopt.getopt(args[1:], 'hnurlt', ['help', 'name=', 'usermode=', 'runmode=', 'logdir=', 'testid='])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_RUNPROFILE_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    name = ''
    usermode = TOOLCFG.RDEF_AUTO_ALIAS
    runmode = TOOLCFG.RDEF_NORMAL_ALIAS
    logdir = ''
    logid = ''
    for option, value in opts:
        if option in ('--name'):
            name = value
        elif option in ('--usermode'):
            usermode = value
        elif option in ('--runmode'):
            runmode = value
        elif option in ('--logdir'):
            logdir = value
        elif option in ('--testid'):
            logid = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_RUNPROFILE_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not name:
        print(TOOLCFG.RTEST_MSG_1)
        TOOLIB.MENU_RUNPROFILE_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)


    if usermode == TOOLCFG.RDEF_INT_ALIAS:
        usermode = CFG.SW_UM_INTERACTIVE
    else:
        usermode = usermode.lower()

    if runmode == TOOLCFG.RDEF_NORMAL_ALIAS:
        runmode = '0'
    elif runmode == TOOLCFG.RDEF_PARL_ALIAS:
        runmode = '1'

    #Call executor
    args = [args[0], CFG.SW_TD_PROFILE, name, usermode, runmode, logdir, logid]
    executor_main = getattr(executor, 'main')
    executor_main(args)

    SYS.exitTC(SYS.EXIT_NO_ERROR)


if __name__ == "__main__":
    main(sys.argv)
