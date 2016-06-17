function goto_views(url){
	window.location.href = url;
}

function flush_circle() {
	$('.circle').each(function(index, el) {
		var num = $("#angle").text() * 3.6;
		if (num<=180) {
			$(this).find('.right').css('transform', "rotate(" + num + "deg)");
		} else{
			if(num > 360){
				num = 360;
			}
			$(this).find('.right').css('transform', "rotate(180deg)");
			$(this).find('.left').css('transform', "rotate(" + (num - 180) + "deg)");
		};
	});
}

function get_remain_bonus(timer, url, url_go){
	$.post(url, function(data){
		if(data.state == 0){
			if(data.has_bonus == 0){
				clearInterval(timer);
				window.location.href = url_go;
			}
			else{
				$("#picture").attr('src', data.picture);
				$("#name").text(data.name);
				$("#remain").text(data.remain);
				if(data.type == 0){
					$("#number").html('向TABLE号桌发出普通串串<font class="font_number"> NUMBER </font>串'.replace(/TABLE/, data.table).replace(/NUMBER/, data.number));
				}else{
					if(data.type == 2)
						$("#name").text("趣八八");
					$("#number").html('发出手气串串<font class="font_number"> NUMBER </font>串'.replace(/NUMBER/, data.number));
				}
				var angle = (Number(data.number) - Number(data.remain))*100/Number(data.number);
				$('#angle').text(angle.toString());
				flush_circle();
			}
		}
	}, 'json');				
}


function timer_has_bonus(url, url_go){
	var timer =setInterval(function(){
			$.post(url, function(data){
				if(data.state == 0){
					if(data.has_bonus == 1){
						clearInterval(timer);
						window.location.href = url_go;
					}
				}
			}, "json");
		}, 1000);				
}


function soccerOnload()
{
	setTimeout("blink()", 300);
}

function blink()
{
	soccer.style.visibility=(soccer.style.visibility=="hidden") ? "visible" : "hidden";
	setTimeout("blink()", 300);
}

function show(){
	var imgid=document.getElementById("imgid");
	if(imgid.style.visibility == "visible")
		imgid.style.visibility = "hidden";
	else
		imgid.style.visibility = "visible";
	setTimeout('show()',300);
}

jQuery.fn.extend({
	
	slideFocus: function(){
		var This = $(this);
		var sWidth = $(This).width(),
			len    =$(This).find('ul li').length,
			index  = 0,
			Timer;

		// btn event
		var btn = "<div class='btn'>";
		for(var i=0; i < len; i++) {
			btn += "<span></span>";
		};
		btn += "</div><div class='preNext pre'></div><div class='preNext next'></div>";
		$(This).append(btn);
		$(This).find('.btn span').eq(0).addClass('on');


		$(This).find('.btn span').mouseover(function(){
			index = $(This).find('.btn span').index(this);
			Tony(index);
		});

		$(This).find('.next').click(function(){
			index++;
			if(index == len){index = 0;}
			Tony(index);
		});

		$(This).find('.pre').click(function(){
			index--;
			if(index == -1){index = len - 1;}
			Tony(index);
		});


		// start setInterval		
		$(This).find('ul').css("width",sWidth * (len));
		$(This).hover(function(){
			clearInterval(Timer);
			show($(This).find('.preNext'));
		},function(){
			hide($(This).find('.preNext'));
			Timer=setInterval(function(){
				Tony(index);
				index++;
				if(len == index){index = 0;}
			}, 2000)
		}).trigger("mouseleave");

		function Tony(index){
			var new_width = -index * sWidth;
			$(This).find('ul').stop(true,false).animate({'left' : new_width},300);
			$(This).find('.btn span').stop(true,false).eq(index).addClass('on').siblings().removeClass('on');
		};

		
		// show hide
		function show(obj){ $(obj).stop(true,false).fadeIn();}
		function hide(obj){ $(obj).stop(true,false).fadeOut();}
	}
});