$(document).ready(function(){
	"use strict";


/*=========== MENU ===========
1. Scroll To Top 
2. Carrusel Own
3. Animacion de Inicio Pagina
4. Carrito de compras
======================================*/

    // 1. Scroll To Top 
		$(window).on('scroll',function () {
			if ($(this).scrollTop() > 600) {
				$('.return-to-top').fadeIn();
			} else {
				$('.return-to-top').fadeOut();
			}
		});
		$('.return-to-top').on('click',function(){
				$('html, body').animate({
				scrollTop: 0
			}, 1500);
			return false;
		});
	
	
	// 2. owl carousel
	
		// i. client (carousel)
		
			$('#client').owlCarousel({
				items:5,
				loop:true,
				smartSpeed: 1000,
				autoplay:true,
				dots:false,
				autoplayHoverPause:true,
				responsive:{
						0:{
							items:2
						},
						415:{
							items:3
						},
						600:{
							items:3

						},
						1200:{
							items:5
						}
					}
				});
				
				
				$('.play').on('click',function(){
					owl.trigger('play.owl.autoplay',[1000])
				})
				$('.stop').on('click',function(){
					owl.trigger('stop.owl.autoplay')
				})

		// ii.  testimonial-carousel
		
			$("#feature-carousel").owlCarousel({
				items: 1,
				autoplay: true,
				loop: true,
				dots:false,
				mouseDrag:true,
				nav:false,
				smartSpeed:1000,
				transitionStyle:"fade",
				animateIn: 'fadeIn',
				animateOut: 'fadeOutLeft'
				// navText:["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"]
			});


    // 3. welcome animation support

        $(window).load(function(){
        	$(".welcome-hero-txt h4,.welcome-hero-txt h2,.welcome-hero-txt p").removeClass("animated fadeInUp").css({'opacity':'0'});
            $(".welcome-hero-txt button").removeClass("animated fadeInDown").css({'opacity':'0'});
        });

        $(window).load(function(){
        	$(".welcome-hero-txt h4,.welcome-hero-txt h2,.welcome-hero-txt p").addClass("animated fadeInUp").css({'opacity':'0'});
            $(".welcome-hero-txt button").addClass("animated fadeInDown").css({'opacity':'0'});
        });


	// 4. Carrito de compras
		$(".cart-close").click(function(){
			$(this).parents(".single-cart-list").fadeOut();
		});

	// 5.-Pagina Imagen Carrusel

	// Código para el carrusel de fotos
		const carousel = document.getElementById('carousel');
		let currentImageIndex = 0;
		const images = carousel.getElementsByTagName('img');
		
		function showImage(index) {
		for (let i = 0; i < images.length; i++) {
			images[i].style.display = 'none';
		}
		
		images[index].style.display = 'block';
		}
		
		function nextImage() {
		currentImageIndex++;
		if (currentImageIndex >= images.length) {
			currentImageIndex = 0;
		}
		
		showImage(currentImageIndex);
		}
		
		function previousImage() {
		currentImageIndex--;
		if (currentImageIndex < 0) {
			currentImageIndex = images.length - 1;
		}
		
		showImage(currentImageIndex);
		}
		
		showImage(currentImageIndex);

	

});