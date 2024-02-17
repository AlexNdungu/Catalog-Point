// Get all the items
let select_category_popup = document.getElementById('select_category_popup');
let book_category_select_btn = document.getElementById('book_category_select_btn');
let close_select_category_btn = document.getElementById('close_select_category');
let category_loading_section = document.getElementById('category_loading_section');
let all_category_container = document.getElementById('all_category_container');

// Add event listener
// Open the select category popup
book_category_select_btn.addEventListener('click', ()=> {
    select_category_popup.style.display = 'flex';
});

// Close the select category popup
close_select_category_btn.addEventListener('click', ()=> {
    select_category_popup.style.display = 'none';
});


// Functions

