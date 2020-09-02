function addbasket(product_id, product_price) {

	var xhr = new XMLHttpRequest()

	xhr.onreadystatechange = function() {
	if (this.readyState === this.DONE) {
	           if (this.responseText == "login") {
		   	window.location.href = '/accounts/login/?next=/shop/add-basket/'+product_id;
		   } else {
		   	console.log(this.responseText)
		   }
	}
	}

	xhr.open("GET", "/shop/add-basket/"+product_id) 
	xhr.send()

	//update total amount
	amount = document.getElementById('baskettotal').textContent
	amount = parseInt(amount)
	amount = amount || 0

	amount += product_price 
	document.getElementById('baskettotal').textContent = amount
}
