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
// Get all categories
function getAllCategories(){

    // Show loading section
    category_loading_section.style.display = 'flex';
    all_category_container.style.display = 'none';

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

            if(response.status == 'empty'){

                // show failed message
                message_popup_failed.style.display = 'flex';
                failed_message_popup.innerHTML = 'No category found. Add a category first.';

                // redirect to add category page
                setTimeout(() => {
                    window.location.href = '/NewCategory/';
                }, 3000);

            }
            else if (response.status == 'present'){

                // show success message
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = 'All categories loaded successfully.';

                // Hide loading section and show all categories
                category_loading_section.style.display = 'none';
                all_category_container.style.display = 'flex';
                
                let categories = response.categories;
                $('#all_category_container').empty();
                // loop through the categories
                for(let i = 0; i < categories.length; i++){

                    // replace space with - in categories[i]
                    let new_category_id = categories[i].replace(/ /g, '-');

                    let category_item = `
                        <!--Category item-->
                        <div class="category_item_container">
                            <div class="category_item">
                                <span>${categories[i]}</span>
                            </div>
                            <div class="category_item_info" id='${new_category_id}'>
                                <div class="category_info_icon_section">
                                    <svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12.002 2.005c5.518 0 9.998 4.48 9.998 9.997 0 5.518-4.48 9.998-9.998 9.998-5.517 0-9.997-4.48-9.997-9.998 0-5.517 4.48-9.997 9.997-9.997zm0 8c-.414 0-.75.336-.75.75v5.5c0 .414.336.75.75.75s.75-.336.75-.75v-5.5c0-.414-.336-.75-.75-.75zm-.002-3c-.552 0-1 .448-1 1s.448 1 1 1 1-.448 1-1-.448-1-1-1z" fill-rule="nonzero"/></svg>
                                </div>
                            </div>
                        </div>
                    `;

                    $('#all_category_container').append(category_item);

                }

                // Add event listiner to all category_item_info buttons
                let category_item_info = document.getElementsByClassName('category_item_info');
                for(let i = 0; i < category_item_info.length; i++){
                    category_item_info[i].addEventListener('click', (e)=> {

                        // check if e.target has id and if it is not the category_item_info_popup_head
                        if(e.target.id == '' && !e.target.classList.contains('category_item_info_popup_head')){
                            showCategoryInfoPopup(category_item_info[i].id);
                        }
                        else if(e.target.classList.contains('category_item_info_popup_head')){
                            return;
                        }

                    });
                }

                // hide the success message
                setTimeout(() => {
                    message_popup_success.style.display = 'none';
                }, 4000);
            }
            
        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to get all categories. Try again later.';

            // hide the error message
            setTimeout(() => {
                message_popup_failed.style.display = 'none';
                select_category_popup.style.display = 'none';
            }, 4000);

        }
    });
}

// Show info popup
function showCategoryInfoPopup(category_name){

    // replace - with space in category_name
    let new_category_name = category_name.replace(/-/g, ' ');

    // remove the popup
    $('#category_item_info_popup').remove();

    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('category_name', new_category_name);

    $.ajax({
        type:'POST',
        url:'/getCategoryInfo/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            // show success message
            message_popup_success.style.display = 'flex';
            success_message_popup.innerHTML = new_category_name + ' info loaded successfully.';

            // The popup
            let category_info = `
                <div id="category_item_info_popup">
                    <div class="category_item_info_popup_head">
                        <div id="category_item_info_popup_close">
                            <svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"/></svg>
                        </div>
                    </div>
                    <div class="category_item_info_popup_body">
                        <span id="category_item_info_popup_text">
                            <b>${new_category_name}</b> - ${response.category_description}
                        </span>
                    </div>
                </div>
            `;

            // Append the popup to id of category_name using jquery
            $('#'+category_name).append(category_info);

            // Get the close button and the popup
            let category_item_info_popup_close = document.getElementById('category_item_info_popup_close');
            category_item_info_popup_close.addEventListener('click', (e)=> {
                
                if(e.target.id != ''){
                    // remove the popup
                    $('#category_item_info_popup').remove();
                    // show error message
                    message_popup_failed.style.display = 'flex';
                    failed_message_popup.innerHTML = 'Info popup closed.';
                    // hide the message
                    setTimeout(() => {
                        message_popup_failed.style.display = 'none';
                    }, 4000);
                }

            });

            // hide the success message
            setTimeout(() => {
                message_popup_success.style.display = 'none';
            }, 4000);
            
        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to get category info. Try again later.';

            // hide the error message
            setTimeout(() => {
                message_popup_failed.style.display = 'none';
            }, 4000);
            
        }
    });
}
