var refuse_flag = 1;
function refuse_bonus(id_bonus, url){
	var xmlhttp = new XMLHttpRequest();
	var data = '{"id_bonus":"ID_BONUS", "action":"ajax_bonus_refuse"}';
	data = data.replace(/ID_BONUS/, id_bonus);

	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			alert('已婉拒');
			var id = 'refuseID_BONUS'.replace(/ID_BONUS/, id_bonus);
			document.getElementById(id).setAttribute('class', "blue");
		}
	}
	
	if(refuse_flag)
	{
		refuse_flag = 0;		
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);			
	}
	
	
}

function send_message(url){
	var openid, id_bonus, message, data;
	var xmlhttp = new XMLHttpRequest();
	id_bonus = $("#id_bonus").val();
	if($("#message").val())
	{
		message = $("#message").val();		
	}
	else
	{
		message = $("#message").attr('placeholder');		
	}


	data = '{"id_bonus":"ID_BONUS","message":"MESSAGE", "action":"ajax_bonus_message"}';
	data = data.replace(/ID_BONUS/, id_bonus).replace(/MESSAGE/, message);
  
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
	
function message(id_bonus){
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
	
	document.getElementById("id_bonus").value=id_bonus;		
	document.getElementById("show_message").value=id_bonus;
}