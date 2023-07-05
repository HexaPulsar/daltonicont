$(document).ready(function() {
    function comprobarArchivo() {
        $.ajax({
            url: "/comprobar_archivo",
            type: "GET",
            success: function(response) {
                if (response.archivo_existe) {
                    window.location.href = "/result";
                } else {
                    setTimeout(comprobarArchivo, 5000);  // Realizar la comprobación cada segundo (1000 ms)
                }
            }
        });
    }

    comprobarArchivo();
});