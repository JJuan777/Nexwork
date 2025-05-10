document.addEventListener("DOMContentLoaded", function() {
    cargarConversaciones();
});

let amigoSeleccionado = null;

function cargarConversaciones() {
    fetch('/api/conversaciones/')
        .then(response => response.json())
        .then(data => {
            const listaAmigos = document.getElementById("amigos-list");
            listaAmigos.innerHTML = "";

            data.conversaciones.forEach(conv => {
                listaAmigos.innerHTML += `
                    <li class='list-group-item' onclick='seleccionarAmigo(${conv.id}, \"${conv.participantes.join(', ')}\")'>
                        ${conv.participantes.join(', ')} - ${conv.ultimo_mensaje}
                    </li>`;
            });
        });
}

function seleccionarAmigo(id, usuario) {
    amigoSeleccionado = id;
    document.getElementById("chat-messages").innerHTML = `<h5>Conversando con ${usuario}</h5>`;
    cargarMensajes(id);
}

function cargarMensajes(conversacionId) {
    fetch(`/api/mensajes/${conversacionId}/`)
        .then(response => response.json())
        .then(data => {
            const chatMessages = document.getElementById("chat-messages");
            chatMessages.innerHTML = "";

            data.mensajes.forEach(msg => {
                chatMessages.innerHTML += `
                    <div class='chat-message ${msg.es_mio ? 'sent' : 'received'}'>
                        ${msg.texto}
                    </div>`;
            });
        });
}

function enviarMensaje() {
    const mensaje = document.getElementById("mensaje-input").value.trim();
    if (amigoSeleccionado && mensaje) {
        // Mostrar de inmediato el mensaje como si fuera enviado
        const chatMessages = document.getElementById("chat-messages");
        chatMessages.innerHTML += `<div class='chat-message sent'>${mensaje}</div>`;
        document.getElementById("mensaje-input").value = "";

        // Enviar el mensaje al servidor
        fetch(`/api/mensajes/${amigoSeleccionado}/enviar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Asegúrate de tener configurado el CSRF token
            },
            body: JSON.stringify({ texto: mensaje })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert("Error al enviar el mensaje");
            }
        });
    }
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}