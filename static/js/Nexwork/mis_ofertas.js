document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-filtros');

    // Escucha el submit del formulario
    form.addEventListener('submit', function (e) {
        e.preventDefault(); // evita recarga
        cargarOfertas();
    });

    // Carga inicial sin filtros
    cargarOfertas();
});

function cargarOfertas() {
    const form = document.getElementById('form-filtros');
    const q = form.q.value.trim();
    const ubicacion = form.ubicacion.value;
    const modalidad = form.modalidad.value;

    const params = new URLSearchParams();
    if (q) params.append('q', q);
    if (ubicacion) params.append('ubicacion', ubicacion);
    if (modalidad) params.append('modalidad', modalidad);

    fetch(`/api/mis-ofertas/?${params.toString()}`)
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-ofertas');
            contenedor.innerHTML = '';

            if (data.ofertas.length === 0) {
                contenedor.innerHTML = '<p class="text-muted">No se encontraron ofertas que coincidan con los filtros.</p>';
                return;
            }

            data.ofertas.forEach(oferta => {
                const html = `
                        <div class="col-12 col-md-6">
                            <div class="card shadow-sm h-100 rounded-4">
                                <div class="card-body">
                                    <div class="d-flex align-items-center mb-3">
                                        <img src="${oferta.img_profile}" class="rounded-circle me-3 shadow" width="48" height="48" style="object-fit: cover;">
                                        <div>
                                            <a href="/newworks/view/${oferta.id}/" class="fw-bold mb-0 text-decoration-none text-dark h5 d-block">${oferta.titulo}</a>
                                            <small class="text-muted">Publicado el ${oferta.fecha}</small>
                                        </div>
                                    </div>
                                    <p class="mb-1"><i class="fa-solid fa-location-dot me-1 text-secondary"></i> ${oferta.ubicacion}</p>
                                    <p class="badge bg-light text-dark mb-2">${oferta.modalidad}</p>
                                    <p class="small text-muted">${oferta.descripcion}</p>
                                    <div class="d-grid gap-2 mt-3">
                                        <a href="/estadisticas/view/${oferta.id}/" class="btn btn-sm btn-outline-success w-100">
                                            <i class="fa-solid fa-chart-line me-1"></i> Ver análisis
                                        </a>
                                        <a href="/newworks/postulaciones/${oferta.id}/" class="btn btn-sm btn-outline-primary w-100 position-relative">
                                            <i class="fa-solid fa-users me-1"></i> Ver postulaciones
                                            ${oferta.postulaciones > 0 ? `
                                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                                    ${oferta.postulaciones}
                                                </span>
                                            ` : ''}
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                contenedor.innerHTML += html;
            });
        })
        .catch(err => {
            console.error('Error al cargar ofertas:', err);
        });
}
