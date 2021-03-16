#!/usr/bin/env python3
#==============================================================================
#title           : tools_config.py
#description     : Tools config file.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================


#Template formats
TOOLS_JSON = 'json'
TOOLS_CSV = 'csv'
TOOLS_TEMP_NOTSUP = 'Format not supported yet'
TOOLS_TEMP_NOTFOUND = 'Template file not found.'
TOOLS_TEMP_ERROR = 'Error getting data from template (csv and json only)'

#Generate Backup Strings
GENB_MSG_1 = '  Backup in [%s] already exist'
GENB_MSG_2 = 'No test id set'
GENB_MSG_3 = 'Backup generated [%s]'
GENB_MSG_4 = 'Error generating backup:'
GENB_MSG_5 = '  Test folder [%s] doesn\'t exist'
GENB_MSG_6 = '  Backup folder [%s] doesn\'t exist'

#Run Profile/Test Strings
RDEF_MSG_1 = 'unhandled option for command'
RDEF_AUTO_ALIAS = 'Automation'
RDEF_INT_ALIAS = 'Shell'
RDEF_GUI_ALIAS = 'GUI'
RDEF_NORMAL_ALIAS = 'Normal'
RDEF_PARL_ALIAS = 'Parallel'

#Run Profile Strings
RPROF_MSG_1 = 'Profile Name required'
RPROF_MSG_2 = 'Running Profile...'

#Run Test Strings
RTEST_MSG_1 = 'Test Name required'
RTEST_MSG_2 = 'Running Test...'

#Run Definition Strings
RCUSTOMDEF_MSG_1 = 'Test Name required'
RCUSTOMDEF_MSG_2 = 'Running Custom Definition...'

#Create Profile Strings
PROF_MSG_1 = '[%s] created'
PROF_MSG_2 = 'Profile created:'
PROF_MSG_3 = 'Error creating profile:'
PROF_MSG_4 = 'Profile Template required'
PROF_MSG_5 = 'Error: Profile [ %s ] already exist'

#Create Test Strings
TEST_MSG_1 = '[ %s ] created'
TEST_MSG_2 = 'Error: Test [ %s ] already exist'
TEST_MSG_3 = 'Test \'%s\' created [ OK ]'
TEST_MSG_4 = 'Test created:'
TEST_MSG_5 = 'Error creating test:'
TEST_MSG_6 = 'Test Template required'
TEST_INTMOD = 'Interactive'
TEST_GUIMOD = 'GUI'
TEST_AUTOMOD = 'Automation'
TEST_CHMOD = 0o755

#Delete Profile Strings
DELPROF_MSG_1 = 'Profile deleted'
DELPROF_MSG_2 = 'Error deleting Profile:'
DELPROF_MSG_3 = 'Error: Profile [ %s ] doesn\'t exist'
DELPROF_MSG_4 = 'Profile \'%s\' deleted [ OK ]'
DELPROF_MSG_5 = 'Profile name needed'

#Delete Profile Strings
DELTEST_MSG_1 = 'Test deleted'
DELTEST_MSG_2 = 'Error deleting Test:'
DELTEST_MSG_3 = 'Test name needed'

#Validate test Strings
VALTEST_NOFILE = 'File doesn\'t exist : %s'
VALTEST_NOVALID = 'Test %s was manipulated, It\'s not valid - Current Hash [%s] - Has to check [%s] [ \x1b[1;31mX\x1b[0m ]'
VALTEST_VALID = 'Test %s is Valid - Current Hash [%s] - Has to check [%s] [ \x1b[1;32mOK\x1b[0m ]'
VALTEST_ERROR = 'Error: No key with hash data'
VALTEST_MSG_1 = 'Test folder path needed'

#Shell TCP Strings
TCP_CLI_SHELL_PROMPT = '(Device:%s) > '
TCP_CLI_SHELL = 'tcpshell'
TCP_CLI_SHELL_MSG_1 = 'TCP Ethernet p2p command interface'

#TCP ETH P2P Client/Server Strings
TCP_CLISRV_MSG_1 = 'Waiting to stablish connection interface...'
TCP_CLISRV_MSG_2 = 'root'
TCP_CLISRV_MSG_3 = 'sudo '
TCP_CLISRV_MSG_4 = 'Killed by signal [%d]'
TCP_CLISRV_MSG_5 = 'Server closed!'
TCP_CLISRV_MSG_6 = 'IP already set -> [%s]'
TCP_CLISRV_MSG_7 = 'Changing ip...'
TCP_CLISRV_MSG_8 = 'Setting ip...'
TCP_CLISRV_MSG_9 = 'IP set -> %s'
TCP_CLISRV_MSG_10 = 'No interface Eth p2p detected, please connect an eth cable between host and device'
TCP_CLISRV_MSG_11 = 'No interface Eth p2p running, please connect an eth cable between host and device'
TCP_CLISRV_INT_DOWN = '%sifconfig %s down'
TCP_CLISRV_INT_SET = '%sifconfig %s %s'
TCP_CLISRV_INT_UP = '%sifconfig %s up'

#TCP  ETH P2P Client Strings
TCP_CLI_RESP_TIMEOUT = 90.0 #secs
TCP_CLI_MSG_1 = 'Exit Client'
TCP_CLI_MSG_2 = 'Response to command: <%s>'
TCP_CLI_MSG_3 = '-------------------------------'
TCP_CLI_MSG_4 = 'No connection to Server: Connection refused'
TCP_CLI_MSG_5 = 'Timeout: %s'
TCP_CLI_MSG_6 = 'Rcv Message error: %s'
TCP_CLI_MSG_7 = 'Command needed'
TCP_CLI_MSG_8 = 'Client can\'t run. Server is running in this machine/device'
TCP_CLI_MSG_9 = 'File trying to send doesn\'t exist'
TCP_CLI_MSG_10 = 'Sending File (%d%%) - [%s]...'
TCP_CLI_MSG_11 = 'Done File Sending'


#TCP  ETH P2P Server Strings
TCP_SRV_CMD_TIMEOUT = 60.0 #secs
TCP_SRV_MSG_1 = 'Starting Server...'
TCP_SRV_MSG_2 = 'Listening on %s:%d'
TCP_SRV_MSG_3 = 'Return Code [%s]'
TCP_SRV_MSG_4 = 'Command Output:'
TCP_SRV_MSG_5 = 'ShellCommand command malformed'
TCP_SRV_MSG_6 = 'RunProfile command malformed'
TCP_SRV_MSG_7 = 'RunTest command malformed'
TCP_SRV_MSG_8 = 'RunDefinition not available yet'
TCP_SRV_MSG_9 = 'Unknown command\n'
TCP_SRV_MSG_10 = '<EndCommand>'
TCP_SRV_MSG_11 = 'Error [%s] : %s'
TCP_SRV_MSG_12 = 'Server error: %s'
TCP_SRV_MSG_13 = 'Restarting...'
TCP_SRV_MSG_14 = 'Server can\'t run. A Server is running in this machine/device already'
