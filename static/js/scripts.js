// Función para recargar solo la tabla de alertas
function refreshAlerts() {
    fetch(window.location.href)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newTable = doc.querySelector('.card-body');
            document.querySelector('.card-body').innerHTML = newTable.innerHTML;
        });
}

// Espera a que el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Confirma antes de limpiar
    document.getElementById('clearForm').addEventListener('submit', function(e) {
        if (!confirm('¿Estás seguro de eliminar todas las alertas?')) {
            e.preventDefault();
        }
    });
});

// Evento para el modal de limpieza
document.querySelector('form[action="/clear_alerts"]').addEventListener('submit', (e) => {
    e.preventDefault();
    fetch('/clear_alerts', { method: 'POST' })
        .then(() => {
            refreshAlerts();
            bootstrap.Modal.getInstance(document.getElementById('confirmModal')).hide();
        });
});