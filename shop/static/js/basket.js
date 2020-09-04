function addbasket(product_id) {
    var xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE)
            if (this.responseText === "login")
                window.location.href = '/accounts/login/?next=/shop/add-basket/' + product_id;
            else
                basketTotal('baskettotal')
    }

    xhr.open("GET", "/shop/add-basket/" + product_id)
    xhr.send()
}

function removeBasket(product_id) {
    var xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE)
            location.reload()
    }

    xhr.open("GET", "/shop/remove-basket/" + product_id)
    xhr.send()
}

function basketTotal(dom_id) {
    var xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE)
            //update total amount
            document.getElementById(dom_id).textContent = this.responseText
    }

    xhr.open("GET", "/shop/basket-total/")
    xhr.send()
}

// Only page is loaded
$(document).ready(function () {
    basketTotal('baskettotal')
});
