#!/bin/bash
#***********************************************************************
#Pip Modules
sudo pip3 install setuptools
sudo pip3 install pyqt5

ptest_fwk_path="/Users/plauchu/Workspace/ptest_fwk"
#Create symbolic link to bin path
sudo mkdir -p /usr/local/bin
sudo rm /usr/local/bin/ptfwk_*
sudo ln -s ${ptest_fwk_path}/tools/create_profile.py /usr/local/bin/ptfwk_create_profile
sudo ln -s ${ptest_fwk_path}/tools/create_test.py /usr/local/bin/ptfwk_create_test
sudo ln -s ${ptest_fwk_path}/tools/generate_backup.py /usr/local/bin/ptfwk_generate_backup
sudo ln -s ${ptest_fwk_path}/tools/remove_profile.py /usr/local/bin/ptfwk_remove_profile
sudo ln -s ${ptest_fwk_path}/tools/remove_test.py /usr/local/bin/ptfwk_remove_test
sudo ln -s ${ptest_fwk_path}/tools/run_profile.py /usr/local/bin/ptfwk_run_profile
sudo ln -s ${ptest_fwk_path}/tools/run_test.py /usr/local/bin/ptfwk_run_test
sudo ln -s ${ptest_fwk_path}/tools/shell_tcp.py /usr/local/bin/ptfwk_shell_tcp
sudo ln -s ${ptest_fwk_path}/tools/validate_test.py /usr/local/bin/ptfwk_validate_test
sudo ln -s ${ptest_fwk_path}/tools/tcpcom/ethp2p_server.py /usr/local/bin/ptfwk_ethp2p_server
sudo ln -s ${ptest_fwk_path}/tools/tcpcom/ethp2p_client.py /usr/local/bin/ptfwk_ethp2p_client
