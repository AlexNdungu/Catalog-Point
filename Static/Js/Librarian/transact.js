// get all items
let csrf = document.getElementsByName('csrfmiddlewaretoken');
let table_body = document.getElementById('table_body');
let transaction_no_display = document.getElementById('transaction_no_display');
//
let category_button = document.getElementById('category_button');
let category_button_name = document.getElementById('category_button_name');
let category_list = document.getElementById('category_list');
let the_search_bar = document.getElementById('the_search_bar');
//
let message_popup_success = document.getElementById('message_popup_success');
let success_message_popup = document.getElementById('success_message_popup');
let message_popup_failed = document.getElementById('message_popup_failed');
let failed_message_popup = document.getElementById('failed_message_popup');

// onload function
window.onload = function(){
    getAllTransactions('all');
}


// Get all Transactions
function getAllTransactions(category){

    // empty search bar
    the_search_bar.value = '';

    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('category', category);

    $.ajax({
        type:'POST',
        url:'/getLibTransactions/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            $('#table_body').empty();
            let transaction_number = 0;

            if(response.status == 'empty'){

                transaction_no_display.innerHTML = transaction_number;

                // show error message
                message_popup_failed.style.display = 'flex';
                failed_message_popup.innerHTML = 'No Transactions found';

                // hide error message after 4 seconds
                setTimeout(function(){
                    message_popup_failed.style.display = 'none';
                }, 4000);
                
            }
            else{

                transaction_number = response.transactions.length;
                transaction_no_display.innerHTML = transaction_number;

                // show success message
                message_popup_success.style.display = 'flex';
                success_message_popup.innerHTML = transaction_number + ' Transactions found';
                setTimeout(function(){
                    message_popup_success.style.display = 'none';
                }, 4000);

                // get all books
                let all_transactions = response.transactions;

                for(let i = 0; i < all_transactions.length; i++){

                    // Title
                    const title = all_transactions[i].book_name;
                    const maxLength = 20;
                    let truncatedTitle = title.length > maxLength ? title.substring(0, maxLength) + "..." : title;

                    let table_row = 
                    `<tr>
                        <td>${all_transactions[i].transaction_id}</td>

                        <!--profile image-->
                        <td>
                            <div class="user_image">

                                ${all_transactions[i].profile_pic_url != 'False' ?
                                `<img src="${all_transactions[i].profile_pic_url}" alt="profile_picture">` 
                                :
                                `<span>${all_transactions[i].user_name.charAt(0)}</span>`
                                }

                            </div>
                        </td>

                        <!--cover image-->
                        <td>
                            <div class="cover_image">
                                <img src="${all_transactions[i].book_url}" alt="cover_book">
                            </div>
                        </td>

                        <td>${all_transactions[i].user_name}</td>
                        <td>${truncatedTitle}</td>
                        <td>${all_transactions[i].from_date}</td>
                        <td>${all_transactions[i].to_date}</td>
                        <td>${all_transactions[i].no_of_days}</td>
                        <td>ksh ${all_transactions[i].cost}</td>
                        <td>${all_transactions[i].status}</td>
                        <td>
                            <div class="book_list_controls">

                                <!--Eye-->
                                <div class="book_control">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M288 32c-80.8 0-145.5 36.8-192.6 80.6C48.6 156 17.3 208 2.5 243.7c-3.3 7.9-3.3 16.7 0 24.6C17.3 304 48.6 356 95.4 399.4C142.5 443.2 207.2 480 288 480s145.5-36.8 192.6-80.6c46.8-43.5 78.1-95.4 93-131.1c3.3-7.9 3.3-16.7 0-24.6c-14.9-35.7-46.2-87.7-93-131.1C433.5 68.8 368.8 32 288 32zM144 256a144 144 0 1 1 288 0 144 144 0 1 1 -288 0zm144-64c0 35.3-28.7 64-64 64c-7.1 0-13.9-1.2-20.3-3.3c-5.5-1.8-11.9 1.6-11.7 7.4c.3 6.9 1.3 13.8 3.2 20.7c13.7 51.2 66.4 81.6 117.6 67.9s81.6-66.4 67.9-117.6c-11.1-41.5-47.8-69.4-88.6-71.1c-5.8-.2-9.2 6.1-7.4 11.7c2.1 6.4 3.3 13.2 3.3 20.3z"/></svg>
                                </div>

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
            failed_message_popup.innerHTML = 'Failed to get books. Try again later.';

            // hide error message after 4 seconds
            setTimeout(function(){
                message_popup_failed.style.display = 'none';
            }, 4000);
            
        }
    });

}