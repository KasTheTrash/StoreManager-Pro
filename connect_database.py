import psycopg2 
from psycopg2 import errors

from PyQt6.QtWidgets import QMessageBox , QTableView

class ConnectDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
                user="postgres",
                password="123456",
                host="localhost",
                port="5432",
                database="StoreManager",
                client_encoding='UTF8'
            )#self.cursor = self.conn.cursor()

    def product_insert(self, c_productcode, c_pname, c_color, c_brand_comboBox, c_seasons, c_size, c_material, c_description, c_buying_price, c_sale_price, c_gross_profit, c_price_per_unit, c_quantity, c_tax_percentage):
        print("Executing SQL query with the following data:")
        print(f"Product Code: {c_productcode}, Name: {c_pname}, Brand: {c_brand_comboBox}, etc.")
        
        c_quantity = float(c_quantity)
        c_sale_price = float(c_sale_price)
        
        c_gross_profit = c_quantity * c_sale_price

        # Construct SQL query with placeholders for safe insertion
        sql = """
            INSERT INTO product (pname, color, productcode, brand, seasons, size, material, description, buying_price, sale_price, gross_profit, price_per_unit, quantity, tax_percentage) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """ 

        try:
            with self.conn.cursor() as cursor:
                if self.product_code_exists(c_productcode):
                    print("Product code already exists. Aborting insert.")
                    QMessageBox.warning(None, "Invalid Input", "Ο κωδικός προϊόντος υπάρχει ήδη στη βάση δεδομένων .!.", QMessageBox.StandardButton.Ok)

                    return "Duplicate Product Code"  # Επιστρέφεις κάποιο μήνυμα ή σφάλμα

                # Execute the SQL query with the provided data
                cursor.execute(sql, (c_pname, c_color, c_productcode, c_brand_comboBox, c_seasons, c_size, c_material, c_description, c_buying_price, c_sale_price, c_gross_profit, c_price_per_unit, c_quantity, c_tax_percentage))
                self.conn.commit()
                QMessageBox.information(None, "Success", "Data inserted successfully.", QMessageBox.StandardButton.Ok)
                print("Data inserted successfully.")
            return None
        
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()  # Rollback the transaction on duplicate error
            print("Unique constraint violation detected. Error:", e)
            return None

        except psycopg2.IntegrityError as e:
            self.conn.rollback()  # Rollback the transaction
            print("Insert failed:", e)
            return None
        
        except psycopg2.Error as e:
            print(f"Error occurred: {e}")
            self.conn.rollback()
            return e

    def tabel_insert_view(self,brand_filter=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM product
                    WHERE brand is not null
                    ORDER BY id
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None
        
        #sql = "SELECT * FROM product WHERE brand is not null" #= 'Canguro'
        #
        #with self.conn.cursor() as cursor:
        #        cursor.execute(sql)
        #        result = cursor.fetchall()
        #        #print("Fetched Data:", result)  # Εκτύπωση των δεδομένων
        #        return result

    def tabel_delete_view(self,brand_filter=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM product
                    WHERE brand is not null
                    ORDER BY id
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None
        
        #sql = "SELECT * FROM product WHERE brand is not null" #= 'Canguro'
        #
        #with self.conn.cursor() as cursor:
        #        cursor.execute(sql)
        #        result = cursor.fetchall()
        #        #print("Fetched Data:", result)  # Εκτύπωση των δεδομένων
        #        return result

    def product_code_exists(self, c_productcode):
        sql = "SELECT COUNT(*) FROM product WHERE productcode = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (c_productcode,))
            result = cursor.fetchone()
            return result[0] > 0

    def delete_exists(self, del_productcode,del_seasons,del_brand_comboBox,del_color):
        sql = "SELECT COUNT(*) FROM product WHERE productcode = %s AND seasons = %s AND brand = %s AND color = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (del_productcode,del_seasons,del_brand_comboBox,del_color))
            result = cursor.fetchone()
            return result[0] > 0

    def delete_product(self, del_productcode,del_seasons,del_brand_comboBox, del_quantity, del_color, del_sale_price):
        if not all([del_productcode, del_seasons, del_brand_comboBox, del_color]):
            QMessageBox.warning(None, "Missing Data", 
                "Παρακαλώ συμπληρώστε όλα τα απαραίτητα πεδία (κωδικός, εποχή, μάρκα, χρώμα).", 
                QMessageBox.StandardButton.Ok)
            return None
    
        print("Executing SQL query with the following data:")
        print(f"Product Code: { del_productcode}, seasons: {del_seasons}, Brand: {del_brand_comboBox}, quantity: {del_quantity}, color: {del_color}, sale_price: {del_sale_price}")
        
        if not self.delete_exists(del_productcode, del_seasons, del_brand_comboBox, del_color):
            QMessageBox.warning(None, "Product Not Found", 
                "Το προϊόν με τα συγκεκριμένα στοιχεία δεν βρέθηκε στη βάση δεδομένων.", 
                QMessageBox.StandardButton.Ok)
            return "Product Not Found"
        
        update_sql = """
            UPDATE product
            SET quantity = quantity - %s,
                sale_price = sale_price + %s
            WHERE productcode = %s 
                AND seasons = %s 
                AND brand = %s 
                AND color = %s
                AND quantity >= %s;
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(update_sql, (del_quantity, del_sale_price, del_productcode, del_seasons, del_brand_comboBox, del_color, del_quantity))

                if cursor.rowcount == 0:
                    self.conn.rollback()
                    QMessageBox.warning(None, "Update Failed", 
                        "Η ενημέρωση απέτυχε. Πιθανώς η ποσότητα είναι μεγαλύτερη από το διαθέσιμο απόθεμα.", 
                        QMessageBox.StandardButton.Ok)
                    return None
            
                self.conn.commit()
                QMessageBox.information(None, "Success", 
                    "Η ενημέρωση ολοκληρώθηκε με επιτυχία.", 
                    QMessageBox.StandardButton.Ok)
                print("Data updated successfully.")
                return True
            
        except psycopg2.errors.UniqueViolation as e:
            self.conn.rollback()  # Rollback the transaction on duplicate error
            print("Unique constraint violation detected. Error:", e)
            return None

        except psycopg2.IntegrityError as e:
            self.conn.rollback()  # Rollback the transaction
            print("Insert failed:", e)
            return None
        
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(None, "Error", 
                f"Σφάλμα κατά την ενημέρωση: {str(e)}", 
                QMessageBox.StandardButton.Ok)
            print(f"Error occurred: {e}")
            return None

    def close(self):
        # Κλείσιμο της σύνδεσης όταν τελειώσει η χρήση της βάσης δεδομένων
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
