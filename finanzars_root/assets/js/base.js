$(document).ready(function () {

  $("#atribuciones-btn").click(function () {
      $("#atribucionesModal").modal("show");
  });
  $(document).on('click',function(e){
      if(!(($(e.target).closest("#atribucionesModal").length > 0))){
      $("#atribucionesModal").modal("hide");
      }
  });

  $(".dropdown").click(function() {
      if ($(window).width() < 992) {
          $(this).find(".dropdown-toggle::after").css("transform", $(this).hasClass("show") ? "" : "rotate(180deg)");
      }
  });

  updateDropdownBehavior();
      $(window).resize(updateDropdownBehavior);

  function updateDropdownBehavior() {
      if ($(window).width() >= 992) {
          $(".dropdown").hover(
              function () {
                  $(this).addClass("show");
                  $(this).find(".dropdown-menu").addClass("show");
                  $(this).find(".dropdown-toggle::after").css("transform", "rotate(180deg)");
              },
              function () {
                  $(this).removeClass("show");
                  $(this).find(".dropdown-menu").removeClass("show");
                  $(this).find(".dropdown-toggle::after").css("transform", "");
              }
          );
          $(".dropdown-toggle").removeAttr("data-bs-toggle");
      } else {
          // Si width < 992px, restaurar comportamiento predeterminado
          $(".dropdown").off("mouseenter mouseleave");
          $(".dropdown-toggle").attr("data-bs-toggle", "dropdown");
      }
  }
});

