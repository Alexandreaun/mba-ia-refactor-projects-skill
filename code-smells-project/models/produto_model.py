from constants import CATEGORIA_PADRAO, CATEGORIAS_VALIDAS, NOME_PRODUTO_MAX_LENGTH, NOME_PRODUTO_MIN_LENGTH


class ProdutoModel:
    def __init__(self, db):
        self.db = db

    def get_todos(self):
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM produtos")
        return [self._to_dict(row) for row in cursor.fetchall()]

    def get_por_id(self, produto_id):
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        row = cursor.fetchone()
        return self._to_dict(row) if row else None

    def criar(self, nome, descricao, preco, estoque, categoria):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
            (nome, descricao, preco, estoque, categoria),
        )
        conn.commit()
        return cursor.lastrowid

    def atualizar(self, produto_id, nome, descricao, preco, estoque, categoria):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
            (nome, descricao, preco, estoque, categoria, produto_id),
        )
        conn.commit()
        return True

    def deletar(self, produto_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conn.commit()
        return True

    def buscar(self, termo, categoria=None, preco_min=None, preco_max=None):
        cursor = self.db.get_connection().cursor()

        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        if termo:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            params.extend([f"%{termo}%", f"%{termo}%"])
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if preco_min is not None:
            query += " AND preco >= ?"
            params.append(preco_min)
        if preco_max is not None:
            query += " AND preco <= ?"
            params.append(preco_max)

        cursor.execute(query, params)
        return [self._to_dict(row) for row in cursor.fetchall()]

    @staticmethod
    def validar_dados(dados):
        if not dados:
            return "Dados inválidos"
        if "nome" not in dados:
            return "Nome é obrigatório"
        if "preco" not in dados:
            return "Preço é obrigatório"
        if "estoque" not in dados:
            return "Estoque é obrigatório"

        nome = dados["nome"]
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", CATEGORIA_PADRAO)

        if preco < 0:
            return "Preço não pode ser negativo"
        if estoque < 0:
            return "Estoque não pode ser negativo"
        if len(nome) < NOME_PRODUTO_MIN_LENGTH:
            return "Nome muito curto"
        if len(nome) > NOME_PRODUTO_MAX_LENGTH:
            return "Nome muito longo"
        if categoria not in CATEGORIAS_VALIDAS:
            return f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}"
        return None

    @staticmethod
    def _to_dict(row):
        return {
            "id": row["id"],
            "nome": row["nome"],
            "descricao": row["descricao"],
            "preco": row["preco"],
            "estoque": row["estoque"],
            "categoria": row["categoria"],
            "ativo": row["ativo"],
            "criado_em": row["criado_em"],
        }
