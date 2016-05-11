// JavaScript Document
	function toshare(openid, id_bonus){
		$(".am-share").addClass("am-modal-active");	
		if($(".send_out").length>0){
			$(".send_out").addClass("sharebg-active");
		}else{
			$("body").append('<div class="send_out"></div>');
			$(".send_out").addClass("sharebg-active");
		}
		$(".sharebg-active,.share_btn").click(function(){
			$(".am-share").removeClass("am-modal-active");	
			setTimeout(function(){
				$(".sharebg-active").removeClass("sharebg-active");	
				$(".send_out").unchanged();	
			},300);
		})
		
		document.getElementById("openid").value=openid;
		document.getElementById("id_bonus").value=id_bonus;		
		document.getElementById("show_message").value=id_bonus;
	}