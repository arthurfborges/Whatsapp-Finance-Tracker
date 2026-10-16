from database import get_connection, init_db

# Chave = categoria principal, valor = lista de subcategorias
CATEGORIES = {
    "Alimentação": ["Mercado", "Restaurante", "Delivery"],
    "Transporte": [],
    "Moradia": [],
    "Saúde": [],
    "Lazer": [],
    "Educação": [],
    "Assinaturas": [],
    "Receitas": ["Salário/Bolsa", "Transferência recebida"],
    "Investimentos": ["Renda fixa", "Renda variável"],
    "Outros": [],
}


def get_or_create(conn, name, parent_id=None):
    # "IS" funciona também quando parent_id é NULL (com "=" não funcionaria)
    row = conn.execute(
        "SELECT id FROM categories WHERE name = ? AND parent_id IS ?",
        (name, parent_id),
    ).fetchone()
    if row:
        return row["id"]
    cur = conn.execute(
        "INSERT INTO categories (name, parent_id) VALUES (?, ?)",
        (name, parent_id),
    )
    return cur.lastrowid


def seed():
    init_db()
    with get_connection() as conn:
        for parent_name, children in CATEGORIES.items():
            parent_id = get_or_create(conn, parent_name)
            for child_name in children:
                get_or_create(conn, child_name, parent_id)


if __name__ == "__main__":
    seed()
    print("Categorias criadas.")