(function ($) {
  "use strict";

  // offcanvas-js
  $(".offcanvas-open").click(function () {
    $(".offcanvas-menu").addClass("active");
    $(".offcanvas-overlay").addClass("active");
  });
  $(".offcanvas-menu a").click(function () {
    $(".offcanvas-menu").removeClass("active");
    $(".offcanvas-overlay").removeClass("active");
  });
  $(".close-offcanvas").click(function () {
    $(".offcanvas-menu").removeClass("active");
    $(".offcanvas-overlay").removeClass("active");
  });
  $(document).mouseup(function (e) {
    var container = $(".offmenu");

    // If the target of the click isn't the container
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      $(".offcanvas-menu").removeClass("active");
      $(".offcanvas-overlay").removeClass("active");
    }
  });

  // owl-carousel
  $(".m-slider-active").owlCarousel({
    loop: true,
    margin: 0,
    items: 1,
    dots: false,
    responsiveClass: true,
    nav: true,
    navText: [
      '<i class="far fa-chevron-left"></i>',
      '<i class="far fa-chevron-right"></i>',
    ],
  });

  $('.nice-select').niceSelect();

  $(document).ready(function() {
  	$('.nice-select').change(function(){
  		let lang = $(this).find("option:selected").attr('value');
  		location.href = site_url+'?lang='+lang;
  		return false;     
  	});
  });
})(jQuery);

$(document).ready(function () {
  // scroll up
  $(function () {
    $.scrollUp();
  });

  // preloader
  $("#preloader").fadeOut(500);
});
