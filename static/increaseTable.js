"placeMarkers.js";
var i = 0;
var identifier = 0;
function increaseTable()
	{
	 	i = i+1;
		var newentery = document.getElementById("enteries");
		var row = newentery.insertRow(-1);
		var cell1 = row.insertCell(0);
		var cell2 = row.insertCell(1);
		var cell3 = row.insertCell(2);
		var element1 = document.createElement('input');
		var element2 = document.createElement('input');
		var element3 = document.createElement('input');
		element1.type="text";
		element2.type="text";
		element3.type="text";
		cell1.appendChild(element1);
		cell2.appendChild(element2);
		cell3.appendChild(element3);
		identifier = "pac-input"+i;
		console.log(identifier);
		var input = document.getElementById(identifier);
		var searchBox = new google.maps.places.SearchBox(input);
		marker(element1, identifier, i);
		increaseTable.didrun = true;
	}// JavaScript Document