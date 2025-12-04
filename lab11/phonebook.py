import psycopg2
import psycopg2.extras
def connect():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Hope2007@"
    )

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        phone VARCHAR(20)
    );
    """
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("Table created!")
    except Exception as e:
        print("Error creating table:", e)

def add_or_update_user(name, phone):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("CALL add_or_update_user(%s, %s)", (name, phone))
        conn.commit()
        cur.close()
        conn.close()
        print("User inserted or updated!")
    except Exception as e:
        print("Error:", e)

def search(pattern):
    try:
        conn = connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print("Search error:", e)

def insert_many(names, phones):
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "CALL insert_many_users(%s::text[], %s::text[], NULL)",
            (names, phones)
        )
        cur.execute("SELECT invalid_data FROM insert_many_users(%s, %s)",
                    (names, phones))
        invalid = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        print("Inserted many users!")
        print("Invalid data:", invalid)
    except Exception as e:
        print("Error inserting many users:", e)

def get_page(limit, offset):
    try:
        conn = connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM get_phonebook_page(%s, %s)",
                    (limit, offset))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        conn.close()
    except Exception as e:
        print("Pagination error:", e)

def delete_user(value):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("CALL delete_user_by_value(%s)", (value,))
        conn.commit()
        cur.close()
        conn.close()
        print("Deleted successfully!")
    except Exception as e:
        print("Delete error:", e)
if __name__ == "__main__":
    create_table()
