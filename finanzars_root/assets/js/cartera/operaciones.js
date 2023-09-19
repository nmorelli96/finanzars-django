$(document).ready(function () {
  $(".eliminar-operacion-trash-btn").click(function () {
    // Obtener ID de operacion a eliminar
    var operacionId = $(this).data("operacion-id");

    $("#eliminarOperacionBtn").data("operacion-id", operacionId);

    $("#eliminarOperacionModal").modal("show");

    $("#cancelarEliminarOpBtn").click(function () {
      $("#eliminarOperacionModal").modal("hide");
    });
  });

  $("#eliminarOperacionBtn").click(function () {

    var operacionId = $(this).data("operacion-id");

    var url = eliminarOperacionUrl.replace("0", operacionId);
    $.post(url,
      data = { csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value },
      function () {
        location.reload();
      });

    $("#eliminarOperacionModal").modal("hide");
  });
});

