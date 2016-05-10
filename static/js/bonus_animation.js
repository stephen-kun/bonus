$(document).ready(function () {
	var flag = 25;
    (genClips = function () {
        $t = $('.item1');
        var amount = 5;
        var width = $t.width() / amount;
        var height = $t.height() / amount;
        var totalSquares = Math.pow(amount, 2);
        var y = 0;
        var index = 1;
        for (var z = 0; z <= (amount * width) ; z = z + width) {
            $('<img class="clipped" src="/weixin/static/images/jb' + index + '.png" />').appendTo($('.item1 .clipped-box'));
            if (z === (amount * width) - width) {
                y = y + height;
                z = -width;
            }
            if (index >= 5) {
                index = 1;
            }
            index++;
            if (y === (amount * height)) {
                z = 9999999;
            }
        }
    })();
    function rand(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    var first = false,
        clicked = false;
    // On click
    $('.item1 div.kodai img').on('click', function () {

        if (clicked === false) {
            $('.full').css({
                'display': 'none'
            });
            $('.empty').css({
                'display': 'block'
            });
            clicked = true;

            $('.item1 .clipped-box').css({
                'display': 'block'
            });
            // Apply to each clipped-box div.
            $('.clipped-box img').each(function () {
				if(flag){
					var v = rand(180, 89),
						angle = rand(80, 89), 
						theta = (angle * Math.PI) / 140, 
						g = -9.9; 

					// $(this) as self
					var self = $(this);
					var t = 0,
						z, r, nx, ny,
						totalt =30;
					var negate = [1, -1, 0],
						direction = negate[Math.floor(Math.random() * negate.length)];

					var randDeg = rand(-5, 10),
						randScale = rand(0.9, 1.1),
						randDeg2 = rand(60, 10);

					// And apply those
					$(this).css({
						'transform': 'scale(' + randScale + ') skew(' + randDeg + 'deg) rotateZ(' + randDeg2 + 'deg)'
					});

					// Set an interval
					z = setInterval(function () {
						var ux = (Math.cos(theta) * v) * direction;
						var uy = (Math.sin(theta) * v) - ((+g) * t);
						nx = (ux * t);
						ny = (uy * t) + (0.25 * (g) * Math.pow(t, 2));
						if (ny < -40) {
							ny = -40;
						}
						//$("#html").html("g:" + g + "bottom:" + ny + "left:" + nx + "direction:" + direction);
						$(self).css({
							'top': (ny) + '0px',
							'left': (nx) + 'px'
						});
						// Increase the time by 0.10
						t = t + 0.10;

						//跳出循环
						if (t > totalt) {
							clicked = false;//原false
							first = true;
							clearInterval(z);
						}
					}, 30);		
					flag -= 1;
				}
                
            });
        }
    });
    r = setInterval(function () {
        if (first === true) {
            $('.empty').addClass("");//晃动加Shake
            //TODO:晃动几下
            first = false;
        }
    }, 50);
});