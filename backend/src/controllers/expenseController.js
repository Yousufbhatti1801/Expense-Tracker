export function listExpenses(req, res) {
  res.json({
    data: [],
    message: 'Boilerplate endpoint: connect a database in next step.'
  });
}

export function createExpense(req, res) {
  res.status(501).json({
    message: 'Not implemented yet. Add validation and persistence next.'
  });
}
