function abrirPostulacion(trabajoId, titulo) {
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