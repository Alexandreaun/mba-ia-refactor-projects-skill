const { PAYMENT_STATUS } = require('../config/constants');

class ReportService {
    constructor({ reportModel }) {
        this.reportModel = reportModel;
    }

    async getFinancialReport() {
        const rows = await this.reportModel.financialReportRows();
        const coursesByI = new Map();

        rows.forEach((row) => {
            if (!coursesByI.has(row.course_id)) {
                coursesByI.set(row.course_id, { course: row.course_title, revenue: 0, students: [] });
            }

            const courseData = coursesByI.get(row.course_id);
            if (row.enrollment_id == null) return;

            if (row.payment_status === PAYMENT_STATUS.PAID) {
                courseData.revenue += row.paid_amount;
            }

            courseData.students.push({
                student: row.student_name || 'Unknown',
                paid: row.paid_amount || 0,
            });
        });

        return Array.from(coursesByI.values());
    }
}

module.exports = ReportService;
