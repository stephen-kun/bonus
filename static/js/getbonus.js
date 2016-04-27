function get_bonus(url)
{
// 携带openid 发起get请求
var xmlhttp;
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  
xmlhttp.onreadystatechange=function()
{
	if(xmlhttp.readyState==4 && xmlhttp.status==200)
	{
		var html = '恭喜您抢到红包<font class="f_huangse">NUMBER</font>个';
		document.getElementById("rcv_bonus").innerHTML=html.replace(/NUMBER/,xmlhttp.responseText);
	}
}
xmlhttp.open("GET", url, true);
xmlhttp.send();
}