
var flag_submit_phone = 1;
function submit_phone(openid, url, back_url)
{
	var phone_num = $('#phone').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "phone_num":"PHONE_NUM"}';
	var xmlhttp=new XMLHttpRequest();
	
	data = data.replace(/ACTION/, 'ajax_modify_phone').replace(/OPENID/, openid).replace(/PHONE_NUM/, phone_num);
	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			location.href=back_url;			
		}		
	};
	
	if(flag_submit_phone)
	{
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);	
		flag_submit_phone = 0;
	}
}



var flag_submit_name = 1;
function submit_name(openid, url, back_url)
{
	var name = $('#name').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "name":"NAME"}';
	var xmlhttp=new XMLHttpRequest();
	
	data = data.replace(/ACTION/, 'ajax_modify_name').replace(/OPENID/, openid).replace(/NAME/, name);
	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			location.href=back_url;			
		}		
	};
	
	if(flag_submit_name)
	{
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);	
		flag_submit_name = 0;
	}
}


var flag_submit_sex = 1;
function submit_sex(openid, url, back_url)
{
	var sex = $('#sex').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "sex":"SEX"}';
	var xmlhttp=new XMLHttpRequest();
	
	data = data.replace(/ACTION/, 'ajax_modify_sex').replace(/OPENID/, openid).replace(/SEX/, sex);
	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			location.href=back_url;			
		}		
	};
	
	if(flag_submit_sex)
	{
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);	
		flag_submit_sex = 0;
	}
}

var flag_submit_address = 1;
function submit_address(openid, url, back_url)
{
	var address = $('#address').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "address":"ADDRESS"}';
	var xmlhttp=new XMLHttpRequest();
	
	data = data.replace(/ACTION/, 'ajax_modify_address').replace(/OPENID/, openid).replace(/ADDRESS/, address);
	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			location.href=back_url;			
		}		
	};
	
	if(flag_submit_address)
	{
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);	
		flag_submit_address = 0;
	}
}


var flag_submit_email = 1;
function submit_email(openid, url, back_url)
{
	var email = $('#email').val();
	var data = '{"action":"ACTION", "openid":"OPENID", "email":"EMAIL"}';
	var xmlhttp=new XMLHttpRequest();
	
	data = data.replace(/ACTION/, 'ajax_modify_email').replace(/OPENID/, openid).replace(/EMAIL/, email);
	  
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			location.href=back_url;			
		}		
	};
	
	if(flag_submit_email)
	{
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);	
		flag_submit_email = 0;
	}
}


