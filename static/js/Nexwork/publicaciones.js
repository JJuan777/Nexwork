    // Función para mostrar los placeholders de carga
    function mostrarPlaceholdersPublicaciones(cantidad = 3) {
        const contenedor = document.getElementById('contenedor-publicaciones');
        contenedor.innerHTML = '';

        for (let i = 0; i < cantidad; i++) {
            contenedor.innerHTML += `
                <div class="post mb-4 p-3 rounded shadow-sm">
                    <div class="d-flex align-items-center mb-3">
                        <div class="placeholder rounded-circle me-2" style="width: 50px; height: 50px;"></div>
                        <div class="flex-grow-1">
                            <div class="placeholder col-6 mb-2"></div>
                            <div class="placeholder col-4"></div>
                        </div>
                    </div>
                    <div class="placeholder col-12 mb-2" style="height: 20px;"></div>
                    <div class="placeholder col-10 mb-2" style="height: 20px;"></div>
                    <div class="placeholder col-8 mb-2" style="height: 20px;"></div>
                    <div class="placeholder col-12" style="height: 200px;"></div>
                </div>
            `;
        }
    }

    function cargarPublicaciones(id = null) {
        const contenedor = document.getElementById('contenedor-publicaciones');
        
    
        let url = '/api/publicaciones/';
        if (id !== null) {
            url += `?id=${id}`;
        }
    
        fetch(url)
            .then(res => res.json())
            .then(data => {
                const publicaciones = data.publicaciones;
                contenedor.innerHTML = '';
    
                publicaciones.forEach(pub => {
                    const imgProfileSrc = pub.img_profile.startsWith('data:image') ? pub.img_profile : `${pub.img_profile}`;
    
                    const html = `
                        <div id="publicacion-${pub.id}" class="post mb-4 position-relative">
                            <div class="dropdown position-absolute top-0 end-0 m-2">

                                ${pub.es_mia 
                                 ? ` <button class="btn btn-light btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="fa-solid fa-ellipsis"></i>
                                </button>

                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" onclick="activarEdicionInline(${pub.id})">Editar</a></li>
                                     <li><a class="dropdown-item text-danger" onclick="eliminarPublicacion(${pub.id})">Eliminar</a></li>
                                </ul>` : ''
                                    }
                            </div>

                            <div class="post-author d-flex align-items-center">
                                <img src="${imgProfileSrc}" class="img-profile" alt="User">
                                <div class="post-info ms-2">
                                    <h5 class="mb-0">
                                        <a href="/profile/view/${pub.autor_id}/" class="text-decoration-none text-dark">${pub.nombre}</a>
                                    </h5>
                                    <small class="text-muted d-block">Founder and CEO at Giva | Angel Investor</small>
                                    <small class="text-muted">${pub.fecha}</small>
                                </div>
                            </div>

                            <p class="mt-2 descripcion-publicacion">${pub.descripcion}</p>

                            ${pub.imagen 
                                ? `<img src="${pub.imagen}" class="post-img mt-2" alt="Imagen de publicación">`
                                : ''
                            }
    
                            <div class="post-stats d-flex justify-content-between align-items-center mt-3 mb-2">
                                <div class="d-flex align-items-center gap-2">
                                    <i class="fa-solid fa-thumbs-up text-primary"></i>
                                    <i class="fa-solid fa-heart text-danger"></i>
                                    <i class="fa-solid fa-hands-clapping text-warning"></i>
                                    <span class="liked-users">Adam Doe and 89 others</span>
                                </div>
                                <div>
                                    <span>22 comments · 40 shares</span>
                                </div>
                            </div>
    
                            <div class="post-activity d-flex justify-content-around border-top pt-2">
                                <div class="post-activity-link"><i class="fa-solid fa-thumbs-up me-1"></i>&nbsp;Like</div>
                                <div class="post-activity-link"><i class="fa-regular fa-comment me-1"></i>&nbsp;Comment</div>
                                <div class="post-activity-link"><i class="fa-solid fa-share me-1"></i>&nbsp;Share</div>
                                <div class="post-activity-link"><i class="fa-solid fa-paper-plane me-1"></i>&nbsp;Send</div>
                            </div>
                        </div>
                    `;
                    contenedor.innerHTML += html;
                });
            });
    }    

    // Función para eliminar publicación
    function eliminarPublicacion(publicacionId) {
        Swal.fire({
            title: '¿Eliminar publicación?',
            text: "Esta acción no se puede deshacer",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#d33',
            cancelButtonColor: '#6c757d'
        }).then((result) => {
            if (result.isConfirmed) {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
                fetch(`/api/publicaciones/${publicacionId}/eliminar/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            title: 'Eliminado',
                            text: 'La publicación ha sido eliminada.',
                            icon: 'success',
                            timer: 1000,
                            showConfirmButton: false
                        });
                        cargarPublicaciones(); // Recargar publicaciones
                    } else {
                        Swal.fire('Error', 'No se pudo eliminar la publicación.', 'error');
                    }
                })
                .catch(err => {
                    console.error("Error al eliminar publicación:", err);
                    Swal.fire('Error', 'Ocurrió un error inesperado.', 'error');
                });
            }
        });
    }    

    function activarEdicionInline(publicacionId) {
        const postDiv = document.getElementById(`publicacion-${publicacionId}`);
        const parrafo = postDiv.querySelector('.descripcion-publicacion');
        const imagenActual = postDiv.querySelector('.post-img')?.src || null;
        const descripcionActual = parrafo.textContent.trim();
    
        // Cambiar a formulario editable
        let htmlEdicion = `
            <textarea class="form-control mb-2" id="textarea-editar-${publicacionId}" rows="3">${descripcionActual}</textarea>
            <div class="mt-2 mb-2">
                <label class="form-label">Subir nueva imagen (opcional)</label>
                <input type="file" class="form-control mb-2" id="input-imagen-editar-${publicacionId}">
        `;
    
        if (imagenActual) {
            htmlEdicion += `
                <div class="form-check mt-2">
                    <input class="form-check-input" type="checkbox" id="checkbox-borrar-img-${publicacionId}">
                    <label class="form-check-label" for="checkbox-borrar-img-${publicacionId}">
                        Eliminar imagen actual
                    </label>
                </div>
            `;
        }
    
        htmlEdicion += `
            </div>
            <div class="d-flex gap-2 mt-2">
                <button class="btn btn-primary btn-sm" onclick="guardarEdicionInline(${publicacionId})">Guardar</button>
                <button class="btn btn-secondary btn-sm" onclick="cancelarEdicionInline(${publicacionId}, \`${descripcionActual.replace(/`/g, "\\`")}\`)">Cancelar</button>
            </div>
        `;
    
        parrafo.innerHTML = htmlEdicion;
    
        // Si hay imagen actual, ocultarla mientras editas
        if (imagenActual) {
            const imgElement = postDiv.querySelector('.post-img');
            if (imgElement) imgElement.classList.add('d-none');
        }
    }    

    function guardarEdicionInline(publicacionId) {
        const nuevaDescripcion = document.getElementById(`textarea-editar-${publicacionId}`).value.trim();
        const inputImagen = document.getElementById(`input-imagen-editar-${publicacionId}`);
        const checkboxBorrarImagen = document.getElementById(`checkbox-borrar-img-${publicacionId}`);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        const formData = new FormData();
        formData.append('descripcion', nuevaDescripcion);
    
        if (inputImagen && inputImagen.files.length > 0) {
            formData.append('imagen', inputImagen.files[0]);
        }
    
        if (checkboxBorrarImagen && checkboxBorrarImagen.checked) {
            formData.append('borrar_imagen', 'true');
        }
    
        fetch(`/api/publicaciones/${publicacionId}/editar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                cargarPublicaciones(); // Recarga publicaciones después de guardar
            } else {
                alert("Error al editar publicación");
            }
        })
        .catch(err => {
            console.error("Error al actualizar publicación:", err);
        });
    }    
    
    // Función para cancelar edición inline
    function cancelarEdicionInline(publicacionId, descripcionOriginal) {
        const postDiv = document.getElementById(`publicacion-${publicacionId}`);
        const parrafo = postDiv.querySelector('.descripcion-publicacion');
        const imgElement = postDiv.querySelector('.post-img');
    
        // Volver a mostrar el texto original
        parrafo.innerHTML = descripcionOriginal;
    
        // Volver a mostrar la imagen
        if (imgElement) imgElement.classList.remove('d-none');
    }    

    // cargarPublicaciones(); // Inicial

    // Enviar nueva publicación por AJAX
    const form = document.getElementById("form-publicacion");
    const textarea = form.querySelector("textarea");
    const imagenInput = form.querySelector('input[type="file"]');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append("descripcion", textarea.value);
        formData.append("es_publico", true); 
        if (imagenInput.files.length > 0) {
            formData.append("imagen", imagenInput.files[0]);
        }

        fetch("/api/publicaciones/nueva/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                textarea.value = "";
                imagenInput.value = "";
                cargarPublicaciones(); // Recarga publicaciones
            } else {
                alert("Error al publicar");
            }
        })
        .catch(err => {
            console.error("Error al enviar publicación:", err);
        });
    });


