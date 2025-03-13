# StoreManager-Pro

StoreManager PRO is a warehouse management application that uses the PyQt6 library for the graphical interface and a PostgreSQL database for storing product data.

## Features
- Add, edit, and delete products from the database.
- Manage brands.
- View products through the UI.
- Connect to PostgreSQL via `psycopg2`.
- Fully functional GUI based on PyQt6.

## Requirements
To run the application, you need:

- Python 3.8 or later
- PostgreSQL
- The following Python packages (found in `requirements.txt`):

```sh
pip install -r requirements.txt
```

## Installation & Execution
1. Clone the repository:
   ```sh
   git clone https://github.com/KasTheTrash/StoreManager-PRO.git
   cd StoreManager-PRO
   ```
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python main.py
   ```

## Database Configuration
The application connects to a PostgreSQL database. Make sure you configure the correct credentials in `connect_database.py`:
```python
self.conn = psycopg2.connect(
    user="postgres",
    password="123456",
    host="localhost",
    port="5432",
    database="StoreManager",
    client_encoding='UTF8'
)
```
**Important:** Update the connection details according to your database settings.

## Project Structure
```
StoreManager-PRO/
│-- main.py                # Main application file
│-- connect_database.py    # Database connection
│-- requirements.txt       # Required dependencies
│-- Forms/                 # UI files
│-- management/            # Brand management
│-- storage/               # Warehouse management
```

## Contribution
If you want to contribute:
1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request!

## License
This project is licensed under the MIT License.

