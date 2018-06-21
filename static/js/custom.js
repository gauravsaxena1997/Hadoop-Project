
document.addEventListener ( "DOMContentLoaded" , 
function (event) { 

function sayHello(event) {
	//console.log(this);
	//console.log(event);
	this.textContent="Said It ! ";
	var name = (document.getElementById("name").value);
	var message = "<h3>  Hello " + name + " ! </h3>"
	console.log(message)
	//document.getElementById("content").textContent = message;
	document.getElementById("content").innerHTML = message;

	if(name=="js") {
		var title=document.querySelector("h1").textContent;
		title += " is fun :-) " ;

		document.querySelector("#title").textContent = title;
	}
}
//Unobstructive Event Binding
//document.querySelector("button").addEventListener("click", sayHello);
document.querySelector("button").onclick = sayHello;

document.querySelector("body").addEventListener("mousemove", 
	function (event) {

		if(event.shiftKey == true) {
		console.log(" X: " +event.clientX);
		console.log(" Y: " +event.clientY); 
		}
	});
	
document.querySelector("body").addEventListener("mousemove", 
	function (event) {

		var cord =  "Cursor Cordinates are X: " + event.clientX + " Y: " + event.clientY; 

  		document.getElementById("mouse").innerHTML = cord;
	});

   






	});


