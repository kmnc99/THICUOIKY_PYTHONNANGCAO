import psycopg2
class AppDatabase:
    def __init__(seft, db_name, user, password, host, port):
        seft.db_name = db_name
        seft.user =user
        seft.password = password
        seft.host=host
        seft.port = port
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            print("Error", f"Error connecting to the database: {e}")
            return False