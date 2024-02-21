// get all the needed items
let csrf = document.getElementsByName('csrfmiddlewaretoken');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');


// functions
function deleteBook(){
    
    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('book_id', book_id);

    $.ajax({
        type:'POST',
        url:'/deleteBook/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){


        },
        error: function(error){

            
        }
    });
}