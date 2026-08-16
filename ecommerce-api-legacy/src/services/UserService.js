class UserService {
    constructor({ userModel }) {
        this.userModel = userModel;
    }

    async deleteUser(id) {
        await this.userModel.delete(id);
        return 'Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.';
    }
}

module.exports = UserService;
