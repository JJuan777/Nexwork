function enviarSolicitudAmistad(paraUsuarioId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/api/solicitudes/enviar/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ para_usuario_id: paraUsuarioId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Mostrar toast
            Swal.fire({
                toast: true,
                position: 'top-end',
                icon: 'success',
                title: 'Solicitud enviada con éxito',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true
            });

            // Reemplazar botón sin recargar
            const btn = document.getElementById('btn-contacto');
            if (btn) {
                btn.className = 'btn btn-outline-warning rounded-pill px-4 py-2 shadow';
                btn.disabled = true;
                btn.innerHTML = '<i class="fa-solid fa-clock me-2"></i> Pendiente';
            }
        } else {
            Swal.fire({
                toast: true,
                position: 'top-end',
                icon: 'error',
                title: data.message || 'No se pudo enviar la solicitud',
                showConfirmButton: false,
                timer: 2500,
                timerProgressBar: true
            });
        }
    })
    .catch(err => {
        console.error("Error al enviar solicitud:", err);
        Swal.fire({
            toast: true,
            position: 'top-end',
            icon: 'error',
            title: 'Ocurrió un error inesperado',
            showConfirmButton: false,
            timer: 2500,
            timerProgressBar: true
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const imgContainer = document.getElementById('profile-img-wrapper');
    const fileInput = document.getElementById('input-img-profile');
    const imgElement = document.getElementById('img-profile');

    const usuarioId = window.usuarioId;  // Asegúrate que esté disponible

    imgContainer.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        const file = this.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('imagen', file);

        fetch(`/api/usuario/${usuarioId}/actualizar_img/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                imgElement.src = data.img_profile;
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error al subir imagen:', error);
            alert('Error al subir la imagen');
        });
    });

    // Obtener CSRF desde cookie
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                return c.substring(name.length + 1);
            }
        }
        return '';
    }
});

const bannerBtn = document.getElementById('btn-banner-upload');
const bannerInput = document.getElementById('input-banner-profile');
const bannerImg = document.getElementById('img-banner');

const usuarioId = window.usuarioId;  // Asegúrate que esté disponible en el template

// Al hacer clic en el ícono
bannerBtn.addEventListener('click', () => {
    bannerInput.click();
});

// Al seleccionar imagen
bannerInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('imagen', file);

    fetch(`/api/usuario/${usuarioId}/actualizar_banner/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            bannerImg.src = data.banner_profile;
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error al subir banner:', error);
        alert('Error al subir el banner');
    });
});

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name + '=')) {
            return c.substring(name.length + 1);
        }
    }
    return '';
}
function eliminarContacto(usuarioId) {
    Swal.fire({
        title: '¿Eliminar contacto?',
        text: 'Esta acción no se puede deshacer',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/api/eliminar-contacto/${usuarioId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: 'Eliminado',
                        text: 'El contacto ha sido eliminado exitosamente.',
                        icon: 'success',
                        timer: 2000,
                        showConfirmButton: false
                    }).then(() => location.reload());
                } else {
                    Swal.fire({
                        title: 'Error',
                        text: 'No se pudo eliminar el contacto.',
                        icon: 'error'
                    });
                }
            })
            .catch(() => {
                Swal.fire({
                    title: 'Error',
                    text: 'Ocurrió un problema al comunicarse con el servidor.',
                    icon: 'error'
                });
            });
        }
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
