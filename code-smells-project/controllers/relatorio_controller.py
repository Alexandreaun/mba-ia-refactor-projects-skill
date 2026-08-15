from views.response import success


class RelatorioController:
    def __init__(self, pedido_model):
        self.pedido_model = pedido_model

    def relatorio_vendas(self):
        relatorio = self.pedido_model.relatorio_vendas()
        return success(relatorio)
