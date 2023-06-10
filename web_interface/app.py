from flask import Flask, render_template, redirect, url_for, send_file, abort, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

def write_text(filename, msg):
    with open(filename, 'w') as f:
        f.write(msg)
        f.close()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER_FILES'] = 'static/files/'
app.config['UPLOAD_FOLDER_IMAGES'] = 'static/images/'
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.config['MODIFIED_FILENAME'] = 'modified' + app.config['UPLOAD_EXTENSIONS'][0]

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
            abort(400)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER_FILES'],secure_filename(app.config['MODIFIED_FILENAME']))) # Then save the file
        return redirect(url_for('parameters')) # Go to param.html
    else:
        return render_template('index.html', file_form=formulario)

@app.route('/parameters', methods=['GET',"POST"])
def parameters():
    if request.method == 'POST':
        box = request.form.getlist('preferences') # All checkboxes values stored in array of strings
        mensaje = "".join(box)
        directory = app.config['UPLOAD_FOLDER_FILES'] + app.config['MODIFIED_FILENAME'] # Get the saved file
        write_text(directory,mensaje) # Modify it with the function
        print("File has been uploaded and edited.")
        return redirect(url_for('result')) # Go to param.html
    else:
        return render_template('param.html')

@app.route('/about')
def about_us():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'Prototipo_HLD.png')
    return render_template('about.html', user_image = full_filename)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/download') 
def download_file():
    return send_file(
        app.config['UPLOAD_FOLDER_FILES'] + app.config['MODIFIED_FILENAME'],
        download_name=app.config['MODIFIED_FILENAME'],
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)