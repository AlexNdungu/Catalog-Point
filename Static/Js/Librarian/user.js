// get all the needed items
let csrf = document.getElementsByName('csrfmiddlewaretoken');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');


// functions
function deleteUser(){
    
    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('username', username);

    $.ajax({
        type:'POST',
        url:'/deleteUser/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            if(response.status == 'not_found'){
                // show error message
                message_popup_failed.style.display = 'flex';
                failed_message_popup.innerHTML = 'User not found. Try again later.';

                // hide error message after 4 seconds
                setTimeout(function(){
                    message_popup_failed.style.display = 'none';
                }, 4000);
            }
            else if(response.status == 'deleted'){
                // show success message
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'User deleted successfully. You will be redirected to the users page in 4 seconds.';

                // hide success message after 4 seconds
                setTimeout(function(){
                    message_popup_success.style.display = 'none';
                    window.location.href = '/AllUsers/';
                }, 4000);

            }

        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to delete the user. Try again later.';

            // hide error message after 4 seconds
            setTimeout(function(){
                message_popup_failed.style.display = 'none';
            }, 4000);
            
        }
    });
}