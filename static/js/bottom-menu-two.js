window.onload = function(){
	$('#indexmenu ul li').each(function(j){
		$('#indexmenu ul li').eq(j).removeClass("on");
		$('#indexmenu ul li span').eq(j).animate({bottom:-$('#indexmenu ul li span').eq(j).height()},100);
	});
}

$('#indexmenu ul li').each(function(i){
	$(this).click(function(){
		if($(this).attr("class")!="on"){
			$('#indexmenu ul .on span').animate({bottom:-$('#indexmenu ul .on span').height()},200);
			$('#indexmenu ul .on').removeClass("on");
			$(this).addClass("on");
			$('#indexmenu ul li span').eq(i).animate({bottom:35},200);
			$('.footer_front').show();
		}else{
			$('#indexmenu ul li span').eq(i).animate({bottom:-$('#indexmenu ul li span').eq(i).height()},200);
			$(this).removeClass("on");
			$('.footer_front').hide();
		}
	});
});

$('.footer_front').click(function(){
	$('#indexmenu ul .on span').animate({bottom:-$('#indexmenu ul .on span').height()},200);
	$('#indexmenu ul .on').removeClass("on");
	$(this).hide();
});