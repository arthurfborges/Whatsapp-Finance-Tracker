import sqlite3

DB_PATH = "finance.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            parent_id INTEGER REFERENCES categories(id),
            UNIQUE (name, parent_id)
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            pluggy_id      TEXT NOT NULL UNIQUE,
            date           TEXT NOT NULL,          -- formato ISO: 2026-10-13
            amount_cents   INTEGER NOT NULL,       -- negativo = saiu, positivo = entrou
            bank_desc      TEXT,                   -- descrição original do banco
            user_note      TEXT,                   -- o que VOCÊ respondeu no WhatsApp
            category_id    INTEGER REFERENCES categories(id),
            kind           TEXT,                   -- expense / income / investment / transfer
            status         TEXT NOT NULL DEFAULT 'pending',
            raw_json       TEXT,
            created_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)

if __name__ == "__main__":
    init_db()
    print("Banco de dados criado")