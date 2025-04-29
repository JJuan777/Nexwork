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
    
                    const yaDioLike = pub.ya_dio_like;
                    const likeIconClass = yaDioLike ? 'fa-solid text-primary' : 'fa-regular';
                    const likeTextClass = yaDioLike ? 'text-primary' : '';
    
                    const html = `
                        <div id="publicacion-${pub.id}" class="post mb-4 position-relative p-3 rounded shadow-sm bg-white">
                            <!-- Dropdown editar/eliminar -->
                            ${pub.es_mia ? `
                            <div class="dropdown position-absolute top-0 end-0 m-2">
                                <button class="btn btn-light btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="fa-solid fa-ellipsis"></i>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" onclick="activarEdicionInline(${pub.id})">Editar</a></li>
                                    <li><a class="dropdown-item text-danger" onclick="eliminarPublicacion(${pub.id})">Eliminar</a></li>
                                </ul>
                            </div>
                            ` : ''}
    
                            <!-- Autor -->
                            <div class="post-author d-flex align-items-center mb-2">
                                <img src="${imgProfileSrc}" class="img-profile" alt="User">
                                <div class="post-info ms-2">
                                    <h5 class="mb-0">
                                        <a href="/profile/view/${pub.autor_id}/" class="text-decoration-none text-dark">${pub.nombre}</a>
                                    </h5>
                                    <small class="text-muted d-block">Founder and CEO at Giva | Angel Investor</small>
                                    <small class="text-muted">${pub.fecha}</small>
                                </div>
                            </div>
    
                            <!-- Descripción -->
                            <p class="mt-2 descripcion-publicacion">${pub.descripcion}</p>
    
                            <!-- Imagen -->
                            ${pub.imagen ? `<img src="${pub.imagen}" class="post-img mt-2 img-fluid rounded" alt="Imagen de publicación">` : ''}
    
                            <!-- Likes y comentarios resumen -->
                            <div class="post-stats d-flex justify-content-between align-items-center mt-3 mb-2">
                                <div class="d-flex align-items-center gap-2">
                                    ${pub.likes_count > 0 ? `<i class="fa-solid fa-thumbs-up text-primary"></i>` : ''}
                                    ${pub.likes_count > 0 ? `
                                        <span class="liked-users">
                                            ${pub.usuarios_like.join(', ')}${pub.likes_count > 3 ? ` y ${pub.likes_count - 3} más les gusta esto` : ''}
                                        </span>` : ''}
                                </div>
                                <div>
                                    ${pub.comentarios_count > 0 ? `
                                       <span style="cursor:pointer;" onclick="toggleComentarios(${pub.id})">
                                            ${pub.comentarios_count} ${pub.comentarios_count === 1 ? 'comentario' : 'comentarios'}
                                        </span>` : ''}
                                </div>
                            </div>
    
                            <!-- Botones Like, Comment, Share -->
                            <div class="post-activity d-flex justify-content-around border-top pt-2 mt-2">
                                <div class="post-activity-link ${likeTextClass}" 
                                    id="btn-like-${pub.id}" 
                                    data-ya-dio-like="${yaDioLike}" 
                                    onclick="toggleLike(${pub.id}, this.getAttribute('data-ya-dio-like') === 'true')">
                                    <i class="${likeIconClass} fa-thumbs-up me-1"></i>&nbsp;Like
                                </div>
                                <div class="post-activity-link" onclick="mostrarFormularioComentario(${pub.id})">
                                    <i class="fa-regular fa-comment me-1"></i>&nbsp;Comment
                                </div>
                                <div class="post-activity-link"><i class="fa-solid fa-share me-1"></i>&nbsp;Share</div>
                                <div class="post-activity-link"><i class="fa-solid fa-paper-plane me-1"></i>&nbsp;Send</div>
                            </div>
    
                            <!-- Aquí los comentarios se cargarán -->
                            <div id="comentarios-publicacion-${pub.id}" class="comentarios-container border-top mt-3 pt-3"></div>
                        </div>
                    `;
    
                    contenedor.innerHTML += html;
                });
            });
    }

    function mostrarFormularioComentario(publicacionId) {
        const contenedor = document.getElementById(`comentarios-publicacion-${publicacionId}`);
        const formularioExistente = document.getElementById(`form-comentario-${publicacionId}`);
    
        // Si ya existe, lo removemos (toggle cerrar)
        if (formularioExistente) {
            formularioExistente.remove();
            return;
        }
    
        const formHtml = `
            <form id="form-comentario-${publicacionId}" class="mt-1 mb-3">
                <div class="d-flex gap-2">
                    <textarea class="form-control" id="textarea-comentario-${publicacionId}" rows="1" placeholder="Escribe un comentario..." style="resize: none;"></textarea>
                    <button type="submit" class="btn btn-primary">Publicar</button>
                </div>
            </form>
        `;
    
        contenedor.insertAdjacentHTML('afterbegin', formHtml);
    
        // Asociar evento submit
        const form = document.getElementById(`form-comentario-${publicacionId}`);
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            enviarComentario(publicacionId);
        });
    }    

    function enviarComentario(publicacionId) {
        const textarea = document.getElementById(`textarea-comentario-${publicacionId}`);
        const texto = textarea.value.trim();
    
        if (!texto) {
            alert('Escribe algo antes de publicar.');
            return;
        }
    
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        fetch(`/api/comentarios/nuevo/${publicacionId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ contenido: texto })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                textarea.value = '';
                cargarComentarios(publicacionId); // Recargar comentarios actualizados
            } else {
                alert('Error al publicar comentario.');
            }
        })
        .catch(err => {
            console.error('Error al enviar comentario:', err);
        });
    }    

    function toggleComentarios(publicacionId) {
        const contenedor = document.getElementById(`comentarios-publicacion-${publicacionId}`);
    
        if (contenedor.children.length > 0) {
            // Si hay comentarios, aplicar fade-out a cada uno
            Array.from(contenedor.children).forEach(child => {
                child.classList.remove('fade-in', 'show');
                child.classList.add('fade-out', 'hide');
            });
    
            // Después de la duración de la animación (300ms), vaciar el contenedor
            setTimeout(() => {
                contenedor.innerHTML = '';
            }, 300);
        } else {
            // Si está vacío, cargar comentarios
            cargarComentarios(publicacionId);
        }
    }     
    
    function cargarComentarios(publicacionId) {
        const contenedor = document.getElementById(`comentarios-publicacion-${publicacionId}`);
        
        contenedor.innerHTML = '<div class="text-muted">Cargando comentarios...</div>';
    
        fetch(`/api/comentarios/${publicacionId}/`)
            .then(res => res.json())
            .then(data => {
                contenedor.innerHTML = ''; 
    
                if (data.comentarios.length === 0) {
                    contenedor.innerHTML = '<div class="text-muted">No hay comentarios todavía.</div>';
                    return;
                }
    
                data.comentarios.forEach(comentario => {
                    const divComentario = document.createElement('div');
                    divComentario.classList.add('fade-in');  // Añadimos animación
                    divComentario.id = `comentario-${comentario.comentario_id}`;
                    divComentario.innerHTML = `
                        <div class="d-flex align-items-start mb-3">
                            <img src="${comentario.img_profile}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                            <div class="flex-grow-1">
                                <div class="bg-light rounded-3 p-2 position-relative">
                                    <div class="d-flex justify-content-between align-items-start mb-1">
                                        <div class="d-flex align-items-center">
                                            <strong class="me-2">${comentario.autor}</strong>
                                            <small class="text-muted">${comentario.fecha}</small>
                                        </div>

                                        ${comentario.es_mio ? `
                                        <div class="dropup">
                                        <button class="btn btn-sm btn-light" type="button" data-bs-toggle="dropdown">
                                            <i class="fa-solid fa-ellipsis-vertical"></i>
                                        </button>
                                        <ul class="dropdown-menu dropdown-menu-end" style="z-index: 9999;">
                                            <a class="dropdown-item"  onclick="activarEdicionComentario(${comentario.comentario_id}, '${comentario.contenido.replace(/'/g, "\\'")}')">Editar</a>
                                            <li><a class="dropdown-item text-danger" onclick="eliminarComentario(${comentario.comentario_id}, ${publicacionId})">Eliminar</a></li>
                                        </ul>
                                    </div>
                                        ` : ''}
                                    </div>
                                    <p class="mb-0">${comentario.contenido}</p>
                                </div>
                            </div>
                        </div>
                    `;
                    contenedor.appendChild(divComentario);
    
                    // Activar el fade-in de manera asíncrona
                    setTimeout(() => {
                        divComentario.classList.add('show');
                    }, 10);
                });
            })
            .catch(err => {
                console.error("Error cargando comentarios:", err);
                contenedor.innerHTML = '<div class="text-danger">Error al cargar comentarios.</div>';
            });
    }

    function activarEdicionComentario(comentarioId, contenido) {
        const comentarioDiv = document.getElementById(`comentario-${comentarioId}`);
        if (!comentarioDiv) {
            console.error('No se encontró el contenedor del comentario:', comentarioId);
            return;
        }
    
        comentarioDiv.innerHTML = `
            <textarea class="form-control mb-2" id="textarea-editar-comentario-${comentarioId}" rows="2">${contenido}</textarea>
            <div class="d-flex gap-2 mb-3">
                <button class="btn btn-sm btn-primary" onclick="guardarEdicionComentario(${comentarioId})">Guardar</button>
                <button class="btn btn-sm btn-secondary" onclick="cancelarEdicionComentario(${comentarioId}, '${contenido.replace(/'/g, "\\'")}')">Cancelar</button>
            </div>
        `;
    }
    
    function guardarEdicionComentario(comentarioId) {
        const textarea = document.getElementById(`textarea-editar-comentario-${comentarioId}`);
        const nuevoTexto = textarea.value.trim();
    
        if (!nuevoTexto) {
            alert('El comentario no puede estar vacío.');
            return;
        }
    
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        fetch(`/api/comentarios/editar/${comentarioId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ contenido: nuevoTexto })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                cargarComentarios(data.publicacion_id); // refresca comentarios
            } else {
                alert('Error al actualizar comentario.');
            }
        })
        .catch(err => {
            console.error("Error al editar comentario:", err);
        });
    }
    
    function cancelarEdicionComentario(comentarioId, contenidoOriginal) {
        cargarComentarios(obtenerPublicacionIdDesdeComentario(comentarioId)); // o recarga entera
    }    
    function eliminarComentario(comentarioId, publicacionId) {
        Swal.fire({
            title: '¿Eliminar comentario?',
            text: "Esta acción no se puede deshacer",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#aaa',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
                fetch(`/api/comentarios/eliminar/${comentarioId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Eliminar con animación
                        const comentarioDiv = document.getElementById(`comentario-${comentarioId}`);
                        comentarioDiv.classList.add('fade-out', 'hide');
                        setTimeout(() => comentarioDiv.remove(), 300);
                    } else {
                        Swal.fire('Error', 'No se pudo eliminar el comentario.', 'error');
                    }
                })
                .catch(err => {
                    console.error('Error al eliminar comentario:', err);
                    Swal.fire('Error', 'Ocurrió un error inesperado.', 'error');
                });
            }
        });
    }    
    
    function toggleLike(publicacionId, yaDioLike) {
        const method = yaDioLike ? 'DELETE' : 'POST';
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        fetch(`/api/likes/${publicacionId}/`, {
            method: method,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Solo actualizar el botón visualmente
                actualizarBotonLike(publicacionId, data.liked);
                cargarPublicaciones(window.usuarioId); // Recargar publicaciones para actualizar el contador de likes
            }
        })
        .catch(err => {
            console.error("Error al dar/quitar like:", err);
        });
    }
    
    function actualizarBotonLike(id, liked) {
        const likeBtn = document.getElementById(`btn-like-${id}`);
        const icon = likeBtn.querySelector('i');
    
        if (liked) {
            likeBtn.classList.add('text-primary');
            icon.classList.remove('fa-regular');
            icon.classList.add('fa-solid');
        } else {
            likeBtn.classList.remove('text-primary');
            icon.classList.remove('fa-solid');
            icon.classList.add('fa-regular');
        }
    
        // actualizar data-ya-dio-like
        likeBtn.setAttribute('data-ya-dio-like', liked ? 'true' : 'false');
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
                        cargarPublicaciones(window.usuarioId); // Recargar publicaciones
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
                cargarPublicaciones(window.usuarioId); // Recarga publicaciones después de guardar
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
                cargarPublicaciones(window.usuarioId); // Recarga publicaciones
            } else {
                alert("Error al publicar");
            }
        })
        .catch(err => {
            console.error("Error al enviar publicación:", err);
        });
    });


