#!/usr/bin/env python3
#==============================================================================
#title           : create_profile.py
#description     : Command to create a profile definition from template
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Command to create a profile definition from template
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from config import config as CFG
from lib import sys_lib as SYS
from tools.toolslib import tools_lib as TOOLIB
from tools.toolsconfig import tools_config as TOOLCFG
from tools.toolsconfig import profile_config as PCFG

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import datetime
import os
from os.path import basename
import json
import getopt

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class CreateProfile(object):
    """
    Class to create a profile
    """

    def __init__(self, template_file):
        """
        Constructor

        type: string
        @param: template_file - name of template file
        """

        self.template_file = template_file

    #==========================================================================

    def create(self):
        """
        Create file
        """

        #Get Info from template
        template = self.__getTemplateInfo()
        if not template:
            print(TOOLCFG.TOOLS_TEMP_ERROR)
            SYS.exitTC(SYS.EXIT_ERROR)

        #Create profile file
        pathfile = '%s/%s.py' % (CFG.SW_PROF_PATH, template['name'])

        if os.path.exists(pathfile):
            return SYS.EXIT_ERROR, TOOLCFG.PROF_MSG_5 % template['name']

        date_time = datetime.datetime.now()
        profile_file = open(pathfile,'a')
        profile_file.write(PCFG.PROFILE_INFO % (template['name'], CFG.SW_FWK_VERSION,
                                                date_time, template['descp']) )
        profile_file.write(PCFG.PROFILE_HEAD % (template['name'],
                                                template['descp']) )
        for k,v in template['tests'].items():
            profile_file.write(PCFG.PROFILE_TEST % (k, v['name'],  v['descp']))
        profile_file.write(PCFG.PROFILE_FOOT)
        profile_file.close()

        return SYS.EXIT_NO_ERROR, TOOLCFG.PROF_MSG_1 % pathfile

    #==========================================================================

    def __getTemplateInfo(self):
        """
        Get info from template
        """

        template = []
        pathfile = '%s/%s' % (CFG.SW_TEMP_PROF_PATH, self.template_file)
        try:
            template_file = open(pathfile,'r')
        except FileNotFoundError:
            print (TOOLCFG.TOOLS_TEMP_NOTFOUND)
            SYS.exitTC(SYS.EXIT_ERROR)
        if self.template_file.split(".")[-1] == TOOLCFG.TOOLS_JSON :
            template = json.load(template_file)
        if self.template_file.split(".")[-1] == TOOLCFG.TOOLS_CSV :
            template_file.readline() #ignore first line
            name = basename(self.template_file)
            descp = template_file.readline().split(',')[0]
            template_file.readline() #ignore third line
            tests = {}
            test = {}
            while True:
                line = template_file.readline()
                if not line:
                    break
                info = line.split(',')
                test['name'] = info[1].rstrip()
                test['descp'] = info[2].rstrip()
                tests[info[0].rstrip()] = test
                test = {}

            template = ({'name' : name.rstrip().split('.')[0] ,
                         'descp' : descp.rstrip(),
                         'tests' : tests})

        return template

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """

    try:
        opts, argmts = getopt.getopt(args[1:], 'ht', ['help', 'template='])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_CREATEPROFILE_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    template = ''
    for option, value in opts:
        if option in ('--template'):
            template = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_CREATEPROFILE_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not template:
        print(TOOLCFG.PROF_MSG_4)
        TOOLIB.MENU_CREATEPROFILE_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    profile = CreateProfile(template)
    rc, rout = profile.create()

    message = TOOLCFG.PROF_MSG_2
    if rc:
        message = TOOLCFG.PROF_MSG_3

    print(message)
    print(rout)
    SYS.exitTC(rc)


if __name__ == "__main__":
    main(sys.argv)
