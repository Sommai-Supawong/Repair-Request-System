document.querySelectorAll('form[data-confirm]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    Swal.fire({title: form.dataset.confirm, icon: 'question', showCancelButton: true, confirmButtonText: 'ยืนยัน', cancelButtonText: 'ยกเลิก'})
      .then((result) => { if (result.isConfirmed) form.submit(); });
  });
});
