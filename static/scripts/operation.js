// create-btn
//
// let form_create = document.querySelector('td.create');
// let create_btn = document.querySelector('.btn.create');
//
// create_btn.onclick = function () {
//     if (create_btn.textContent === "Добавить запись") {
//         create_btn.textContent = 'Скрыть форму';
//         form_create.classList.remove('d-none');
//     } else {
//         create_btn.textContent = 'Добавить запись';
//         form_create.classList.add('d-none');
//     }
// }

// checkboxes

let checkboxes = document.querySelectorAll("td.checkbox>input");
let general_checkbox = document.querySelector("th>input");

general_checkbox.onchange = function () {
    for (let checkbox of checkboxes)
        checkbox.checked = general_checkbox.checked;
};

for (let checkbox of checkboxes) {
    checkbox.onchange = function () {
        if (!checkbox.checked)
            general_checkbox.checked = false;
    }
}

// create-btn
let tr_create = document.querySelector('tr.create');
let create_btn = tr_create.querySelector('.btn.create');

create_btn.onclick = async function () {
    let d = {};
    let elems = tr_create.querySelectorAll('.form-control');
    for (let elem of elems)
        d[elem.name] = elem.value;

    await fetch(location.pathname, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'text/json'
        },
        body: JSON.stringify(d)
    });
    location.reload()
};

// delete-btn

let del_btn = document.querySelector('.btn.delete');

del_btn.onclick = async function () {
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
};

// cancel-update-btn

let tr_update = document.querySelector('tr.update');
let cancel_update = document.querySelector('.btn.cancel-update');

cancel_update.onclick = function () {
    cancel_update.classList.add('d-none');
    tr_update.classList.add('d-none');
    tr_create.classList.remove('d-none');
};

// update-btn
let update_btns = document.querySelectorAll('.btn.update');
tr_update.classList.add('d-none');

for (let btn of update_btns)
    btn.onclick = async function () {

        cancel_update.classList.remove('d-none');
        let d = {};
        let record = btn.parentNode.parentNode;
        let elems = record.querySelectorAll('td.record');

        for (let elem of elems)
            d[elem.classList[0]] = elem.textContent;


        tr_update.classList.remove('d-none');
        tr_create.classList.add('d-none');

        var date = new Date(d['date']);
        let tzo = date.getTimezoneOffset() / 60;
        date.setHours(-tzo);
        d['date'] = date.toISOString().split('T')[0];

        d['amount'] = Math.abs(parseFloat(d['amount']));

        for (let x of tr_update.querySelectorAll('.form-control')) {
            x.value = d[x.classList[0]];
        }

        tr_update.querySelector('.id > b').textContent = d['id'];


    }

tr_update.querySelector('button.update').onclick = async function () {
    let elems = tr_update.querySelectorAll('.form-control');
    let d = {};
    for (let elem of elems)
        d[elem.name] = elem.value;

    d['id'] = tr_update.querySelector('td > b').textContent;

    await fetch(document.location.pathname, {
        method: 'UPDATE',
        mode: 'cors',
        headers: {
            'Content-Type': 'text/json'
        },
        body: JSON.stringify(d)
    });

    location.reload();
};


// last_id

let e = document.querySelector('td.checkbox > input');
let last_id = 0;
if (e !== null)
    last_id = e.dataset.id;
document.querySelector('td > b').textContent = parseInt(last_id) + 1;

// form-controls

let amount = tr_create.querySelector('input.form-control.amount');
let submit = tr_create.querySelector('.btn.create');
submit.setAttribute('disabled', '');

amount.onchange = function () {
    let val = parseFloat(amount.value);
    if (isNaN(val) || val <= 0) {
        submit.setAttribute('disabled', '');
        amount.classList.add('is-invalid');
    } else {
        submit.removeAttribute('disabled');
        amount.classList.remove('is-invalid');
        amount.value = val;
    }
};

amount_u = tr_update.querySelector('input.form-control.amount');
submit_u = tr_update.querySelector('.btn.update');

amount_u.onchange = function () {
    let val = parseFloat(amount_u.value);
    if (isNaN(val) || val <= 0) {
        submit_u.setAttribute('disabled', '');
        amount_u.classList.add('is-invalid');
    } else {
        submit_u.removeAttribute('disabled');
        amount_u.classList.remove('is-invalid');
        amount_u.value = val;
    }
};