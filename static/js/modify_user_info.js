
function submit_phone(openid, url, back_url)
{
	var phone_num = $('#phone').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "phone_num":"PHONE_NUM"}';
	data = data.replace(/ACTION/, 'ajax_modify_phone').replace(/OPENID/, openid).replace(/PHONE_NUM/, phone_num);
	
	$.post(url, data, function(data, status){
		if(status == 'success'){
			location.href=back_url;	
		}
	});
}



function submit_name(openid, url, back_url)
{
	var name = $('#name').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "name":"NAME"}';
	data = data.replace(/ACTION/, 'ajax_modify_name').replace(/OPENID/, openid).replace(/NAME/, name);
	  
	$.post(url, data, function(data, status){
		if(status == 'success'){
			location.href=back_url;	
		}
	});
}


function submit_sex_woman(openid, url, back_url)
{
	var sex = $('#sex_woman').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "sex":"SEX"}';
	data = data.replace(/ACTION/, 'ajax_modify_sex').replace(/OPENID/, openid).replace(/SEX/, sex);
	  
	$.post(url, data, function(data, status){
		if(status == 'success'){
			location.href=back_url;	
		}
	});
}


function submit_address(openid, url, back_url)
{
	var address = $('#address').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "address":"ADDRESS"}';
	data = data.replace(/ACTION/, 'ajax_modify_address').replace(/OPENID/, openid).replace(/ADDRESS/, address);
	  
	$.post(url, data, function(data, status){
		if(status == 'success'){
			location.href=back_url;	
		}
	});
}


function submit_sex_man(openid, url, back_url)
{
	var sex = $('#sex_man').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "sex":"SEX"}';

	
	data = data.replace(/ACTION/, 'ajax_modify_sex').replace(/OPENID/, openid).replace(/SEX/, sex);
	  
	$.post(url, data, function(data, status){
		if(status == 'success'){
			location.href=back_url;	
		}
	});
}



function submit_email(openid, url, back_url)
{
	var email = $('#email').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "email":"EMAIL"}';

	
	data = data.replace(/ACTION/, 'ajax_modify_email').replace(/OPENID/, openid).replace(/EMAIL/, email);
	  
	$.post(url, data, function(data, status){
		if(status == 'success'){
			location.href=back_url;	
		}
	});
}


