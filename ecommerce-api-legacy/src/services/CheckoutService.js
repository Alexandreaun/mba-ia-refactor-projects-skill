const { hashPassword } = require('../utils/crypto');
const { cache } = require('../utils/cache');
const logger = require('../utils/logger');
const { PAYMENT_STATUS, VISA_CARD_PREFIX, DEFAULT_PASSWORD } = require('../config/constants');

class CheckoutService {
    constructor({ courseModel, userModel, enrollmentModel, paymentModel, auditLogModel, config }) {
        this.courseModel = courseModel;
        this.userModel = userModel;
        this.enrollmentModel = enrollmentModel;
        this.paymentModel = paymentModel;
        this.auditLogModel = auditLogModel;
        this.config = config;
    }

    async checkout({ userName, email, password, courseId, cardNumber }) {
        const course = await this.courseModel.findActiveById(courseId);
        if (!course) {
            throw Object.assign(new Error('Curso não encontrado'), { status: 404 });
        }

        const existingUser = await this.userModel.findByEmail(email);
        const userId = existingUser ? existingUser.id : await this._registerUser(userName, email, password);

        logger.info(`Processando pagamento na chave ${this.config.paymentGatewayKey}`, {
            card: `${cardNumber.slice(0, 4)}********`,
        });
        const status = cardNumber.startsWith(VISA_CARD_PREFIX) ? PAYMENT_STATUS.PAID : PAYMENT_STATUS.DENIED;

        if (status === PAYMENT_STATUS.DENIED) {
            throw Object.assign(new Error('Pagamento recusado'), { status: 400 });
        }

        const enrollment = await this.enrollmentModel.create(userId, courseId);
        await this.paymentModel.create(enrollment.lastID, course.price, status);
        await this.auditLogModel.record(`Checkout curso ${courseId} por ${userId}`);

        cache.set(`last_checkout_${userId}`, course.title);

        return { message: 'Sucesso', enrollmentId: enrollment.lastID };
    }

    async _registerUser(userName, email, password) {
        const passwordHash = await hashPassword(password || DEFAULT_PASSWORD);
        const created = await this.userModel.create({ name: userName, email, passwordHash });
        return created.lastID;
    }
}

module.exports = CheckoutService;
