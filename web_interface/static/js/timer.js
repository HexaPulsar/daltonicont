function actualizarTemporizador() {
    $.getJSON('/tiempo_restante', function(data) {
        var tiempoRestante = data.tiempo_restante;
        $('#tiempo-restante').text(tiempoRestante);
    });
}

actualizarTemporizador(); // Actualizar el temporizador inicialmente

setInterval(actualizarTemporizador, 1000); // Actualizar el temporizador cada segundo