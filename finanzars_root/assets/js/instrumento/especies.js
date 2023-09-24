document.addEventListener("DOMContentLoaded", function () {

  // Filtrado con formato de lista de moneda y plazo
  const form = document.querySelector('#especies-filter');
  
  form.addEventListener('submit', function(event) {
    const monedaBtns = document.getElementById('moneda-btns')
    const plazoBtns = document.getElementById('plazo-btns')
    const monedaCheckboxes = monedaBtns.querySelectorAll('input[type="checkbox"]');
    const plazoCheckboxes = plazoBtns.querySelectorAll('input[type="checkbox"]');
    const monedaValues = [];
    const plazoValues = [];

    // Obtenemos los valores de plazo y moneda seleccionados y los agregamos a un array
    plazoCheckboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        plazoValues.push(checkbox.value);
      }
    });
    monedaCheckboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        monedaValues.push(checkbox.value);
      }
    });

    // Unimos los valores seleccionados y los pasamos a un hidden input para que los parsee django-filters
    form.querySelector('input[name="plazo"]').value = plazoValues.join(',');
    form.querySelector('input[name="moneda"]').value = monedaValues.join(',');
  });

  
  // Función para obtener las watchlists del usuario y mostrar el modal
  function showAgregarFavoritoModal(especieId) {

    fetch(watchlistsDataUrl)
      .then((response) => response.json())
      .then((watchlists) => {
        const modalBody = document.querySelector("#agregarFavoritoModal .modal-body");
        modalBody.innerHTML = ""; // Limpia el contenido anterior

        const form = document.createElement("form");
        form.method = "post";
        form.id = "agregarFavoritoForm";
        form.noValidate = true;
        if (watchlists.length > 0){
          form.innerHTML = `
            <input type="hidden" id="especieIdInput" name="especie_id_input" value="${especieId}">
            <label class="mb-2">Seleccioná las watchlists en las que querés incluir la especie:</label>
            <div id="watchlists-checkboxes" class="d-flex flex-column gap-1">
              <!-- Aquí se llenarán los checkboxes con las watchlists -->
            </div>
          `;
        }
        else {
          form.innerHTML = `<p>Para empezar a seguir tus especies favoritas, <a href=${watchlistsUrl}>creá una watchlist entrando acá</a></p>`
        }

        const checkboxesDiv = form.querySelector("#watchlists-checkboxes");

        // Llena el modal con los checkboxes de las watchlists
        watchlists.forEach((watchlist) => {
          const checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.name = "watchlists";
          checkbox.value = watchlist.id;
          checkbox.checked = watchlist.especies.includes(parseInt(especieId));
          checkbox.setAttribute("data-watchlist-id", watchlist.id); // Nuevo atributo para identificar el checkbox
          checkbox.classList.add("form-check-input");
          checkbox.classList.add("me-1");

          checkbox.addEventListener("change", function () {
            // Obtener el valor actual del checkbox
            const isChecked = this.checked;

            // Obtener el ID de la especie y la watchlist
            const especieId = document.getElementById("especieIdInput").value;
            const watchlistId = this.value;

            // Crear un FormData para enviar la información
            const formData = new FormData();
            formData.append("especie_id", especieId);
            formData.append("watchlist", watchlistId);

            // Determinar la URL para agregar o eliminar según el estado del checkbox
            const url = isChecked ? agregarFavoritoUrl : eliminarFavoritoUrl;

            // Enviar la petición usando fetch
            fetch(url, {
              method: "POST",
              headers: {
                "X-CSRFToken": token,
              },
              body: formData,
            })
              .then((response) => {
                if (response.ok) {
                  // Actualizar el estado del checkbox en la interfaz
                  this.checked = isChecked;
                  console.log("Cambio realizado exitosamente");
                } else {
                  console.error("Error al realizar el cambio");
                }
              })
              .catch((error) => {
                console.error("Error al realizar el cambio", error);
              });
          });

          const label = document.createElement("label");
          label.appendChild(checkbox);
          label.appendChild(document.createTextNode(watchlist.nombre));
          checkboxesDiv.appendChild(label);
        });


        // Agrega el formulario al modal
        modalBody.appendChild(form);

        // Muestra el modal
        const agregarFavoritoModal = new bootstrap.Modal(document.getElementById("agregarFavoritoModal"));
        agregarFavoritoModal.show();
      })
      .catch((error) => {
        console.error("Error al obtener las watchlists del usuario", error);
      });
  }

  const agregarFavoritoBtns = document.querySelectorAll(".agregar-favorito-btn");

  agregarFavoritoBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const especieId = btn.dataset.especieId;
      showAgregarFavoritoModal(especieId);
    });
  });

  const agregarFavoritoModal = document.getElementById("agregarFavoritoModal");
  agregarFavoritoModal.addEventListener("hidden.bs.modal", function () {
    // Refrescar cuando el modal se oculte.
    location.reload();
  });



  // Función para obtener las watchlists del usuario
  function getWatchlists() {
    if (userAuthenticated) {
      $.ajax({
        url: watchlistsDataUrl,
        method: "GET",
        dataType: "json",
        success: function (data) {
          // Obtener la lista de especies en todas las watchlists del usuario
          var especiesEnWatchlist = [].concat(...data.map(watchlist => watchlist.especies));

          // Actualizar el ícono de la estrella en cada fila de la tabla
          $(".agregar-favorito-btn").each(function () {
            var especieId = $(this).data("especie-id");
            if (especiesEnWatchlist.includes(especieId)) {
              $(this).html('<i class="fa-solid fa-star fa-sm" style="color: gold; text-shadow: 0px 0px 1px rgba(0, 0, 0, 1);"></i>');
              $(this).data("favorito", true);
            } else {
              $(this).html('<i class="fa-regular fa-star fa-sm" style="color: rgb(230, 195, 0); text-shadow: 0px 0px 1px rgba(0, 0, 0, 1);"></i>');
              $(this).data("favorito", false);
            }
          });
        },
        error: function (error) {
          console.error("Error al obtener las watchlists del usuario", error);
        },
      });
    }
    else {
      $(".agregar-favorito-btn").each(function () {
        var especieId = $(this).data("especie-id");
        $(this).html('<i class="fa-regular fa-star fa-sm" style="color: rgb(230, 195, 0); text-shadow: 0px 0px 1px rgba(0, 0, 0, 1);"></i>');
      });
      $(document).on("click", ".fa-regular.fa-star", function () {
        window.location.href = loginUrl;
      });
    }
  }

  // Llama a la función para obtener las watchlists al cargar la página
  getWatchlists();

  // Agregar un listener para actualizar las watchlists cuando se agrega una nueva especie a la watchlist
  $(document).on("click", ".agregar-favorito-modal-btn", function () {
    getWatchlists();
  });
});
