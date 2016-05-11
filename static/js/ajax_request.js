
function ajax_request(url, cfunc, data)
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
	xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
	xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	  
	xmlhttp.onreadystatechange=cfunc;
	xmlhttp.open("POST", url, true);
	xmlhttp.send(data);
}