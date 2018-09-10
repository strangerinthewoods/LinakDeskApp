# MIT License
# 
# Copyright (c) 2017 Arkadiusz Netczuk <dev.arnet@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


import sys

from . import uiloader
from . import tray_icon
from .qt import QApplication

from linakdeskapp.gui.devices_list_dialog import DevicesListDialog



UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class MainWindow(QtBaseClass):
    def __init__(self):
        super().__init__()
        self.connector = None
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.statusBar().showMessage("Ready")
        
        ## Init QSystemTrayIcon
        self.tray_icon = tray_icon.TrayIcon(self)
        self.tray_icon.show()

    def attachConnector(self, connector):
        if self.connector != None:
            ## disconnect from old object
            self.connector.newConnection.disconnect( self.newConnection )
            
        self.connector = connector
        self.connector.newConnection.connect( self.newConnection )


    # =======================================


    ## slot
    def newConnection(self, deviceObject):
        if deviceObject == None:
            return
        self.ui.deviceControl.attachDevice( deviceObject )
        
    ## slot
    def closeApplication(self):
        self.close()

    ## slot
    def connectToDevice(self):
        deviceDialog = DevicesListDialog(self)
        deviceDialog.attachConnector(self.connector)
        deviceDialog.exec_()                            ### modal mode
    
    ## slot    
    def disconnectFromDevice(self):
        self.ui.deviceControl.attachDevice( None )

        
    # =======================================


    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.show()
#         self.tray_icon.showMessage( "Tray Program",
#                                     "Application was minimized to Tray",
#                                     QSystemTrayIcon.Information, 2000
#                                 )


def execApp():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec_())
