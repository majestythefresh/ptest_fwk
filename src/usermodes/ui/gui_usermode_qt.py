#!/usr/bin/env python3
#==============================================================================
#title           : gui_usermode.py
#description     : UI defition and template.
#author          : Arturo Plauchu (arturo.plauchu@gmail.com)
#date            : September 2017
#python_version  : 3 or later
#license         : GPL v2.0
#==============================================================================
"""
UI defition and template for GUI UserMode.
"""

#==============================================================================
#============================= FWK IMPORTS ====================================
#==============================================================================

from lib import common_lib as LIB
from config import config as CFG
from tools.tcpcom import ethp2p_client


#==============================================================================
#============================= OTHER IMPORTS ==================================
#==============================================================================

import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QAction, QMessageBox

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QTableView

#==============================================================================
#=================================== VARS =====================================
#==============================================================================

#UI template XML
qtCreatorFile = '%s/ui/gui_usermode.ui' % CFG.SW_USERMODES_PATH
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#==============================================================================
#================================ CLASSES =====================================
#==============================================================================

class TestDefinitionUI(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Class to represent test definition into GUI.
    """

    def __init__(self, args, test_def):
        """
        Constructor
        """

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        quit = QAction("Quit", self)
        quit.triggered.connect(self.cancelRun)
        self.args = args
        self.testdef = test_def

    #==========================================================================

    def setContent(self):
        """
        Set data to GUI elements according to test definition
        """

        #Populate text field elements and set chekc button values
        self.type_definition.setText('%s:' % self.args[1].upper())
        self.testdefinition_name.setText('%s' % self.args[2])
        if self.args[6]:
            self.test_id_edit.setText(self.args[6])

        if self.args[5]:
            self.log_folder_edit.setText(self.args[5])
        else:
            self.log_folder_edit.setText(CFG.SW_LOGS_PATH)

        if int(self.args[4]):
            self.parallel_radio_button.setChecked(True)
        else:
            self.normal_radio_button.setChecked(True)

        #Populate list elements
        data = []
        if self.args[1] == 'test':
            header = [ '', 'Order', 'Test Case', 'Mode', 'Conc. Inst.', 'Prot.', 'Args', 'Description']
            for testcase_key, testcase_value in sorted(self.testdef['test_cases'].items()):
                argmts = ''
                prot = '0'
                if testcase_value['protected']:
                    prot = '1'
                if 'args' in testcase_value:
                    argmts = testcase_value['args']
                data.append(['1',testcase_key, testcase_value['name'], testcase_value['mode'], testcase_value['concurrency_inst'], prot, argmts, testcase_value['descp']])
        else:
            header = ['','', 'Test', 'Order', 'Test Case', 'Mode', 'Conc. Inst.', 'Prot.', 'Args', 'Description']
            for test_key, test_value in self.testdef['tests'].items():
                test_name = test_value['name']
                #print(self.testdef['tests'][test_key]['test_cases'])
                for testcase_key, testcase_value in sorted(self.testdef['tests'][test_key]['test_cases'].items()):
                    argmts = ''
                    prot = '0'
                    if testcase_value['protected']:
                        prot = '1'
                    if 'args' in testcase_value:
                        argmts = testcase_value['args']
                    data.append(['1', test_key, test_name, testcase_key, testcase_value['name'], testcase_value['mode'], testcase_value['concurrency_inst'], prot, argmts, testcase_value['descp']])

        self.model = TestCaseModel(None, data, header, self.args[1])
        delegate = CheckBoxDelegate(None)
        self.definition_tableView.setItemDelegateForColumn(0, delegate)
        if self.args[1] == 'test':
            self.definition_tableView.setItemDelegateForColumn(5, delegate)
        else:
            self.definition_tableView.setItemDelegateForColumn(7, delegate)
        self.definition_tableView.resizeColumnsToContents()
        self.definition_tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.definition_tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.definition_tableView.clicked.connect(self.selectRow)
        self.definition_tableView.setModel(self.model)
        header = self.definition_tableView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        if self.args[1] == 'test':
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        else:
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)

    #==========================================================================

    def getCustomDefinition(self):
        """
        Get data from GUI elements according to test custom definition selected
        """

        run_mode = '0'

        test_id = self.test_id_edit.text()
        if test_id == 'Auto generated':
            test_id = ''

        log_folder = self.log_folder_edit.text()

        if self.parallel_radio_button.isChecked():
            run_mode = '1'

        #test_def = self.model.getCustomDefinition()
        tableview_content = self.model.getCustomDefinition()

        for row in (tableview_content):
            if int(row[0]):
                if self.args[1] == 'test':
                    if int(row[5]):
                        self.testdef['test_cases'][row[1]]['protected'] = 1
                    else :
                        self.testdef['test_cases'][row[1]]['protected'] = 0
                else:
                    if int(row[6]):
                        self.testdef['tests'][row[1]]['test_cases'][row[3]]['protected'] = 1
                    else :
                        self.testdef['tests'][row[1]]['test_cases'][row[3]]['protected'] = 0
            else:
                if self.args[1] == 'test':
                    del self.testdef['test_cases'][row[1]]
                else:
                    del self.testdef['tests'][row[1]]['test_cases'][row[3]]

        #return test_def, run_mode, test_id, log_folder
        return self.testdef, run_mode, test_id, log_folder

    #==========================================================================

    def closeEvent(self, event):
        """
        Close window event
        """

        sys.exit(0)

    #==========================================================================

    @pyqtSlot()
    def cancelRun(self):
        """
        Cancel button event
        """

        sys.exit(0)

    #==========================================================================

    @pyqtSlot()
    def selectDeviceRunEth(self):
        """
        Eth Radio Button event
        """

        self.log_folder_edit.setText('%s/%s/output/logs' % (CFG.SW_EMB_LINUX_PATH, CFG.SW_FWK_NAME))

    #==========================================================================

    @pyqtSlot()
    def selectDeviceRunLocal(self):
        """
        Local Radio Button event
        """

        self.log_folder_edit.setText(CFG.SW_LOGS_PATH)

    #==========================================================================

    @pyqtSlot()
    def runDef(self):
        """
        Run Button event
        """

        #Eth Radio Button Selected?
        if self.eth_radio_button.isChecked():
            testdef, run_mode, test_id, log_folder = self.getCustomDefinition()

            if testdef['type'] == 'test':
                for testcase_key, testcase_value in testdef['test_cases'].items():
                    del testcase_value['descp']
            else:
                for test_key, test_value in testdef['tests'].items():
                    for testcase_key, testcase_value in self.testdef['tests'][test_key]['test_cases'].items():
                        del testcase_value['descp']

            cmd = 'RunDefinition|%s|%s|%s|%s' % (testdef, run_mode, test_id, log_folder)
            #Call tcp client
            argms = ['gui_usermode', '--command=%s' % cmd, '--verbose=1']
            eth_p2p_client = getattr(ethp2p_client, 'main')
            eth_p2p_client(argms)
            sys.exit(0)

        else: #Local test
            QtCore.QCoreApplication.instance().quit()

    #==========================================================================

    @pyqtSlot()
    def selectRow(self):
        """
        Select list element event
        """

        #index = self.definition_tableView.selectedIndexes()
        #self.definition_tableView.model().setData(index, )
        #print ("index : ", index)
        pass

#==============================================================================

class CheckBoxDelegate(QtWidgets.QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column to which it's applied.
    """

    def __init__(self, parent):
        """
        Constructor
        """

        QtWidgets.QItemDelegate.__init__(self, parent)

    #==========================================================================

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """

        return None

    #==========================================================================

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """

        self.drawCheck(painter, option, option.rect, QtCore.Qt.Unchecked if int(index.data()) == 0 else QtCore.Qt.Checked)

    #==========================================================================

    def editorEvent(self, event, model, option, index):
        """
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        """

        if not int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False

        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            return True

        return False

    #==========================================================================

    def setModelData (self, editor, model, index):
        """
        The user wanted to change the old state in the opposite.
        """

        model.setData(index, 1 if int(index.data()) == 0 else 0, QtCore.Qt.EditRole)


#==============================================================================

class TestCaseModel(QtCore.QAbstractTableModel):
    """
    Table Model definition and behavior
    """

    def __init__(self, parent, mylist, header, type, *args):
        """
        Constructor
        """

        super(TestCaseModel, self).__init__()
        self.datatable = None
        self.header = header
        self.mylist = mylist
        self.type = type

    #==========================================================================

    def update(self, dataIn):
        self.datatable = dataIn

    #==========================================================================

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        if role == QtCore.Qt.EditRole:
            return value
        elif role == QtCore.Qt.DisplayRole:
            return value

    #==========================================================================

    def flags(self, index):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

    #==========================================================================

    def headerData(self, col, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    #==========================================================================

    def rowCount(self, parent):
        return len(self.mylist)

    #==========================================================================

    def columnCount(self, parent):
        return len(self.mylist[0])

    #==========================================================================

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return False
        #print(">>> setData() role = ", role)
        #print(">>> setData() index.column() = ", index.column())
        #print(">>> setData() index.data() = ", index.data())
        #print(">>> setData() value = ", value)
        #print(">>> setData() index.row = ", index.row())
        #print(">>> setData() index.column = ", index.column())
        if self.type == 'test':
            prot_column = 5
        else:
            prot_column = 7
        if index.column() == 0 or index.column() == prot_column:
            if index.data() == 0:
                self.mylist[index.row()][index.column()] = 1
            else:
                self.mylist[index.row()][index.column()] = 0
        return True

    #==========================================================================

    def getCustomDefinition(self):

        return self.mylist
