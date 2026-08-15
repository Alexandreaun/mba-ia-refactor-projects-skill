const bcrypt = require('bcryptjs');

const SALT_ROUNDS = 12;

function hashPassword(password) {
    return bcrypt.hash(password, SALT_ROUNDS);
}

module.exports = { hashPassword };
