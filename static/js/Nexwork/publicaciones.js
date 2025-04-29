document.addEventListener("DOMContentLoaded", function () {

    // Cargar publicaciones
    function cargarPublicaciones() {
        fetch('/api/publicaciones/')
            .then(res => res.json())
            .then(data => {
                const publicaciones = data.publicaciones;
                const contenedor = document.getElementById('contenedor-publicaciones');
                contenedor.innerHTML = '';
    
                publicaciones.forEach(pub => {
                    const imgProfileSrc = pub.img_profile.startsWith('data:image') ? pub.img_profile : `/${pub.img_profile}`;

                    const html = `
                    <div class="post mb-4 position-relative">
                        <!-- Dropdown -->
                        <div class="dropdown position-absolute top-0 end-0 m-2">
                            <button class="btn btn-light btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="fa-solid fa-ellipsis"></i>
                            </button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="#">Editar</a></li>
                                <li><a class="dropdown-item" href="#">Eliminar</a></li>
                            </ul>
                        </div>

                        <div class="post-author d-flex align-items-center">
                            <img src="${imgProfileSrc}" class="img-profile" alt="User">
                            <div class="post-info ms-2">
                                <h5 class="mb-0">${pub.nombre}</h5>
                                <small class="text-muted d-block">Founder and CEO at Giva | Angel Investor</small>
                                <small class="text-muted">${pub.fecha}</small>
                            </div>
                        </div>

                        <p class="mt-2">${pub.descripcion}</p>

                        ${
                            pub.imagen 
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

    cargarPublicaciones(); // Inicial

    // Enviar nueva publicación por AJAX
    const form = document.getElementById("form-publicacion");
    const textarea = form.querySelector("textarea");
    const imagenInput = form.querySelector('input[type="file"]');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData();
        formData.append("descripcion", textarea.value);
        formData.append("es_publico", true); // o controlar según lógica
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

});
