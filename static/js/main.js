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