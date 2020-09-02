function addbasket(product_id, product_price) {
    var xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE)
            if (this.responseText === "login")
                window.location.href = '/accounts/login/?next=/shop/add-basket/' + product_id;
            else
                basketTotal('baskettotal', -1)
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

function basketTotal(dom_id, order_id) {
    var xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE)
            //update total amount
            document.getElementById(dom_id).textContent = this.responseText
    }

    if (order_id === -1)
        xhr.open("GET", "/shop/basket-total/")
    else
        xhr.open("GET", "/shop/basket-total/" + order_id)
    xhr.send()
}

//TODO maybe put in some onload function
basketTotal('baskettotal', -1)
