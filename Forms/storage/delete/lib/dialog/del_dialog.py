from PyQt6.QtWidgets import QDialog,QMessageBox ,QComboBox
import psycopg2
from PyQt6.QtGui import QKeyEvent,QStandardItemModel, QStandardItem
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6 import uic 
from connect_database import ConnectDatabase

class Ui_DellDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Forms/storage/delete/lib/dialog/del_dialog.ui", self)
        self.del_add_pushButton.clicked.connect(self.del_product_info)
        self.setWindowTitle("Προβολή & Διαχείριση Δεδομένων")
        self.del_table_update()
        
        self.load_existing_brands()
        
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()  # Αγνοεί το πλήκτρο Esc
        else:
            super().keyPressEvent(event)  # Για όλα τα άλλα πλήκτρα, ακολουθεί την κανονική συμπεριφορ

    def get_del_product_info(self):
        print("get_del_product_info")
        # Function to retrieve product information from the form
        del_productcode = self.del_productcode_lineEdit.text().strip()
        del_seasons = self.del_season_lineEdit.text().strip()
        del_brand_comboBox = self.del_brand_comboBox.currentText()
        del_quantity = self.del_quantity_lineEdit.text().strip()
        del_color = self.del_color_lineEdit.text().strip()
        del_sale_price = self.del_sale_price_lineEdit.text().strip()
        del_description = self.del_description_plainTextEdit.toPlainText().strip()
        
        product_info = {
            "del_productcode": del_productcode,
            "del_color": del_color,
            "del_seasons": del_seasons,
            "del_description": del_description,
            "del_sale_price": del_sale_price,
            "del_quantity": del_quantity,
            "del_brand_comboBox": del_brand_comboBox
            }
        
        return product_info

    def del_product_info(self):
        del_product_info = self.get_del_product_info()
        print("Product Info:", del_product_info)
        
        self.db = ConnectDatabase()
        
        if  not del_product_info["del_productcode"].strip():
            QMessageBox.warning(None, "Invalid Input", "Product Code must be a valid Text.", QMessageBox.StandardButton.Ok)
            return
        
        if   not del_product_info["del_seasons"].strip():
            QMessageBox.warning(None, "Invalid Input", "Seasons must be a valid integer.", QMessageBox.StandardButton.Ok)
            return
        
        elif self.del_brand_comboBox.currentText().strip() == "" or self.del_brand_comboBox.count() == 0:
            QMessageBox.warning(None, "Invalid Input", "Brand  must be a valid integer.", QMessageBox.StandardButton.Ok)
            return
        
        elif not del_product_info["del_quantity"].isdigit():
            QMessageBox.warning(None, "Invalid Input", "Quantity  must be a valid integer.", QMessageBox.StandardButton.Ok)
            return
        
        elif not del_product_info["del_color"].isdigit():
            QMessageBox.warning(None, "Invalid Input", "Color must be a valid Color.", QMessageBox.StandardButton.Ok)
            return
        
        elif not del_product_info["del_sale_price"].isdigit():
            QMessageBox.warning(None, "Invalid Input", "Sale price must be a valid integer.", QMessageBox.StandardButton.Ok)
            return
        success = False
        try:
            # Insert product info into the database     
            if del_product_info["del_productcode"] and del_product_info["del_brand_comboBox"] is not None and del_product_info ["del_seasons"] and del_product_info ["del_quantity"] and del_product_info ["del_sale_price"]:
                print("deleting product info into the database...")
                delete_result = self.db.delete_product(del_productcode=del_product_info["del_productcode"],
                                                    del_seasons=del_product_info["del_seasons"],
                                                    del_brand_comboBox=del_product_info["del_brand_comboBox"],
                                                    del_quantity=del_product_info["del_quantity"],
                                                    del_color=del_product_info["del_color"],
                                                    del_sale_price=del_product_info["del_sale_price"]
                                                    #del_description=del_product_info["del_description"]
                                                    )
                if delete_result == "Product Not Found":
                    success = False
                else:
                    success = True
            if success:
                self.clear_fields()                 
                
        except psycopg2.errors.UniqueViolation as e:
            self.db.connection.rollback()  # Rollback the transaction on duplicate error
            print("Unique constraint violation detected. Error:", e)  # Debugging print

            # Display message box for duplicate key error
            QMessageBox.warning(
                self, 
                "Product Not Found", 
                f"Product code ({del_product_info['del_productcode']}) Product Not Found.", 
                QMessageBox.StandardButton.Ok
            )
            #self.add_btn.setDisabled(False)
        except psycopg2.IntegrityError as e:
            self.db.connection.rollback()  # Rollback the transaction in case of a general IntegrityError
            error_message = str(e)
            print("IntegrityError detected:", error_message)  # Debugging print

            QMessageBox.warning(
                self, 
                "Insert Failed", 
                f"Insert failed due to a database constraint: {error_message}", 
                QMessageBox.StandardButton.Ok
            )
            #self.add_btn.setDisabled(False)
        except Exception as e:
            #self.db.connection.rollback()  # Rollback the transaction in case of other unexpected errors
            # Handle any other unexpected errors
            print("An unexpected error occurred:", e)  # Debugging print
            QMessageBox.critical(None, "Database Error", "An unexpected error occurred: {}".format(str(e)))
            
        self.del_table_update()
            
    def del_table_update(self, brand_filter=None):
        try:
            #print("del_table_update")
            self.db = ConnectDatabase()
            #print("Updating table...")
            data = self.db.tabel_delete_view()  # brand_filter brand_filter='Canguro'
            #print("Data for table update:", data)
            if data is None:
                print("No data returned from database")
                return
            # Δημιουργία μοντέλου
            self.model = QStandardItemModel()
            self.model.setHorizontalHeaderLabels(["ID" ,"Product Code", "Name", "Color", "Brand", "Seasons", "Size", "Material", "Description", "Buying Price", "Sale Price", "Gross Profit", "Price Per Unit", "Quantity", "Tax Percentage", "creation date"])

            for row in data:
                items = [QStandardItem(str(item)) for item in row]
                self.model.appendRow(items)

            self.proxy_model = QSortFilterProxyModel()
            self.proxy_model.setSourceModel(self.model)
            self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
            if hasattr(self, 'del_tableView'):
                self.del_tableView.setModel(self.proxy_model)
                self.del_tableView.setSortingEnabled(True)

                # Προαιρετικά: Ρύθμιση μεγέθους στηλών
                for column in range(self.model.columnCount()):
                    self.del_tableView.resizeColumnToContents(column)
            else:
                print("del_tableView not found")

        except Exception as e:
            print(f"Error in del_table_update: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to update table: {str(e)}")

    def load_existing_brands(self):
        try:
            self.db = ConnectDatabase()
            with self.db.conn.cursor() as cursor:
                #cursor.execute("SELECT DISTINCT brand FROM product WHERE brand IS NOT NULL ORDER BY brand")
                cursor.execute("SELECT DISTINCT brand_name FROM brands WHERE brand_name IS NOT NULL AND active = True ORDER BY brand_name")
                brands = cursor.fetchall()
                self.del_brand_comboBox.clear()
                for brand in brands:
                    self.del_brand_comboBox.addItem(brand[0])
        except Exception as e:
            QMessageBox.warning(self, "Σφάλμα", f"Σφάλμα κατά τη φόρτωση των μαρκών: {str(e)}")

    def clear_fields(self):
        self.del_productcode_lineEdit.clear()
        self.del_color_lineEdit.clear()
        self.del_season_lineEdit.clear()
        self.del_quantity_lineEdit.clear()
        self.del_sale_price_lineEdit.clear()
        self.del_description_plainTextEdit.clear()
        self.del_brand_comboBox.setCurrentIndex(0)