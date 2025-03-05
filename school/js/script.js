/* ===================================================================

 * スマホ向けメインメニュー

=================================================================== */
$(function(){
	$(window).on('load resize', function(){
		var windowWidth = $(window).width();
		if ($('#main').css('float') == 'none') {
			$('nav h3').show();
			$('nav ul').hide();
		}else {
			$('nav h3').hide();
			$('nav ul').show();
		}
	});
	$('nav h3').click(function(){
		$(this).toggleClass("menuOpen").next().slideToggle();
	});
});
