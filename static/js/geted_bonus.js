function refuse_bonus(id_bonus, url){
	var data = '{"id_bonus":"ID_BONUS", "action":"ajax_bonus_refuse"}';
	data = data.replace(/ID_BONUS/, id_bonus);

	
	$.post(url, data, function(data, status){
		if(status == 'success'){
			alert('已婉拒');
			var id = 'refuseID_BONUS'.replace(/ID_BONUS/, id_bonus);
			document.getElementById(id).setAttribute('class', "blue");
		}
	});	
	
}

var snd_flag = false;
function send_message(url){
	if(snd_flag){
		return;
	}
	snd_flag = true;
	var openid, id_bonus, message, data;
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
  
	$.post(url, data, function(data, status){
		if(status == 'success'){
			var id = $("#show_message").val();
			$("#" + id).text(message);
			snd_flag = false;
		}
	});	
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
	
	$("#id_bonus").val(id_bonus);		
	$("#show_message").val(id_bonus);
}