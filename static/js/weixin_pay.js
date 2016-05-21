function wx_pay_result(url, openid, prepay_id, url_go){
	
	var timer = setInterval(function(){
		var xmlhttp = new XMLHttpRequest();
		var data = '{"openid":"OPENID","prepay_id":"PREPAY_ID", "action":"ajax_weixin_pay"}';
		data = data.replace(/OPENID/, openid).replace(/PREPAY_ID/, prepay_id);
		
		xmlhttp.onreadystatechange=function()
		{
			if(xmlhttp.readyState==4 && xmlhttp.status==200)
			{
				// 实现跳转
				var response = JSON.parse(xmlhttp.responseText);
				if(response.status == 'SUCCESS' && response.result == 'SUCCESS'){
					window.location.href = url_go;	
					clearInterval(timer);
				}
				if()

			}
		}

		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);			
	}, 2000);
	

}


function onBridgeReady(url, openid, pay_param, pay_suc_url){
	WeixinJSBridge.invoke(
		'getBrandWCPayRequest',
		pay_param,
		function(res){
			if (res.err_msg == "get_brand_wcpay_request:ok") {
				alert("支付成功");
				wx_pay_result(url, openid, pay_param['package'], pay_suc_url);				
			}
			if (res.err_msg == "get_brand_wcpay_request:cancel") {
				alert("交易取消");
			}
			if (res.err_msg == "get_brand_wcpay_request:fail") {
				alert("支付失败");
			}
		}
		
	);
}


function consumer_pay(url, openid, pay_param, pay_suc_url){
	if (typeof WeixinJSBridge == "undefined"){
		if( document.addEventListener ){
			document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
		}else if (document.attachEvent){
			document.attachEvent('WeixinJSBridgeReady', onBridgeReady); 
			document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
		}
	}else{
		onBridgeReady(url, openid, pay_param, pay_suc_url);
	} 	
}


