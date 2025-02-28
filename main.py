import subprocess
import os
import sys
import logging
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow,QVBoxLayout, QStatusBar, QWidget, QLabel, QPushButton, QTextEdit, QMdiSubWindow, QMdiArea, QDialog, QMessageBox ,QLineEdit, QPlainTextEdit ,QComboBox, QTableView 
from PyQt6.QtGui import QAction, QKeySequence, QKeyEvent, QShortcut, QIntValidator 
from PyQt6.QtCore import Qt
from PyQt6 import uic 
from Forms.storage.insert.lib.dialog.ins_dialog import Ui_Dialog as InsertDialog
from Forms.storage.delete.lib.dialog.del_dialog import Ui_DellDialog as DellDialog
from Forms.management.Add_brand.add_brands import Ui_AddBrand as BrandDialog
from connect_database import ConnectDatabase

APP_VERSION = "Alpha 1.0"
logging.basicConfig(level=logging.INFO)

class MyDialog(QDialog):
    def __init__(self, dialog_type):
        super().__init__()
        self.ui = dialog_type()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()  # Αγνοεί το πλήκτρο Esc
        else:
            super().keyPressEvent(event)  # Για όλα τα άλλα πλήκτρα, ακολουθεί την κανονική συμπεριφορ
            
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "main.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("StoreManager PRO")
        
        # Set up version label
        self.statusBar = self.findChild(QStatusBar, "statusbar")
        self.versionLabel = QLabel(f"Version: {APP_VERSION}")
        self.statusBar.addWidget(self.versionLabel)
        #addWidget() moving the verion label to the right
        #addPermanentWidget() moving the verion label to the left

        self.db = ConnectDatabase()

        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.setCentralWidget(self.mdi)

        self.sub_window_map = {}  # Change to a list
        self.setup_actions()
        self.show()
        
    def setup_actions(self):
        self.actionUpdate.triggered.connect(self.run_update_script)
        self.findChild(QAction, "aview").triggered.connect(self.view_item)
        self.findChild(QAction, "acins").triggered.connect(lambda: self.insert_item(InsertDialog, 'Εισαγωγή στοιχείων'))
        self.findChild(QAction, "aedit").triggered.connect(self.view_item)
        self.findChild(QAction, "adel").triggered.connect(lambda: self.delete_item(DellDialog, 'Τροποποιησή στοιχείων'))
        self.findChild(QAction, "actionAdd_brands").triggered.connect(self.show_brand_dialog)

    def run_update_script(self):
        try:
            result = subprocess.run(['python', r'Forms/management/update/update.py'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("Update script executed successfully.")
                logging.info(result.stdout)
            else:
                logging.error("Error running update script.")
                logging.error(result.stderr)
        except Exception as e:
            logging.exception("Exception while running update script.")

    def view_item(self):
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle('view item')
            sub.destroyed.connect(lambda: self.sub_window_closed('view'))
            self.mdi.addSubWindow(sub)
            self.mdi.tabsClosable()
            sub.show()
            self.sub_window_map['view'] = sub
            
    def insert_item(self, dialog_type,title):
        if 'insert'in self.sub_window_map:
            existing_sub_window = self.sub_window_map['insert']
            if existing_sub_window.isVisible():
                existing_sub_window.raise_()  
                return  

        sub = QMdiSubWindow()
        sub.setWindowTitle(title)
        sub.setFixedSize(940, 655)
        sub.setWindowFlags(Qt.WindowType.SubWindow | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

        try:
            cdialog = dialog_type()
            cdialog.setupUi(sub)
            logging.info("Dialog setup successfully\n")
        except Exception as e:
            logging.exception(f"Error in dialog setup: {e}\n")
        
        self.sub_window_map['insert'] = sub
        self.dialog_instance = cdialog
        
        self.mdi.addSubWindow(sub)
        sub.show()

    def edit_item(self):
        sub = QMdiSubWindow()
        sub.setWidget(QTextEdit())
        sub.setWindowTitle('delete item')
        sub.destroyed.connect(lambda: self.sub_window_closed('delete'))
        self.mdi.addSubWindow(sub)
        sub.show()
        logging.info("Delete item action triggered")
        
        
    def delete_item(self, dialog_type,title):
        if 'edit'in self.sub_window_map:
            existing_sub_window = self.sub_window_map['edit']
            if existing_sub_window.isVisible():
                existing_sub_window.raise_()  
                return  

        sub = QMdiSubWindow()
        sub.setWindowTitle(title)
        sub.setFixedSize(940, 655)
        sub.setWindowFlags(Qt.WindowType.SubWindow | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowCloseButtonHint)

        try:
            dialog = dialog_type()
            sub.setWidget(dialog)
            logging.info("Dialog setup successfully\n")
        except Exception as e:
            logging.exception(f"Error in dialog setup: {e}\n")
            
        self.sub_window_map['edit'] = sub
        
        self.mdi.addSubWindow(sub)
        sub.show()
    
    def show_brand_dialog(self):
        dialog = BrandDialog(self)
        dialog.exec()
        
if __name__ == "__main__":
    import sys
    import atexit
    app = QApplication(sys.argv)
    #@atexit.register
    UIWindow = UI()
    sys.exit(app.exec())
