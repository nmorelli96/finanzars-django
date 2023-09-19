function formatNumber(number) {
  return number.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function formatPercentage(number) {
  return number.toFixed(2).replace('.', ',');
}

$(document).ready(function () {

  $(function () {
    $('[data-bs-toggle="tooltip"]').tooltip()
    $(document).on('click', 'input[type=number]', function () { this.select(); });
  });

  const radioContado = $("#modo-contado");
  const radioCuotas = $("#modo-cuotas");
  const contadoPill = $("#cont-pill");
  const cuotasPill = $("#cuot-pill");
  const contadoVsCuotas = $("#contado-vs-cuotas");
  const cuotasVsCuotas = $("#cuotas-vs-cuotas");
  const resultadosCont = $("#cont-resultados");
  const resultadosCuot = $("#cuot-resultados");

  cuotasVsCuotas.hide();
  resultadosCont.hide();
  resultadosCuot.hide();

  radioContado.on("change", function () {
    if (radioContado.prop("checked")) {
      contadoVsCuotas.show();
      cuotasVsCuotas.hide();
      resultadosCont.hide();
      resultadosCuot.hide();
      contadoPill.removeClass("btn-secondary").addClass("btn-success");
      cuotasPill.removeClass("btn-success").addClass("btn-secondary");
    }
  });

  radioCuotas.on("change", function () {
    if (radioCuotas.prop("checked")) {
      contadoVsCuotas.hide();
      cuotasVsCuotas.show();
      resultadosCont.hide();
      resultadosCuot.hide();
      contadoPill.removeClass("btn-success").addClass("btn-secondary");
      cuotasPill.removeClass("btn-secondary").addClass("btn-success");
    }
  });

  $("#cont-btn").click(function () {
    const importeContado = parseFloat($("#cont-importe-contado").val());
    const importeCuotas = parseFloat($("#cont-importe-cuotas").val());
    const cuotas = parseInt($("#cont-cuotas").val());

    const tasaInflacion = parseFloat($("#inflacion").val() / 100);
    const tasaMP = parseFloat($("#mercado-pago-tna").val() / 100);
    const tasaPF = parseFloat($("#plazo-fijo-tna").val() / 100);

    if (importeContado > 0 && importeCuotas > 0 && (cuotas > 0 && cuotas < 121)) {
      resultadosCont.show();

      const importePorCuota = importeCuotas / cuotas;
      const totalAjustado = finance.PV(tasaInflacion, cuotas, -importePorCuota);
      const descuento = totalAjustado / importeContado - 1;
      const recargo = importeCuotas / importeContado - 1;

      $("#cont-importe-por-cuota").text(`$ ${formatNumber(importePorCuota)}`);
      $("#cont-total-ajustado").text(`$ ${formatNumber(totalAjustado)}`);
      $("#cont-descuento").text(`${formatPercentage(descuento * 100)}%`);
      $("#cont-recargo").text(`${formatPercentage(recargo * 100)}%`);

      if (descuento > 0) {
        $("#cont-conviene").text("Contado")
      }
      else {
        $("#cont-conviene").text("Cuotas")
      }

      $("#cont-conviene").css({
        "font-weight": "700",
        "color": "forestgreen",
      });

      // Tabla de cuotas ajustadas
      const tablaContado = $("#cont-tabla-cuotas");
      tablaContado.empty();
      for (let i = 1; i <= cuotas; i++) {
        const valorAjustado = importePorCuota / (1 + tasaInflacion) ** i;
        tablaContado.append(`<tr><td>${i}</td>
        <td>${formatNumber(valorAjustado)}</td></tr>`);
      }

      // Tabla de inversión
      const tablaMPContado = $("#cont-tabla-mp");
      tablaMPContado.empty();
      for (let i = 1; i <= cuotas; i++) {
        const valorSinRestarMP = finance.FV(tasaMP / 12, i, 0, -importeContado);
        const valorRestandoMP = finance.FV(tasaMP / 12, i, importePorCuota, -importeContado);
        const valorSinRestarPF = finance.FV(tasaPF / 12, i, 0, -importeContado);
        const valorRestandoPF = finance.FV(tasaPF / 12, i, importePorCuota, -importeContado);
        tablaMPContado.append(`<tr><td>${i}</td>
        <td>${formatNumber(valorSinRestarMP)}</td>
        <td>${formatNumber(valorRestandoMP)}</td>
        <td>${formatNumber(valorSinRestarPF)}</td>
        <td>${formatNumber(valorRestandoPF)}</td></tr>`);
      }
    }
  });

  $("#cuot-btn").click(function () {
    const importeCuotaA = parseFloat($("#cuot-importe-a").val());
    const importeCuotaB = parseFloat($("#cuot-importe-b").val());
    const cuotasA = parseInt($("#cuot-cuotas-a").val());
    const cuotasB = parseInt($("#cuot-cuotas-b").val());

    const tasaInflacion = parseFloat($("#inflacion").val() / 100);
    const tasaMP = parseFloat($("#mercado-pago-tna").val() / 100);
    const tasaPF = parseFloat($("#plazo-fijo-tna").val() / 100);

    if (importeCuotaA > 0 && importeCuotaB > 0 && (cuotasA > 0 && cuotasA < 121) && (cuotasB > 0 && cuotasB < 121)) {

      resultadosCuot.show();

      const importePorCuotaA = importeCuotaA / cuotasA;
      const importePorCuotaB = importeCuotaB / cuotasB;
      const totalAjustadoA = finance.PV(tasaInflacion, cuotasA, -importePorCuotaA);
      const totalAjustadoB = finance.PV(tasaInflacion, cuotasB, -importePorCuotaB);

      const descuento = 1 - totalAjustadoB / totalAjustadoA;

      $("#cuot-importe-por-cuota-a").text(`$ ${formatNumber(importePorCuotaA)}`);
      $("#cuot-importe-por-cuota-b").text(`$ ${formatNumber(importePorCuotaB)}`);
      $("#cuot-total-ajustado-a").text(`$ ${formatNumber(totalAjustadoA)}`);
      $("#cuot-total-ajustado-b").text(`$ ${formatNumber(totalAjustadoB)}`);
      $("#cuot-descuento").text(`${formatPercentage(descuento * 100)}%`);

      if (descuento > 0) {
        $("#cuot-conviene").text("Cuotas B")
      }
      else {
        $("#cuot-conviene").text("Cuotas A")
      }

      $("#cuot-conviene").css({
        "font-weight": "700",
        "color": "forestgreen",
      });

      // Tabla de cuotas ajustadas
      const tablaCuotas = $("#cuot-tabla-cuotas");
      tablaCuotas.empty();
      const cuotasToShow = cuotasA > cuotasB ? cuotasA : cuotasB;
      for (let i = 1; i <= cuotasToShow; i++) {
        const valorAjustadoA = importePorCuotaA / Math.pow(1 + tasaInflacion, Math.min(i, cuotasA));
        const valorAjustadoB = importePorCuotaB / Math.pow(1 + tasaInflacion, Math.min(i, cuotasB));

        const cuotaToShowA = i <= cuotasA ? i : "-";
        const cuotaToShowB = i <= cuotasB ? i : "-";
        const valortoShowA = cuotaToShowA != "-" ? valorAjustadoA.toFixed(2) : "-";
        const valortoShowB = cuotaToShowB != "-" ? valorAjustadoB.toFixed(2) : "-";

        tablaCuotas.append(`<tr><td>${cuotaToShowA}</td>
        <td>${valortoShowA.replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}</td>
        <td>${cuotaToShowB}</td>
        <td>${valortoShowB.replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}</td></tr>`);
      }
    }
  });
});