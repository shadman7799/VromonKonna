$(document).ready(function(){
    $('.our-slider').owlCarousel({
        startPosition: 0,
        margin: 20,
        dots: true,
        loop: true,
        autoplay: true,
        pagination:true,
        dotsEach:true,
        lazyLoad:true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            }
        }
    });
});

$(document).ready(function() {
    // Show or hide the sticky footer button
    $(window).scroll(function() {
        if ($(this).scrollTop() > 200) {
            $('.go-top').fadeIn(200);
        } else {
            $('.go-top').fadeOut(200);
        }
    });
    
    // Animate the scroll to top
    $('.go-top').click(function(event) {
        event.preventDefault();
        
        $('html, body').animate({scrollTop: 0}, 300);
    })
});
