const express = require('express');

function createRouter({ checkoutController, reportController, userController }) {
    const router = express.Router();

    router.post('/api/checkout', checkoutController.handle);
    router.get('/api/admin/financial-report', reportController.handle);
    router.delete('/api/users/:id', userController.delete);

    return router;
}

module.exports = createRouter;
