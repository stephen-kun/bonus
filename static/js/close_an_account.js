/*
 * jQuery Reveal Plugin 1.0
 * www.ZURB.com
 * Copyright 2010, ZURB
 * Free to use under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
*/

var flag_close_account = 1;
var flag_check_code = 0;   
function action_create_ticket(openid, total_money, url){
	var auth_code ;
	auth_code = $("#auth_code").val();
	var ticket_value = Number($("#ticket_value").val());
	var sum = Number(total_money) + Number($("#user_wallet").val());
	
	if(!ticket_value){
		alert("请设置券面值！");
		return;
	}
	else if(ticket_value == 0 && sum > 0){
		var info = '您能设置的最大券值为SUM';
		info = info.replace(/SUM/, sum);
		alert(info);
		return;
	}
	
	if(!auth_code){
		alert("请输入6位验证码！");
		return;
	}

	if(!sum){
		alert("没有串串");
		return;
	}
	
	
	var user_wallet, action;
	var xmlhttp = new XMLHttpRequest();
	user_wallet = document.getElementById("user_wallet").value;
	auth_code = document.getElementById("auth_code").value;
	action = 'ajax_create_ticket';
	var data = '{"openid":"OPENID", "action":"ACTION", "user_wallet":"USER_WALLET", "total_money":"TOTAL_MONEY","ticket_value":"TICKET_VALUE","auth_code":"AUTH_CODE"}';
	data = data.replace(/OPENID/, openid).replace(/ACTION/, action).replace(/USER_WALLET/, user_wallet).replace(/TOTAL_MONEY/,total_money).replace(/TICKET_VALUE/,ticket_value).replace(/AUTH_CODE/, auth_code);

	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4 && xmlhttp.status==200)
		{
			var JSONObject = JSON.parse(xmlhttp.responseText);
			var html = '<p>PART1</p><p>PART2</p><p>PART3</p>';
			if(JSONObject.status)
			{
				alert(JSONObject.error_message);								
			}
			else
			{					
				var a=document.getElementById("create_ticket");					
				a.style.backgroundColor="#bdbec0";
				a.value = '查看券';			
				document.getElementById("ticket_code").innerHTML = html.replace(/PART1/,JSONObject.part1).replace(/PART2/,JSONObject.part2).replace(/PART3/,JSONObject.part3);
				document.getElementById("value").innerHTML = JSONObject.ticket_value;	
				flag_check_code = 1;
				var modalLocation = $("#create_ticket").attr('data-reveal-id');
				$('#'+modalLocation).reveal($(this).data());								
			}

		}
	}
	
	if(flag_close_account)
	{
		flag_close_account = 0;	
		xmlhttp.open("POST", url, true);
		xmlhttp.send(data);			
	}
	
	if(flag_check_code)
	{
		$('input[data-reveal-id]').live('click', function(e) {
			e.preventDefault();
			var modalLocation = $(this).attr('data-reveal-id');
			$('#'+modalLocation).reveal($(this).data());			

		});			
	}	

}


(function($) {

/*---------------------------
 Defaults for Reveal
----------------------------*/
/*---------------------------
 Extend and Execute
----------------------------*/

    $.fn.reveal = function(options) {
        
        
        var defaults = {  
	    	animation: 'fadeAndPop', //fade, fadeAndPop, none
		    animationspeed: 300, //how fast animtions are
		    closeonbackgroundclick: true, //if you click background will modal close?
		    dismissmodalclass: 'close-reveal-modal' //the class of a button or element that will close an open modal
    	}; 
    	
        //Extend dem' options
        var options = $.extend({}, defaults, options); 
	
        return this.each(function() {
        
/*---------------------------
 Global Variables
----------------------------*/
        	var modal = $(this),
        		topMeasure  = parseInt(modal.css('top')),
				topOffset = modal.height() + topMeasure,
          		locked = false,
				modalBG = $('.reveal-modal-bg');

/*---------------------------
 Create Modal BG
----------------------------*/
			if(modalBG.length == 0) {
				modalBG = $('<div class="reveal-modal-bg" />').insertAfter(modal);
				modalBG.css({position:"absolute",height:$(document).height(),opacity:"0.35"});
			}		    
        	
/*---------------------------
 Open and add Closing Listeners
----------------------------*/
        	//Open Modal Immediately
    		openModal();
			
			//Close Modal Listeners
			var closeButton = $('.' + options.dismissmodalclass).bind('click.modalEvent',closeModal)
			if(futures.closeonbackgroundclick) {   //options
				modalBG.css({"cursor":"pointer"})
				modalBG.bind('click.modalEvent',closeModal)
			}
			
    		
/*---------------------------
 Open & Close Animations
----------------------------*/
			//Entrance Animations
			function openModal() {
				modalBG.unbind('click.modalEvent');
				$('.' + options.dismissmodalclass).unbind('click.modalEvent');
				if(!locked) {
					lockModal();
					if(options.animation == "fadeAndPop") {
						modal.css({'top': $(document).scrollTop()-topOffset, 'opacity' : 0, 'visibility' : 'visible'});
						modalBG.fadeIn(options.animationspeed/2);
						modal.delay(options.animationspeed/2).animate({
							"top": $(document).scrollTop()+topMeasure,
							"opacity" : 1
						}, options.animationspeed,unlockModal());					
					}
					if(options.animation == "fade") {
						modal.css({'opacity' : 0, 'visibility' : 'visible', 'top': $(document).scrollTop()+topMeasure});
						modalBG.fadeIn(options.animationspeed/2);
						modal.delay(options.animationspeed/2).animate({
							"opacity" : 1
						}, options.animationspeed,unlockModal());					
					} 
					if(options.animation == "none") {
						modal.css({'visibility' : 'visible', 'top':$(document).scrollTop()+topMeasure});
						modalBG.css({"display":"block"});	
						unlockModal()				
					}   
				}
			}    	
			
			//Closing Animation
			function closeModal() {
				if(!locked) {
					lockModal();
					if(options.animation == "fadeAndPop") {
						modalBG.delay(options.animationspeed).fadeOut(options.animationspeed);
						modal.animate({
							"top":  $(document).scrollTop()-topOffset,
							"opacity" : 0
						}, options.animationspeed/2, function() {
							modal.css({'top':topMeasure, 'opacity' : 1, 'visibility' : 'hidden'});
							unlockModal();
						});					
					}  	
					if(options.animation == "fade") {
						modalBG.delay(options.animationspeed).fadeOut(options.animationspeed);
						modal.animate({
							"opacity" : 0
						}, options.animationspeed, function() {
							modal.css({'opacity' : 1, 'visibility' : 'hidden', 'top' : topMeasure});
							unlockModal();
						});					
					}  	
					if(options.animation == "none") {
						modal.css({'visibility' : 'hidden', 'top' : topMeasure});
						modalBG.css({'display' : 'none'});	
					}   			
				}
			}
			
/*---------------------------
 Animations Locks
----------------------------*/
			function unlockModal() { 
				locked = false;
			}
			function lockModal() {
				locked = true;
			}	
			
        });//each call
    }//orbit plugin call
})(jQuery);
        