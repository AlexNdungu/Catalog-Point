// get all the needed items
let csrf = document.getElementsByName('csrfmiddlewaretoken');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');
//
let borrow_popup = document.getElementById('borrow_popup');
let proceed_with_borrow_btn = document.getElementById('proceed_with_borrow');
let from_date = document.getElementById('from_date');
let to_date = document.getElementById('to_date');
let no_of_days = document.getElementById('no_of_days');
let cost_in_ksh = document.getElementById('cost_in_ksh');


// event listeners
proceed_with_borrow_btn.addEventListener('click', function(){
    // check if any of the fields is empty
    if(from_date.value == '' || to_date.value == ''){
        // show error message
        message_popup_failed.style.display = 'flex';
        failed_message_popup.innerHTML = 'Fill in all the fields to proceed with the borrowing process.';

        // hide error message after 4 seconds
        setTimeout(function(){
            message_popup_failed.style.display = 'none';
        }, 4000);
    }
    else{
        // proceed with the borrowing process
        borrowBook();
    }
});

// functions
// Delete book
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

            if(response.status == 'not_found'){
                // show error message
                message_popup_failed.style.display = 'flex';
                failed_message_popup.innerHTML = 'Book not found. Try again later.';

                // hide error message after 4 seconds
                setTimeout(function(){
                    message_popup_failed.style.display = 'none';
                }, 4000);
            }
            else if(response.status == 'deleted'){
                // show success message
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'Book deleted successfully. You will be redirected to the books page in 4 seconds.';

                // hide success message after 4 seconds
                setTimeout(function(){
                    message_popup_success.style.display = 'none';
                    window.location.href = '/AllBooks/';
                }, 4000);

            }


        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to delete the book. Try again later.';

            // hide error message after 4 seconds
            setTimeout(function(){
                message_popup_failed.style.display = 'none';
            }, 4000);
            
        }
    });
}

// borrow book
function borrowBook(){
    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('book_id', book_id);
    formData.append('from_date', from_date.value);
    formData.append('to_date', to_date.value);
    formData.append('no_of_days', no_of_days.value);
    formData.append('cost_in_ksh', cost_in_ksh.value);

    $.ajax({
        type:'POST',
        url:'/borrowBook/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            if(response.status == 'not_available'){
                // show error message
                message_popup_failed.style.display = 'flex';
                failed_message_popup.innerHTML = 'Book not available for borrowing. Try again later.';

                // hide error message after 4 seconds
                setTimeout(function(){
                    message_popup_failed.style.display = 'none';
                }, 4000);
            }
            else if(response.status == 'borrowed'){
                // show success message
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'Book borrowed successfully.';
                //
                document.getElementById('single_det_control_Borrow').style.display = 'none';
                document.getElementById('single_det_control_pending').style.display = 'flex';

                // hide success message after 4 seconds
                setTimeout(function(){
                    message_popup_success.style.display = 'none';
                    borrow_popup.style.display = 'none';
                }, 4000);
            }

        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to borrow the book. Try again later.';

            // hide error message after 4 seconds
            setTimeout(function(){
                message_popup_failed.style.display = 'none';
            }, 4000);
            
        }
    });
}
    