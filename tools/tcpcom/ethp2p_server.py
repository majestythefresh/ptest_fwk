#!/usr/bin/env python3
#==============================================================================
#title           : ethp2p_server.py
#description     : TCP Ethernet P2P server.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Class to set up and run a server into device based on TCP Eth P2P connection and
listen for command to execute tests and send responses as status and final output.
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
import signal
import socket
import time
import re
import subprocess
import getpass
import getopt

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class ETHP2PServer(object):
    """
    Class to listen commands via TCP Eth
    """

    def __init__(self, ip_server, port_server):
        """
        Constructor

        type: string
        @param: ip_server - ip server

        type: string
        @param: port_server - port server
        """

        self.server_ip = ip_server
        self.server_port = int(port_server)
        self.client = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_recv_mode =  False
        self.file_name = ''
        self.file_ext = ''
        self.file_dest = ''

    #==========================================================================

    def start (self) :
        """
        Run Server.
        """

        #Check if server can run.
        rc = self.__canRun()

        #Setting up server interface
        if rc:
            rc, rout = self.__setUp()
        else:
            print(TOOLCFG.TCP_SRV_MSG_14)
            SYS.exitTC(SYS.EXIT_ERROR)

        print(rout)
        if rc:
            return rc, rout

        self.__listenCommand()

        return 1, TOOLCFG.TCP_SRV_MSG_13

    #==========================================================================

    def stop(self, signum, frame):
        """
        Stop execution by signal trap

        type: signal
        @param: signum - sys signal

        type: stack
        @param: frame - stack traceback
        """

        if self.client:
            self.client.send(TOOLCFG.TCP_CLISRV_MSG_5.encode())
            time.sleep(5)
            self.client.close()
            self.client = None
        if self.server:
            self.server.close()
            self.server = None
        print(TOOLCFG.TCP_CLISRV_MSG_5)
        print(TOOLCFG.TCP_CLISRV_MSG_4 % signum)
        SYS.exitTC(SYS.EXIT_BY_SIGNAL)

    #==========================================================================

    def __canRun (self) :
        """
        Set up of interface to Eth p2p com.
        """

        rc, rout = SYS.runShellCommand('ps ax | grep "ethp2p_server.py" | grep -v %d | grep -v "grep"' % os.getpid())

        if not rc:
            return False
        else:
            return True

    #==========================================================================

    def __setUp (self) :
        """
        Set up of interface to Eth p2p com.
        """

        setIP_flag = False

        sudo_cmd = ''
        if getpass.getuser() != TOOLCFG.TCP_CLISRV_MSG_2:
            sudo_cmd = TOOLCFG.TCP_CLISRV_MSG_3

        #Look for an eth p2p interface
        rc, rout = SYS.runShellCommand('ifconfig | grep -E \'%s\'' % CFG.SW_TCP_ETHP2P_INTERFACE)
        if rc:
            return rc, TOOLCFG.TCP_CLISRV_MSG_10

        #Splitting interface name
        interface = rout.split(':')
        if len(rout): int_Ethernet = interface[0]

        #is Interface running?
        rc, rout = SYS.runShellCommand('ifconfig | grep %s -A 2 | grep RUNNING' % int_Ethernet)
        if rc:
            return rc, TOOLCFG.TCP_CLISRV_MSG_11
        else:
            #does Interface have an IP?
            rc, rout = SYS.runShellCommand('ifconfig | grep %s -A 4 | grep RUNNING -A 4 | grep \'inet \' | awk \'{print $2}\'' % int_Ethernet)
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', rout):
                message = TOOLCFG.TCP_CLISRV_MSG_6 % rout.strip('\n')
                if CFG.SW_TCP_SERVER_IP != rout.strip('\n'):
                    print(TOOLCFG.TCP_CLISRV_MSG_7)
                    setIP_flag = True
            else:
                print(TOOLCFG.TCP_CLISRV_MSG_8)
                setIP_flag = True

            if setIP_flag:
                SYS.runShellCommand(TOOLCFG.TCP_CLISRV_INT_DOWN % (sudo_cmd, int_Ethernet))
                time.sleep(5)
                SYS.runShellCommand(TOOLCFG.TCP_CLISRV_INT_SET % (sudo_cmd, int_Ethernet, self.server_ip))
                time.sleep(5)
                SYS.runShellCommand(TOOLCFG.TCP_CLISRV_INT_UP % (sudo_cmd, int_Ethernet ))
                time.sleep(10)
                message = TOOLCFG.TCP_CLISRV_MSG_9 % self.server_ip

        return 0, message

    #==========================================================================

    def __listenCommand (self) :
        """
        Put to listen for commands.
        """

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.server_ip, self.server_port))
            self.server.listen(5)
            print(TOOLCFG.TCP_SRV_MSG_2 % (self.server_ip, self.server_port))

            #Keep listening until signal stops server
            while True:
                self.client, client_address = self.server.accept()
                client_input = self.client.recv(1024)

                if self.file_recv_mode: #Image Mode
                    self.__recvFile(client_input)

                else: #Commands available

                    #Command to run shell command
                    if re.match(r'ShellCommand:+', client_input.decode()):
                        self.__shellCmd(client_input)
                    #Command to run profile
                    elif re.match(r'RunProfile:+', client_input.decode()):
                        self.__runProfile(client_input)
                    #Command to run test
                    elif re.match(r'RunTest:+', client_input.decode()):
                        self.__runTest(client_input)
                    #Command to call and run custom definition (User/Custom GUI Mode)
                    elif re.match(r'RunDefinition\|+', client_input.decode()):
                        self.__runDefinition(client_input)
                    #Command to receive a file
                    elif re.match(r'SendFile:+', client_input.decode()):
                        self.__sendFile(client_input)
                    #Command Help
                    elif re.match(r'Help', client_input.decode()):
                        self.client.send(TOOLIB.MENU_TCPSERVER_USAGE.encode())
                    #No defined command
                    else:
                        resp = TOOLCFG.TCP_SRV_MSG_9
                        self.client.send(resp.encode())

                time.sleep(0.1)
                resp = TOOLCFG.TCP_SRV_MSG_10
                self.client.send(resp.encode())

        except SystemExit as e:
            self.stop(SYS.EXIT_BY_SIGNAL, None)

        except :
            print(TOOLCFG.TCP_SRV_MSG_12 % sys.exc_info()[0])
            if self.client:
                self.client.close()
                self.client = None
            if self.server:
                self.server.close()
                self.server = None
            return

    #==========================================================================

    def __shellCmd (self, client_input) :
        """
        execute command and send output to client connected.
        """

        shellCmd = client_input.decode().split(':')
        if len(shellCmd) > 1:
            #Run command with timeout
            rc, rout = SYS.runShellCommand(shellCmd[1], TOOLCFG.TCP_SRV_CMD_TIMEOUT)
            resp = TOOLCFG.TCP_SRV_MSG_3 % rc
            self.client.send(resp.encode())
            resp = TOOLCFG.TCP_SRV_MSG_4
            self.client.send(resp.encode())
            resp = rout
            self.client.send(resp.encode())
        else:
            resp = TOOLCFG.TCP_CLISRV_MSG_10
            self.client.send(resp.encode())

    #==========================================================================

    def __runProfile (self, client_input) :
        """
        execute Profile and send output to client connected.
        """

        self.client.send()
        profileCmd = client_input.decode().split(':')
        if len(profileCmd) > 1:
            profile = profileCmd[1]
            profile_script = '%s/run_profile.py' % CFG.SW_TOOLS_PATH
            cmd = [profile_script, '--name=%s' % profile, '--usermode=Automation', '--runmode=Normal']
            self.client.send(TOOLCFG.RPROF_MSG_2.encode())
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, b''):
                self.client.send(line)
            p.stdout.close()
            p.wait()
        else:
            resp = TOOLCFG.TCP_CLISRV_MSG_11
            self.client.send(resp.encode())

    #==========================================================================

    def __runTest (self, client_input) :
        """
        execute Test and send output to client connected.
        """

        testCmd = client_input.decode().split(':')
        if len(testCmd) > 1:
            test = testCmd[1]
            test_script = '%s/run_test.py' % CFG.SW_TOOLS_PATH
            cmd = [test_script, '--name=%s' % test, '--usermode=Automation', '--runmode=Normal']
            self.client.send(TOOLCFG.RTEST_MSG_2.encode())
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, b''):
                self.client.send(line)
            p.stdout.close()
            p.wait()
        else:
            resp = TOOLCFG.TCP_SRV_MSG_7
            self.client.send(resp.encode())

    #==========================================================================

    def __runDefinition (self, client_input) :
        """
        execute Custom Definition and send output to client connected.
        """

        testCmd = client_input.decode().split('|')
        if len(testCmd) > 4:
            testdef = testCmd[1]
            runmode = testCmd[2]
            logdir = testCmd[4]
            testid = testCmd[3]
            test_script = '%s/run_definition.py' % CFG.SW_TOOLS_PATH
            cmd = [test_script, '--def=%s' % testdef, '--runmode=%s' % runmode, '--logdir=%s' % logdir, '--testid=%s' % testid]
            self.client.send(TOOLCFG.RCUSTOMDEF_MSG_2.encode())
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, b''):
                self.client.send(line)
            p.stdout.close()
            p.wait()
        else:
            resp = TOOLCFG.TCP_SRV_MSG_8
            self.client.send(resp.encode())

    #==========================================================================

    def __sendFile (self, client_input) :
        """
        put server in Image receive mode.
        """

        fileCmd = client_input.decode().split(':')
        if len(fileCmd) >= 3:
            self.file_name = fileCmd[1]
            self.file_ext = fileCmd[2]
            self.file_dest = fileCmd[3]
            self.file_recv_mode =  True
            self.client.send('<Image Mode OK>'.encode())
            #print('File name ----->',self.file_name)
            #print('File ext ----->',self.file_ext)
            #print('Server File Mode ----->',self.file_recv_mode)
        else:
            self.client.send('<Image Mode ERROR>'.encode)

    #==========================================================================

    def __recvFile (self, client_input) :
        """
        receive Image and return server to Command mode.
        """

        if self.file_ext:
            file_to_write = '%s/%s.%s' % (self.file_dest, self.file_name, self.file_ext)
        else:
            file_to_write = '%s/%s' % (self.file_dest, self.file_name)
        sfile = open(file_to_write,'wb')
        while (client_input):
            print("<Receiving File [%s]...>" % file_to_write)
            sfile.write(client_input)
            client_input = self.client.recv(1024)
        sfile.close()
        self.file_recv_mode = False

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """

    try:
        opts, argmts = getopt.getopt(args[1:], 'h', ['help'])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_ETHP2PSERVER_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    for option, value in opts:
        if option in ('-h', '--help'):
            TOOLIB.MENU_ETHP2PSERVER_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    server = ETHP2PServer(CFG.SW_TCP_SERVER_IP, CFG.SW_TCP_SERVER_PORT)

    # set signal traps
    signal.signal(signal.SIGINT, server.stop)
    signal.signal(signal.SIGTERM, server.stop)

    print(TOOLCFG.TCP_SRV_MSG_1)
    rc = True
    while rc:
        print(TOOLCFG.TCP_CLISRV_MSG_1)
        rc, rout = server.start()
        print(TOOLCFG.TCP_SRV_MSG_11 % (rc, rout))
        time.sleep(2)

    SYS.exitTC(SYS.EXIT_NO_ERROR)


if __name__ == "__main__":
    main(sys.argv)
