const logger = require('../utils/logger');

function errorHandler(err, req, res, next) {
    logger.error(`Erro não tratado em ${req.method} ${req.originalUrl}`, {
        error: err.message,
        stack: err.stack,
    });

    const status = err.status || 500;
    const message = status === 500 ? 'Erro interno do servidor' : err.message;
    res.status(status).send(message);
}

module.exports = errorHandler;
