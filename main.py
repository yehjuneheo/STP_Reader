from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods_Face
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

        # Initialize a STEP reader
        reader = STEPControl_Reader()

        # Read the file
        status = reader.ReadFile(f.filename)

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

        return f'Surface area: {props.Mass()}'

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
