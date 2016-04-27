/*
 * jQuery Reveal Plugin 1.0
 * www.ZURB.com
 * Copyright 2010, ZURB
 * Free to use under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
*/

var flag = 1;
function setSelectUserNo(radioObj){  
	  
	var radioCheck= $(radioObj).val();  
	if("1"==radioCheck){  
		$(radioObj).attr("checked",false);  
		$(radioObj).val("0");  
		  
	}else{   
		$(radioObj).val("1");  
		  
	}  
}    

function action_create_ticket(openid, url){
	var auth_code ;
	auth_code = document.getElementById("auth_code").value;
	if(auth_code){
		if(flag){
			var person_wallet, action;
			var xmlhttp;
			person_wallet = document.getElementById("person_wallet").value;
			auth_code = document.getElementById("auth_code").value;
			action = 'ajax_create_ticket';
			data = '{"openid":"OPENID", "action":"ACTION", "person_wallet":"PERSON_WALLET", "auth_code":"AUTH_CODE"}';
			data = data.replace(/OPENID/, openid).replace(/ACTION/, action).replace(/PERSON_WALLET/, person_wallet).replace(/AUTH_CODE/, auth_code);

			if (window.XMLHttpRequest)
			  {// code for IE7+, Firefox, Chrome, Opera, Safari
			  xmlhttp=new XMLHttpRequest();
			  }
			else
			  {// code for IE6, IE5
			  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
			  }
			  
			xmlhttp.onreadystatechange=function()
			{
				if(xmlhttp.readyState==4 && xmlhttp.status==200)
				{
					var JSONObject = JSON.parse(xmlhttp.responseText);
					var html = '<p>PART1</p><p>PART2</p><p>PART3</p>';
					if(JSONObject.status)
					{
						var a=document.getElementById("create_ticket");					
						a.style.backgroundColor="#bdbec0";
						a.value = '查看券';			
						var ticket_num = document.getElementById("ticket_num");
						ticket_num.innerHTML = html.replace(/PART1/,JSONObject.part1).replace(/PART2/,JSONObject.part2).replace(/PART3/,JSONObject.part3);
						flag = 0;	

						var modalLocation = $("#create_ticket").attr('data-reveal-id');
						$('#'+modalLocation).reveal($(this).data());			
					
					}
					else
					{
						alert("验证码有误，请重新输入！");
					}

				}
			}
			xmlhttp.open("POST", url, true);
			xmlhttp.send(data);	
		}
		else
		{
			$('input[data-reveal-id]').live('click', function(e) {
				e.preventDefault();
				var modalLocation = $(this).attr('data-reveal-id');
				$('#'+modalLocation).reveal($(this).data());			

			});			
		}	
	}
	else{
		alert("请输入验证码！");
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
        