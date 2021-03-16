#!/usr/bin/env python3
#==============================================================================
#title           : tools_lib.py
#description     : Example lib file to create classes or methods to achieve
#                  results and no overload tools methods.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================


#==============================================================================
#============================= HELPER FUNCTIONS ===============================
#==============================================================================

#Create Profile Usage instructions
def MENU_CREATEPROFILE_USAGE():
    """
    Create Profile Script usage
    """

    print ('\nUsage: \n \
            \n create_profile.py: \n \
            \n \
            create_profile.py --template=template_file\n \
            \n \
                        template : csv template file\n \
            \n \
            Example: \n \
            \n \
                Create profile with a template: \n \
                    create_profile.py --template=Manufacturing.csv\n \
            \n \
            Note:  Profile definition will be created into src/profiles/ as .py file\n \
            ')

#Create Test Usage instructions
def MENU_CREATETEST_USAGE():
    """
    Create Test Script usage
    """

    print ('\nUsage: \n \
            \n create_test.py: \n \
            \n \
            create_test.py --template=template_file\n \
            \n \
                        template : csv template file\n \
            \n \
            Example: \n \
            \n \
                Create test with a template: \n \
                    create_test.py --template=UsbTest.csv\n \
            \n \
            Note:  Test definition will be created into src/tests/ as folder with lib, config, and test files\n \
            ')

#Delete Profile Usage instructions
def MENU_DELETEPROFILE_USAGE():
    """
    Delete Profile Script usage
    """

    print ('\nUsage: \n \
            \n remove_profile.py: \n \
            \n \
            remove_profile.py --profile=profile_name\n \
            \n \
                        profile : string profile name\n \
            \n \
            Example: \n \
            \n \
                Delete Profile example1 (profile file and templates): \n \
                    remove_profile.py --profile=example1\n \
            ')

#Delete Profile Usage instructions
def MENU_DELETETEST_USAGE():
    """
    Delete Test Script usage
    """

    print ('\nUsage: \n \
            \n remove_test.py: \n \
            \n \
            remove_test.py --test=test_name\n \
            \n \
                        test : string test name\n \
            \n \
            Example: \n \
            \n \
                Delete Test example1 (test files and templates): \n \
                    remove_test.py --test=example1\n \
            ')

#Run Test Usage instructions
def MENU_RUNTEST_USAGE():
    """
    Run Test Script usage
    """

    print ('\nUsage: \n \
            \n run_test.py: \n \
            \n \
            run_test.py --name=name --usermode=usermode --runmode=runmode --logdir=logpath --testid=custom_id\n \
            \n \
                        name : name of test (required)\n \
                        usermode : user mode [ Automation | Shell | GUI ] (optional, Automation by default)\n \
                        runmode : run mode [ Normal | Parallel ] (optional, Normal by default)\n \
                        logdir : log path (optional, by default output/logs/...)\n\
                         testid : custom ID (optional, by default numeric auto-generated ID)\n\
            \n \
            Example: \n \
            \n \
                run test in Automation and Normal mode: \n \
                    run_test.py --name=testexample1 --usermode=Automation --runmode=Normal\n \
            \n \
            Note:  Test definition will run and output logs will be stored in logdir path if it was set or stored into output/logs as Test ID folder with test results inside\n \
            ')

#Run Definition Usage instructions
def MENU_RUNDEF_USAGE():
    """
    Run Test Script usage
    """

    print ('\nUsage: \n \
            \n run_definition.py: \n \
            \n \
            run_test.py --def=name --runmode=runmode --logdir=logpath --testid=custom_id\n \
            \n \
                        def : string with collection (required)\n \
                        runmode : run mode [ Normal | Parallel ] (optional, Normal by default)\n \
                        logdir : log path (optional, by default output/logs/...)\n\
                         testid : custom ID (optional, by default numeric auto-generated ID)\n\
            \n \
            Example: \n \
            \n \
                run custom test definition in Automation and Normal mode: \n \
                    run_definition.py --def="{\'type\': \'test\', \'name\': \'testexample1\', \'usermodes\': {\'automation\': 1, \'interactive\': 1, \'gui\': 1}, \'test_cases\': {1: {\'name\': \'firstmethod\', \'descp\': \'Method to test bla bla 1\', \'mode\': \'normal\', \'concurrency_inst\': 1, \'protected\': 0}, 2: {\'name\': \'secondmethod\', \'descp\': \'Method to test bla bla 2\', \'mode\': \'normal\', \'concurrency_inst\': 1, \'protected\': 0}}}" --runmode=Normal \n \
            \n \
            Note:  Test definition will run and output logs will be stored in logdir path if it was set or stored into output/logs as Test ID folder with test results inside\n \
            ')

#Run Profile Usage instructions
def MENU_RUNPROFILE_USAGE():
    """
    Run Profile Script usage
    """

    print ('\nUsage: \n \
            \n run_profile.py: \n \
            \n \
            run_profile.py --name=name --usermode=usermode --runmode=runmode --logdir=logpath  --testid=custom_id\n \
            \n \
                        name : name of test (required)\n \
                        usermode : user mode [ Automation | Shell | GUI ] (optional, Automation by default)\n \
                        runmode : run mode [ Normal | Parallel ] (optional, Normal by default)\n \
                        logdir : (optional, by default output/logs/...)\n\
                         testid : custom ID (optional, by default numeric auto-generated ID)\n\
            \n \
            Example: \n \
            \n \
                run profile in Automation and Normal mode: \n \
                    run_profile.py --name=profileexample1 --usermode=Automation --runmode=Normal\n \
            \n \
            Note:  Profile definition will run and output logs will be stored in logdir path if it was set or stored into output/logs as Test ID folder with test results inside\n \
            ')

#Generate Backup Usage instructions
def MENU_GENBACK_USAGE():
    """
    Generate Backup Script usage
    """

    print ('\nUsage: \n \
            \n generate_backup.py: \n \
            \n \
            generate_backup.py --testfolder=testid_folder --backupfolder=backup_folder\n \
            \n \
                        testfolder : string with folder path\n \
                        backupfolder : string path to create backup\n \
            \n \
            Example: \n \
            \n \
                Generate Backup for Test ID 000001: \n \
                    generate_backup.py --testfolder=/path/to/test/folder/000001 --backupfolder=/backup/path\n \
            \n \
            ')

#Generate Backup Usage instructions
def MENU_VALTEST_USAGE():
    """
    Validate results from Test ID folder
    """

    print ('\nUsage: \n \
            \n validate_test.py: \n \
            \n \
            validate_test.py --testfolder=testid_folder\n \
            \n \
                        testfolder : string with folder path\n \
            \n \
            Example: \n \
            \n \
                Validate results from Test ID 000001: \n \
                    validate_test.py --testfolder=/path/to/testid/000001\n \
            ')

#Menu TCP ETH P2P server Usage
def MENU_ETHP2PSERVER_USAGE():
    """
    TCP ETH P2P SERVER Script usage
    """

    print ('\nUsage: \n \
            \n ethp2p_server.py: \n \
            \n \
            ethp2p_server.py\n \
            \n \
            Example: \n \
            \n \
                Run server: \n \
                    ethp2p_server.py\n \
            \n \
            Note: you need root/sudo credentials to set network interface (command will ask).\n \
            ')

#Menu TCP client Usage
def MENU_ETHP2PCLIENT_USAGE():
    """
    TCP ETH P2P CLIENT Script usage
    """

    print ('\nUsage: \n \
            \n ethp2p_client.py: \n \
            \n \
            ethp2p_client.py --command=\'command_str\' --verbose=value\n \
            \n \
                        command : cmd message in Server protocol\n \
                        verbose : watch verbose mode [ 0 | 1 ]. 0: verbose at the end of execution, 1: in time\n \
            \n \
            Example: \n \
            \n \
                Run a Command and get ouput: \n \
                    ethp2p_client.py --command=\'ShellCommand:ls -l\'\n \
            \n \
                Help Command/ Get List of available commands: \n \
                    ethp2p_client.py --command=\'Help\'\n \
            \n \
            Note: you need root/sudo credentials to set network interface (command will ask).\n \
            ')

#Menu TCP server commands
MENU_TCPSERVER_USAGE = '\n\
            \nCommands: \n \
            \n \
              ShellCommad: run a shell command\n \
            \n \
                  example: ShellCommand:ls\n \
            \n \
              RunTest: run test name definition\n \
            \n \
                  example: RunTest:testexample1\n \
            \n \
              RunProfile: run profile name definition\n \
            \n \
                  example: RunProfile:profileexample1\n \
            \n \
            '
