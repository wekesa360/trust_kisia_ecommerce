$(document).ready(function () {
    // catch the form's submit event
    ifPersistDevice();
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
    


// Setting the device cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
let device = getCookie('device')

if (device == null || device == undefined) {
    device = uuidv4()
}
document.cookie = 'device=' + device + ";domain=;path=/"    

console.log(document.device)

// cookies
const ifPersistDevice = async() => {
    try {   
        const res = await fetch('{% url "shop:persists" %}');
        value = await res.json();
        console.log(value)
    } catch (err) {
        console.error(err);
    }
};