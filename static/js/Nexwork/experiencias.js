document.addEventListener('DOMContentLoaded', function () {
	const contenedor = document.getElementById('contenedor-experiencias');
	const usuarioId = window.usuarioId;
    const contenedoruser = document.getElementById('contenedor-perfil');
    const esPropietario = contenedoruser.dataset.esPropietario === 'true';


	fetch(`/api/usuario/${usuarioId}/experiencias/`)
		.then(res => res.json())
		.then(data => {
			const experiencias = data.experiencias;
			if (experiencias.length === 0) {
				contenedor.innerHTML = '<p class="text-muted">Sin experiencia registrada.</p>';
				return;
			}

			contenedor.innerHTML = '';
			experiencias.forEach((exp, index) => {
				const techs = exp.tecnologias.map(tag => `
					<span class="badge bg-primary-subtle text-primary mt-1 me-1">${tag}</span>
				`).join('');

				const descripcionHtml = exp.descripcion
					? `<p class="mt-2 text-muted small descripcion-text">${exp.descripcion}</p>`
					: `<p class="mt-2 text-muted small descripcion-text text-muted fst-italic">Sin descripción</p>`;

                    const botonesAccion = esPropietario ? `
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
					<div class="card shadow-sm rounded-3 mb-4 position-relative" data-index="${index}" data-id="${exp.id}">

						<!-- Botones de acción -->
                        ${botonesAccion}

						<div class="card-body">
							<!-- Puesto -->
							<h6 class="fw-semibold mb-0 puesto-text">${exp.puesto}</h6>
							<input type="text" class="form-control form-control-sm mb-2 d-none puesto-input" value="${exp.puesto}">

							<!-- Empresa y fechas -->
							<small class="text-muted d-block mb-2 empresa-text">
								${exp.empresa} · ${exp.fecha_inicio} - ${exp.fecha_fin}
							</small>
							<div class="d-none mb-2 empresa-inputs">
								<input type="text" class="form-control form-control-sm mb-1 empresa-input" value="${exp.empresa}">
								<div class="d-flex gap-2">
                                <input type="date" class="form-control form-control-sm fecha-inicio-input" value="${convertToInputDate(exp.fecha_inicio)}">
                                <input type="date" class="form-control form-control-sm fecha-fin-input" value="${exp.fecha_fin !== 'Presente' ? convertToInputYear(exp.fecha_fin) : ''}">
                            </div>

						</div>

							<!-- Tecnologías -->
							<div class="tecnologias-text mb-2">${techs}</div>
							<input type="text" class="form-control form-control-sm d-none tecnologias-input" value="${exp.tecnologias.join(', ')}">
							<small class="text-muted d-none tecnologia-ayuda">Separadas por comas. Máximo 5 tecnologías.</small>

							<!-- Descripción -->
							<div class="descripcion-section">
								${descripcionHtml}
								<textarea class="form-control form-control-sm descripcion-input d-none">${exp.descripcion || ''}</textarea>
							</div>
                            <!-- Botones de acción -->
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

					// Mostrar campos editables
					card.querySelector('.puesto-text').classList.add('d-none');
					card.querySelector('.puesto-input').classList.remove('d-none');

					card.querySelector('.empresa-text').classList.add('d-none');
					card.querySelector('.empresa-inputs').classList.remove('d-none');

					card.querySelector('.tecnologias-text').classList.add('d-none');
					card.querySelector('.tecnologias-input').classList.remove('d-none');
					card.querySelector('.tecnologia-ayuda').classList.remove('d-none');

					card.querySelector('.descripcion-text')?.classList.add('d-none');
					card.querySelector('.descripcion-input').classList.remove('d-none');

					card.querySelector('.guardar-btn').classList.remove('d-none');
                    card.querySelector('.cancelar-btn').classList.remove('d-none');
					btn.disabled = true;
				});
			});

            document.addEventListener('click', function (e) {
                if (e.target.closest('.cancelar-btn')) {
                    const card = e.target.closest('.card');
            
                    // Restaurar campos
                    card.querySelector('.puesto-input').value = card.dataset.originalPuesto;
                    card.querySelector('.empresa-input').value = card.dataset.originalEmpresa;
                    card.querySelector('.fecha-inicio-input').value = card.dataset.originalFechaInicio;
                    card.querySelector('.fecha-fin-input').value = card.dataset.originalFechaFin;
                    card.querySelector('.tecnologias-input').value = card.dataset.originalTecnologias;
                    card.querySelector('.descripcion-input').value = card.dataset.originalDescripcion;
            
                    // Revertir vista a modo solo lectura
                    card.querySelector('.puesto-text').classList.remove('d-none');
                    card.querySelector('.puesto-input').classList.add('d-none');
            
                    card.querySelector('.empresa-text').classList.remove('d-none');
                    card.querySelector('.empresa-inputs').classList.add('d-none');
            
                    card.querySelector('.tecnologias-text').classList.remove('d-none');
                    card.querySelector('.tecnologias-input').classList.add('d-none');
                    card.querySelector('.tecnologia-ayuda').classList.add('d-none');
            
                    card.querySelector('.descripcion-input').classList.add('d-none');
                    card.querySelector('.descripcion-text')?.classList.remove('d-none');
            
                    card.querySelector('.guardar-btn').classList.add('d-none');
                    card.querySelector('.cancelar-btn').classList.add('d-none');
                    card.querySelector('.edit-btn').disabled = false;
                }
            });
            

			// Guardar cambios (solo lógica frontend por ahora)
			document.addEventListener('click', function (e) {
				if (e.target.closest('.guardar-btn')) {
					const card = e.target.closest('.card');
					const tecnologiasInput = card.querySelector('.tecnologias-input').value;
					const tecnologias = tecnologiasInput.split(',').map(tag => tag.trim()).filter(Boolean);

					if (tecnologias.length > 5) {
						alert("Solo puedes ingresar hasta 5 tecnologías.");
						return;
					}

					const experienciaId = card.dataset.id;  // necesitas guardar este en data-id

                    fetch(`/api/experiencia/${experienciaId}/actualizar/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            puesto: card.querySelector('.puesto-input').value,
                            empresa: card.querySelector('.empresa-input').value,
                            fecha_inicio: card.querySelector('.fecha-inicio-input').value,
                            fecha_fin: card.querySelector('.fecha-fin-input').value || null,
                            tecnologias,
                            descripcion: card.querySelector('.descripcion-input').value
                        })                        
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire({
                                icon: 'success',
                                title: '¡Éxito!',
                                text: 'Cambios guardados correctamente.',
                                confirmButtonColor: '#3085d6'
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Error al guardar',
                                text: data.error || 'Ocurrió un error desconocido.',
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
				}
			});
		})
		.catch(err => {
			console.error(err);
			contenedor.innerHTML = '<p class="text-danger">Error al cargar experiencias.</p>';
		});

        function convertToInputDate(fechaTexto) {
            // Convierte "May 2023" a "2023-05-01"
            const meses = {
                Jan: '01', Feb: '02', Mar: '03', Apr: '04', May: '05', Jun: '06',
                Jul: '07', Aug: '08', Sep: '09', Oct: '10', Nov: '11', Dec: '12'
            };
            const partes = fechaTexto.split(' ');
            if (partes.length !== 2) return '';
            return `${partes[1]}-${meses[partes[0]]}-01`;
        }
        
        function convertToInputYear(añoTexto) {
            // Convierte "2023" a "2023-12-31"
            return /^\d{4}$/.test(añoTexto) ? `${añoTexto}-12-31` : '';
        }
        
});

document.getElementById('form-nueva-experiencia').addEventListener('submit', function (e) {
	e.preventDefault();

	const form = e.target;
	const tecnologiasRaw = form.tecnologias.value.split(',').map(t => t.trim()).filter(Boolean);

	if (tecnologiasRaw.length > 5) {
		Swal.fire({
			icon: 'warning',
			title: 'Demasiadas tecnologías',
			text: 'Solo puedes ingresar hasta 5 tecnologías.',
		});
		return;
	}

	const payload = {
		puesto: form.puesto.value,
		empresa: form.empresa.value,
		fecha_inicio: form.fecha_inicio.value,
		fecha_fin: form.fecha_fin.value || null,
		tecnologias: tecnologiasRaw,
		descripcion: form.descripcion.value
	};

	fetch(`/api/usuario/${window.usuarioId}/experiencias/nueva/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(payload)
	})
	.then(res => res.json())
	.then(data => {
		if (data.success) {
			Swal.fire({
				icon: 'success',
				title: 'Agregado correctamente',
				showConfirmButton: false,
				timer: 1500
			}).then(() => {
				// Cierra modal y recarga
				const modal = bootstrap.Modal.getInstance(document.getElementById('modalNuevaExperiencia'));
				modal.hide();
				form.reset();
				location.reload(); // o volver a llamar fetch()
			});
		} else {
			Swal.fire({
				icon: 'error',
				title: 'Error al guardar',
				text: data.error || 'Ocurrió un error inesperado'
			});
		}
	})
	.catch(() => {
		Swal.fire({
			icon: 'error',
			title: 'Error de red',
			text: 'No se pudo enviar el formulario.'
		});
	});
});
document.addEventListener('click', function (e) {
	if (e.target.closest('.btn-delete')) {
		const card = e.target.closest('.card');
		const experienciaId = card.dataset.id;

		Swal.fire({
			icon: 'warning',
			title: '¿Eliminar experiencia?',
			text: 'Esta acción no se puede deshacer.',
			showCancelButton: true,
			confirmButtonText: 'Sí, eliminar',
			cancelButtonText: 'Cancelar',
			confirmButtonColor: '#d33'
		}).then((result) => {
			if (result.isConfirmed) {
				fetch(`/api/experiencia/${experienciaId}/eliminar/`, {
					method: 'DELETE'
				})
				.then(res => res.json())
				.then(data => {
					if (data.success) {
						card.remove();
						Swal.fire({
							icon: 'success',
							title: 'Eliminado',
							text: 'La experiencia fue eliminada correctamente.',
							timer: 1500,
							showConfirmButton: false
						});
					} else {
						Swal.fire({
							icon: 'error',
							title: 'Error al eliminar',
							text: data.error || 'Error desconocido'
						});
					}
				})
				.catch(() => {
					Swal.fire({
						icon: 'error',
						title: 'Error de red',
						text: 'No se pudo conectar al servidor.'
					});
				});
			}
		});
	}
});
