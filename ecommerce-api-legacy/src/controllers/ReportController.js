class ReportController {
    constructor({ reportService }) {
        this.reportService = reportService;
        this.handle = this.handle.bind(this);
    }

    async handle(req, res, next) {
        try {
            const report = await this.reportService.getFinancialReport();
            res.json(report);
        } catch (error) {
            next(error);
        }
    }
}

module.exports = ReportController;
