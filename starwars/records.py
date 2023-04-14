import sqlite3

def inicializar_base_datos():
    conn = sqlite3.connect("records.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            record INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

inicializar_base_datos()

def agregar_record(nombre, record):
    conn = sqlite3.connect("records.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO records (nombre, record) VALUES (?, ?)", (nombre, record))
    
    conn.commit()
    conn.close()


def actualizar_record(id, record):
    conn = sqlite3.connect("records.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE records SET record = ? WHERE id = ?", (record, id))
    
    conn.commit()
    conn.close()


def recuperar_records():
    conn = sqlite3.connect("records.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM records ORDER BY record DESC")
    records = [{"id": r[0], "nombre": r[1], "record": r[2]} for r in cursor.fetchall()]
    
    conn.close()
    
    return records