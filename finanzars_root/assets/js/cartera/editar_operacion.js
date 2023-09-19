$(document).ready(function () {

  $("#cancelarEditarOpBtn").click(function () {

    var url = operacionesUrl;

    window.location.href = url;
  });

  $("#id_tipo").change(function () {
    var url = $("#operacion-form").attr("data-activos-url");  // get the url of the `load_especies` view
    var tipoId = $(this).val();  // get the selected tipo ID from the HTML input

    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/includes/ajax/load_especies/)
      data: {
        'tipo': tipoId             // add the tipo id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_especies` view function
        $("#id_activo").html(data);  // replace the contents of the especie input with the data that came from the server
      }
    });
  });

  function cargarEspecie() {
    var url = $("#operacion-form").attr("data-especies-url");  // get the url of the `load_especies` view
    var activoId = $("#id_activo").val();  // get the selected tipo ID from the HTML input
    var plazo = $("#id_plazo").val();
    var especie = $("#id_especie option:selected").text();
    var especieOriginalStr = especie.split(" ")[0]

    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/includes/ajax/load_especies/)
      data: {
        'activo': activoId,       // add the tipo id to the GET parameters
        'plazo': plazo
      },
      success: function (data) {   // `data` is the return of the `load_especies` view function
        var especieInSelect = $(data).filter(function () {
          return $(this).text().includes(especieOriginalStr);
        });

        var especieValue = especieInSelect.val()

        $("#id_especie").html(data);
        $("#id_especie").val(especieValue);  // replace the contents of the especie input with the data that came from the server
      }
    });
  }

  $("#id_activo").change(function () {
    cargarEspecie()
  });
  cargarEspecie()

  $(document).ready(function () {
    var activoId = $("#id_activo").val();

    var url = $("#operacion-form").attr("data-activo-name-url");

    function cargarNombreActivo() {
      $.ajax({
        url: url,
        data: {
          'activo': activoId,
        },
        success: function (data) {
          $("#nombreActivoDiv").html(data);
        }
      });
    }

    cargarNombreActivo();

    $("#id_activo").change(function () {
      activoId = $(this).val();
      cargarNombreActivo();
    });



    $(function () {
      $('[data-bs-toggle="tooltip"]').tooltip()
    });

    // Obtener referencias a los campos del formulario
    const obtenerMepBtn = document.getElementById("obtener-mep-btn");
    const mepInput = document.getElementById("cotiz_mep_field");
    const operacionSelect = document.getElementById("operacion_field");
    const cantidadInput = document.getElementById("cantidad_field");
    const precioArsInput = document.getElementById("precio_ars_field");
    const precioUsdInput = document.getElementById("precio_usd_field");
    const calcularArsBtn = document.getElementById("calcular-ars-btn");
    const calcularUsdBtn = document.getElementById("calcular-usd-btn");
    const totalArsInput = document.getElementById("total_ars_field");
    const totalUsdInput = document.getElementById("total_usd_field");
    const calcularTotalArsBtn = document.getElementById("calcular-total-ars-btn");
    const calcularTotalUsdBtn = document.getElementById("calcular-total-usd-btn");

    obtenerMepBtn.addEventListener("click", function () {
      // Realizar la solicitud para obtener el valor MEP desde el servidor
      fetch(loadMepUrl)
        .then((response) => response.json())
        .then((data) => {
          // Obtener el valor de cotiz_mep_input y establecer el valor MEP obtenido
          mepInput.value = data.toFixed(2);
        })
        .catch((error) => {
          console.error("Error al obtener el valor MEP:", error);
        });
    });

    totalArsInput.value = (cantidadInput.value * precioArsInput.value).toFixed(6)
    totalUsdInput.value = (cantidadInput.value * precioUsdInput.value).toFixed(6)

    calcularArsBtn.addEventListener("click", function () {
      precioArsInput.value = (precioUsdInput.value * mepInput.value).toFixed(6)
      totalArsInput.value = (cantidadInput.value * precioArsInput.value).toFixed(6)
    });

    calcularUsdBtn.addEventListener("click", function () {
      precioUsdInput.value = (precioArsInput.value / mepInput.value).toFixed(6)
      totalUsdInput.value = (cantidadInput.value * precioUsdInput.value).toFixed(6)
    });

    calcularTotalArsBtn.addEventListener("click", function () {
      totalArsInput.value = (totalUsdInput.value * mepInput.value).toFixed(6)
    });

    calcularTotalUsdBtn.addEventListener("click", function () {
      totalUsdInput.value = (totalArsInput.value / mepInput.value).toFixed(6)
    });

    [mepInput, cantidadInput, precioArsInput, precioUsdInput].forEach(function (element) {
      element.addEventListener("change", function () {
        totalArsInput.value = (cantidadInput.value * precioArsInput.value).toFixed(6)
        totalUsdInput.value = (cantidadInput.value * precioUsdInput.value).toFixed(6)
      });
    });

    const operacion = operacionSelect.options[operacionSelect.selectedIndex].value;
    if (operacion === "Venta" || operacion === "Compra") {
      cantidadInput.readOnly = false;
      precioArsInput.readOnly = false;
      calcularArsBtn.disabled = false;
      precioUsdInput.readOnly = false;
      calcularUsdBtn.disabled = false;
      totalArsInput.readOnly = true;
      totalUsdInput.readOnly = true;
      calcularTotalArsBtn.hidden = true;
      calcularTotalUsdBtn.hidden = true;
      cantidadInput.style.backgroundColor = "white";
      precioArsInput.style.backgroundColor = "white";
      precioUsdInput.style.backgroundColor = "white";
      totalArsInput.style.backgroundColor = "lightgray";
      totalUsdInput.style.backgroundColor = "lightgray";
    } else {
      cantidadInput.readOnly = true;
      precioArsInput.readOnly = true;
      calcularArsBtn.hidden = true;
      precioUsdInput.readOnly = true;
      calcularUsdBtn.hidden = true;
      totalArsInput.readOnly = false;
      totalUsdInput.readOnly = false;
      calcularTotalArsBtn.hidden = false;
      calcularTotalUsdBtn.hidden = false;
      cantidadInput.style.backgroundColor = "lightgray";
      precioArsInput.style.backgroundColor = "lightgray";
      precioUsdInput.style.backgroundColor = "lightgray";
      totalArsInput.style.backgroundColor = "white";
      totalUsdInput.style.backgroundColor = "white";
    }

    function ajustarCampos() {
      const operacion = operacionSelect.options[operacionSelect.selectedIndex].value;
      if (operacion === "Venta" || operacion === "Compra") {
        cantidadInput.readOnly = false;
        precioArsInput.readOnly = false;
        calcularArsBtn.hidden = false;
        precioUsdInput.readOnly = false;
        calcularUsdBtn.hidden = false;
        totalArsInput.readOnly = true;
        totalUsdInput.readOnly = true;
        cantidadInput.value = "";
        precioArsInput.value = "";
        precioUsdInput.value = "";
        totalArsInput.value = 0;
        totalUsdInput.value = 0;
        calcularTotalArsBtn.hidden = true;
        calcularTotalUsdBtn.hidden = true;
        cantidadInput.style.backgroundColor = "white";
        precioArsInput.style.backgroundColor = "white";
        precioUsdInput.style.backgroundColor = "white";
        totalArsInput.style.backgroundColor = "lightgray";
        totalUsdInput.style.backgroundColor = "lightgray";
      } else {
        cantidadInput.readOnly = true;
        precioArsInput.readOnly = true;
        precioUsdInput.readOnly = true;
        calcularArsBtn.hidden = true;
        calcularUsdBtn.hidden = true;
        totalArsInput.readOnly = false;
        totalUsdInput.readOnly = false;
        cantidadInput.value = 0;
        precioArsInput.value = 0;
        precioUsdInput.value = 0;
        totalArsInput.value = 0;
        totalUsdInput.value = 0;
        calcularTotalArsBtn.hidden = false;
        calcularTotalUsdBtn.hidden = false;
        cantidadInput.style.backgroundColor = "lightgray";
        precioArsInput.style.backgroundColor = "lightgray";
        precioUsdInput.style.backgroundColor = "lightgray";
        totalArsInput.style.backgroundColor = "white";
        totalUsdInput.style.backgroundColor = "white";
      }
    }
    operacionSelect.addEventListener("change", ajustarCampos);

  });
});