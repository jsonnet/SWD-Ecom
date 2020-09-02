function addbasket(product_id, product_price) {

    var xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE) {
            if (this.responseText === "login") {
                window.location.href = '/accounts/login/?next=/shop/add-basket/' + product_id;
            } else {
    		//update basket
    		basketTotal('baskettotal')
            }
        }
    }

    xhr.open("GET", "/shop/add-basket/" + product_id)
    xhr.send()


}

function removeBasket(product_id){
    //TODO implement
    console.log("This should remove " + product_id)
}

function basketTotal(dom_id) {
	
    var xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function () {
        if (this.readyState === this.DONE) {

	    //update total amount
	    amount = this.responseText

	    document.getElementById(dom_id).textContent = amount

        }
    }

    xhr.open("GET", "/shop/basket-total")
    xhr.send()
   

}

//TODO maybe put in some onload function
basketTotal('baskettotal')
