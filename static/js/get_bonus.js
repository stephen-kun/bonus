
//窗口水平居中
$(window).resize(function(){
	tc_center();
});

function tc_center(){
	var _top=($(window).height()-$(".popup").height())/2;
	var _left=($(window).width()-$(".popup").width())/2;
	
	$(".popup").css({bottom:_bottom,left:_left});
}	

function click_get_bonus(url, openid, url_go){
	var data = '{"action":"ACTION", "openid":"OPENID", "timestamp":"TIMESTAMP"}';
	var curr_time = new Date();
	data = data.replace(/ACTION/, 'ajax_get_bonus').replace(/OPENID/,openid).replace(/TIMESTAMP/, curr_time);
	
	$.post(url, data, function(data, status){
		if(status=='success')
		{
			var JSONObject = JSON.parse(data);
			if(JSONObject.status == '0')
			{
				if(JSONObject.result == '0'){
					$("#rcv_bonus").html('手慢了');
					$("#link1").hide();
					
					// 控制结果样式弹出
					$("#popup").fadeIn(1500);//查找ID为popup的DIV fadeIn()显示弹出时间
					tc_center();					
				}
				else if(JSONObject.result == '1'){
					$("#rcv_bonus").html('已抢到<font color="#ff4800">NUMBER</font>串'.replace(/NUMBER/, JSONObject.number));
					var url = $("#detail_url").attr('href');
					url = url.replace(/ID_BONUS/, JSONObject.id_bonus);
					$("#detail_url").attr('href', url);
					$("#link2").hide();
					
					// 控制结果样式弹出
					$("#popup").fadeIn(1500);//查找ID为popup的DIV fadeIn()显示弹出时间
					tc_center();										
				}	
				else if(JSONObject.result == '2'){
					window.location.href = url_go;						
				}				
			}
			else
			{
				alert(JSONObject.error_msg);
			}
			

		}
	});	

}	
	