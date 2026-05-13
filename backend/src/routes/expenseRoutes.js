import { Router } from 'express';
import { createExpense, listExpenses } from '../controllers/expenseController.js';

const router = Router();

router.get('/', listExpenses);
router.post('/', createExpense);

export default router;
