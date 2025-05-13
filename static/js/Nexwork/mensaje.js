document.addEventListener("DOMContentLoaded", function() {
    cargarConversaciones();
});

    let amigoSeleccionado = null;
    let chatSocket = null;

    function cargarConversaciones() {
        fetch('/api/conversaciones/')
            .then(response => response.json())
            .then(data => {
                const listaAmigos = document.getElementById("amigos-list");
                listaAmigos.innerHTML = "";
    
                data.conversaciones.forEach(conv => {
                    listaAmigos.innerHTML += `
                        <li class='list-group-item d-flex align-items-center' onclick='seleccionarAmigo(${conv.id}, \"${conv.participante_nombre}\")'>
                            <img src="${conv.img_url}" alt="Imagen" class="rounded-circle me-2" style="width: 40px; height: 40px; object-fit: cover;">
                            <div>
                                <strong>${conv.participante_nombre}</strong><br>
                                <small>${conv.ultimo_mensaje}</small>
                            </div>
                        </li>`;
                });
            });
    }    

    // Filtrar amigos y mostrar lista
    function filtrarAmigos() {
        const query = document.getElementById("buscar-amigos").value.trim();
        if (query.length === 0) {
            cargarConversaciones();
            return;
        }

        fetch(`/api/filtrar_amigos/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                const listaAmigos = document.getElementById("amigos-list");
                listaAmigos.innerHTML = "";

                data.amigos.slice(0, 5).forEach(amigo => {
                    listaAmigos.innerHTML += `
                        <li class='list-group-item d-flex align-items-center' 
                            onclick='seleccionarAmigo(${amigo.id_conversacion}, \"${amigo.nombre}\", ${amigo.id_amigo}, \"${amigo.img_url}\")'>
                            <img src="${amigo.img_url}" alt="Imagen de perfil" class="rounded-circle me-2" style="width: 40px; height: 40px; object-fit: cover;">
                            <div>${amigo.nombre}</div>
                        </li>`;
                });
            })
            .catch(error => console.error("Error al filtrar amigos:", error));
    }


    // Seleccionar amigo y gestionar la conversación
    function seleccionarAmigo(idConversacion, usuario, otroUsuarioId = null, imgUrl = null) {
        // Mostrar el encabezado y el área de mensajes
        document.getElementById("chat-header").classList.remove("d-none");
        document.getElementById("chat-messages").classList.remove("d-none");
        document.getElementById("chat-input-container").classList.remove("d-none");

        // Cambiar el texto del título de la conversación
        document.getElementById("titulo-conversacion").textContent = `${usuario}`;
        
        // Cambiar la imagen del usuario
        const imgAmigo = document.getElementById("img-amigo");
        if (imgUrl) {
            imgAmigo.src = imgUrl;
        } else {
            imgAmigo.src = "/static/images/Nexwork/default-profile.png";
        }

        // Verificar si la conversación existe
        if (idConversacion) {
            amigoSeleccionado = idConversacion;
            cargarMensajes(idConversacion);
            configurarWebSocket(idConversacion);
        } else if (otroUsuarioId) {
            crearConversacion(otroUsuarioId, usuario);
        } else {
            console.error("No se proporcionó un ID de conversación ni de usuario.");
        }
    }

    function cargarConversaciones() {
        fetch('/api/conversaciones/')
            .then(response => response.json())
            .then(data => {
                const listaAmigos = document.getElementById("amigos-list");
                listaAmigos.innerHTML = "";
    
                data.conversaciones.forEach(conv => {
                    listaAmigos.innerHTML += `
                        <li class='list-group-item d-flex align-items-center' 
                            onclick='seleccionarAmigo(${conv.id}, \"${conv.participante_nombre}\", null, \"${conv.img_url}\")'>
                            <img src="${conv.img_url}" alt="Imagen" class="rounded-circle me-2" style="width: 40px; height: 40px; object-fit: cover;">
                            <div>
                                <strong>${conv.participante_nombre}</strong><br>
                                <small>${conv.ultimo_mensaje}</small>
                            </div>
                        </li>`;
                });
            });
    }    

    // Cargar mensajes de la conversación
    function cargarMensajes(conversacionId) {
        fetch(`/api/mensajes/${conversacionId}/`)
            .then(response => response.json())
            .then(data => {
                const chatMessages = document.getElementById("chat-messages");
                chatMessages.innerHTML = "";

                data.mensajes.forEach(msg => {
                    mostrarMensaje(msg.texto, msg.es_mio);
                });
            })
            .catch(error => console.error("Error al cargar los mensajes:", error));
    }

    // Configurar WebSocket
    function configurarWebSocket(conversacionId) {
        if (chatSocket) {
            chatSocket.close();
        }

        chatSocket = new WebSocket(`ws://${window.location.host}/ws/socket-server/${conversacionId}/`);
        chatSocket.onmessage = function(e) {
            let data = JSON.parse(e.data);
            if (data.type === 'chat') {
                mostrarMensaje(data.message, data.es_mio);
            }
        };
    }

    // Función para configurar el WebSocket
    function configurarWebSocket(conversacionId) {
        if (chatSocket) {
            chatSocket.close();
        }

        chatSocket = new WebSocket(`ws://${window.location.host}/ws/socket-server/${conversacionId}/`);
        chatSocket.onmessage = function(e) {
            let data = JSON.parse(e.data);
            if (data.type === 'chat') {
                mostrarMensaje(data.message, data.es_mio);
            }
        };
    }


    function cargarMensajes(conversacionId) {
        fetch(`/api/mensajes/${conversacionId}/`)
            .then(response => response.json())
            .then(data => {

                data.mensajes.forEach(msg => {
                    mostrarMensaje(msg.texto, msg.es_mio);
                });
            });
    }

    function enviarMensaje() {
        const mensaje = document.getElementById("mensaje-input").value.trim();
        if (amigoSeleccionado && mensaje && chatSocket) {
            chatSocket.send(JSON.stringify({
                'message': mensaje
            }));
            document.getElementById("mensaje-input").value = "";
        }
    }

    function mostrarMensaje(texto, esMio) {
        const chatMessages = document.getElementById("chat-messages");
        const mensajeElemento = document.createElement("div");
        mensajeElemento.className = `chat-message ${esMio ? 'sent' : 'received'}`;
        mensajeElemento.textContent = texto;

        chatMessages.appendChild(mensajeElemento);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }