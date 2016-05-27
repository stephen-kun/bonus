
//窗口水平居中
$(window).resize(function(){
	tc_center();
});

function tc_center(){
	var _top=($(window).height()-$(".popup").height())/2;
	var _left=($(window).width()-$(".popup").width())/2;
	
	$(".popup").css({bottom:_bottom,left:_left});
}	


function click_get_bonus(url, openid){
	// ajax 请求
	var data = '{"action":"ACTION", "openid":"OPENID", "timestamp":"TIMESTAMP"}';
	var curr_time = new Date();
	data = data.replace(/ACTION/, 'ajax_get_bonus').replace(/OPENID/,openid).replace(/TIMESTAMP/, curr_time);
	
	$.post(url, data, function(data, status){
		if(status=='success')
		{
			var JSONObject = JSON.parse(data);
			if(JSONObject.status == '0')
			{
				if(JSONObject.number == '0'){
					$("#rcv_bonus").html('<font class="f_huangse">手慢了，红包已抢完</font>');
					$("#link1").hide();
				}
				else{
					var html = '恭喜您！抢到<font class="f_huangse">NUMBER</font>红包！';
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
			$("#popup").fadeIn(1500);//查找ID为popup的DIV fadeIn()显示弹出时间
			tc_center();
		}
	});	

}	
	