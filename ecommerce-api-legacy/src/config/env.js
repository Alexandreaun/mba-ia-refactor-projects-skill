const fs = require('fs');
const path = require('path');

function loadEnvFile() {
    const envPath = path.resolve(__dirname, '../../.env');
    if (!fs.existsSync(envPath)) return;

    const content = fs.readFileSync(envPath, 'utf-8');
    content.split('\n').forEach((line) => {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) return;

        const separatorIndex = trimmed.indexOf('=');
        if (separatorIndex === -1) return;

        const key = trimmed.slice(0, separatorIndex).trim();
        const value = trimmed.slice(separatorIndex + 1).trim();
        if (!(key in process.env)) process.env[key] = value;
    });
}

loadEnvFile();

const config = {
    port: Number(process.env.PORT) || 3000,
    dbUser: process.env.DB_USER,
    dbPass: process.env.DB_PASS,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    smtpUser: process.env.SMTP_USER,
};

module.exports = { config };
