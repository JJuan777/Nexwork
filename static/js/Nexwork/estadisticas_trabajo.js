function campoPorId(id) {
    if (id.includes('paises')) return 'pais';
    if (id.includes('ciudades')) return 'ciudad';
    if (id.includes('estados')) return 'estado';
    return '';
}

function renderEtiquetas(data, id) {
    const contenedor = document.getElementById(id);
    contenedor.innerHTML = '';
    const campo = campoPorId(id);

    data.forEach(item => {
        const valor = item[campo] || 'Desconocido';
        const span = document.createElement('span');
        span.className = 'etiqueta-lugar';
        span.textContent = `${valor} (${item.total})`;
        span.title = `Filtrar por ${campo}`;

        span.addEventListener('click', () => {
            const urlParams = new URLSearchParams();
            const fecha = document.getElementById('input-fecha').value;
            if (fecha) urlParams.append('fecha_inicio', fecha);

            if (campo === 'pais') urlParams.append('pais', valor);
            if (campo === 'estado') urlParams.append('estado', valor);
            if (campo === 'ciudad') urlParams.append('ciudad', valor);

            cargarGraficoFromParams(urlParams);
        });

        contenedor.appendChild(span);
    });
}

function cargarGraficoFromParams(params) {
    const url = new URL(`/api/vistas-por-pais/${trabajoId}/`, window.location.origin);
    for (const [key, value] of params.entries()) {
        url.searchParams.append(key, value);
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const labels = data.paises.map(item => item.pais || 'Desconocido');
            const datos = data.paises.map(item => item.total);

            const ctx = document.getElementById('graficoPaises').getContext('2d');
            if (window.graficoPaises instanceof Chart) window.graficoPaises.destroy();
            window.graficoPaises = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Cantidad de vistas',
                        data: datos,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

            renderEtiquetas(data.paises, 'etiquetas-paises');
            renderEtiquetas(data.estados, 'etiquetas-estados');
            renderEtiquetas(data.ciudades, 'etiquetas-ciudades');
        });
}

document.addEventListener("DOMContentLoaded", function () {
    cargarGraficoFromParams(new URLSearchParams());

    const form = document.getElementById('filtro-form');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const fecha = document.getElementById('input-fecha').value;
            const paises = document.getElementById('input-paises').value;

            const params = new URLSearchParams();
            if (fecha) params.append('fecha_inicio', fecha);
            if (paises) params.append('paises', paises);

            cargarGraficoFromParams(params);
        });
    }
});
