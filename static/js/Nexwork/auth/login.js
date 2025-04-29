document.addEventListener("DOMContentLoaded", function () { 
    const form = document.querySelector("form");
    const userInput = document.getElementById("inputUser");
    const passwordInput = document.getElementById("inputPassword");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const data = {
            usuario: userInput.value,
            password: passwordInput.value
        };

        fetch("/login_auth", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                showToast("success", result.message);
                setTimeout(() => {
                    window.location.href = "/";
                }, 1000);
            } else {
                showToast("error", result.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            showToast("error", "Ocurrió un error al procesar la solicitud");
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Función para mostrar toast
    function showToast(icon, message) {
        Swal.fire({
            toast: true,
            position: 'top-end',
            icon: icon,
            title: message,
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true
        });
    }
});
