



let create_form = document.querySelector('form.create');
let update_form = document.querySelector('form.update');
let cancel_update_btn = document.querySelector('button.cancel-update');

let update_btns = document.querySelectorAll('button.update');
for (let update_btn of update_btns) {
    update_btn.onclick = function () {
        create_form.classList.add('d-none');
        update_form.classList.remove('d-none');
        cancel_update_btn.classList.remove('d-none');

        let record = update_btn.parentNode.parentNode;

        update_form.querySelector('input.name').value = record.querySelector('.name').textContent;
        update_form.querySelector('input.for-expenses').checked = record.querySelector('.for-expenses').textContent === 'Да';
        update_form.querySelector('input.id').value = record.querySelector('.id').textContent;
    }
}

cancel_update_btn.onclick = function () {
    update_form.classList.add('d-none');
    create_form.classList.remove('d-none');
    cancel_update_btn.classList.add('d-none');
}