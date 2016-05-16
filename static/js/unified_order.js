
var flag_order =1;
function unified_order(url, url_go, openid, bonus_type)
{
	var sum = 0;
	var table = $('input').filter("[name='table']").val();
	var bonus_num = $('input').filter("[name='bonus_num']").val();
	if(!table){
		alert('请输入桌号！');
		return ;
	}
	
	if(!bonus_num){
		alert("请输入红包个数！");
		return;
	}
	
	$("input").map(function(){
		if(($(this).attr('name') == 'message')||($(this).attr('name') == 'order')){
			return sum;
		}
		sum += Number($(this).val());
		return sum});	
		
	if(sum == (Number(table) + Number(bonus_num))){
		alert("红包里还没有东西！");
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
	var data = '{' + input_str + user_str + '}';
	
	var xmlhttp=new XMLHttpRequest();

	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			window.location.href = url_go;
		}
	};
	
	if(flag_order){
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);		
		flag_order = 0;
	}
}