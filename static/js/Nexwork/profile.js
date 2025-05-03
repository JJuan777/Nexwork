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
