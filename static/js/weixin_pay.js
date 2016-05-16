var flag_pay = 1;
function consumer_pay(url, url_go, openid, money, method){
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	  
	var data_str = '{"money":"MONEY", "openid":"OPENID", "action":"ACTION", "method":"METHOD"}';
	var data = data_str.replace(/MONEY/, money).replace(/OPENID/, openid).replace(/ACTION/, 'ajax_weixin_pay').replace(/METHOD/, method);
	
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			// 实现跳转
			alert("支付成功");
			window.location.href = url_go;
		}
	}
	if(flag_pay)
	{
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);	
		flag_pay = 0;
	}

}