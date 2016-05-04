
function click_get_bonus(url, openid){
	$(".tch-share").addClass("tch-modal-active");	
	if($(".tchsharebg").length>0){
		$(".tchsharebg").addClass("tchsharebg-active");
	}else{
		$("body").append('<div class="tchsharebg"></div>');
		$(".tchsharebg").addClass("tchsharebg-active");
	}
	$(".tchsharebg-active,.tchshare_btn").click(function(){
		$(".tch-share").removeClass("tch-modal-active");	
		setTimeout(function(){
			$(".tchsharebg-active").removeClass("tchsharebg-active");	
			$(".tchsharebg").remove();	
		},300);
	});
	
	// ajax 请求
	var data = '{"action":"ACTION", "openid":"OPENID", "timestamp":"TIMESTAMP"}';
	var curr_time = new Date();
	data = data.replace(/ACTION/, 'ajax_get_bonus').replace(/OPENID/,openid).replace(/TIMESTAMP/, curr_time);
	ajax_get_bonus(url, data);		
}	
	
function ajax_get_bonus(url, data)
{
	
	var xmlhttp=new XMLHttpRequest();
	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			var JSONObject = JSON.parse(xmlhttp.responseText);
			if(JSONObject.status == '0')
			{
				if(JSONObject.number == '0'){
					$("#rcv_bonus").html('<font class="f_huangse">手慢了，红包已抢完</font>');
					$("#link1").hide();
				}
				else{
					var html = '恭喜您！抢到<font class="f_huangse">NUMBER</font>串串！';
					html = html.replace(/NUMBER/, JSONObject.number);
					$("#rcv_bonus").html(html);
					$("#link2").hide();
				}				
			}
			else
			{
				alert(JSONObject.error_msg);
			}
			
			// 控制结果样式弹出
			
		}
	};
	
	xmlhttp.open("POST", url, true);
	xmlhttp.send(data);
}	
	
