document.addEventListener('DOMContentLoaded', function () {
    const filtroInput = document.getElementById('filtroTexto');
    const ordenSelect = document.getElementById('ordenPostulaciones');

    function cargarPostulaciones() {
        const texto = filtroInput ? filtroInput.value : '';
        const orden = ordenSelect ? ordenSelect.value : 'recientes';

        fetch(`/api/postulaciones/${window.trabajoId}/usuarios/?search=${encodeURIComponent(texto)}&orden=${orden}`)
            .then(res => res.json())
            .then(data => {
                const contenedor = document.getElementById('contenedor-postulantes');
                contenedor.innerHTML = '';

                if (data.usuarios.length === 0) {
                    contenedor.innerHTML = '<p class="text-muted">Aún no hay postulaciones.</p>';
                    return;
                }

                data.usuarios.forEach(user => {
                    const mensajeCorto = user.mensaje.length > 150 
                        ? user.mensaje.slice(0, 150) + '...' 
                        : user.mensaje;

                    const tieneMas = user.mensaje.length > 150;

                    const html = `
                        <div class="col-md-6">
                            <div class="card h-100 shadow-sm rounded-4">
                                <div class="card-body d-flex flex-column">
                                    <div class="d-flex align-items-center mb-3">
                                        <img src="${user.img_profile}" class="rounded-circle shadow me-3" width="60" height="60" style="object-fit: cover;">
                                        <div>
                                            <a href="/profile/view/${user.id}/" class="fw-bold mb-0 text-decoration-none text-dark h5 d-block">${user.nombre}</a>
                                            <small class="text-muted">${user.ocupacion || 'Sin ocupación registrada'}</small>
                                        </div>
                                    </div>
                                    <p class="mb-1"><i class="fa-solid fa-envelope me-1"></i> ${user.correo}</p>
                                    <p class="mb-1"><i class="fa-solid fa-phone me-1"></i> ${user.telefono}</p>
                                    <p class="mb-2"><i class="fa-solid fa-calendar-day me-1"></i> Postulado el ${user.fecha_postulacion}</p>

                                    <div class="mb-3">
                                        <h6 class="fw-semibold mb-1"><i class="fa-solid fa-message me-1 text-primary"></i>Mensaje de postulación</h6>
                                        <p class="text-muted mb-1" id="mensaje-${user.id}">${mensajeCorto}</p>
                                        ${tieneMas ? `<button class="btn btn-link p-0" onclick="mostrarMas(${user.id}, \`${user.mensaje.replace(/`/g, "\\`")}\`)">Mostrar más</button>` : ''}
                                    </div>

                                    <div class="mb-2">
                                        <h6 class="fw-semibold mb-1">Experiencia</h6>
                                        ${user.experiencia.map(e => `
                                            <p class="mb-1"><strong>${e.puesto}</strong> en ${e.empresa} (${e.inicio} - ${e.fin})</p>
                                            <small class="text-muted">Tecnologías: ${e.tecnologias}</small>
                                        `).join('')}
                                    </div>

                                    <div class="mb-3">
                                        <h6 class="fw-semibold mb-1">Educación</h6>
                                        ${user.educacion.map(e => `
                                            <p class="mb-1"><strong>${e.titulo}</strong> - ${e.institucion} (${e.inicio} - ${e.fin})</p>
                                            <small class="text-muted">Áreas: ${e.areas}</small>
                                        `).join('')}
                                    </div>

                                    <div class="mt-auto">
                                        <a href="#" class="btn btn-outline-primary w-100">
                                            <i class="fa-solid fa-paper-plane me-1"></i> Contactar
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    contenedor.innerHTML += html;
                });
            });
    }

    if (filtroInput) filtroInput.addEventListener('input', cargarPostulaciones);
    if (ordenSelect) ordenSelect.addEventListener('change', cargarPostulaciones);

    cargarPostulaciones();
});

function mostrarMas(id, textoCompleto) {
    const p = document.getElementById(`mensaje-${id}`);
    p.textContent = textoCompleto;
    event.target.remove();
}
