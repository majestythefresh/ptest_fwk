#!/usr/bin/env python3
#==============================================================================
#title           : create_test.py
#description     : Command to create a test definition from template
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
from tools.toolsconfig import test_config as TCFG

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

class CreateTest(object):
    """
    Class to create a test
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

        #Create test dirs
        testdir =  '%s/%s' % (CFG.SW_TEST_PATH, template['name'])
        testlibdir =  '%s/testlib' % (testdir)
        testcfgdir =  '%s/testconfig' % (testdir)
        if not os.path.exists(testdir):
            os.makedirs(testdir)
            os.makedirs(testlibdir)
            os.makedirs(testcfgdir)
        else:
            return SYS.EXIT_ERROR, TOOLCFG.TEST_MSG_2 % template['name']
        #Create test file
        self.__createTestFile(testdir, template)
        #Create lib file
        self.__createLibFile(testlibdir, template)
        #Create lib file
        self.__createCfgFile(testcfgdir, template)

        return SYS.EXIT_NO_ERROR, TOOLCFG.TEST_MSG_3 % template['name']

    #==========================================================================

    def __getTemplateInfo(self):
        """
        Get info from template
        """

        template = []
        pathfile = '%s/%s' % (CFG.SW_TEMP_TEST_PATH, self.template_file)
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

            umodes = template_file.readline().split(',')
            template_file.readline() #ignore fifth line
            usermodes = {}
            for umode in umodes:
                if umode == TOOLCFG.TEST_INTMOD:
                    usermodes['interactive'] = 1
                if umode == TOOLCFG.TEST_GUIMOD:
                    usermodes['gui'] = 1
                if umode == TOOLCFG.TEST_AUTOMOD:
                    usermodes['automation'] = 1

            test_cases = {}
            test_case = {}
            while True:
                line = template_file.readline()
                if not line:
                    break
                info = line.split(',')
                test_case['name'] = info[1].rstrip()
                test_case['descp'] = info[2].rstrip()
                test_case['mode'] = info[3].rstrip()
                test_case['concurrency_inst'] = info[4].rstrip()
                test_case['protected'] = info[5].rstrip()
                if len(info) > 6:
                    args = info[6].rstrip().replace("|", ",")
                    test_case['args'] = args
                test_cases[info[0].rstrip()] = test_case
                test_case = {}

            template = ({'name' : name.rstrip().split('.')[0] ,
                         'descp' : descp.rstrip(),
                         'usermodes' : usermodes,
                         'test_cases' : test_cases})

        return template

    #==========================================================================

    def __createTestFile(self, testdir, template):
        """
        Create Test file
        """

        testcase_hash = {}
        pathfile = '%s/%s.py' % (testdir, template['name'])
        date_time = datetime.datetime.now()
        test_file = open(pathfile,'a')
        test_file.write(TCFG.TESTFILE_INFO % (template['name'], CFG.SW_FWK_VERSION,
                                              date_time, template['descp']) )
        test_file.write(TCFG.TESTFILE_HEAD % (template['name'], template['name'],
                                              template['name'], template['name'],
                                              template['name']))
        for k,v in template['test_cases'].items():
            if not v['name'] in testcase_hash:
                testcase_hash[v['name']] = 1
                test_file.write(TCFG.TESTFILE_TC % (v['name'],  v['descp']) )
        test_file.write(TCFG.TESTFILE_FOOT)
        test_file.close()
        os.chmod(pathfile, TOOLCFG.TEST_CHMOD)

        print(TOOLCFG.TEST_MSG_1 % pathfile)

    #==========================================================================

    def __createLibFile(self, testlibdir, template):
        """
        Create Test Lib file
        """

        pathfile = '%s/%s_lib.py' % (testlibdir, template['name'])
        date_time = datetime.datetime.now()
        testlib_file = open(pathfile,'a')
        testlib_file.write(TCFG.TESTLIBFILE_INFO % (template['name'], CFG.SW_FWK_VERSION,
                                                    date_time, template['descp']) )
        testlib_file.write(TCFG.TESTLIBFILE_HEAD % (template['name'], template['name']))
        testlib_file.write(TCFG.TESTLIBFILE_TESTDEF_1 % (template['name'], template['descp']))
        for k,v in template['usermodes'].items():
            testlib_file.write(TCFG.TESTLIBFILE_TESTDEF_2 % (k, v))
        testlib_file.write(TCFG.TESTLIBFILE_TESTDEF_3)
        for k,v in sorted(template['test_cases'].items()):
            if 'args' in v:
                testlib_file.write(TCFG.TESTLIBFILE_TESTDEF_4_ARGS % (k, v['name'], v['descp'],
                                                                v['mode'], v['concurrency_inst'],
                                                                v['protected'], v['args']))
            else:
                testlib_file.write(TCFG.TESTLIBFILE_TESTDEF_4 % (k, v['name'], v['descp'],
                                                                v['mode'], v['concurrency_inst'],
                                                                v['protected']))
        testlib_file.write(TCFG.TESTLIBFILE_TESTDEF_5)
        testlib_file.write(TCFG.TESTLIBFILE_EXT % (template['name'], template['name']))
        testlib_file.close()
        os.chmod(pathfile, TOOLCFG.TEST_CHMOD)

        print(TOOLCFG.TEST_MSG_1 % pathfile)

    #==========================================================================

    def __createCfgFile(self, testcfgdir, template):
        """
        Create Test Config file
        """

        pathfile = '%s/%s_config.py' % (testcfgdir, template['name'])
        date_time = datetime.datetime.now()
        testcfg_file = open(pathfile,'a')
        testcfg_file.write(TCFG.TESTCFGFILE_INFO % (template['name'], CFG.SW_FWK_VERSION,
                                                    date_time, template['descp']) )
        testcfg_file.write(TCFG.TESTCFGFILE_HEAD % (template['name'], template['name']))
        testcfg_file.close()
        os.chmod(pathfile, TOOLCFG.TEST_CHMOD)

        print(TOOLCFG.TEST_MSG_1 % pathfile)


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
        TOOLIB.MENU_CREATETEST_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    template = ''
    for option, value in opts:
        if option in ('--template'):
            template = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_CREATETEST_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not template:
        print(TOOLCFG.TEST_MSG_6)
        TOOLIB.MENU_CREATETEST_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    test = CreateTest(template)
    rc, rout = test.create()

    message = TOOLCFG.TEST_MSG_4
    if rc:
        message = TOOLCFG.TEST_MSG_5

    print(message)
    print(rout)
    SYS.exitTC(rc)


if __name__ == "__main__":
    main(sys.argv)
