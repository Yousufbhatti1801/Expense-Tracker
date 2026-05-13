import { renderExpenseForm } from '../components/expense-form.js';

export function renderDashboard(rootEl) {
  rootEl.innerHTML = `
    <div class="card">
      <h2>Dashboard (Boilerplate)</h2>
      <p>Total: Rs 0</p>
      <div id="expense-form-slot"></div>
    </div>
  `;

  const slot = rootEl.querySelector('#expense-form-slot');
  if (slot) {
    renderExpenseForm(slot);
  }
}
