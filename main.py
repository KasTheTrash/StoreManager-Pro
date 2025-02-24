import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow,QVBoxLayout,  QWidget, QLabel, QPushButton, QTextEdit, QMdiSubWindow, QMdiArea, QDialog, QMessageBox ,QLineEdit, QPlainTextEdit ,QComboBox, QTableView 
from PyQt6.QtGui import QAction, QKeySequence, QKeyEvent, QShortcut, QIntValidator 
from PyQt6.QtCore import Qt
from PyQt6 import uic 
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import atexit
import psycopg2
from psycopg2 import errors 
from Forms.storage.insert.lib.dialog.ins_dialog import Ui_Dialog as InsertDialog
from Forms.storage.delete.lib.dialog.del_dialog import Ui_DellDialog as DellDialog
from Forms.management.Add_brand.add_brands import Ui_AddBrand as BrandDialog
from connect_database import ConnectDatabase
import sys


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
        uic.loadUi("main.ui", self)
        self.setWindowTitle("StoreManager PRO")
        
        self.db = ConnectDatabase()
        
        self.actionUpdate.triggered.connect(self.run_update_script)
        
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        self.setCentralWidget(self.mdi)
        
        #views findChild
        self.action_view = self.findChild(QAction, "aview")
        
        #inserts findChild
        self.action_c_ins = self.findChild(QAction, "acins") 
        
        #edit findChild
        self.action_edit = self.findChild(QAction, "aedit") 
        
        #deletes findChild
        self.action_delete = self.findChild(QAction, "adel")
        
        #add brand findChild
        self.action_addbrand = self.findChild(QAction, "actionAdd_brands")
        
        #views actions
        self.action_view.triggered.connect(self.view_item)
        
        #edits actions
        self.action_delete.triggered.connect(lambda: self.delete_item(DellDialog, 'Τροποποιησή στοιχείων'))
        
        #inserts actions
        self.action_c_ins.triggered.connect(lambda: self.insert_item(InsertDialog, 'Εισαγωγή στοιχείων'))
        
        #deletes actions
        self.action_edit.triggered.connect(self.view_item)
        
        self.action_addbrand.triggered.connect(self.show_brand_dialog)   #lambda: self.add_brands(BrandDialog, 'Προσθήκη νέου brand')
        
        #subwindows checking 
        self.sub_window_map = {}  # Change to a list
        
        self.show()
        
    def run_update_script(self):
        result = subprocess.run(['python', r'Forms/management/update/update.py'])
        if result.returncode == 0:
            print("Η εκτέλεση του update ήταν επιτυχής.")
            print(result.stdout) 
        else:
            print("Σφάλμα κατά την εκτέλεση του update.")
            print(result.stderr)  
        
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
        # κοιτάει μεσα στο map του subwindow αν υπαρχει η insert και δεν επιτρέπει να ξανα τρεξει αμα τρεχει ηδη
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
            print("Dialog setup successfully\n")
        except Exception as e:
            print(f"Error in dialog setup: {e}\n")
        
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
        print("Delete item action triggered")
        
        
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
            print("Dialog setup successfully\n")
        except Exception as e:
            print(f"Error in dialog setup: {e}\n")# Ή κάποιο άλλο μέθοδο για να ρυθμίσεις το UI
            
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
