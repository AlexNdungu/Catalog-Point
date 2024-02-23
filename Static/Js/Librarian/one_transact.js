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
    formData.append('transaction_id', transaction_id);

    $.ajax({
        type:'POST',
        url:'/performActionOnTransaction/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            if(response.status == 'not_found'){
                message_popup_failed.style.display = 'flex';
                failed_message_popup.innerHTML = 'Transaction not found';
                setTimeout(() => {
                    message_popup_failed.style.display = 'none';
                }, 4000);
            }
            else if(response.status == 'approved'){
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'Book transaction approved';
                // hide the two buttons
                document.getElementById('single_det_control_approved').style.display = 'none';
                document.getElementById('single_det_control_denied').style.display = 'none';
                document.getElementById('single_det_control_return').style.display = 'flex';
                show_status.innerHTML = 'Approved';
                setTimeout(() => {
                    message_popup_success.style.display = 'none';
                }, 4000);
            }
            else if(response.status == 'denied'){
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'Book transaction denied';
                // hide the two buttons
                document.getElementById('single_det_control_approved').style.display = 'none';
                document.getElementById('single_det_control_denied').style.display = 'none';
                document.getElementById('single_det_control_delete').style.display = 'flex';
                show_status.innerHTML = 'Denied';
                setTimeout(() => {
                    message_popup_success.style.display = 'none';
                }, 4000);
            }
            else if(response.status == 'returned'){
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'Book transaction returned';
                // hide the two buttons
                document.getElementById('single_det_control_return').style.display = 'none';
                document.getElementById('single_det_control_delete').style.display = 'flex';
                show_status.innerHTML = 'Returned';
                setTimeout(() => {
                    message_popup_success.style.display = 'none';
                }, 4000);
            }
            else if(response.status == 'deleted'){
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'Book transaction deleted';
                // hide the two buttons
                document.getElementById('single_det_control_delete').style.display = 'none';
                show_status.innerHTML = 'Deleted';
                setTimeout(() => {
                    message_popup_success.style.display = 'none';
                    // redirect to the transactions page
                    window.location.href = '/LibTransactions/';
                }, 4000);
            }

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