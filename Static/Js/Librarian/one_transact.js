// Get all the elements
let csrf = document.getElementsByName('csrfmiddlewaretoken');
let show_status = document.getElementById('show_status');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');

// Functions
function performAction(action,transaction_id){

    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('action', action);

    $.ajax({
        type:'POST',
        url:'/performActionOnTransaction/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            
        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to complete action. Try again later.';

            // hide the error message
            setTimeout(() => {
                message_popup_failed.style.display = 'none';
                select_category_popup.style.display = 'none';
            }, 4000);

        }
    });
}