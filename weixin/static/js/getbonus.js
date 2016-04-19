function get_bonus(openid)
{
// 携带openid 发起post请求
var xmlhttp;
//var jsonData = {openid : openid};
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
		document.getElementById("rcv_bonus").innerHTML=xmlhttp.responseText;
	}
}
xmlhttp.open("POST", "http://120.76.122.53/weixin/view_action_get_bonus", true);
xmlhttp.send(openid);
}