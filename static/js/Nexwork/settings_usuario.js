document.addEventListener("DOMContentLoaded", function() {
    cargarAjustesUsuario();
});

// Cargar los datos del usuario en los campos
function cargarAjustesUsuario() {
    fetch("/api/user/settings/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("input-nombre").value = data.nombre;
            document.getElementById("input-apellidos").value = data.apellidos;
            document.getElementById("input-correo").value = data.correo;
            document.getElementById("input-usuario").value = data.usuario;
            document.getElementById("input-ocupacion").value = data.ocupacion;
        })
        .catch(error => {
            console.error("Error al cargar los ajustes del usuario:", error);
            mostrarToast("Error al cargar los datos del usuario.", "error");
        });
}

// Guardar los cambios del usuario
function guardarAjustesUsuario() {
    const nombre = document.getElementById("input-nombre").value.trim();
    const apellidos = document.getElementById("input-apellidos").value.trim();
    const correo = document.getElementById("input-correo").value.trim();
    const usuario = document.getElementById("input-usuario").value.trim();
    const ocupacion = document.getElementById("input-ocupacion").value.trim();

    // Validaciones de campos obligatorios
    if (!nombre || !apellidos || !correo || !usuario) {
        mostrarToast("Por favor, completa todos los campos obligatorios.", "warning");
        return;
    }

    // Validación de formato de correo
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexCorreo.test(correo)) {
        mostrarToast("El formato del correo electrónico no es válido.", "warning");
        return;
    }

    fetch("/api/user/settings/update/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            nombre: nombre,
            apellidos: apellidos,
            correo: correo,
            usuario: usuario,
            ocupacion: ocupacion
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarToast("Cambios guardados correctamente.", "success");
            setTimeout(() => {
                window.location.href = "/login";
            }, 1000); // Redirigir después de 1 segundo
        } else {
            mostrarToast(data.message || "Error al guardar los cambios.", "error");
        }
    })
    .catch(error => {
        console.error("Error al guardar los ajustes del usuario:", error);
        mostrarToast("Error al guardar los cambios.", "error");
    });
}

// Cambiar contraseña del usuario
function cambiarContrasena() {
    const nuevaContrasena = document.getElementById("input-password").value;
    const confirmarContrasena = document.getElementById("input-confirm-password").value;

    // Validaciones de contraseña
    if (nuevaContrasena.length < 8) {
        mostrarToast("La contraseña debe tener al menos 8 caracteres.", "warning");
        return;
    }

    if (nuevaContrasena !== confirmarContrasena) {
        mostrarToast("Las contraseñas no coinciden.", "warning");
        return;
    }

    fetch("/api/user/settings/update-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            nueva_contrasena: nuevaContrasena,
            confirmar_contrasena: confirmarContrasena
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarToast("Contraseña actualizada correctamente.", "success");
            document.getElementById("input-password").value = "";
            document.getElementById("input-confirm-password").value = "";
            setTimeout(() => {
                window.location.href = "/login";
            }, 1000); // Redirigir después de 1 segundo
        } else {
            mostrarToast(data.message || "Error al cambiar la contraseña.", "error");
        }
    })
    .catch(error => {
        console.error("Error al cambiar la contraseña:", error);
        mostrarToast("Error al cambiar la contraseña.", "error");
    });
}

// Función para mostrar notificaciones tipo toast (SweetAlert2)
function mostrarToast(mensaje, tipo) {
    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: tipo,
        title: mensaje,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    });
}

// Obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
