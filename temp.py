import os
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods_Face
import subprocess

app = Flask(__name__, static_folder='uploads')
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)

        # Initialize a STEP reader
        reader = STEPControl_Reader()

        # Read the file
        status = reader.ReadFile(filepath)

        if status == IFSelect_RetDone:  # check status
            reader.TransferRoots()
            shape = reader.OneShape()

        # Compute surface area
        props = GProp_GProps()
        face_exp = TopExp_Explorer(shape, TopAbs_FACE)

        while face_exp.More():
            face = topods_Face(face_exp.Current())
            brepgprop_SurfaceProperties(face, props)
            face_exp.Next()

        # Convert the STEP file to glTF using CAD Exchanger CLI
        gltf_filename = filename.rsplit('.', 1)[0] + '.gltf'
        gltf_filepath = os.path.join(app.config['UPLOAD_FOLDER'], gltf_filename)
        subprocess.run(["cadexchangercli", "-i", filepath, "-e", gltf_filepath])

        return redirect(url_for('display_model', surface_area=props.Mass(), gltf_filename=gltf_filename))

    return '''
    <!doctype html>
    <title>Upload a STEP File</title>
    <h1>Upload a STEP File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/display/<float:surface_area>/<string:gltf_filename>')
def display_model(surface_area, gltf_filename):
    return render_template('index.html', surface_area=surface_area, gltf_filename=gltf_filename)

if __name__ == "__main__":
    app.run(debug=True)
