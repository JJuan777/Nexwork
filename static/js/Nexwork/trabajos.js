document.addEventListener('DOMContentLoaded', function () {
    const formFiltros = document.getElementById('form-filtros');

    // Cargar trabajos al inicio
    cargarTrabajos();

    // Al enviar el formulario
    formFiltros.addEventListener('submit', function (e) {
        e.preventDefault();
        cargarTrabajos();
    });
});

function cargarTrabajos() {
    const form = document.getElementById('form-filtros');
    const params = new URLSearchParams(new FormData(form)).toString();
    const url = `/api/trabajos/?${params}`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-trabajos');
            contenedor.innerHTML = '';

            data.trabajos.forEach(trabajo => {
                const deshabilitado = trabajo.ya_postulado;
                const btnTexto = deshabilitado ? 'Ya postulado' : 'Postularme';
                const btnClase = deshabilitado ? 'disabled' : '';
                const puedePostular = window.usuarioRolId !== 1;  // Solo si NO es Empresa
            
                // Botón solo si puede postular
                let botonHTML = '';
                if (puedePostular) {
                    botonHTML = `
                        <button class="btn btn-outline-primary btn-sm mt-2 w-100 btn-postular ${btnClase}" 
                            data-id="${trabajo.id}" 
                            data-titulo="${trabajo.titulo}"
                            ${deshabilitado ? 'disabled' : ''}>
                            <i class="fa-solid fa-paper-plane me-1"></i> ${btnTexto}
                        </button>
                    `;
                }
            
                const html = `
                    <div class="col">
                        <div class="card shadow-sm rounded-4 h-100">
                            <div class="card-body">
                                <div class="d-flex align-items-center mb-3">
                                    <img src="${trabajo.img_profile}" class="rounded-circle me-3 shadow" width="48" height="48" style="object-fit: cover;">
                                    <div>
                                        <h5 class="card-title fw-bold mb-0">
                                            <a href="/newworks/view/${trabajo.id}/" class="text-decoration-none text-dark">${trabajo.titulo}</a>
                                        </h5>
                                        <small class="text-muted">
                                            Publicado por <a href="/profile/view/${trabajo.autor_id}/" class="text-decoration-none fw-semibold">
                                                ${trabajo.autor_nombre}
                                            </a><br>
                                            ${trabajo.fecha}
                                        </small>
                                    </div>
                                </div>
                                <p class="mb-1"><i class="fa-solid fa-location-dot me-1 text-secondary"></i> ${trabajo.ubicacion}</p>
                                <p class="badge bg-light text-dark mb-2">${trabajo.modalidad}</p>
                                ${trabajo.descripcion ? `<p class="card-text small text-muted">${trabajo.descripcion}</p>` : ''}
                                ${botonHTML}
                            </div>
                        </div>
                    </div>`;
                
                contenedor.innerHTML += html;
            });            

            document.querySelectorAll('.btn-postular:not(.disabled)').forEach(btn => {
                btn.addEventListener('click', () => {
                    const trabajoId = btn.dataset.id;
                    const titulo = btn.dataset.titulo;

                    Swal.fire({
                        title: `Postularse a: ${titulo}`,
                        input: 'textarea',
                        inputLabel: 'Mensaje de presentación',
                        inputPlaceholder: 'Escribe una breve presentación...',
                        inputAttributes: {
                            'aria-label': 'Mensaje'
                        },
                        showCancelButton: true,
                        confirmButtonText: 'Enviar',
                        cancelButtonText: 'Cancelar',
                        preConfirm: (mensaje) => {
                            if (!mensaje.trim()) {
                                Swal.showValidationMessage('El mensaje no puede estar vacío.');
                            }
                            return mensaje;
                        }
                    }).then(result => {
                        if (result.isConfirmed) {
                            fetch(`/api/trabajos/${trabajoId}/postularse/`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': getCookie('csrftoken')
                                },
                                body: JSON.stringify({ mensaje: result.value })
                            })
                            .then(res => res.json())
                            .then(data => {
                                if (data.success) {
                                    Swal.fire({
                                        icon: 'success',
                                        title: '¡Postulado!',
                                        text: 'Tu mensaje ha sido enviado.',
                                        confirmButtonText: 'OK'
                                    }).then(() => {
                                        cargarTrabajos();
                                    });
                                } else {
                                    Swal.fire('Error', data.error || 'No se pudo enviar la postulación.', 'error');
                                }
                            })
                            .catch(() => {
                                Swal.fire('Error', 'Error de red al enviar la postulación.', 'error');
                            });
                        }
                    });
                });
            });
        })
        .catch(err => {
            console.error('Error al cargar trabajos:', err);
        });
}

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
