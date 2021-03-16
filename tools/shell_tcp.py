#!/usr/bin/env python3
#==============================================================================
#title           : shell_tcp.py
#description     : Command to execute mini shell via tcp p2p eth
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
Command to execute mini shell via tcp p2p eth
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from config import config as CFG
from lib import sys_lib as SYS
from tools.toolsconfig import tools_config as TOOLCFG
from tools.tcpcom import ethp2p_client

#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
import cmd

#==============================================================================
#================================ FUNCTIONS ===================================
#==============================================================================

#...

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class Commands(cmd.Cmd):
    """
    Class to manage commands like shell behaviour
    """

    prompt = TOOLCFG.TCP_CLI_SHELL_PROMPT % CFG.SW_TCP_SERVER_IP

    #Auto complete
    SH_CMDS = [ 'ls -l', 'ls -l $HOME', 'ls $HOME/workspace', 'ls -l /usr/bin/', 'dmesg' ]

    #==========================================================================

    def do_shell(self, command):
        """
        execute a shell command into connected device
        example: shell ls -l
        """

        cmd = 'ShellCommand:%s' % command
        #Call tcp client
        argms = [TOOLCFG.TCP_CLI_SHELL, '--command=%s' % cmd]
        client_main = getattr(ethp2p_client, 'main')
        client_main(argms)

    def do_sendFile(self, command):
        """
        send file to connected device
        example: sendFile /home/plauchu/testfile.txt /root/workspace
        """

        sfile = command.split(' ')
        if len(sfile) > 1:
            #Call tcp client
            argms = [TOOLCFG.TCP_CLI_SHELL, '--file_from=%s' % sfile[0], '--file_to=%s' % sfile[1]]
            client_main = getattr(ethp2p_client, 'main')
            client_main(argms)
        else:
            print('Error', sfile)
            SYS.exitTC(SYS.EXIT_ERROR)

    #==========================================================================

    def complete_shell(self, text, line, begidx, endidx):
        if not text:
            completions = self.SH_CMDS[:]
        else:
            completions = [ f
                            for f in self.SH_CMDS
                            if f.startswith(text)
                            ]
        return completions

    #==========================================================================

    def do_quit(self, line):
        """
        quit program
        """

        SYS.exitTC(SYS.EXIT_NO_ERROR)

    #==========================================================================

    def do_exit(self, line):
        """
        quit program
        """

        SYS.exitTC(SYS.EXIT_NO_ERROR)

    #==========================================================================

    def do_EOF(self, line):
        return True

#==============================================================================
#================================ MAIN ========================================
#==============================================================================

def main(args):
    """
    Main function
    """
    cmd = Commands()
    cmd.cmdloop(TOOLCFG.TCP_CLI_SHELL_MSG_1)

if __name__ == "__main__":
    main(sys.argv)
