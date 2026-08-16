from constants import (
    DESCONTO_FAIXA_1_LIMIAR,
    DESCONTO_FAIXA_1_TAXA,
    DESCONTO_FAIXA_2_LIMIAR,
    DESCONTO_FAIXA_2_TAXA,
    DESCONTO_FAIXA_3_LIMIAR,
    DESCONTO_FAIXA_3_TAXA,
    STATUS_APROVADO,
    STATUS_CANCELADO,
    STATUS_PENDENTE,
)


class PedidoModel:
    def __init__(self, db):
        self.db = db

    def criar(self, usuario_id, itens):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        produto_ids = [item["produto_id"] for item in itens]
        placeholders = ",".join("?" for _ in produto_ids)
        cursor.execute(f"SELECT * FROM produtos WHERE id IN ({placeholders})", produto_ids)
        produtos_por_id = {row["id"]: row for row in cursor.fetchall()}

        total = 0
        for item in itens:
            produto = produtos_por_id.get(item["produto_id"])
            if produto is None:
                return {"erro": f"Produto {item['produto_id']} não encontrado"}
            if produto["estoque"] < item["quantidade"]:
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            total += produto["preco"] * item["quantidade"]

        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, ?, ?)",
            (usuario_id, STATUS_PENDENTE, total),
        )
        pedido_id = cursor.lastrowid

        for item in itens:
            produto = produtos_por_id[item["produto_id"]]
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], produto["preco"]),
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"]),
            )

        conn.commit()
        return {"pedido_id": pedido_id, "total": total}

    def get_por_usuario(self, usuario_id):
        return self._listar(usuario_id=usuario_id)

    def get_todos(self):
        return self._listar()

    def _listar(self, usuario_id=None):
        cursor = self.db.get_connection().cursor()
        if usuario_id is not None:
            cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?", (usuario_id,))
        else:
            cursor.execute("SELECT * FROM pedidos")
        pedidos_rows = cursor.fetchall()
        if not pedidos_rows:
            return []

        pedido_ids = [row["id"] for row in pedidos_rows]
        placeholders = ",".join("?" for _ in pedido_ids)
        cursor.execute(
            f"""
            SELECT itens_pedido.pedido_id, itens_pedido.produto_id, itens_pedido.quantidade,
                   itens_pedido.preco_unitario, produtos.nome AS produto_nome
            FROM itens_pedido
            LEFT JOIN produtos ON produtos.id = itens_pedido.produto_id
            WHERE itens_pedido.pedido_id IN ({placeholders})
            """,
            pedido_ids,
        )
        itens_por_pedido = {}
        for item in cursor.fetchall():
            itens_por_pedido.setdefault(item["pedido_id"], []).append({
                "produto_id": item["produto_id"],
                "produto_nome": item["produto_nome"] if item["produto_nome"] else "Desconhecido",
                "quantidade": item["quantidade"],
                "preco_unitario": item["preco_unitario"],
            })

        return [
            {
                "id": row["id"],
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": itens_por_pedido.get(row["id"], []),
            }
            for row in pedidos_rows
        ]

    def atualizar_status(self, pedido_id, novo_status):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
        conn.commit()
        return True

    def relatorio_vendas(self):
        cursor = self.db.get_connection().cursor()

        cursor.execute("SELECT COUNT(*) FROM pedidos")
        total_pedidos = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total) FROM pedidos")
        faturamento = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", (STATUS_PENDENTE,))
        pendentes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", (STATUS_APROVADO,))
        aprovados = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", (STATUS_CANCELADO,))
        cancelados = cursor.fetchone()[0]

        desconto = 0
        if faturamento > DESCONTO_FAIXA_1_LIMIAR:
            desconto = faturamento * DESCONTO_FAIXA_1_TAXA
        elif faturamento > DESCONTO_FAIXA_2_LIMIAR:
            desconto = faturamento * DESCONTO_FAIXA_2_TAXA
        elif faturamento > DESCONTO_FAIXA_3_LIMIAR:
            desconto = faturamento * DESCONTO_FAIXA_3_TAXA

        return {
            "total_pedidos": total_pedidos,
            "faturamento_bruto": round(faturamento, 2),
            "desconto_aplicavel": round(desconto, 2),
            "faturamento_liquido": round(faturamento - desconto, 2),
            "pedidos_pendentes": pendentes,
            "pedidos_aprovados": aprovados,
            "pedidos_cancelados": cancelados,
            "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
        }
