document.addEventListener('DOMContentLoaded', function () {
	const contenedor = document.getElementById('contenedor-educacion');
	const usuarioId = window.usuarioId;
	const esPropietario = document.getElementById('contenedor-perfil').dataset.esPropietario === 'true';

	fetch(`/api/usuario/${usuarioId}/educacion/`)
		.then(res => res.json())
		.then(data => {
			const educaciones = data.educaciones;
			if (educaciones.length === 0) {
				contenedor.innerHTML = '<p class="text-muted">Sin educación registrada.</p>';
				return;
			}

			contenedor.innerHTML = '';
			educaciones.forEach((edu, index) => {
				const tags = edu.areas.map(area => `
					<span class="badge bg-secondary-subtle text-secondary mt-1 me-1">${area}</span>
				`).join('');

				const botones = esPropietario ? `
					<div class="position-absolute top-0 end-0 m-2 d-flex gap-1">
						<button class="btn btn-sm btn-light edit-btn" title="Editar">
							<i class="fa-solid fa-pen-to-square text-primary"></i>
						</button>
						<button class="btn btn-sm btn-light btn-delete" title="Eliminar">
							<i class="fa-solid fa-trash text-danger"></i>
						</button>
					</div>
				` : '';

				const html = `
					<div class="card shadow-sm rounded-3 mb-4 position-relative" data-index="${index}" data-id="${edu.id}">
						${botones}
						<div class="card-body">
							<h6 class="fw-semibold mb-0 titulo-text">${edu.titulo}</h6>
							<input type="text" class="form-control form-control-sm mb-2 d-none titulo-input" value="${edu.titulo}">

							<small class="text-muted d-block mb-2 institucion-text">${edu.institucion} · ${edu.fecha_inicio} - ${edu.fecha_fin}</small>
							<div class="d-none mb-2 institucion-inputs">
								<input type="text" class="form-control form-control-sm mb-1 institucion-input" value="${edu.institucion}">
								<div class="d-flex gap-2">
									<input type="date" class="form-control form-control-sm fecha-inicio-input" value="${edu.fecha_inicio}">
									<input type="date" class="form-control form-control-sm fecha-fin-input" value="${edu.fecha_fin !== 'Presente' ? edu.fecha_fin : ''}">
								</div>
							</div>

							<div class="areas-text mb-2">${tags}</div>
							<input type="text" class="form-control form-control-sm d-none areas-input" value="${edu.areas.join(', ')}">
							<small class="text-muted d-none areas-ayuda">Máx 5 áreas, separadas por coma.</small>

							<div class="d-flex justify-content-start gap-2 mt-3">
								<button class="btn btn-sm btn-outline-success d-none guardar-btn">
									<i class="fa-solid fa-check me-1"></i> Guardar cambios
								</button>
								<button class="btn btn-sm btn-outline-secondary d-none cancelar-btn" type="button">
									<i class="fa-solid fa-xmark me-1"></i> Cancelar
								</button>
							</div>
						</div>
					</div>
				`;
				contenedor.innerHTML += html;
			});

			document.querySelectorAll('.edit-btn').forEach((btn, index) => {
				btn.addEventListener('click', () => {
					const card = document.querySelector(`.card[data-index="${index}"]`);
					card.querySelector('.titulo-text').classList.add('d-none');
					card.querySelector('.titulo-input').classList.remove('d-none');

					card.querySelector('.institucion-text').classList.add('d-none');
					card.querySelector('.institucion-inputs').classList.remove('d-none');

					card.querySelector('.areas-text').classList.add('d-none');
					card.querySelector('.areas-input').classList.remove('d-none');
					card.querySelector('.areas-ayuda').classList.remove('d-none');

					card.querySelector('.guardar-btn').classList.remove('d-none');
					card.querySelector('.cancelar-btn').classList.remove('d-none');

					btn.disabled = true;
				});
			});

			document.querySelectorAll('.cancelar-btn').forEach((btn, index) => {
				btn.addEventListener('click', () => location.reload());
			});

			document.querySelectorAll('.guardar-btn').forEach((btn) => {
				btn.addEventListener('click', () => {
					const card = btn.closest('.card');
					const id = card.dataset.id;

					const areas = card.querySelector('.areas-input').value.split(',').map(a => a.trim()).filter(Boolean);
					if (areas.length > 5) {
						Swal.fire('Límite excedido', 'Solo se permiten hasta 5 áreas.', 'warning');
						return;
					}

					const payload = {
						titulo: card.querySelector('.titulo-input').value,
						institucion: card.querySelector('.institucion-input').value,
						fecha_inicio: card.querySelector('.fecha-inicio-input').value,
						fecha_fin: card.querySelector('.fecha-fin-input').value || null,
						areas
					};

					fetch(`/api/educacion/${id}/actualizar/`, {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify(payload)
					})
						.then(res => res.json())
						.then(data => {
							if (data.success) {
								Swal.fire('Guardado', 'Cambios guardados correctamente.', 'success').then(() => location.reload());
							} else {
								Swal.fire('Error', data.error || 'Error desconocido.', 'error');
							}
						})
						.catch(() => {
							Swal.fire('Error', 'No se pudo conectar con el servidor.', 'error');
						});
				});
			});

			document.querySelectorAll('.btn-delete').forEach(btn => {
				btn.addEventListener('click', () => {
					const card = btn.closest('.card');
					const id = card.dataset.id;

					Swal.fire({
						title: '¿Eliminar esta educación?',
						text: 'Esta acción no se puede deshacer.',
						icon: 'warning',
						showCancelButton: true,
						confirmButtonText: 'Sí, eliminar',
						cancelButtonText: 'Cancelar',
						confirmButtonColor: '#d33'
					}).then(result => {
						if (result.isConfirmed) {
							fetch(`/api/educacion/${id}/eliminar/`, { method: 'DELETE' })
								.then(res => res.json())
								.then(data => {
									if (data.success) {
										Swal.fire('Eliminado', 'La educación fue eliminada.', 'success').then(() => location.reload());
									} else {
										Swal.fire('Error', data.error || 'No se pudo eliminar.', 'error');
									}
								})
								.catch(() => {
									Swal.fire('Error', 'Fallo la conexión al servidor.', 'error');
								});
						}
					});
				});
			});
		})
		.catch(err => {
			console.error(err);
			contenedor.innerHTML = '<p class="text-danger">Error al cargar educación.</p>';
		});
});

document.getElementById('form-nueva-educacion').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = e.target;
    const data = {
        titulo: form.titulo.value,
        institucion: form.institucion.value,
        fecha_inicio: form.fecha_inicio.value,
        fecha_fin: form.fecha_fin.value || null,
        areas_estudio: form.areas_estudio.value
    };

    const areas = data.areas_estudio.split(',').map(tag => tag.trim()).filter(Boolean);
    if (areas.length > 5) {
        Swal.fire({
            icon: 'warning',
            title: 'Límite de áreas',
            text: 'Solo puedes ingresar hasta 5 áreas de estudio.',
            confirmButtonColor: '#d33'
        });
        return;
    }

    fetch(`/api/usuario/${window.usuarioId}/educacion/crear/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(resp => {
        if (resp.success) {
            Swal.fire({
                icon: 'success',
                title: '¡Agregado!',
                text: 'Educación guardada correctamente.',
                confirmButtonColor: '#3085d6'
            }).then(() => {
                location.reload();
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: resp.error || 'Error desconocido.',
                confirmButtonColor: '#d33'
            });
        }
    })
    .catch(() => {
        Swal.fire({
            icon: 'error',
            title: 'Error de red',
            text: 'No se pudo conectar al servidor.',
            confirmButtonColor: '#d33'
        });
    });
});
