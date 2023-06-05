import sqlite3
        
class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_file)

    def close_connection(self):
        self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS mywgs
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        price REAL,
                        size REAL,
                        wg_size TEXT,
                        quarter TEXT,
                        address TEXT,
                        availability TEXT,
                        link TEXT,
                        distance REAL,
                        contacted INTEGER)''')
        
        

    def insert_dictionary(self, dictionary):
        self.create_connection()
        cursor = self.conn.cursor()
        query = '''INSERT INTO mywgs (title, price, size, wg_size, quarter, address, availability, link, distance, contacted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        values = (dictionary['title'], dictionary['price'], float(dictionary['size']), dictionary['wg-size'],
                dictionary['quater'], dictionary['address'], dictionary['availability'],
                dictionary['link'], float(dictionary['distance']), int(dictionary['contacted']))
        cursor.execute(query, values)
        self.conn.commit()
        
        
    def entry_exists(self, link):
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM mywgs WHERE link = ?", (link,))
        count = cursor.fetchone()[0]
        return count > 0
    

    def retrieve_all_dictionaries(self):
        self.create_connection()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mywgs")
        result = cursor.fetchall()
        retrieved_dicts = []
        for row in result:
            retrieved_dict = {
                'title': row[1],
                'price': row[2],
                'size': row[3],
                'wg-size': row[4],
                'quater': row[5],
                'address': row[6],
                'availability': row[7],
                'link': row[8],
                'distance': row[9],
                'contacted': bool(row[10])
            }
            retrieved_dicts.append(retrieved_dict)
        return retrieved_dicts
    
    
    def write_dicts_to_table(self,dicts):
        self.create_connection()
        self.create_table()
        for dictionary in dicts:
            self.insert_dictionary( dictionary)
        self.close_connection()
    
    
    def read_dicts_from_table(self):
        self.create_connection()
        retrieved_dicts = self.retrieve_all_dictionaries()
        self.close_connection()
        return retrieved_dicts