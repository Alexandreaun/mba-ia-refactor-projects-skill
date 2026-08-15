class UserController {
    constructor({ userService }) {
        this.userService = userService;
        this.delete = this.delete.bind(this);
    }

    async delete(req, res, next) {
        try {
            const message = await this.userService.deleteUser(req.params.id);
            res.send(message);
        } catch (error) {
            next(error);
        }
    }
}

module.exports = UserController;
