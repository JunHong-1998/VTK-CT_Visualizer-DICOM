from vtkmodules.vtkRenderingCore import *
from vtkmodules.vtkInteractionStyle import *
from vtkmodules.vtkInteractionWidgets import *
from vtkmodules.vtkCommonTransforms import *
from vtkmodules.vtkIOImage import* #DICOMImageReader
from vtkmodules.vtkRenderingVolumeOpenGL2 import * #smartvolumemapper
from vtkmodules.vtkCommonDataModel import * # ImageData, Piecewise
from vtkmodules.vtkRenderingAnnotation import *
from vtkmodules.vtkFiltersCore import *
from vtkmodules.vtkInteractionWidgets import *
from vtkmodules.vtkRenderingVolume import *
from vtkmodules.vtkCommonCore import *
from vtkmodules.vtkInteractionStyle import*

class VTK:
    def __init__(self, file):
        self.colourVol = [[-750.0, 0.08, 0.05, 0.03],
                    [-350.0, 0.39, 0.25, 0.16],
                    [-200.0, 0.80, 0.80, 0.80],
                    [2750.0, 0.70, 0.70, 0.70],
                    [3000.0, 0.35, 0.35, 0.35]]
        self.colourSurf = [[500, 0.1, 0.3, 1, 0.3],
                           [1158, 0.1, 0.6, 1, 0.5],
                           [2750, 0.1, 1, 1, 1]]
        self.reader(file)
        self.rendering()

    def reader(self, file):
        self.imageData = vtkImageData()
        reader = vtkDICOMImageReader()
        reader.SetDirectoryName(file)
        reader.SetDataScalarTypeToUnsignedShort()
        reader.UpdateWholeExtent()
        reader.Update()
        # self.r = reader.GetOutput().GetPointData().GetScalars().GetRange()
        self.imageData.ShallowCopy(reader.GetOutput())



    def rendering(self):
        self.renderer = vtkRenderer()
        self.volumeSetting()
        self.surfaceSetting()
        self.renderer.AddVolume(self.volume)

    def surfaceUpdate(self, flag=None):
        if flag:
            surface = self.colourSurf[flag]

        else:
            surface = self.colourSurf[-1]
            self.actor_surf.append(vtkActor())
        lut = vtkColorTransferFunction()
        lut.SetColorSpaceToHSV()
        lut.AddHSVPoint(surface[0], surface[1], surface[2], surface[3])

        contours = vtkFlyingEdges3D()
        contours.SetInputData(self.imageData)
        contours.ComputeNormalsOn()

        contours.SetValue(0, surface[0])

        mapper = vtkDataSetMapper()
        mapper.SetInputConnection(contours.GetOutputPort())
        mapper.SetLookupTable(lut)

        if flag:
            self.actor_surf[flag].SetMapper(mapper)
            self.actor_surf[flag].GetProperty().SetOpacity(surface[4])

        else:
            self.actor_surf[-1].SetMapper(mapper)
            self.actor_surf[-1].GetProperty().SetOpacity(surface[4])

    def surfaceSetting(self):
        self.actor_surf = []

        for i, surface in enumerate (self.colourSurf):
            self.actor_surf.append(vtkActor())
            lut = vtkColorTransferFunction()
            lut.SetColorSpaceToHSV()
            lut.AddHSVPoint(surface[0], surface[1], surface[2], surface[3])

            contours = vtkFlyingEdges3D()
            contours.SetInputData(self.imageData)
            contours.ComputeNormalsOn()

            contours.SetValue(0, surface[0])

            mapper = vtkDataSetMapper()
            mapper.SetInputConnection(contours.GetOutputPort())
            mapper.SetLookupTable(lut)
            # mapper.ImmediateModeRenderingOff()

            # self.actor_surf[i] = vtkActor()
            self.actor_surf[i].SetMapper(mapper)
            self.actor_surf[i].GetProperty().SetOpacity(surface[4])


    def lighting(self, color, diffColor, ambColor, specColor, Pos, FocalPos, intens):
        self.light = vtkLight()
        self.light.SetPosition(Pos[0].value(), Pos[1].value(), Pos[2].value())
        self.light.SetFocalPoint(FocalPos[0].value(), FocalPos[1].value(), FocalPos[2].value())
        self.light.SetColor(color[0].value(), color[1].value(), color[2].value())
        self.light.SetDiffuseColor(diffColor[0].value(), diffColor[1].value(), diffColor[2].value())
        self.light.SetAmbientColor(ambColor[0].value(), ambColor[1].value(), ambColor[2].value())
        self.light.SetSpecularColor(specColor[0].value(), specColor[1].value(), specColor[2].value())
        self.light.SetLightTypeToSceneLight()
        self.light.SetIntensity(intens[0].value())
        self.renderer.AddLight(self.light)

    def volumeUpdateColor(self):
        colour = self.color()
        self.volumeProperty.SetColor(colour)
        self.volume.SetProperty(self.volumeProperty)

    def volumeSetting(self):
        self.volume = vtkVolume()
        volumeMapper = self.volMapper()
        self.volume.SetMapper(volumeMapper)
        self.volProperty()
        self.volume.SetProperty(self.volumeProperty)
        # return volume

    def volMapper(self):
        volumeMapper = vtkSmartVolumeMapper()
        volumeMapper.SetBlendModeToComposite()
        volumeMapper.SetRequestedRenderModeToGPU()
        volumeMapper.SetInputData(self.imageData)
        return volumeMapper

    def volProperty(self):
        self.volumeProperty = vtkVolumeProperty()
        self.volumeProperty.ShadeOn()
        self.volumeProperty.SetInterpolationTypeToLinear()
        self.volumeProperty.SetAmbient(0.1)
        self.volumeProperty.SetDiffuse(0.9)
        self.volumeProperty.SetSpecular(0.2)
        self.volumeProperty.SetSpecularPower(10.0)
        gradientOpacity = self.grad_Opacity()
        self.volumeProperty.SetGradientOpacity(gradientOpacity)
        scalarOpacity = self.scal_Opacity()
        self.volumeProperty.SetScalarOpacity(scalarOpacity)
        colour = self.color()
        self.volumeProperty.SetColor(colour)
        # return self.volumeProperty

    def grad_Opacity(self):
        gradientOpacity = vtkPiecewiseFunction()
        gradientOpacity.AddPoint(0.0, 0.0)
        gradientOpacity.AddPoint(2000.0, 1.0)
        return gradientOpacity

    def scal_Opacity(self):
        scalarOpacity = vtkPiecewiseFunction()
        scalarOpacity.AddPoint(-800.0, 0.0)
        scalarOpacity.AddPoint(-750.0, 1.0)
        scalarOpacity.AddPoint(-350.0, 1.0)
        scalarOpacity.AddPoint(-300.0, 0.0)
        scalarOpacity.AddPoint(-200.0, 0.0)
        scalarOpacity.AddPoint(-100.0, 1.0)
        scalarOpacity.AddPoint(1000.0, 0.0)
        scalarOpacity.AddPoint(2750.0, 0.0)
        scalarOpacity.AddPoint(2976.0, 1.0)
        scalarOpacity.AddPoint(3000.0, 0.0)
        return scalarOpacity

    def color(self):
        colour = vtkColorTransferFunction()
        for color in self.colourVol:
            colour.AddRGBPoint(color[0], color[1], color[2], color[3])
        return colour

    def box(self, interactor):
        self.boxWidget = vtkBoxWidget()
        self.boxWidget.SetInteractor(interactor)
        self.boxWidget.SetProp3D(self.volume)
        # self.boxWidget.SetCurrentRenderer(self.renderer)
        self.boxWidget.SetPlaceFactor(1.25)  # Make the box 1.25x larger than the actor
        self.boxWidget.PlaceWidget()
        # self.boxWidget.AddObserver('InteractionEvent', self.boxCallback)
        # boxWidget.Off()

    def axes_setup(self, iren):
        self.axesActor = vtkAxesActor()
        self.axesActor.SetTotalLength(300, 300, 300)  # Set the total length of the axes in 3 dimensions
        self.axesActor.SetShaftType(0)
        self.axesActor.SetCylinderRadius(0.02)
        self.axesActor.SetAxisLabels(1)       # Enable:1/disable:0 drawing the axis labels
        self.axesActor.GetXAxisCaptionActor2D().SetWidth(0.03)
        self.axesActor.GetYAxisCaptionActor2D().SetWidth(0.03)
        self.axesActor.GetZAxisCaptionActor2D().SetWidth(0.03)

        self.axes = vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(self.axesActor)
        self.axes.SetInteractor(iren)
        self.axes.SetEnabled(1)
        self.axes.InteractiveOff()
        self.renderer.ResetCamera()

