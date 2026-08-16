from werkzeug.security import check_password_hash, generate_password_hash

from constants import TIPO_USUARIO_PADRAO


class UsuarioModel:
    def __init__(self, db):
        self.db = db

    def get_todos(self):
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM usuarios")
        return [self._to_dict(row) for row in cursor.fetchall()]

    def get_por_id(self, usuario_id):
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        return self._to_dict(row) if row else None

    def criar(self, nome, email, senha, tipo=TIPO_USUARIO_PADRAO):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, generate_password_hash(senha), tipo),
        )
        conn.commit()
        return cursor.lastrowid

    def login(self, email, senha):
        cursor = self.db.get_connection().cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row and check_password_hash(row["senha"], senha):
            return {"id": row["id"], "nome": row["nome"], "email": row["email"], "tipo": row["tipo"]}
        return None

    @staticmethod
    def _to_dict(row):
        return {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "tipo": row["tipo"],
            "criado_em": row["criado_em"],
        }
