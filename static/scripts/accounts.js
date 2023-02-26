

let create_form = document.querySelector('form.create');
let update_form = document.querySelector('form.update');
let cancel_update_btn = document.querySelector('button.cancel-update');
let delete_transfers = document.querySelector('button.delete-transfers')

let update_btns = document.querySelectorAll('button.update');
for (let update_btn of update_btns) {
    update_btn.onclick = function () {
        create_form.classList.add('d-none');
        update_form.classList.remove('d-none');
        cancel_update_btn.classList.remove('d-none');

        let record = update_btn.parentNode.parentNode;


        update_form.querySelector('h2').textContent = 'Редактирование счёта ' + record.querySelector('.id').textContent;

        update_form.querySelector('input.name').value = record.querySelector('.name').textContent;
        update_form.querySelector('input.balance').value = record.querySelector('.balance').textContent;
        update_form.querySelector('input.id').value = record.querySelector('.id').textContent;
    }
}

cancel_update_btn.onclick = function () {
    update_form.classList.add('d-none');
    create_form.classList.remove('d-none');
    cancel_update_btn.classList.add('d-none');
}

let transfer_btn = document.querySelector('.btn.transfer');
let transfer_form = document.querySelector('div.transfer');

transfer_btn.onclick = function () {
    if (transfer_btn.textContent === 'Перевод'){
        transfer_form.classList.remove('d-none');
        transfer_btn.textContent = 'Отмена перевода';
        transfer_btn.classList.remove('btn-success');
        transfer_btn.classList.add('btn-danger');
        delete_transfers.classList.remove('d-none');
    }
    else {
        transfer_form.classList.add('d-none');
        transfer_btn.textContent = 'Перевод';
        transfer_btn.classList.add('btn-success');
        transfer_btn.classList.remove('btn-danger');
        delete_transfers.classList.add('d-none');
    }
}

let transfer_create_btn = document.querySelector('.btn.create');


let checkboxes = document.querySelectorAll('td.checkbox > input');
let general_checkbox = document.querySelector('th > input');

general_checkbox.onclick = function () {
    for (let checkbox of checkboxes) {
        checkbox.checked = general_checkbox.checked;
    }
}

for (let checkbox of checkboxes) {
    checkbox.onclick = function () {
        if (!checkbox.checked)
            general_checkbox.checked = false;
    }
}


delete_transfers.onclick = async function () {
    let ids = [];
    for (let checkbox of checkboxes)
        if (checkbox.checked)
            ids.push(checkbox.dataset.id);


    await fetch(document.location.pathname, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
            'Content-Type': 'text/json'
        },
        body: JSON.stringify({'ids': ids})
    });

    location.reload();
}

