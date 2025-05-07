document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/solicitudes/')
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-solicitudes');
            contenedor.innerHTML = '';

            if (data.solicitudes.length === 0) {
                contenedor.innerHTML = '<p class="text-muted">No tienes solicitudes pendientes.</p>';
                return;
            }

            data.solicitudes.forEach(sol => {
                const card = `
                    <div class="col-md-6 mb-4">
                        <div class="card shadow-sm rounded-4 p-3 d-flex flex-row align-items-center gap-3">
                            <img src="${sol.img_profile}" class="rounded-circle" width="60" height="60" style="object-fit: cover;">
                            <div class="flex-grow-1">
                                <h6 class="fw-bold mb-1">${sol.nombre}</h6>
                                <small class="text-muted">Enviada el ${sol.fecha}</small>
                                <div class="mt-2 d-flex gap-2">
                                    <button class="btn btn-sm btn-outline-success btn-accion" data-id="${sol.id}" data-accion="aceptar">Aceptar</button>
                                    <button class="btn btn-sm btn-outline-danger btn-accion" data-id="${sol.id}" data-accion="rechazar">Rechazar</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                contenedor.innerHTML += card;
            });
        });
});

document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-accion')) {
        const btn = e.target;
        const id = btn.dataset.id;
        const accion = btn.dataset.accion;

        fetch(`/api/solicitudes/${id}/procesar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ accion: accion })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                btn.closest('.col-md-6').remove();
            
                // Mostrar mensaje si ya no hay solicitudes
                const tarjetasRestantes = document.querySelectorAll('#contenedor-solicitudes .col-md-6');
                if (tarjetasRestantes.length === 0) {
                    const contenedor = document.getElementById('contenedor-solicitudes');
                    contenedor.innerHTML = '<p class="text-muted">No tienes solicitudes pendientes.</p>';
                }
            
                // Actualizar contador
                fetch('/api/contador-solicitudes/')
                    .then(res => res.json())
                    .then(data => {
                        const contador = document.querySelector('.badge.bg-danger');
                        if (contador) {
                            if (data.count > 0) {
                                contador.textContent = data.count;
                            } else {
                                contador.remove();
                            }
                        } else if (data.count > 0) {
                            const navLink = document.querySelector('a[href*="/solicitudes"]');
                            if (navLink) {
                                const span = document.createElement('span');
                                span.className = 'position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger';
                                span.textContent = data.count;
                                navLink.appendChild(span);
                            }
                        }
                    });
            }                       
        });
    }
});
fetch('/api/contador-solicitudes/')
    .then(res => res.json())
    .then(data => {
        const contador = document.querySelector('.badge.bg-danger');
        if (contador) {
            if (data.count > 0) {
                contador.textContent = data.count;
            } else {
                contador.remove();  // elimina el badge si ya no hay solicitudes
            }
        } else if (data.count > 0) {
            // Si el contador no existía y ahora hay solicitudes, lo insertamos
            const navLink = document.querySelector('a[href*="/solicitudes"]');
            if (navLink) {
                const span = document.createElement('span');
                span.className = 'position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger';
                span.textContent = data.count;
                navLink.appendChild(span);
            }
        }
    });

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}