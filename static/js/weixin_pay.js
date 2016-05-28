

function consumer_pay(url, url_go, openid, prepay_id, total_fee){
	var request_data = '{"openid":"OPENID","prepay_id":"PREPAY_ID", "action":"ajax_weixin_pay", "total_fee":"TOTAL_FEE"}';
	request_data = request_data.replace(/OPENID/, openid).replace(/PREPAY_ID/, prepay_id).replace(/TOTAL_FEE/, total_fee);
	var i_count = 0;


	$.post(url, request_data, function(data, status){
		var response = JSON.parse(data);
		if(status == 'success'){
			if(response.status == 'SUCCESS' && response.result == 'SUCCESS'){
				$("#weixin").html('<input type="button" class="gray" value="微信支付" >');
				window.location.href = url_go;	
			}else if(response.result == 'USERPAYING'){
				var timer = setInterval(function(){
					$.post(url,request_data,function(data, status){
						var response = JSON.parse(data);
						if(status == 'success'){
							if(response.status == 'SUCCESS' && response.result == 'SUCCESS'){
								$("#weixin").html('<input type="button" class="gray" value="微信支付" >');
								window.location.href = url_go;	
								clearInterval(timer);
							}							
						}
						else if(response.result == 'USERPAYING'){
							// 等待提示
							if(i_count >= 5){
								clearInterval(timer);
								alert('网络异常');
								window.location.href = url_go;	
							}
							i_count += 1;
						}
						else{
							$("#weixin").html('<input type="button" class="gray" value="微信支付" >');
							alert('支付失败');
							window.location.href = url_go;							
						}						
					});
				}, 2000);
			}else{
				$("#weixin").html('<input type="button" class="gray" value="微信支付" >');
				alert('支付失败');
				window.location.href = url_go;				
			}
		}else{
			
		}
	});		
};
