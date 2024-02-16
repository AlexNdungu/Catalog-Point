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
let upload_plus_icon = document.getElementById('upload_plus_icon');
let upload_spinner = document.getElementById('upload_spinner');


// Event listeners
// Discard
cancel_btn.addEventListener('click', discard);

// Upload
submit_btn.addEventListener('click', () => {
    
    // Check if the title and description are empty
    if(categ_title.value && categ_description.value){
        upload();
    }
    else{
        // Show the failed pop up
        message_popup_failed.style.display = 'flex';
        failed_message_popup.innerHTML = 'Please fill in the title and description';

        // Hide the failed pop up after 2 seconds
        setTimeout(function(){
            message_popup_failed.style.display = 'none';
        }, 4000);
    }
});

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

// Upload function
function upload(){

    // Show spinner
    upload_spinner.style.display = "flex";
    upload_plus_icon.style.display = "none";

    // Disable the submit_btn
    submit_btn.style.pointerEvents = "none";

    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('categ_title', categ_title.value);
    formData.append('categ_description', categ_description.value);

    $.ajax({
        type:'POST',
        url:'/createNewCategory/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            // Show the success pop up
            message_popup_success.style.display = 'flex';
            success_message_popup.innerHTML = 'Category has been created successfully';

            // Hide spinner
            upload_spinner.style.display = "none";
            upload_plus_icon.style.display = "flex";

            // Enable the submit_btn
            submit_btn.style.pointerEvents = "auto";

            // Hide the success pop up after 2 seconds
            setTimeout(function(){
                message_popup_success.style.display = 'none';
            }, 4000);

            
        },
        error: function(error){

            // Show the failed pop up
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Category creation has failed. Please try again later';

            // Hide spinner
            upload_spinner.style.display = "none";
            upload_plus_icon.style.display = "flex";

            // Enable the submit_btn
            submit_btn.style.pointerEvents = "auto";

            // Hide the failed pop up after 2 seconds
            setTimeout(function(){
                message_popup_failed.style.display = 'none';
            }, 4000);

        }
    }); 
}