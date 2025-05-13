document.addEventListener('DOMContentLoaded', function () {

    let historiasGlobal = [];
    let historiaActual = 0;

    function mostrarHistoria(index) {
        const historia = historiasGlobal[index];
        if (!historia) return;

        historiaActual = index;

        document.getElementById('autorVerHistoria').textContent = historia.autor;
        document.getElementById('horaVerHistoria').textContent = historia.hora;
        const imagen = document.getElementById('imagenVerHistoria');
        imagen.classList.remove('show', 'fade-in');
        void imagen.offsetWidth;  // Reiniciar animación
        imagen.classList.add('fade-in');
        imagen.src = historia.imagen;
        setTimeout(() => {
            imagen.classList.add('show');
        }, 10);

        document.getElementById('textoVerHistoria').textContent = historia.texto || '';

        const btnEliminar = document.getElementById('btnEliminarHistoria');
        const footer = document.getElementById('footerEliminarHistoria');
        if (historia.es_mia) {
            footer.classList.remove('d-none');
            btnEliminar.setAttribute('data-id', historia.id);
        } else {
            footer.classList.add('d-none');
            btnEliminar.removeAttribute('data-id');
        }

        document.getElementById('btnAnteriorHistoria').style.display = index > 0 ? 'block' : 'none';
        document.getElementById('btnSiguienteHistoria').style.display = index < historiasGlobal.length - 1 ? 'block' : 'none';
    }

    function actualizarFlechasScroll() {
        const contenedor = document.getElementById('contenedor-historias');
        const left = document.getElementById('btn-historias-left');
        const right = document.getElementById('btn-historias-right');

        const scrollLeft = contenedor.scrollLeft;
        const maxScrollLeft = contenedor.scrollWidth - contenedor.clientWidth;

        if (scrollLeft <= 0) {
            left.classList.add('d-none');
        } else {
            left.classList.remove('d-none');
        }

        if (scrollLeft >= maxScrollLeft - 1) {
            right.classList.add('d-none');
        } else {
            right.classList.remove('d-none');
        }
    }

    function cargarHistorias() {
        fetch('/api/historias/')
            .then(response => response.json())
            .then(data => {
                const contenedor = document.getElementById('contenedor-historias');
                contenedor.innerHTML = '';

                historiasGlobal = data.historias;

                contenedor.innerHTML += `
                    <div class="text-center" style="min-width: 75px;">
                        <div class="position-relative mb-1">
                            <div class="rounded-circle border d-flex align-items-center justify-content-center"
                                style="width: 68px; height: 68px; background-color: #f0f0f0; cursor: pointer;"
                                data-bs-toggle="modal" data-bs-target="#modalHistoria">
                                <i class="fa-solid fa-plus text-primary"></i>
                            </div>
                        </div>
                        <small class="d-block text-truncate" style="max-width: 75px;">Tu historia</small>
                    </div>
                `;

                data.historias.forEach((historia, i) => {
                    const historiaEl = document.createElement('div');
                    historiaEl.className = 'text-center';
                    historiaEl.style.minWidth = '75px';
                    historiaEl.innerHTML = `
                        <div class="mb-1" style="cursor: pointer;">
                            <img src="${historia.imagen}" class="rounded-circle border border-3" width="68" height="68" style="object-fit: cover; border-color: #d6249f;">
                        </div>
                        <small class="d-block text-truncate" style="max-width: 75px;">${historia.nombre}</small>
                    `;

                    historiaEl.addEventListener('click', () => {
                        mostrarHistoria(i);
                        const modal = new bootstrap.Modal(document.getElementById('modalVerHistoria'));
                        modal.show();
                    });

                    contenedor.appendChild(historiaEl);
                });

                actualizarFlechasScroll();
            })
            .catch(error => {
                console.error("Error cargando historias:", error);
            });
    }

    cargarHistorias();

    const inputImg = document.getElementById('inputHistoriaImg');
    const previewImg = document.getElementById('previewHistoriaImg');

    if (inputImg) {
        inputImg.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewImg.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            } else {
                previewImg.classList.add('d-none');
                previewImg.src = "#";
            }
        });
    }

    const formHistoria = document.getElementById('formHistoria');
    if (formHistoria) {
        formHistoria.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(formHistoria);

            fetch('/api/historias/publicar/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) throw new Error("Error al publicar historia");
                return response.json();
            })
            .then(data => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('modalHistoria'));
                modal.hide();

                formHistoria.reset();
                previewImg.classList.add('d-none');
                previewImg.src = "#";

                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    icon: 'success',
                    title: 'Historia publicada',
                    showConfirmButton: false,
                    timer: 2000,
                    timerProgressBar: true
                });

                cargarHistorias();
            })
            .catch(error => {
                console.error("Error al publicar historia:", error);
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'No se pudo publicar la historia.'
                });
            });
        });
    }

    const btnEliminarHistoria = document.getElementById('btnEliminarHistoria');
    if (btnEliminarHistoria) {
        btnEliminarHistoria.addEventListener('click', () => {
            const historiaId = btnEliminarHistoria.getAttribute('data-id');

            Swal.fire({
                title: '¿Eliminar historia?',
                text: 'Esta acción no se puede deshacer.',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/api/historias/eliminar/${historiaId}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        }
                    })
                    .then(res => {
                        if (!res.ok) throw new Error("Error eliminando historia");
                        return res.json();
                    })
                    .then(() => {
                        Swal.fire({
                            toast: true,
                            position: 'top-end',
                            icon: 'success',
                            title: 'Historia eliminada',
                            showConfirmButton: false,
                            timer: 2000
                        });
                        bootstrap.Modal.getInstance(document.getElementById('modalVerHistoria')).hide();
                        cargarHistorias();
                    })
                    .catch(err => {
                        Swal.fire('Error', 'No se pudo eliminar la historia', 'error');
                    });
                }
            });
        });
    }

    document.getElementById('btnAnteriorHistoria').addEventListener('click', () => {
        if (historiaActual > 0) {
            mostrarHistoria(historiaActual - 1);
        }
    });

    document.getElementById('btnSiguienteHistoria').addEventListener('click', () => {
        if (historiaActual < historiasGlobal.length - 1) {
            mostrarHistoria(historiaActual + 1);
        }
    });

    document.addEventListener('keydown', (e) => {
        const modal = document.getElementById('modalVerHistoria');
        if (!modal.classList.contains('show')) return;

        if (e.key === 'ArrowRight') {
            if (historiaActual < historiasGlobal.length - 1) {
                mostrarHistoria(historiaActual + 1);
            }
        } else if (e.key === 'ArrowLeft') {
            if (historiaActual > 0) {
                mostrarHistoria(historiaActual - 1);
            }
        }
    });

    const contenedorHistorias = document.getElementById('contenedor-historias');
    contenedorHistorias.addEventListener('wheel', function(e) {
        if (e.deltaY !== 0) {
            e.preventDefault();
            this.scrollLeft += e.deltaY;
            actualizarFlechasScroll();
        }
    });

    document.getElementById('btn-historias-left').addEventListener('click', () => {
        contenedorHistorias.scrollBy({ left: -150, behavior: 'smooth' });
        setTimeout(actualizarFlechasScroll, 200);
    });

    document.getElementById('btn-historias-right').addEventListener('click', () => {
        contenedorHistorias.scrollBy({ left: 150, behavior: 'smooth' });
        setTimeout(actualizarFlechasScroll, 200);
    });

    contenedorHistorias.addEventListener('scroll', actualizarFlechasScroll);
});
