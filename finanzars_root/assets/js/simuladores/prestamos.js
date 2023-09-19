function calculateSum(array) {
  return array.reduce((accumulator, value) => {
    return accumulator + value;
  }, 0);
}

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

  const francesRadio = $("#frances-radio");
  const alemanRadio = $("#aleman-radio");
  const americanoRadio = $("#americano-radio");
  const directoRadio = $("#directo-radio");
  const francesPill = $("#frances-pill");
  const alemanPill = $("#aleman-pill");
  const americanoPill = $("#americano-pill");
  const directoPill = $("#directo-pill");

  const prestamoTitle = $("#prestamo-title");
  const prestamoResultados = $("#prestamo-resultados");

  francesRadio.prop("checked", true)
  prestamoResultados.hide();

  function cambiarSistemaPrestamo(titulo, pillElement) {
    prestamoTitle.html(titulo);
    prestamoResultados.hide();
    francesPill.removeClass("btn-success").addClass("btn-secondary");
    alemanPill.removeClass("btn-success").addClass("btn-secondary");
    americanoPill.removeClass("btn-success").addClass("btn-secondary");
    directoPill.removeClass("btn-success").addClass("btn-secondary");
    pillElement.removeClass("btn-secondary").addClass("btn-success");
  }

  francesRadio.on("change", function () {
    if (francesRadio.prop("checked")) {
      cambiarSistemaPrestamo("Sistema Francés", francesPill);
    }
  });

  alemanRadio.on("change", function () {
    if (alemanRadio.prop("checked")) {
      cambiarSistemaPrestamo("Sistema Alemán", alemanPill);
    }
  });

  americanoRadio.on("change", function () {
    if (americanoRadio.prop("checked")) {
      cambiarSistemaPrestamo("Sistema Americano", americanoPill);
    }
  });

  directoRadio.on("change", function () {
    if (directoRadio.prop("checked")) {
      cambiarSistemaPrestamo("Sistema de Interés Directo", directoPill);
    }
  });

  $("#prestamo-btn").click(function () {
    const inflacion = parseFloat($("#inflacion").val() / 100);
    const capital = parseFloat($("#prestamo-capital").val());
    const tna = parseFloat($("#prestamo-tna").val() / 100);
    const periodos = parseInt($("#prestamo-periodos").val());
    const iva = parseFloat($("#prestamo-iva").val() / 100) || 0;
    const seguro = parseFloat($("#prestamo-seguro").val() / 100) || 0;
    const otorgamiento = parseFloat($("#prestamo-otorgamiento").val() / 100) || 0;
    const mantenimiento = parseFloat($("#prestamo-mantenimiento").val()) || 0;

    let totalTotalArr = []

    if (capital > 0 && tna > 0 && (periodos > 0 && periodos < 481)) {
      prestamoResultados.show();

      let aRecibir = capital * (1 - otorgamiento);
      $("#prestamo-recibir").text(`$ ${formatNumber(aRecibir)}`);

      // Tabla de cuotas
      const prestamoTabla = $("#prestamo-tabla");
      prestamoTabla.empty();
      let totalCapitalArr = []
      let totalInteresArr = []
      let totalCuotaPuraArr = []
      let totalSeguroArr = []
      let totalMantenimientoArr = []
      let totalIvaArr = []
      let capitalAdeudado = 0;
      let cuotaPura = 0;
      let capitalCuota = 0;
      let interesCuota = 0;
      for (let i = 0; i <= periodos; i++) {
        if (i == 0) {
          capitalAdeudado = capital;
          const seguroCuota = 0, mantenimientoCuota = 0, ivaCuota = 0;
          capitalCuota = interesCuota = cuotaPura = 0;
          totalCuota = -aRecibir;
          totalTotalArr.push(totalCuota);
          prestamoTabla.push(`<tr><td>${i}</td>
            <td>${capitalAdeudado.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}</td>
            <td></td><td></td><td></td><td></td><td></td><td></td>
            <td>${totalCuota.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}</td></tr>`)
        }
        else {
          if (francesRadio.prop("checked")) {
            cuotaPura = capital * (tna / 12 / (1 - (1 + tna / 12) ** (- periodos)));
            totalCuotaPuraArr.push(cuotaPura);
            capitalCuota = cuotaPura / (1 + tna / 12) ** (periodos - i + 1);
            totalCapitalArr.push(capitalCuota);
            interesCuota = capitalAdeudado * tna / 12;
            totalInteresArr.push(interesCuota);
          }
          if (alemanRadio.prop("checked")) {
            capitalCuota = capital / periodos;
            totalCapitalArr.push(capitalCuota);
            interesCuota = capitalAdeudado * tna / 12;
            totalInteresArr.push(interesCuota);
            cuotaPura = capitalCuota + interesCuota;
            totalCuotaPuraArr.push(cuotaPura);
          }
          if (americanoRadio.prop("checked")) {
            interesCuota = capitalAdeudado * tna / 12;
            totalInteresArr.push(interesCuota);
            if (i !== periodos) {
              capitalCuota = 0;
            } else {
              capitalCuota = capital;
              capitalAdeudado = 0;
            }
            totalCapitalArr.push(capitalCuota);
            cuotaPura = capitalCuota + interesCuota;
            totalCuotaPuraArr.push(cuotaPura);
          }
          if (directoRadio.prop("checked")) {
            capitalCuota = capital / periodos;
            totalCapitalArr.push(capitalCuota);
            interesCuota = capital * tna / 12;
            totalInteresArr.push(interesCuota);
            cuotaPura = capitalCuota + interesCuota;
            totalCuotaPuraArr.push(cuotaPura);
          }
          let seguroCuota = capitalAdeudado * seguro;
          totalSeguroArr.push(seguroCuota);
          let mantenimientoCuota = mantenimiento;
          totalMantenimientoArr.push(mantenimientoCuota);
          let ivaCuota = interesCuota * iva;
          totalIvaArr.push(ivaCuota);
          let totalCuota = cuotaPura + seguroCuota + mantenimientoCuota + ivaCuota;
          totalTotalArr.push(totalCuota)
          prestamoTabla.append(`<tr>
            <td>${i}</td>
            <td>${formatNumber(capitalAdeudado)}</td>
            <td>${formatNumber(capitalCuota)}</td>
            <td>${formatNumber(interesCuota)}</td>
            <td>${formatNumber(cuotaPura)}</td>
            <td>${formatNumber(seguroCuota)}</td>
            <td>${formatNumber(mantenimientoCuota)}</td>
            <td>${formatNumber(ivaCuota)}</td>
            <td>${formatNumber(totalCuota)}</td>
            </tr>
          `);
          if (!(americanoRadio.prop("checked"))) {
            capitalAdeudado = capitalAdeudado - capitalCuota;
          }
        }
      }

      // Fila de Totales

      let totalCapital = calculateSum(totalCapitalArr);
      let totalInteres = calculateSum(totalInteresArr);
      let totalCuotaPura = calculateSum(totalCuotaPuraArr);
      let totalSeguro = calculateSum(totalSeguroArr);
      let totalMantenimiento = calculateSum(totalMantenimientoArr);
      let totalIva = calculateSum(totalIvaArr);
      vaTotalArr = totalTotalArr.slice(1)
      let totalTotal = calculateSum(vaTotalArr);

      prestamoTabla.append(`<tr>
        <td colspan="2" class="fw-bold">Totales</td>
        <td class="fw-bold">${formatNumber(totalCapital)}</td>
        <td class="fw-bold">${formatNumber(totalInteres)}</td>
        <td class="fw-bold">${formatNumber(totalCuotaPura)}</td>
        <td class="fw-bold">${formatNumber(totalSeguro)}</td>
        <td class="fw-bold">${formatNumber(totalMantenimiento)}</td>
        <td class="fw-bold">${formatNumber(totalIva)}</td>
        <td class="fw-bold">${formatNumber(totalTotal)}</td>
        </tr>
      `);
      const tea = ((1 + tna / 12) ** 12) - 1;
      const cftMensual = finance.IRR(totalTotalArr);
      const cft = ((1 + cftMensual) ** 12) - 1;
      vaTotalArr = totalTotalArr.slice(1)
      const va = finance.NPV(inflacion, ...vaTotalArr);
      const vf = calculateSum(vaTotalArr);

      $("#prestamo-tea").text(`${formatPercentage(tea * 100)}%`);
      $("#prestamo-cft-mensual").text(`${formatPercentage(cftMensual * 100)}%`);
      $("#prestamo-cft").text(`${formatPercentage(cft * 100)}%`);
      $("#prestamo-va").text(`$ ${formatNumber(va)}`);
      $("#prestamo-vf").text(`$ ${formatNumber(vf)}`);

      if (va < vf) {
        $("#prestamo-va").css({
          "font-weight": "700",
          "color": "forestgreen",
        });
        $("#prestamo-vf").css({
          "font-weight": "700",
          "color": "crimson",
        });
      }
      else {
        $("#prestamo-va").css({
          "font-weight": "700",
          "color": "crimson",
        });
        $("#prestamo-vf").css({
          "font-weight": "700",
          "color": "forestgreen",
        });
      }
    }
  });
});