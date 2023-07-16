from flask import Flask, render_template, redirect, url_for, send_file, abort, request, session, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import time
from wtforms.validators import InputRequired
import threading
import datetime
import backend.filter as filter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER_FILES'] = 'static/files/'
app.config['UPLOAD_FOLDER_IMAGES'] = 'static/images/'
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf']
app.config['USER_FILENAME'] = 'archivo' + app.config['UPLOAD_EXTENSIONS'][1]
app.config['TRANSFORMED_FILENAME'] = 'filtrado' + app.config['UPLOAD_EXTENSIONS'][1]

# Variables para actualizar el contador
tiempo_final = datetime.datetime.now()
final_time_set = False

# Crear carpeta /files donde van los archivos subidos y transformados.
def crear_carpeta(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print("Carpeta creada: ", ruta_carpeta)
    else:
        print("La carpeta ya existe: ", ruta_carpeta)

# Eliminar archivo modificado cuando se suba uno nuevo.
def borrar_archivo(ruta_archivo):
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
        print("Archivo borrado: ", ruta_archivo)
    else:
        print("El archivo no existe: ", ruta_archivo)

# Función de prueba
def write_text(filename, msg):
    full_path = os.path.join(os.getcwd(),'web_interface' ,'static', 'files',filename)
    time.sleep(3)
    msg = "".join(msg)
    with open(full_path, 'w') as f:
        f.write(msg)
        f.close()
    print("Modificado!")

# Clase para trabajar con archivos subidos por el usuarios
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

# Ruta de la página principal
@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    formulario = UploadFileForm()
    if formulario.validate_on_submit():
        file = formulario.file.data # First grab the file
        filename = file.filename # Get filename
        file_ext = os.path.splitext(filename)[1] # Get file extention
        if file_ext not in app.config['UPLOAD_EXTENSIONS']: # Check if file extention is allowed
            return render_template('not_pdf.html')
        app.config['DOWNLOAD_FILENAME'] = os.path.splitext(filename)[0] + "_modified" + file_ext
        ruta_carpeta = os.path.join(os.getcwd(),'web_interface', 'static', 'files')
        crear_carpeta(ruta_carpeta)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER_FILES'],secure_filename(app.config['USER_FILENAME']))) # Then save the file
        ruta_archivo = os.path.join(os.getcwd(),'web_interface' ,'static', 'files',app.config['DOWNLOAD_FILENAME'])
        borrar_archivo(ruta_archivo)
        return redirect(url_for('parameters')) # Go to param.html
    else:
        return render_template('index.html', file_form=formulario)

# Ruta para ver la página al subir un archivo que no es un pdf
@app.route('/failed')
def failed():
    return render_template('not_pdf.html')

# Ruta para ver la página "Acerca de nosotros"
@app.route('/about')
def about_us():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'Prototipo_HLD.png')
    return render_template('about.html', user_image = full_filename)

# Ruta para elegir los parámetros de la transformación
@app.route('/parameters', methods=['GET',"POST"])
def parameters():
    if request.method == 'POST':
        box = request.form.getlist('preferences') # All checkboxes values stored in array of strings
        print(box)
        session['msg'] = box
        return redirect(url_for('wait')) # Go to param.html
    else:
        return render_template('param.html')

# Ruta para ver la página de espera mientras se transforma el archivo
@app.route('/wait')
def wait():
    mensaje = session.get('msg')
    t = threading.Thread(target=filter.full_pipeline, args=(mensaje))
    t.start()
    return render_template('wait.html')

# Función para calcular el tiempo restante para que se transforme el archivo
@app.route('/tiempo_restante')
def tiempo_restante():
    global final_time_set
    global tiempo_final
    tiempo_actual = datetime.datetime.now().second
    if not final_time_set:
        transformation_time = 10
        tiempo_final = datetime.datetime.now() + datetime.timedelta(seconds=transformation_time)
        final_time_set = True
    tiempo_restante = tiempo_final.second - tiempo_actual
    return jsonify({'tiempo_restante': tiempo_restante})

# Función para comprobar si ya existe el archivo transformado
@app.route("/comprobar_archivo")
def comprobar_archivo():
    ruta_archivo = os.path.join(os.getcwd(),'web_interface' ,'static', 'files',app.config['TRANSFORMED_FILENAME'])  # Ruta completa al archivo que estás esperando
    if os.path.isfile(ruta_archivo):
        return jsonify({"archivo_existe": True})
    else:
        return jsonify({"archivo_existe": False})

# Ruta para ver la página para descargar el archivo transformado
@app.route('/result')
def result():
    global final_time_set
    global tiempo_final
    final_time_set = False
    tiempo_final = datetime.datetime.now()
    return render_template('result.html')

# Función para descargar el archivo
@app.route('/download') 
def download_file():
    return send_file(
        app.config['UPLOAD_FOLDER_FILES'] + app.config['TRANSFORMED_FILENAME'],
        download_name=app.config['DOWNLOAD_FILENAME'],
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)