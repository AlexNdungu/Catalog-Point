// get all items
let csrf = document.getElementsByName('csrfmiddlewaretoken');
let table_body = document.getElementById('table_body');

// Functions

// onload function
window.onload = function(){
    getAllBooks('all');
}

// Get all books
function getAllBooks(category){

    // First we create form data
    let formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf[0].value);
    formData.append('category', category);

    $.ajax({
        type:'POST',
        url:'/getAllBooks/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response){

            console.log(response);
        },
        error: function(error){

            
        }
    });

}