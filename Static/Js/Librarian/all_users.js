// get all items
let csrf = document.getElementsByName('csrfmiddlewaretoken');
let table_body = document.getElementById('table_body');
let user_no_display = document.getElementById('user_no_display');
let the_search_bar = document.getElementById('the_search_bar');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');


// onload function
window.onload = function(){
    getAllUsers();
}

// search bar
the_search_bar.addEventListener('keyup', function(){

    // check if there are divs with class of book_from_db
    if(document.getElementsByClassName('user_from_db').length > 0){
        searchUsers(the_search_bar.value);
    }
    else{
        // show error message
        message_popup_failed.style.display = 'flex';
        failed_message_popup.innerHTML = 'No Users to be searched';

        // hide error message after 4 seconds
        setTimeout(function(){
            message_popup_failed.style.display = 'none';
        }, 4000);
    
    }
});

// Get all books
function getAllUsers(){

    // empty search bar
    the_search_bar.value = '';

    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);

    $.ajax({
        type:'POST',
        url:'/getAllUsers/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            $('#table_body').empty();
            let user_number = 0;

            if(response.status == 'empty'){

                user_no_display.innerHTML = user_number;

                // show error message
                message_popup_failed.style.display = 'flex';
                failed_message_popup.innerHTML = 'No Users found';

                // hide error message after 4 seconds
                setTimeout(function(){
                    message_popup_failed.style.display = 'none';
                }, 4000);
                
            }
            else{

                user_number = response.users.length;
                user_no_display.innerHTML = user_number;

                // show success message
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = user_number + ' Users found';
                setTimeout(function(){
                    message_popup_success.style.display = 'none';
                }, 4000);

                // get all books
                let all_users = response.users;

                for(let i = 0; i < all_users.length; i++){

                    console.log(all_users[i].profile_pic);

                    let table_row = 
                    `<tr class='user_from_db'>
                        <td>${all_users[i].profile_id}</td>
                        <!--Cover image-->
                        <td>
                            <div class="user_image">

                                ${all_users[i].profile_pic != 'False' ?
                                `<img src="${all_users[i].profile_pic}" alt="profile_picture">` 
                                :
                                `<span>${all_users[i].full_name.charAt(0)}</span>`
                                }

                            </div>
                        </td>

                        <td class='user_full_name' >${all_users[i].full_name}</td>
                        <td>${all_users[i].email}</td>
                        <td>${all_users[i].added_on}</td>
                        <td>${all_users[i].books_borrowed}</td>
                        <td>ksh ${all_users[i].charges}</td>
                        <td>
                            <div class="book_list_controls">

                                <!--Eye-->
                                <a href="/profile/${all_users[i].username}" class="book_control">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M288 32c-80.8 0-145.5 36.8-192.6 80.6C48.6 156 17.3 208 2.5 243.7c-3.3 7.9-3.3 16.7 0 24.6C17.3 304 48.6 356 95.4 399.4C142.5 443.2 207.2 480 288 480s145.5-36.8 192.6-80.6c46.8-43.5 78.1-95.4 93-131.1c3.3-7.9 3.3-16.7 0-24.6c-14.9-35.7-46.2-87.7-93-131.1C433.5 68.8 368.8 32 288 32zM144 256a144 144 0 1 1 288 0 144 144 0 1 1 -288 0zm144-64c0 35.3-28.7 64-64 64c-7.1 0-13.9-1.2-20.3-3.3c-5.5-1.8-11.9 1.6-11.7 7.4c.3 6.9 1.3 13.8 3.2 20.7c13.7 51.2 66.4 81.6 117.6 67.9s81.6-66.4 67.9-117.6c-11.1-41.5-47.8-69.4-88.6-71.1c-5.8-.2-9.2 6.1-7.4 11.7c2.1 6.4 3.3 13.2 3.3 20.3z"/></svg>
                                </a>

                                <!--Pen-->
                                <!-- <div class="book_control">
                                    <svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m4.481 15.659c-1.334 3.916-1.48 4.232-1.48 4.587 0 .528.46.749.749.749.352 0 .668-.137 4.574-1.492zm1.06-1.061 3.846 3.846 11.321-11.311c.195-.195.293-.45.293-.707 0-.255-.098-.51-.293-.706-.692-.691-1.742-1.74-2.435-2.432-.195-.195-.451-.293-.707-.293-.254 0-.51.098-.706.293z" fill-rule="nonzero"/></svg>
                                </div> -->

                                <!--Delete-->
                                <!-- <div class="book_control">
                                    <svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m4.015 5.494h-.253c-.413 0-.747-.335-.747-.747s.334-.747.747-.747h5.253v-1c0-.535.474-1 1-1h4c.526 0 1 .465 1 1v1h5.254c.412 0 .746.335.746.747s-.334.747-.746.747h-.254v15.435c0 .591-.448 1.071-1 1.071-2.873 0-11.127 0-14 0-.552 0-1-.48-1-1.071zm14.5 0h-13v15.006h13zm-4.25 2.506c-.414 0-.75.336-.75.75v8.5c0 .414.336.75.75.75s.75-.336.75-.75v-8.5c0-.414-.336-.75-.75-.75zm-4.5 0c-.414 0-.75.336-.75.75v8.5c0 .414.336.75.75.75s.75-.336.75-.75v-8.5c0-.414-.336-.75-.75-.75zm3.75-4v-.5h-3v.5z" fill-rule="nonzero"/></svg>
                                </div> -->
                            </div>
                        </td>
                    </tr>
                    `;

                    $('#table_body').append(table_row);

                }

            }

        },
        error: function(error){

            // show error message
            message_popup_failed.style.display = 'flex';
            failed_message_popup.innerHTML = 'Failed to get Users. Try again later.';

            // hide error message after 4 seconds
            setTimeout(function(){
                message_popup_failed.style.display = 'none';
            }, 4000);
            
        }
    });

}

// search users function
function searchUsers(input_value){

    // get the needed elements
    let user_txtValue = '';
    let user_from_db = document.getElementsByClassName('user_from_db');
    let user_full_name = document.getElementsByClassName('user_full_name');
    let user_count = 0;

    let filter = input_value.toUpperCase();

    for (i = 0; i < user_from_db.length; i++) {

        user_txtValue = user_full_name[i].textContent || user_full_name[i].innerText;

        if (user_txtValue.toUpperCase().indexOf(filter) > -1) {
            user_from_db[i].style.display = "";
        }
        else {
            user_from_db[i].style.display = "none";
        }

    }

    // update count
    for (i = 0; i < user_from_db.length; i++) {
        if(user_from_db[i].style.display == ''){
            user_count++;
        }
    }

    // show number of books found
    user_no_display.innerHTML = user_count;

}