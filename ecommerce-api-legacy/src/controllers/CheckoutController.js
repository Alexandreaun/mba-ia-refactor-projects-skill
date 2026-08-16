class CheckoutController {
    constructor({ checkoutService }) {
        this.checkoutService = checkoutService;
        this.handle = this.handle.bind(this);
    }

    async handle(req, res, next) {
        try {
            const { usr: userName, eml: email, pwd: password, c_id: courseId, card: cardNumber } = req.body;

            if (!userName || !email || !courseId || !cardNumber) {
                return res.status(400).send('Bad Request');
            }

            const result = await this.checkoutService.checkout({ userName, email, password, courseId, cardNumber });
            res.status(200).json({ msg: result.message, enrollment_id: result.enrollmentId });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = CheckoutController;
