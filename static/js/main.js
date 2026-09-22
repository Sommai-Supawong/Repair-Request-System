(() => {
  const body = document.body;
  const menuButton = document.querySelector('[data-toggle-menu]');
  const menuBackdrop = document.querySelector('[data-close-menu]');
  const setMenu = (open) => {
    body.classList.toggle('menu-open', open);
    if (menuBackdrop) menuBackdrop.hidden = !open;
    if (menuButton) { menuButton.setAttribute('aria-expanded', String(open)); menuButton.setAttribute('aria-label', open ? 'ปิดเมนูหลัก' : 'เปิดเมนูหลัก'); }
  };
  menuButton?.addEventListener('click', () => setMenu(!body.classList.contains('menu-open')));
  menuBackdrop?.addEventListener('click', () => setMenu(false));
  document.querySelector('[data-toggle-filters]')?.addEventListener('click', (event) => {
    const panel = document.getElementById(event.currentTarget.getAttribute('aria-controls'));
    const open = panel?.classList.toggle('open') ?? false;
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });
  const closeModal = (modal) => { if (!modal) return; modal.hidden = true; body.classList.remove('modal-open'); };
  const openModal = (modal) => { if (!modal) return; modal.hidden = false; body.classList.add('modal-open'); window.setTimeout(() => modal.querySelector('input:not([type="hidden"]), select, textarea, button')?.focus(), 0); };
  document.querySelector('[data-toggle-create-user]')?.addEventListener('click', () => openModal(document.getElementById('createUser')));
  document.querySelectorAll('[data-toggle-user]').forEach((button) => button.addEventListener('click', () => openModal(document.getElementById(button.dataset.toggleUser))));
  document.querySelectorAll('[data-close-modal]').forEach((button) => button.addEventListener('click', () => closeModal(button.closest('.modal-shell'))));
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    const activeModal = document.querySelector('.modal-shell:not([hidden])');
    if (activeModal) closeModal(activeModal); else if (body.classList.contains('menu-open')) setMenu(false);
  });
  const errorMessage = (field) => {
    if (field.validity.valueMissing) return 'กรุณากรอกข้อมูลในช่องนี้';
    if (field.validity.typeMismatch) return 'กรุณากรอกข้อมูลให้ถูกต้อง';
    if (field.validity.tooShort) return `กรุณากรอกอย่างน้อย ${field.minLength} ตัวอักษร`;
    if (field.validity.rangeUnderflow) return `ค่าต้องไม่น้อยกว่า ${field.min}`;
    return 'กรุณาตรวจสอบข้อมูลในช่องนี้';
  };
  const showFieldState = (field) => {
    if (!field.matches('input, select, textarea') || field.type === 'hidden') return;
    const error = field.closest('.form-group')?.querySelector('.field-error');
    const invalid = !field.validity.valid;
    field.classList.toggle('invalid', invalid); field.setAttribute('aria-invalid', String(invalid));
    if (error) error.textContent = invalid ? errorMessage(field) : '';
  };
  document.querySelectorAll('form[data-validate]').forEach((form) => {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', (event) => {
      const fields = [...form.querySelectorAll('input, select, textarea')]; fields.forEach(showFieldState);
      const firstInvalid = fields.find((field) => !field.validity.valid);
      if (firstInvalid) { event.preventDefault(); firstInvalid.focus(); }
    });
    form.querySelectorAll('input, select, textarea').forEach((field) => {
      field.addEventListener('blur', () => showFieldState(field));
      field.addEventListener('input', () => { if (field.classList.contains('invalid')) showFieldState(field); });
      field.addEventListener('change', () => { if (field.classList.contains('invalid')) showFieldState(field); });
    });
  });
  document.querySelectorAll('[data-image-input]').forEach((input) => {
    input.addEventListener('change', () => {
      const preview = input.parentElement?.querySelector('[data-image-preview]') || input.nextElementSibling;
      if (!preview) return; preview.replaceChildren();
      [...input.files].forEach((file, index) => {
        const item = document.createElement('div'); item.className = 'preview-item';
        const image = document.createElement('img'); image.alt = `ตัวอย่าง ${file.name}`;
        const url = URL.createObjectURL(file); image.src = url; image.addEventListener('load', () => URL.revokeObjectURL(url), { once: true });
        const name = document.createElement('span'); name.textContent = file.name;
        const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'preview-remove'; remove.setAttribute('aria-label', `นำ ${file.name} ออก`); remove.textContent = '×';
        remove.addEventListener('click', () => {
          const transfer = new DataTransfer();
          [...input.files].forEach((selected, selectedIndex) => { if (selectedIndex !== index) transfer.items.add(selected); });
          input.files = transfer.files; input.dispatchEvent(new Event('change'));
        });
        item.append(image, name, remove); preview.append(item);
      });
    });
  });
  const confirmDialog = document.querySelector('[data-confirm-dialog]');
  const confirmMessage = confirmDialog?.querySelector('[data-confirm-message]');
  let pendingForm = null;
  document.querySelectorAll('form[data-confirm]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      if (event.defaultPrevented || form.dataset.confirmed === 'true') return;
      event.preventDefault(); pendingForm = form; if (confirmMessage) confirmMessage.textContent = form.dataset.confirm;
      if (confirmDialog) { confirmDialog.hidden = false; body.classList.add('modal-open'); confirmDialog.querySelector('[data-confirm-accept]')?.focus(); }
    });
  });
  const dismissConfirm = () => { if (confirmDialog) confirmDialog.hidden = true; body.classList.remove('modal-open'); pendingForm = null; };
  confirmDialog?.querySelector('[data-confirm-cancel]')?.addEventListener('click', dismissConfirm);
  confirmDialog?.querySelector('.confirm-backdrop')?.addEventListener('click', dismissConfirm);
  confirmDialog?.querySelector('[data-confirm-accept]')?.addEventListener('click', () => { if (!pendingForm) return; const form = pendingForm; dismissConfirm(); form.dataset.confirmed = 'true'; form.requestSubmit(); });
  document.querySelectorAll('[data-dismiss-toast]').forEach((button) => button.addEventListener('click', () => button.closest('.app-toast')?.remove()));
  document.querySelectorAll('.toast-success').forEach((toast) => window.setTimeout(() => toast.remove(), 4200));
  document.querySelector('[data-toggle-password]')?.addEventListener('click', (event) => {
    const input = event.currentTarget.parentElement?.querySelector('input'); if (!input) return;
    const visible = input.type === 'text'; input.type = visible ? 'password' : 'text'; event.currentTarget.textContent = visible ? 'แสดง' : 'ซ่อน'; event.currentTarget.setAttribute('aria-label', visible ? 'แสดงรหัสผ่าน' : 'ซ่อนรหัสผ่าน');
  });
  const search = document.querySelector('[data-user-search]');
  search?.addEventListener('input', () => { const query = search.value.trim().toLocaleLowerCase('th'); document.querySelectorAll('[data-user-row]').forEach((row) => { row.hidden = !row.dataset.searchText.toLocaleLowerCase('th').includes(query); }); });
})();
