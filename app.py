from OCC.Display.SimpleGui import init_display
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties, brepgprop_VolumeProperties
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods_Face, topods_Solid
from OCC.Core.gp import gp_Pnt
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Graphic3d import Graphic3d_MaterialAspect
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.AIS import AIS_ColoredShape
from OCC.Core.BRep import BRep_Tool
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Surface
from OCC.Core.GeomLProp import GeomLProp_SLProps
from OCC.Core.GeomAbs import GeomAbs_C0
from OCC.Core.gp import gp_Pnt
import numpy

# Initialize a STEP reader
reader = STEPControl_Reader()

# Read the file
status = reader.ReadFile('sample.stp')

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

surface_area = props.Mass()
print('Surface area:', surface_area)

# Compute object volume
props_vol = GProp_GProps()
solid_exp = TopExp_Explorer(shape, TopAbs_SOLID)

while solid_exp.More():
    solid = topods_Solid(solid_exp.Current())
    brepgprop_VolumeProperties(solid, props_vol)
    solid_exp.Next()

object_volume = props_vol.Mass()
print('Object volume:', object_volume)


def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

# Initialize the 3D display
display, start_display, add_menu, add_function_to_menu = init_display()

# Display the shape
display.DisplayShape(shape, update=True)

# Determine the bounding box of the shape
bbox = Bnd_Box()
brepbndlib_Add(shape, bbox)
xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

# Create a box
box_shape = BRepPrimAPI_MakeBox(gp_Pnt(xmin, ymin, zmin), gp_Pnt(xmax, ymax, zmax)).Shape()

# Compute box volume
props_vol_box = GProp_GProps()
box_solid = topods_Solid(box_shape)
brepgprop_VolumeProperties(box_solid, props_vol_box)
box_volume = props_vol_box.Mass()
print('Box volume:', box_volume)

# Compute volume difference
volume_difference = box_volume - object_volume
print('Volume difference:', volume_difference)

# Set the box to be semi-transparent
colored_ais_box = AIS_ColoredShape(box_shape)
colored_ais_box.SetTransparency(0.7)  # Set the transparency level here (0-1)
colored_ais_box.SetColor(Quantity_Color(1, 1, 1, Quantity_TOC_RGB))  # Change the color here if necessary


print('Surface area:', surface_area)
print('Object volume:', object_volume)
print('Box volume:', box_volume)
print('Volume difference:', volume_difference)

display.Context.Display(colored_ais_box, True)
start_display()

