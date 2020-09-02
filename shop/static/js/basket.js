function addbasket(product_id) {

	var xhr = new XMLHttpRequest()

	xhr.onreadystatechange = function() {
	if (this.readyState === this.DONE) {
	            console.log(this.responseText)
	}
	}

	xhr.open("GET", "/shop/add-basket/"+product_id) 
	xhr.send()
}
