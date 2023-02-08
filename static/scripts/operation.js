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

// filter

let category_general_checkbox = document.querySelector('label > input.category-general');
let cat_checkboxes = document.querySelectorAll('label > input.category');

category_general_checkbox.onchange = function () {
    for (let checkbox of cat_checkboxes)
        checkbox.checked = category_general_checkbox.checked;
};

for (let checkbox of cat_checkboxes) {
    checkbox.onchange = function () {
        if (!checkbox.checked)
            category_general_checkbox.checked = false;
    }
}

let account_general_checkbox = document.querySelector('label > input.account-general');
let acc_checkboxes = document.querySelectorAll('label > input.account');

account_general_checkbox.onchange = function () {
    for (let checkbox of acc_checkboxes)
        checkbox.checked = account_general_checkbox.checked;
};

for (let checkbox of acc_checkboxes) {
    checkbox.onchange = function () {
        if (!checkbox.checked)
            account_general_checkbox.checked = false;
    }
}

let filter_form = document.querySelector('form.filter');
let filter_btn = document.querySelector('.btn.filter');
let filter_hide_btn = document.querySelector('.btn.filter-hide');
let search_btn = document.querySelector('.btn.search');

filter_btn.onclick = function () {
    search_btn.classList.remove('d-none');
    filter_hide_btn.classList.remove('d-none');
    filter_btn.classList.add('d-none');
    filter_form.classList.remove('d-none');
}

filter_hide_btn.onclick = function () {
    search_btn.classList.add('d-none');
    filter_hide_btn.classList.add('d-none');
    filter_btn.classList.remove('d-none');
    filter_form.classList.add('d-none');
}

if (location.href.includes('&') && location.href.includes('?'))
    filter_btn.click();

search_btn.onclick = function () {
    let general_category = filter_form.querySelector('input.hidden-input-category');
    let categories = filter_form.querySelectorAll('label > input.category');
    let cat_ids = [];
    for (let category of categories) {
        if (category.checked)
            cat_ids.push(parseInt(category.value));
    }
    general_category.value = JSON.stringify(cat_ids);

    let general_account = filter_form.querySelector('input.hidden-input-account');
    let accounts = filter_form.querySelectorAll('label > input.account');
    let acc_ids = [];
    for (let account of accounts) {
        if (account.checked)
            acc_ids.push(parseInt(account.value));
    }
    general_account.value = JSON.stringify(acc_ids);

    filter_form.submit();
}



/*
search_btn.onclick = async function () {
    let d = {}

    d['categories'] = [];
    for (let x of cat_checkboxes) {
        if (x.checked)
            d['categories'].push(x.dataset.id);
    }

    d['accounts'] = [];
    for (let x of acc_checkboxes) {
        if (x.checked)
            d['accounts'].push(x.dataset.id);
    }

    let date_from = filter_form.querySelector('input.date-from').value;
    let date_to = filter_form.querySelector('input.date-to').value;
    if (date_from !== '')
        d['date_from'] = date_from;
    if (date_to.value !== '')
        d['date_to'] = date_to;

    let amount_from = filter_form.querySelector('input.amount-from').value;
    let amount_to = filter_form.querySelector('input.amount-to').value;
    if (amount_from !== '')
        d['amount_from'] = amount_from;
    if (amount_to.value !== '')
        d['amount_to'] = amount_to;

    let notice = filter_form.querySelector('textarea.notice').value;
    if (notice !== '')
        d['notice'] = notice;

    await fetch(location.pathname, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'text/json'
        },
        body: JSON.stringify(d)
    });

    location.reload();
}
*/

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

let analysis_btn = document.querySelector('.btn.analysis');
let analysis_div = document.querySelector('div.analysis');

analysis_btn.onclick = function () {
    if (analysis_btn.textContent === 'Аналитика'){
        analysis_div.classList.remove('d-none');
        analysis_btn.textContent = 'Скрыть аналитику';
        analysis_btn.classList.remove('btn-primary');
        analysis_btn.classList.add('btn-danger');
    }
    else {
        analysis_div.classList.add('d-none');
        analysis_btn.textContent = 'Аналитика';
        analysis_btn.classList.add('btn-primary');
        analysis_btn.classList.remove('btn-danger');
    }

}


// last_id

// let e = document.querySelector('td.checkbox > input');
// let last_id = 0;
// if (e !== null)
//     last_id = e.dataset.id;
// document.querySelector('td > b').textContent = parseInt(last_id) + 1;

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