#!/usr/bin/env python3
#==============================================================================
#title           : config.py
#description     : Config file to define general HW and SW variables
#                  as constant.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================

import platform

#==============================================================================
#=============================== CONFIG HW ====================================
#==============================================================================

#Machine Hardware supported
HW_MACHINE_HOST = 'x86_64'
HW_MACHINE_UNKNOWN = 'unknown' #another arch

#==============================================================================
#=============================== CONFIG SW ====================================
#==============================================================================

#Framework Version
SW_FWK_VERSION = 'v0.1.2'

#Platforms supported
SW_LINUX = 'Linux'
SW_OSX = 'Darwin'

#Framework Path for supported OS
SW_LINUX_PATH = '/home/plauchu/Projects'   #Linux work station
SW_EMB_LINUX_PATH = '/home/device/workspace'   #Embedded Linux device
SW_MACOS_PATH = '/Users/plauchu/Workspace' #OSX work station


#==============================================================================

#Paths
SW_FWK_NAME = 'ptest_fwk'

if platform.system() == SW_LINUX: #Linux OS
    if platform.machine() == HW_MACHINE_HOST: #Personal/ Another Linux host
        SW_FWK_PATH = '%s/%s' % (SW_LINUX_PATH, SW_FWK_NAME)
        SW_TCP_ETHP2P_INTERFACE = 'enp[0-9]{2}' #Fedora 27 p2p interface eth pattern
    else: #('unknown')
        SW_FWK_PATH = '%s/%s' % (SW_EMB_LINUX_PATH, SW_FWK_NAME)
        SW_TCP_ETHP2P_INTERFACE = 'enx' #Device p2p interface eth pattern
else: #Darwin OS
    SW_FWK_PATH = '%s/%s' % (SW_MACOS_PATH, SW_FWK_NAME)
    SW_TCP_ETHP2P_INTERFACE = 'en[4-9]' #MAC OSX

SW_PROF_PATH = '%s/src/profiles' % SW_FWK_PATH
SW_TEST_PATH = '%s/src/tests' % SW_FWK_PATH
SW_LOGS_PATH = '%s/output/logs' % SW_FWK_PATH
SW_BACKUP_PATH = '%s/output/backups' % SW_FWK_PATH
SW_TEMPLATES_PATH = '%s/templates' % SW_FWK_PATH
SW_TEMP_PROF_PATH = '%s/profiles' % SW_TEMPLATES_PATH
SW_TEMP_TEST_PATH = '%s/tests' % SW_TEMPLATES_PATH
SW_TOOLS_PATH = '%s/tools' % SW_FWK_PATH
SW_USERMODES_PATH = '%s/src/usermodes' % SW_FWK_PATH

#==============================================================================

#Logging...
#Log ID
SW_TEST_ID_INIT = '000000'
#Log DEBUG msg activated
SW_LOG_DEBUG = False

#==============================================================================

#Definition types
SW_TD_PROFILE = 'profile'
SW_TD_TEST = 'test'
SW_CUSTOM_TD = 'custom'

#==============================================================================

#Test Cases Modes
SW_TC_NORMAL = 'normal'
SW_TC_CONC = 'concurrency'

#==============================================================================

#User modes
SW_UM_AUTOMATION = 'automation'
SW_UM_INTERACTIVE = 'interactive'
SW_UM_GUI = 'gui'

#==============================================================================

#TCP P2P COM Tools
SW_TCP_SERVER_IP = '192.168.0.100'
SW_TCP_SERVER_PORT = '1500'
SW_TCP_CLIENT_IP = '192.168.0.200'

#==============================================================================

#Strings
SW_SEP_STR = '====================================================='

#==============================================================================
#============================= HELPER FUNCTIONS ===============================
#==============================================================================

#Usage instructions
def SW_EXECUTOR_USAGE():
    """
    Executor Script usage
    """

    print ('\nUsage: \n \
            \n executor.py: \n \
            \n \
            executor.py type name usermode runmode\n \
            \n \
                        type : type of definition [ profile | test ]\n \
                        name : name of definition\n \
                        usermode : mode to run as User [ automation | interactive | gui ]\n \
                        runmode : mode to run testcases [ 0 (sequential) | 1 (parallel) ]\n \
            \n \
            Example: \n \
            \n \
                Run Profile with testcases run sequentially: \n \
                    executor.py profile profileexample1 automation 0\n \
            \n \
                Run Test with testcases run parallelly: \n \
                    executor.py test testexample1 automation 1\n \
            ')
