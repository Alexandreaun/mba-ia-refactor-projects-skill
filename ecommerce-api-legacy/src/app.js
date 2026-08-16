const express = require('express');
const { config } = require('./config/env');
const Database = require('./models/db');
const UserModel = require('./models/UserModel');
const CourseModel = require('./models/CourseModel');
const EnrollmentModel = require('./models/EnrollmentModel');
const PaymentModel = require('./models/PaymentModel');
const AuditLogModel = require('./models/AuditLogModel');
const ReportModel = require('./models/ReportModel');
const CheckoutService = require('./services/CheckoutService');
const ReportService = require('./services/ReportService');
const UserService = require('./services/UserService');
const CheckoutController = require('./controllers/CheckoutController');
const ReportController = require('./controllers/ReportController');
const UserController = require('./controllers/UserController');
const createRouter = require('./routes');
const errorHandler = require('./middleware/errorHandler');
const logger = require('./utils/logger');

async function bootstrap() {
    try {
        const app = express();
        app.use(express.json());

        const db = new Database();
        await db.init();
        logger.info('Banco de dados inicializado com sucesso.');

        const userModel = new UserModel(db);
        const courseModel = new CourseModel(db);
        const enrollmentModel = new EnrollmentModel(db);
        const paymentModel = new PaymentModel(db);
        const auditLogModel = new AuditLogModel(db);
        const reportModel = new ReportModel(db);

        const checkoutService = new CheckoutService({
            courseModel,
            userModel,
            enrollmentModel,
            paymentModel,
            auditLogModel,
            config,
        });
        const reportService = new ReportService({ reportModel });
        const userService = new UserService({ userModel });

        const checkoutController = new CheckoutController({ checkoutService });
        const reportController = new ReportController({ reportService });
        const userController = new UserController({ userService });

        app.use(createRouter({ checkoutController, reportController, userController }));
        app.use(errorHandler);

        app.listen(config.port, () => {
            logger.info(`Frankenstein LMS rodando e pronto na porta ${config.port}...`);
        });
    } catch (error) {
        logger.error('Falha crítica ao iniciar a aplicação', { error: error.message, stack: error.stack });
        process.exit(1);
    }
}

bootstrap();
