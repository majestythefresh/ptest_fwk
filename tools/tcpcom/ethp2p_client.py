#!/usr/bin/env python3
#==============================================================================
#title           : ethp2p_client.py
#description     : TCP Ethernet P2P client.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Class to set up and run a server based on TCP ETh P2P and listen for command to
execute tests and send responses as status and final output
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
import getpass
import getopt
from os.path import basename

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class ETHP2PClient(object):
    """
    Class to send commands via TCP Eth from host to device server
    """

    def __init__(self, ip_server, port_server, caller, verbose=False):
        """
        Constructor

        type: string
        @param: ip_server - ip from server to connect

        type: string
        @param: port_server - port from server to connect

        type: string
        @param: caller - reference to a caller to diff behaviour
                         from normal to tcp shell

        type: bool
        @param: verbose - verbose flag to indicate watch in time or keep in
                          buffer response from server
        """

        self.client = None
        self.server_ip = ip_server
        self.server_port = int(port_server)
        self.caller = caller
        self.watch_flag = verbose

    #==========================================================================

    def start (self) :
        """
        Run Server.
        """

        #Check if client can run.
        rc = self.__canRun()

        #Setting up client interface
        if rc:
            rc, rout = self.__setUp()
        else:
            print(TOOLCFG.TCP_CLI_MSG_8)
            SYS.exitTC(SYS.EXIT_ERROR)

        if not rc and self.caller == TOOLCFG.TCP_CLI_SHELL:
            return rc, rout

        print(rout)
        return rc, rout

    #==========================================================================

    def stop (self, signum, frame):
        """
        Stop execution by signal trap

        type: signal
        @param: signum - sys signal

        type: stack
        @param: frame - stack traceback
        """

        if self.client:
            self.client.close()
        print(TOOLCFG.TCP_CLISRV_MSG_4 % signum)
        SYS.exitTC(SYS.EXIT_BY_SIGNAL)

    #==========================================================================

    def sendCommand (self, cmd) :
        """
        send command to server.

        type: string
        @param: cmd - string pattern with command to run
        """

        response_output = ''
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_ip, self.server_port))
            data = ''
            message = cmd
            self.client.send(message.encode())
            print (TOOLCFG.TCP_CLI_MSG_2 % message)
            #receive data and Wait for and End Command message from server
            while data != TOOLCFG.TCP_CLISRV_MSG_5 and not re.match(r'<EndCommand>+', data):
                self.client.settimeout(TOOLCFG.TCP_CLI_RESP_TIMEOUT)
                try:
                    data = self.client.recv(1024)
                    if data == "b''":
                        break
                    data = data.decode()
                    if self.watch_flag:
                        print ("%s" % data)
                    else:
                        response_output = '%s\n%s' % (response_output, data)

                except socket.timeout as e:
                    print(TOOLCFG.TCP_CLI_MSG_5 % e)
                    self.client.shutdown(socket.SHUT_WR)
                    break

                except:
                    print(TOOLCFG.TCP_CLI_MSG_6 % sys.exc_info()[0])
                    break

            self.client.close()

        except (ConnectionRefusedError, OSError) as e:
            return SYS.EXIT_ERROR, TOOLCFG.TCP_CLI_MSG_4


        return SYS.EXIT_NO_ERROR, response_output

    #==========================================================================

    def sendFile (self, source_file, file_dest) :
        """
        send file to server.

        type: string
        @param: source_file - full path for file to send

        type: string
        @param: file_dest - destination path into server
        """

        response_output = ''
        file_name = ''
        file_ext = ''
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_ip, self.server_port))
            data = ''

            if not os.path.exists(source_file):
                return SYS.EXIT_ERROR, TOOLCFG.TCP_CLI_MSG_9
            sizeof_file = os.path.getsize(source_file)

            #Splitting source file name and destination
            name = basename(source_file)
            file_fullname = name.split('.')
            file_name = file_fullname[0]
            if len(file_fullname) >= 2 :
                file_ext = file_fullname[1]
            message = 'SendFile:%s:%s:%s' % ( file_name, file_ext, file_dest )

            #Send command message to put server in Image Mode recv.
            self.client.send(message.encode())
            data = self.client.recv(1024)
            ok_resp = data.decode()
            data = ''
            print (TOOLCFG.TCP_CLI_MSG_2 % message)
            print ("%s" % ok_resp)
            self.client.close()

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_ip, self.server_port))
            #If we received OK ack from Server, Image file tranfer starts.
            if re.match(r'<Image Mode OK>+', ok_resp):
                time.sleep(1)
                f = open(source_file,'rb')
                file_stream = f.read(1024)
                perc_inc = 100/(sizeof_file/1024)
                cont = 1
                while (file_stream):
                    increment = 100 if (perc_inc*cont) > 100 else (perc_inc*cont)
                    print(TOOLCFG.TCP_CLI_MSG_10 % (increment, name))
                    self.client.send(file_stream)
                    file_stream = f.read(1024)
                    cont += 1
                print(TOOLCFG.TCP_CLI_MSG_11)
                self.client.shutdown(socket.SHUT_WR)
                print(self.client.recv(1024).decode())

            self.client.close()

        except (ConnectionRefusedError, OSError) as e:
            return SYS.EXIT_ERROR, TOOLCFG.TCP_CLI_MSG_4

        return SYS.EXIT_NO_ERROR, response_output

    #==========================================================================

    def __canRun (self) :
        """
        Set up of interface to Eth p2p com.
        """

        rc, rout = SYS.runShellCommand('ps ax | grep "ethp2p_server.py" | grep -v "grep"')

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
                if CFG.SW_TCP_CLIENT_IP != rout.strip('\n'):
                    print(TOOLCFG.TCP_CLISRV_MSG_7)
                    setIP_flag = True
            else:
                print(TOOLCFG.TCP_CLISRV_MSG_8)
                setIP_flag = True

            if setIP_flag:
                SYS.runShellCommand(TOOLCFG.TCP_CLISRV_INT_DOWN % (sudo_cmd, int_Ethernet))
                time.sleep(5)
                SYS.runShellCommand(TOOLCFG.TCP_CLISRV_INT_SET % (sudo_cmd, int_Ethernet, CFG.SW_TCP_CLIENT_IP))
                time.sleep(5)
                SYS.runShellCommand(TOOLCFG.TCP_CLISRV_INT_UP % (sudo_cmd, int_Ethernet ))
                time.sleep(10)
                message = TOOLCFG.TCP_CLISRV_MSG_9 % CFG.SW_TCP_CLIENT_IP

        return 0, message


#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """

    try:
        opts, argmts = getopt.getopt(args[1:], 'hcfv', ['help', 'command=', 'file_from=', 'file_to=', 'verbose='])
    except getopt.GetoptError as err:
        print(err)
        TOOLIB.MENU_ETHP2PCLIENT_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    command = ''
    source_file = ''
    dest_file = ''
    verbose = 0
    verbose_flag = False
    for option, value in opts:
        if option in ('--command'):
            command = value
        elif option in ('--file_from'):
            source_file = value
        elif option in ('--file_to'):
            dest_file = value
        elif option in ('--verbose'):
            verbose = value
        elif option in ('-h', '--help'):
            TOOLIB.MENU_ETHP2PCLIENT_USAGE()
            SYS.exitTC(SYS.EXIT_NO_ERROR)
        else:
            print(TOOLCFG.RDEF_MSG_1)
            SYS.exitTC(SYS.EXIT_ERROR)

    if not command and not source_file:
        print(TOOLCFG.TCP_CLI_MSG_7)
        TOOLIB.MENU_ETHP2PCLIENT_USAGE()
        SYS.exitTC(SYS.EXIT_ERROR)

    if int(verbose):
        verbose_flag = True

    client = ETHP2PClient(CFG.SW_TCP_SERVER_IP, CFG.SW_TCP_SERVER_PORT, args[0], verbose_flag)

    # set signal traps
    signal.signal(signal.SIGINT, client.stop)
    signal.signal(signal.SIGTERM, client.stop)

    while True:
        print(TOOLCFG.TCP_CLISRV_MSG_1)
        rc, rout = client.start()
        if not rc:
            break
        time.sleep(2)

    if command:
        rc, rout = client.sendCommand (command)
    else:
        rc, rout = client.sendFile (source_file, dest_file)

    if not verbose_flag:
        print(rout)
    elif args[0] == 'gui_usermode':
        print(rout)

    if rc:
        SYS.exitTC(SYS.EXIT_ERROR)

    if args[0] != TOOLCFG.TCP_CLI_SHELL:
        print(TOOLCFG.TCP_CLI_MSG_1)
        SYS.exitTC(SYS.EXIT_NO_ERROR)


if __name__ == "__main__":
    main(sys.argv)
