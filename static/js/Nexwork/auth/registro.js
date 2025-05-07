document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const password1 = formData.get('password1');
    const password2 = formData.get('password2');

    if (password1 !== password2) {
        alert('Las contraseñas no coinciden.');
        return;
    }

    fetch("/api/registro/", {
        method: 'POST',
        headers: { 'X-CSRFToken': '{{ csrf_token }}' },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            alert(data.error);
        }
    });
});