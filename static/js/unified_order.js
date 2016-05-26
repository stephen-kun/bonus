
var flag_order =1;
function unified_order(url, url_go, openid, bonus_type, pay_suc_url)
{
	var sum = 0;
	var table = $('input').filter("[name='table']").val();
	var bonus_num = $('input').filter("[name='bonus_num']").val();
	if(!table){
		alert('请输入桌号, 串串个数, 红包个数！');
		return ;
	}
	
	/*
	$("input").map(function(){
		if(($(this).attr('name') == 'table')||($(this).attr('name') == 'message')||($(this).attr('name') == 'order')||($(this).attr('name') == 'bonus_num')){
			return sum;
		}
		sum += Number($(this).val());
		return sum});	
		
	if(sum == 0){
		alert("请输入串串个数，红包个数！");
		return;
	}else if(sum < 0){
		alert("红包个数必须大于0！");
		return;			
	}else if()((!bonus_num) || (Number(bonus_num) == 0)){
		alert("请输入红包个数！");
		return;
	}else if(sum < Number(bonus_num)){
		alert("亲，串串不够塞红包哦！");
		return;		
	}
	*/
	
	if(!bonus_num){
		alert("请输入红包个数！");
		return;
	}
	
	$("input").map(function(){
		if(($(this).attr('name') == 'bonus_num')||($(this).attr('name') == 'table')||($(this).attr('name') == 'message')||($(this).attr('name') == 'order')){
			return sum;
		}
		sum += Number($(this).val());
		return sum});	
		
	if(sum == 0){
		alert("红包里还没有东西！");
		return;
	}
	
	if(sum < 0){
		alert("串串个数必须大于0！");
		return;			
	}
	
	if(sum < Number(bonus_num)){
		alert("亲，串串不够塞红包哦！");
		return;		
	}	
	
	if(Number(bonus_num) < 0){
		alert("红包个数必须大于0！");
		return;			
	}
	
	var input_str = $("input").map(function(){
		var str = '';
		if($(this).attr('name') != 'order')
		{
			if($(this).val())
			{	
				str = '"' + $(this).attr('name') + '"' + ':' + '"' + $(this).val() + '"';
			}
			else{
				str = '"' + $(this).attr('name') + '"' + ':' + '"' + $(this).attr('placeholder') + '"';
			}
			
		}
		return str;}).get().join();
	
	var user_str = '"action":"ACTION","openid":"OPENID","bonus_type":"BONUS_TYPE"'.replace(/ACTION/, 'ajax_weixin_order').replace(/OPENID/, openid).replace(/BONUS_TYPE/, bonus_type);
	var request_data = '{' + input_str + user_str + '}';
	
	if(flag_order){
		flag_order = 0;
		$.post(url, request_data, function(data, status){
			if(status == 'success'){
				var result = JSON.parse(data);
				if(result.status == 'SUCCESS' && result.result == 'SUCCESS'){
					if(result.pay_type == 'WALLET_PAY')
					{
						// 余额支付
						alert("红包已发送");
						window.location.href = pay_suc_url;	
					}
					else if(result.pay_type == 'WEIXIN_PAY')
					{
						// 微信支付
						window.location.href = url_go;				
					}				
				}
				else if(result.status == 'SUCCESS' && result.result == 'FAIL'){
					if(result.err_code == 'INEXISTENCE')
					{
						// 桌台不存在
						alert("该桌台不错在");
						flag_order = 1;	
					}
					else if(result.err_code == 'NOTDINING'){
						// 未就餐
						alert('该桌台目前没有就餐');
						flag_order = 1;	
					}					
				}
			}
		});
	}
	
	/*
	var xmlhttp=new XMLHttpRequest();

	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			var result = JSON.parse(xmlhttp.responseText);
			if(result.status == 'SUCCESS' && result.result == 'SUCCESS'){					
				if(result.pay_type == 'WALLET_PAY')
				{
					// 余额支付
					alert("红包已发送");
					window.location.href = pay_suc_url;	
				}
				else if(result.pay_type == 'WEIXIN_PAY')
				{
					// 微信支付
					window.location.href = url_go;				
				}
							
			}else if(result.status == 'SUCCESS' && result.result == 'FAIL'){
				if(result.err_code == 'INEXISTENCE')
				{
					// 桌台不存在
					alert("该桌台不错在");
					flag_order = 1;	
				}
				else if(result.err_code == 'NOTDINING'){
					// 未就餐
					alert('该桌台目前没有就餐');
					flag_order = 1;	
				}				
			}
		}
	};
	
	if(flag_order){
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);		
		flag_order = 0;
	}
	*/
}