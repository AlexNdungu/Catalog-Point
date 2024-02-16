// Get title and description of the category
let categ_title = document.getElementById('category_title');
let categ_description = document.getElementById('category_desc');
let csrf = document.getElementsByName('csrfmiddlewaretoken');
let cancel_btn = document.getElementById('cancel_btn');
let submit_btn = document.getElementById('add_cat_btn');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');


//
cancel_btn.addEventListener('click', discard);

// Discard function
function discard() {
    categ_title.value = '';
    categ_description.value = '';

    // Show the success pop up
    message_popup_failed.style.display = 'flex';
    failed_message_popup.innerHTML = 'Category creation has been discarded';

    // Hide the success pop up after 2 seconds
    setTimeout(function(){
        message_popup_failed.style.display = 'none';
    }, 4000);

}