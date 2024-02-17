// Get all the items
let select_category_popup = document.getElementById('select_category_popup');
let book_category_select_btn = document.getElementById('book_category_select_btn');
let close_select_category_btn = document.getElementById('close_select_category');
let category_loading_section = document.getElementById('category_loading_section');
let all_category_container = document.getElementById('all_category_container');
let csrf = document.getElementsByName('csrfmiddlewaretoken');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');


// Add event listener
// Open the select category popup
book_category_select_btn.addEventListener('click', ()=> {
    select_category_popup.style.display = 'flex';
    // call get all categories function
    getAllCategories();
});

// Close the select category popup
close_select_category_btn.addEventListener('click', ()=> {
    select_category_popup.style.display = 'none';
});


// Functions
function getAllCategories(){

    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);

    $.ajax({
        type:'POST',
        url:'/getAllCategories/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            
        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to get all categories';

            // hide the error message
            setTimeout(() => {
                message_popup_failed.style.display = 'none';
                select_category_popup.style.display = 'none';
            }, 4000);

        }
    });
}
