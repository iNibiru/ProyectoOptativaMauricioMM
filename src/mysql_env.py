from db_connection import create_connection, close_connection

def create_table(conn):
    query = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT,
            subject VARCHAR(100)
        ) ENGINE=InnoDB;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("Tabla 'students' creada o ya existente.")
    cursor.close()

def insert_student(conn, name, age, subject):
    query = "INSERT INTO students (name, age, subject) VALUES (%s, %s, %s);"
    cursor = conn.cursor()
    cursor.execute(query, (name, age, subject))
    conn.commit()
    print("Estudinte agregado: {name}")
    cursor.close()

def get_students(conn):
    query = "SELECT id, name, age, subject FROM students;"
    cursor = conn.cursor()
    cursor.execute(query)
    rows=cursor.fetchall()
    print("\nLista de estudiantes:")
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Age: {r[2]} | Subject: {r[3]}")
    cursor.close()

def main():
    conn= create_connection()
    if conn:
        create_table(conn)
        insert_student(conn, "Mauricio", 23, "Matemáticas")
        insert_student(conn, "KirG0D", 22, "Física")
        get_students(conn)
        close_connection(conn)

if __name__ == "__main__":
    main()
