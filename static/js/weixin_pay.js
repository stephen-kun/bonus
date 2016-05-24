var flag_pay = 1;
function consumer_pay(url, url_go, openid, prepay_id, total_fee){
	if(flag_pay){
		var i_count = 0;
		var timer = setInterval(function(){
			var xmlhttp = new XMLHttpRequest();
			var data = '{"openid":"OPENID","prepay_id":"PREPAY_ID", "action":"ajax_weixin_pay", "total_fee":"TOTAL_FEE"}';
			data = data.replace(/OPENID/, openid).replace(/PREPAY_ID/, prepay_id).replace(/TOTAL_FEE/, total_fee);
			
			xmlhttp.onreadystatechange=function()
			{
				if(xmlhttp.readyState==4 && xmlhttp.status==200)
				{
					// 实现跳转
					var response = JSON.parse(xmlhttp.responseText);
					if(response.status == 'SUCCESS' && response.result == 'SUCCESS'){
						$("#weixin").html('<input type="button" class="gray" value="微信支付" >');
						window.location.href = url_go;	
						clearInterval(timer);
					}
					else if(response.result == 'USERPAYING'){
						// 等待提示
						if(i_count >= 3){
							window.location.href = url_go;	
							clearInterval(timer);
							alert('网络异常')
						}
						i_count += 1;
					}
					else{
						alert('支付失败');
						$("#weixin").html('<input type="button" class="gray" value="微信支付" >');
						window.location.href = url_go;					
					}

				}
			}

			xmlhttp.open("POST", url, true);
			xmlhttp.send(data);			
		}, 2000);	
	}
	flag_pay = 0;
}