document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/trabajos/')
        .then(res => res.json())
        .then(data => {
            const contenedor = document.getElementById('contenedor-trabajos');
            contenedor.innerHTML = '';

            data.trabajos.forEach(trabajo => {
                const html = `
                <div class="card shadow-sm rounded-4 mb-4 w-100">
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-3">
                            <img src="${trabajo.img_profile}" class="rounded-circle me-3 shadow" width="48" height="48" style="object-fit: cover;">
                            <div>
                                <h5 class="card-title fw-bold mb-0">${trabajo.titulo}</h5>
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
                        <a href="#" class="btn btn-outline-primary btn-sm mt-2 w-100">
                            <i class="fa-solid fa-paper-plane me-1"></i> Postularme
                        </a>
                    </div>
                </div>
            `;            
                contenedor.innerHTML += html;
            });
        })
        .catch(err => {
            console.error('Error al cargar trabajos:', err);
        });
});
