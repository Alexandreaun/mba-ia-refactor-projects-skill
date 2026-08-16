class AdminModel:
    def __init__(self, db):
        self.db = db

    def reset_all(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM itens_pedido")
        cursor.execute("DELETE FROM pedidos")
        cursor.execute("DELETE FROM produtos")
        cursor.execute("DELETE FROM usuarios")
        conn.commit()

    def get_counts(self):
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos")
        produtos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        pedidos = cursor.fetchone()[0]
        return {"produtos": produtos, "usuarios": usuarios, "pedidos": pedidos}
