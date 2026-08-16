const logger = require('./logger');

class Cache {
    constructor() {
        this.store = new Map();
    }

    set(key, value) {
        logger.info(`Salvando no cache: ${key}`);
        this.store.set(key, value);
    }

    get(key) {
        return this.store.get(key);
    }
}

const cache = new Cache();

module.exports = { cache };
