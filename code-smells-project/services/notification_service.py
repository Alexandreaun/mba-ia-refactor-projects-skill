import logging

logger = logging.getLogger(__name__)


def notificar_pedido_criado(pedido_id, usuario_id):
    logger.info("Enviando e-mail: pedido %s criado para usuário %s", pedido_id, usuario_id)
    logger.info("Enviando SMS: pedido recebido")
    logger.info("Enviando push: novo pedido recebido pelo sistema")


def notificar_mudanca_status(pedido_id, novo_status):
    if novo_status == "aprovado":
        logger.info("Notificação: pedido %s foi aprovado, preparar envio", pedido_id)
    if novo_status == "cancelado":
        logger.info("Notificação: pedido %s cancelado, devolver estoque", pedido_id)
