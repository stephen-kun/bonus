function refuse_bonus(id_bonus, url){
	var xmlhttp;
	var data = '{"id_bonus":"ID_BONUS", "action":"ajax_bonus_refuse"}';
	data = data.replace(/ID_BONUS/, id_bonus);

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
			var html = '<input type="button" id="button" class="gray" value="Íñ¾Ü">';
			var id = "hID_BONUS".replace(/ID_BONUS/, id_bonus);
			document.getElementById(id).innerHTML = html;
		}
	}
	xmlhttp.open("POST", url, true);
	xmlhttp.send(data);		
	
}

function send_message(url){
	var openid, id_bonus, message, data;
	var xmlhttp;
	openid = document.getElementById("openid").value;
	id_bonus = document.getElementById('id_bonus').value;
	message = document.getElementById("message").value;

	data = '{"openid":"OPENID","id_bonus":"ID_BONUS","message":"MESSAGE", "action":"ajax_bonus_message"}';
	data = data.replace(/OPENID/, openid).replace(/ID_BONUS/, id_bonus).replace(/MESSAGE/, message);

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
			var id = document.getElementById("show_message").value;
			document.getElementById(id).innerHTML=message;
		}
	}
	xmlhttp.open("POST", url, true);
	xmlhttp.send(data);	
}
	
function message(openid, id_bonus){
	$(".am-share").addClass("am-modal-active");	
	if($(".send_out").length>0){
		$(".send_out").addClass("sharebg-active");
	}else{
		$("body").append('<div class="send_out"></div>');
		$(".send_out").addClass("sharebg-active");
	}
	$(".sharebg-active,.share_btn").click(function(){
		$(".am-share").removeClass("am-modal-active");	
		setTimeout(function(){
			$(".sharebg-active").removeClass("sharebg-active");	
			$(".send_out").change();	
		},300);
	})
	
	document.getElementById("openid").value=openid;
	document.getElementById("id_bonus").value=id_bonus;		
	document.getElementById("show_message").value=id_bonus;
}