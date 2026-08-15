from flask import jsonify


def success(data=None, status=200, **extra):
    body = {"sucesso": True}
    if data is not None:
        body["dados"] = data
    body.update(extra)
    return jsonify(body), status


def error(message, status=400, **extra):
    body = {"erro": message, "sucesso": False}
    body.update(extra)
    return jsonify(body), status
