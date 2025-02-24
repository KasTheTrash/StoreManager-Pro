from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QPushButton, 
                            QLineEdit, QLabel, QMessageBox)
from PyQt6 import QtCore
import sys
sys.path.append(r'C:\Users\SUPERPC\Desktop\StoreManager_Pro')
from connect_database import ConnectDatabase

class Ui_AddBrand(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = ConnectDatabase()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        
        self.layout = QVBoxLayout(Dialog)
        
        # Label για το νέο brand
        self.label = QLabel("Εισάγετε νέα μάρκα:")
        self.layout.addWidget(self.label)
        
        # Text field για εισαγωγή νέου brand
        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Όνομα μάρκας")
        self.layout.addWidget(self.brand_input)
        
        # Κουμπί για προσθήκη
        self.add_button = QPushButton("Προσθήκη")
        self.add_button.clicked.connect(self.add_brand)
        self.layout.addWidget(self.add_button)
        
        # ComboBox που θα δείχνει τα υπάρχοντα brands
        self.label_existing = QLabel("Υπάρχουσες μάρκες:")
        self.layout.addWidget(self.label_existing)
        
        self.brands_combo = QComboBox()
        self.layout.addWidget(self.brands_combo)
        
        self.load_existing_brands()
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Προσθήκη Νέας Μάρκας"))

    def load_existing_brands(self):
        try:
            with self.db.conn.cursor() as cursor:
                #cursor.execute("SELECT DISTINCT brand FROM product WHERE brand IS NOT NULL ORDER BY brand")
                cursor.execute("SELECT DISTINCT brand_name FROM brands WHERE brand_name IS NOT NULL AND active = True ORDER BY brand_name")
                brands = cursor.fetchall()
                self.brands_combo.clear()
                for brand in brands:
                    self.brands_combo.addItem(brand[0])
        except Exception as e:
            QMessageBox.warning(self, "Σφάλμα", f"Σφάλμα κατά τη φόρτωση των μαρκών: {str(e)}")

    def add_brand(self):
        new_brand = self.brand_input.text().strip()
        if not new_brand:
            QMessageBox.warning(self, "Σφάλμα", "Παρακαλώ εισάγετε όνομα μάρκας")
            return

        try:
            # Έλεγχος αν η μάρκα υπάρχει ήδη
            with self.db.conn.cursor() as cursor:
                #cursor.execute("SELECT COUNT(*) FROM product WHERE brand = %s", (new_brand,))
                cursor.execute("SELECT COUNT(*) FROM brands WHERE brand_name = %s", (new_brand,))
                if cursor.fetchone()[0] > 0:
                    QMessageBox.warning(self, "Σφάλμα", "Η μάρκα υπάρχει ήδη!")
                    return

                # Εισαγωγή νέας μάρκας (προσάρμοσε το query ανάλογα με τη δομή της βάσης σου)
                cursor.execute("INSERT INTO brands (brand_name) VALUES (%s)", (new_brand,))
                self.db.conn.commit()
                
                self.brands_combo.addItem(new_brand)
                self.brand_input.clear()
                QMessageBox.information(self, "Επιτυχία", "Η μάρκα προστέθηκε επιτυχώς!")
                self.load_existing_brands()  # Ανανέωση της λίστας

        except Exception as e:
            self.db.conn.rollback()
            QMessageBox.warning(self, "Σφάλμα", f"Σφάλμα κατά την προσθήκη: {str(e)}")
