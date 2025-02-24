import psycopg2
import sys


import os

try:
    # Σύνδεση στη βάση δεδομένων PostgreSQL
    conn = psycopg2.connect(
                user="postgres",
                password="123456",
                host="localhost",
                port="5432",
                database="StoreManager",
                client_encoding='UTF8'
            )
    # Ανοίγουμε ένα cursor για εκτέλεση εντολών
    cur = conn.cursor()
    # Βρες τη διαδρομή του φακέλου όπου βρίσκεται το update.py
    current_directory = os.path.dirname(__file__)
    # Δημιούργησε τη διαδρομή για το update.sql
    sql_file_path = os.path.join(current_directory, 'update.sql')
    
    # Διαβάζουμε τις SQL εντολές από ένα αρχείο κειμένου
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read()

    # Διαχωρισμός των εντολών εάν υπάρχουν πολλές
    commands = sql_commands.split(';')

    # Εκτέλεση των SQL εντολών από το αρχείο
    for command in commands:
        if command.strip():  # Βεβαιωθείτε ότι η εντολή δεν είναι κενή
            cur.execute(command)
    print("Οι εντολές εκτελέστηκαν με επιτυχία.")
    #print(sql_commands)
        
    # Εφαρμογή των αλλαγών στη βάση δεδομένων
    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print("Σφάλμα κατά την εκτέλεση των εντολών:"), error
    sys.exit(1)  # Κωδικός εξόδου 1 για αποτυχία
finally:
    # Κλείσιμο του cursor και της σύνδεσης
    if cur:
        cur.close()
    if conn:
        conn.close()
        
sys.exit(0)  # Κωδικός εξόδου 0 για επιτυχία
