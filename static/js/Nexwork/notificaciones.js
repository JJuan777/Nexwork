let offsetNotificaciones = 0;
const limite = 10;

function cargarNotificaciones(reset = false) {
    if (reset) {
        offsetNotificaciones = 0;
        document.getElementById('menu-notificaciones').innerHTML = '';
    }

    fetch(`/api/notificaciones/?offset=${offsetNotificaciones}`)
        .then(res => res.json())
        .then(data => {
            const menu = document.getElementById('menu-notificaciones');
            const contador = document.getElementById('contador-notif');
            const btnMas = document.getElementById('btn-mas-notificaciones');

            if (data.notificaciones.length === 0 && offsetNotificaciones === 0) {
                menu.innerHTML = '<li class="text-muted small px-2">Sin notificaciones.</li>';
            } else {
                data.notificaciones.forEach(n => {
                    const item = `
                        <li class="position-relative">
                            <a href="${n.url}" class="dropdown-item small d-block pe-4 ${n.leido ? '' : 'fw-semibold'} notificacion-link" data-id="${n.id}">
                                ${n.mensaje}
                                <br><small class="text-muted">${n.fecha}</small>
                            </a>
                            <button class="btn btn-sm btn-link position-absolute end-0 top-50 translate-middle-y text-danger eliminar-notificacion" title="Eliminar" data-id="${n.id}">
                                <i class="fa-solid fa-xmark"></i>
                            </button>
                        </li>
                    `;
                    menu.insertAdjacentHTML('beforeend', item);
                });
            }

            // Actualizar contador
            if (data.no_leidas > 0) {
                contador.style.display = 'inline-block';
                contador.textContent = data.no_leidas;
            } else {
                contador.style.display = 'none';
            }

            // Mostrar u ocultar botón "Mostrar más"
            if (data.hay_mas) {
                btnMas.classList.remove('d-none');
            } else {
                btnMas.classList.add('d-none');
            }
        });
}

document.addEventListener('DOMContentLoaded', function () {
    cargarNotificaciones();

    document.getElementById('btn-mas-notificaciones').addEventListener('click', function (e) {
        e.stopPropagation(); // evitar que cierre el dropdown
        offsetNotificaciones += limite;
        cargarNotificaciones();
    });

    document.querySelector('.nav-link.dropdown-toggle').addEventListener('click', function () {
        cargarNotificaciones(true); // reset
    });
});

document.addEventListener('click', function (e) {
    // Marcar como leída
    if (e.target.classList.contains('notificacion-link')) {
        const id = e.target.dataset.id;
        fetch('/api/notificaciones/marcar-leida/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ id: id })
        }).then(() => {
            // Actualizar contador
            fetch('/api/notificaciones/?offset=0')
                .then(res => res.json())
                .then(data => {
                    const contador = document.getElementById('contador-notif');
                    if (data.no_leidas > 0) {
                        contador.style.display = 'inline-block';
                        contador.textContent = data.no_leidas;
                    } else {
                        contador.style.display = 'none';
                    }
                });
        });
    }

    // Eliminar notificación
    if (e.target.closest('.eliminar-notificacion')) {
        e.preventDefault();
        const btn = e.target.closest('.eliminar-notificacion');
        const id = btn.dataset.id;

        fetch('/api/notificaciones/eliminar/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ id: id })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                btn.closest('li').remove();

                // Ver si hay más y actualizar lista y contador
                fetch('/api/notificaciones/?offset=0')
                    .then(res => res.json())
                    .then(data => {
                        const contador = document.getElementById('contador-notif');
                        const menu = document.getElementById('menu-notificaciones');
                        const btnMas = document.getElementById('btn-mas-notificaciones');

                        if (data.no_leidas > 0) {
                            contador.style.display = 'inline-block';
                            contador.textContent = data.no_leidas;
                        } else {
                            contador.style.display = 'none';
                        }

                        if (data.notificaciones.length === 0) {
                            menu.innerHTML = '<li class="text-muted small px-2">Sin notificaciones.</li>';
                            btnMas.classList.add('d-none');
                        }
                    });
            }
        });
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
