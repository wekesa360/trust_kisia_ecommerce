const searchBar = document.getElementById('searchBar');
searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();

    const filteredFields = response['data'].filter((fields) => {
        return (
            fields.name.toLowerCase().includes(searchString) ||
            fields.brand.toLowerCase().includes(searchString)
        );
    });
    displayFields(filteredFields);
});

const displayFields = (fields) => {
    const htmlString = fields
        .map((field) => {
            return `
            <li class="field">
                <h2>${field.name}</h2>
                <p>House: ${field.house}</p>
                <img src="${field.image}"></img>
            </li>
        `;
        })
        .join('');
    fieldsList.innerHTML = htmlString;
}

$(document).ready(function () {
    // catch the form's submit event
    
        // create an AJAX call
        $.ajax({
            data: $(this).serialize(), // get the form data
            url: "{% url 'shop:search' %}",
            // on success
            success: function (response) {
                console.log(response)
                const searchBar = document.getElementById('searchBar');
                

            },
            // on error
            error: function (response) {
                // alert the error if any error occured
                console.log(response.responseJSON.errors)
            }
        });

        return false;
    })