window.onload = function(){
	$('#menu ul li').each(function(j){
		$('#menu ul li').eq(j).removeClass("on");
		$('#menu ul li span').eq(j).animate({bottom:-$('#menu ul li span').eq(j).height()},100);
	});
}

$('#menu ul li').each(function(i){
	$(this).click(function(){
		if($(this).attr("class")!="on"){
			$('#menu ul .on span').animate({bottom:-$('#menu ul .on span').height()},200);
			$('#menu ul .on').removeClass("on");
			$(this).addClass("on");
			$('#menu ul li span').eq(i).animate({bottom:35},200);
			$('.footer_front').show();
		}else{
			$('#menu ul li span').eq(i).animate({bottom:-$('#menu ul li span').eq(i).height()},200);
			$(this).removeClass("on");
			$('.footer_front').hide();
		}
	});
});

$('.footer_front').click(function(){
	$('#menu ul .on span').animate({bottom:-$('#menu ul .on span').height()},200);
	$('#menu ul .on').removeClass("on");
	$(this).hide();
});