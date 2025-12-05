import sqlite3   # ou outro módulo de BD 

class BaseDAO:
    def __init__(self, conn: sqlite3.Connection, table_name: str, pk_name: str):
        self.conn = conn
        self.table_name = table_name
        self.pk_name = pk_name

    def create(self, data: dict):
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders})"
        cur = self.conn.cursor()
        cur.execute(sql, tuple(data.values()))
        self.conn.commit()
        return cur.lastrowid

    def read(self, pk):
        sql = f"SELECT * FROM {self.table_name} WHERE {self.pk_name} = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (pk,))
        return cur.fetchone()

    def update(self, pk, data: dict):
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.pk_name} = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (*data.values(), pk))
        self.conn.commit()
        return cur.rowcount

    def delete(self, pk):
        sql = f"DELETE FROM {self.table_name} WHERE {self.pk_name} = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (pk,))
        self.conn.commit()
        return cur.rowcount

    def list_all(self):
        sql = f"SELECT * FROM {self.table_name}"
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()