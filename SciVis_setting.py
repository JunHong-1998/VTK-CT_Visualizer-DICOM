from SciVis_GUI import *
from SciVis_VTK import *
import os
import numpy as np

class Setting(QMainWindow):

    def __init__(self, parent, filepath):
        self.VTK = VTK(filepath)
        self.filename = filepath
        self.iren = None
        self.light = False
        self.spin_colorPointV = []
        self.spin_colorPointS = []
        self.tempColorPointV = self.spin_colorPointV
        self.tempColorPointS = self.spin_colorPointS
        self.renderMode = 0 #Volume, 1 - surface
        self.zoomy = 100
        QMainWindow.__init__(self, parent)
        self.UI = WidgetUI(self)
        self.spin_camZoom = [self.UI.spinBox(True, -500, 500, 100, 1, lambda: self.controlAction(33, True))]
        self.slid_camZoom = self.UI.SliderWidget(Qt.Horizontal, 100, -500, 500, lambda: self.controlAction(33, False))

    def setup3DAnnotation(self):
        self.VTK.box(self.iren)
        self.VTK.axes_setup(self.iren)

    def setupObserver(self):
        self.iren.RemoveAllObservers()
        self.VTK.boxWidget.AddObserver('InteractionEvent', self.boxCallback)

    def boxCallback(self, obj, event):
        transform = vtkTransform()
        obj.GetTransform(transform)
        obj.GetProp3D().SetUserTransform(transform)
        t = np.array([[transform.GetMatrix().GetElement(r, c) for c in range(4)] for r in range(4)])
        for i in range(3):
            self.spin_renderPosition[i].blockSignals(True)
            self.spin_renderScale[i].blockSignals(True)
            self.spin_renderPosition[i].setValue(t[i][3])
            self.spin_renderScale[i].setValue(t[i][i])
            self.spin_renderPosition[i].blockSignals(False)
            self.spin_renderScale[i].blockSignals(False)
        for actor in self.VTK.actor_surf:
            actor.SetUserTransform(transform)


    def setDefinedColor(self, flag):
        if flag:
            self.spin_colorPointV.clear()

            for i,color in enumerate(self.VTK.colourVol):
                self.spin_colorPointV.append([self.UI.spinBox(True, -10000, 10000, color[0], 1, lambda _, i=i: self.controlAction(27, i), width=50),
                                             self.UI.spinBox(False, 0, 1, color[1], 0.05, lambda _, i=i: self.controlAction(27, i), width=45),
                                             self.UI.spinBox(False, 0, 1, color[2], 0.05, lambda _, i=i: self.controlAction(27, i), width=45),
                                             self.UI.spinBox(False, 0, 1, color[3], 0.05, lambda _, i=i: self.controlAction(27, i), width=45)])
        else:
            self.spin_colorPointS.clear()

            for i,color in enumerate(self.VTK.colourSurf):
                self.spin_colorPointS.append([self.UI.spinBox(True, -10000, 10000, color[0], 1, lambda _, i=i: self.controlAction(27, i), width=50),
                                             self.UI.spinBox(False, 0, 1, color[1], 0.05, lambda _, i=i: self.controlAction(27, i), width=45),
                                             self.UI.spinBox(False, 0, 1, color[2], 0.05, lambda _, i=i: self.controlAction(27, i), width=45),
                                             self.UI.spinBox(False, 0, 1, color[3], 0.05, lambda _, i=i: self.controlAction(27, i), width=45),
                                              self.UI.spinBox(False, 0, 1, color[4], 0.05, lambda _, i=i: self.controlAction(27, i), width=45)])

    def setupCamera(self, cam):
        for i in range(3):
            self.spin_camViewUp[i].blockSignals(True)
            self.spin_camPosition[i].blockSignals(True)
            self.spin_camFocalPoint[i].blockSignals(True)
            self.spin_camViewUp[i].setValue(cam.GetViewUp()[i])
            self.spin_camPosition[i].setValue(cam.GetPosition()[i])
            self.spin_camFocalPoint[i].setValue(cam.GetFocalPoint()[i])
            self.spin_camViewUp[i].blockSignals(False)
            self.spin_camPosition[i].blockSignals(False)
            self.spin_camFocalPoint[i].blockSignals(False)
            if i<2:
                self.spin_camClip[i].blockSignals(True)
                self.spin_camClip[i].setValue(cam.GetClippingRange()[i])
                self.spin_camClip[i].blockSignals(False)

    def Content(self, tabby):

        tab_view = QScrollArea()
        tabby.addTab(tab_view, os.path.basename(self.filename))
        content_View = QWidget()
        tab_view.setWidget(content_View)
        ViewLay = QVBoxLayout(content_View)
        tab_view.setWidgetResizable(True)
        # Change
        btn_change = self.UI.textBtn("Change CT data", colorFG='darkblue', font=("Bold Tahoma", 12), height=30)
        ViewLay.addWidget(btn_change)
        # Annotation
        ViewLay.addWidget(self.UI.TextLabel("Setting", colorBG='darkblue', colorFG='white', align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=35))
        lay_3D = QHBoxLayout()
        btn1 = self.UI.checkbox("3D axis", lambda: self.controlAction(1, btn1), True)
        self.box3D = self.UI.checkbox("3D box (transform)", lambda: self.controlAction(2, self.box3D), False)
        self.spin_bgColor = [self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(11)),
                             self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(11)),
                             self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(11))]
        lay_3D.addWidget(btn1)
        lay_3D.addWidget(self.box3D)
        # 3D axis & Box
        ViewLay.addLayout(lay_3D)
        # BG_color
        ViewLay.addLayout(self.UI.MultiColOpt("Background Colour", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=("R", "G", "B"), optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_bgColor))
        # Render
        self.renderBtn = [self.UI.textBtn("Volume", lambda: self.controlAction(25, 0), colorBG='darkorange', colorFG='Black', font=("Bold Tahoma", 11), height=30, enable=False),
                             self.UI.textBtn("Surface", lambda: self.controlAction(25, 1), colorBG='lightgrey', font=("Bold Tahoma", 11), height=30)]
        ViewLay.addLayout(self.UI.MultiButOpt("Render", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, btn=self.renderBtn))
        # Transform
        text_POS = ["X", "Y", "Z"]
        ViewLay.addWidget(self.UI.TextLabel("Transformation", colorBG='darkblue', colorFG='white', align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=35))
        self.spin_renderPosition = [self.UI.spinBox(False, -100000, 100000, 0, 1, lambda: self.controlAction(28), width=70),
                                   self.UI.spinBox(False, -100000, 100000, 0, 1, lambda: self.controlAction(28), width=70),
                                   self.UI.spinBox(False, -100000, 100000, 0, 1, lambda: self.controlAction(28), width=70)]
        self.spin_renderRotation = [self.UI.spinBox(False, -360, 360, 0, 1, lambda: self.controlAction(29), width=70),
                                    self.UI.spinBox(False, -360, 360, 0, 1, lambda: self.controlAction(29), width=70),
                                    self.UI.spinBox(False, -360, 360, 0, 1, lambda: self.controlAction(29), width=70)]
        self.spin_renderScale = [self.UI.spinBox(False, 0, 100, 1, 0.1, lambda: self.controlAction(30), width=70),
                                    self.UI.spinBox(False, 0, 100, 1, 0.1, lambda: self.controlAction(30), width=70),
                                    self.UI.spinBox(False, 0, 100, 1, 0.1, lambda: self.controlAction(30), width=70)]

        ViewLay.addLayout(self.UI.MultiColOpt("Position", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_renderPosition))
        ViewLay.addLayout(self.UI.MultiColOpt("Rotation", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_renderRotation))
        ViewLay.addLayout(self.UI.MultiColOpt("Scaling", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_renderScale))
        ViewLay.addWidget(self.UI.textBtn("Reset", lambda: self.controlAction(31), colorFG='darkblue', font=("Bold Tahoma", 12), height=30))
        #Camera
        ViewLay.addWidget(self.UI.TextLabel("Camera", colorBG='darkblue', colorFG='white', align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=35))
        cam = self.VTK.renderer.GetActiveCamera()
        self.spin_camViewUp = [self.UI.spinBox(True, -1, 1, cam.GetViewUp()[0], 1, lambda: self.controlAction(3)),
                               self.UI.spinBox(True, -1, 1, cam.GetViewUp()[1], 1, lambda: self.controlAction(3)),
                               self.UI.spinBox(True, -1, 1, cam.GetViewUp()[2], 1, lambda: self.controlAction(3))]
        self.spin_camPosition = [self.UI.spinBox(True, -100000, 100000, cam.GetPosition()[0], 1, lambda: self.controlAction(4)),
                                 self.UI.spinBox(True, -100000, 100000, cam.GetPosition()[1], 1, lambda: self.controlAction(4)),
                                 self.UI.spinBox(True, -100000, 100000, cam.GetPosition()[2], 1, lambda: self.controlAction(4))]
        self.spin_camFocalPoint = [self.UI.spinBox(True, -100000, 100000, cam.GetFocalPoint()[0], 1, lambda: self.controlAction(5)),
                                   self.UI.spinBox(True, -100000, 100000, cam.GetFocalPoint()[1], 1, lambda: self.controlAction(5)),
                                   self.UI.spinBox(True, -100000, 100000, cam.GetFocalPoint()[2], 1, lambda: self.controlAction(5))]
        self.spin_camClip = [self.UI.spinBox(True, -100000, 100000, cam.GetClippingRange()[0], 1, lambda: self.controlAction(6)),
                             self.UI.spinBox(True, -100000, 100000, cam.GetClippingRange()[1], 1, lambda: self.controlAction(6))]
        self.spin_camAngle = [self.UI.spinBox(True, -360, 360, cam.GetViewAngle(), 1, lambda: self.controlAction(7, True))]
        self.slid_camAngle = self.UI.SliderWidget(Qt.Horizontal, cam.GetViewAngle(), -360,360, lambda: self.controlAction(7, False))
        self.spin_camAzimuth = [self.UI.spinBox(True, -360, 360, 0, 1, lambda: self.controlAction(8, True))]
        self.slid_camAzimuth = self.UI.SliderWidget(Qt.Horizontal, 0, -360, 360, lambda: self.controlAction(8, False))
        self.spin_camElevation = [self.UI.spinBox(True, -360, 360, 0, 1, lambda: self.controlAction(9, True))]
        self.slid_camElevation = self.UI.SliderWidget(Qt.Horizontal, 0, -360, 360, lambda: self.controlAction(9, False))
        self.spin_camRoll = [self.UI.spinBox(True, -360, 360, cam.GetRoll(), 1, lambda: self.controlAction(10, True))]
        self.slid_camRoll = self.UI.SliderWidget(Qt.Horizontal, cam.GetRoll(), -360, 360, lambda: self.controlAction(10, False))
        self.spin_camYaw = [self.UI.spinBox(False, -360, 360, 0, 0.05, lambda: self.controlAction(19, True))]
        self.slid_camYaw = self.UI.SliderWidget(Qt.Horizontal, 0, -36000, 36000, lambda: self.controlAction(19, False))
        # self.spin_camZoom = [self.UI.spinBox(True, -500, 500, 100, 1, lambda: self.controlAction(33, True))]
        # self.slid_camZoom = self.UI.SliderWidget(Qt.Horizontal, 100, -500, 500, lambda: self.controlAction(33, False))

        #cam_clip
        ViewLay.addLayout(self.UI.MultiColOpt("Clipping", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=("Near", "Far"), optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camClip))
        #Cam_ViewUp
        ViewLay.addLayout(self.UI.MultiColOpt("ViewUp", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camViewUp))
        # Cam_Position
        ViewLay.addLayout(self.UI.MultiColOpt("Position", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camPosition))
        # Cam_FocalPoint
        ViewLay.addLayout(self.UI.MultiColOpt("Focal Point", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camFocalPoint))
        # Cam_ViewAngle
        ViewLay.addLayout(self.UI.MultiColOpt("View Angle", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camAngle, slider=self.slid_camAngle))
        # Cam_Azimuth
        ViewLay.addLayout(self.UI.MultiColOpt("Azimuth", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camAzimuth, slider=self.slid_camAzimuth))
        # Cam_Elevation
        ViewLay.addLayout(self.UI.MultiColOpt("Elevation", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camElevation, slider=self.slid_camElevation))
        # Cam_Roll
        ViewLay.addLayout(self.UI.MultiColOpt("Roll", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camRoll, slider=self.slid_camRoll))
        # Cam_Yaw
        ViewLay.addLayout(self.UI.MultiColOpt("Yaw", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camYaw, slider=self.slid_camYaw))
        #Zoom
        ViewLay.addLayout(self.UI.MultiColOpt("Zoom", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_camZoom, slider=self.slid_camZoom))
        #Reset
        ViewLay.addWidget(self.UI.textBtn("Reset", lambda: self.controlAction(32), colorFG='darkblue', font=("Bold Tahoma", 12), height=30))

        # Lighting
        btn3 = self.UI.checkbox("                        Lighting", lambda : self.controlAction(12, btn3), False, colorBG='darkblue', colorFG='white', font=("Bold Tahoma", 12), height=35)
        # lightLay.addWidget(self.UI.TextLabel("Lighting", colorBG='darkblue', colorFG='white', align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=35))
        ViewLay.addWidget(btn3)
        self.spin_lightPosition = [self.UI.spinBox(True, -100000, 100000, cam.GetPosition()[0], 1, lambda: self.controlAction(17)),
                                   self.UI.spinBox(True, -100000, 100000, cam.GetPosition()[1], 1, lambda: self.controlAction(17)),
                                   self.UI.spinBox(True, -100000, 100000, cam.GetPosition()[2], 1, lambda: self.controlAction(17))]
        self.spin_lightFocalPoint = [self.UI.spinBox(True, -100000, 100000, cam.GetFocalPoint()[0], 1, lambda: self.controlAction(18)),
                                   self.UI.spinBox(True, -100000, 100000, cam.GetFocalPoint()[1], 1, lambda: self.controlAction(18)),
                                   self.UI.spinBox(True, -100000, 100000, cam.GetFocalPoint()[2], 1, lambda: self.controlAction(18))]
        self.spin_lightColor = [self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(13)),
                             self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(13)),
                             self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(13))]
        self.spin_lightDiffColor = [self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(14)),
                                  self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(14)),
                                  self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(14))]
        self.spin_lightAmbColor = [self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(15)),
                                    self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(15)),
                                    self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(15))]
        self.spin_lightSpecColor = [self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(16)),
                                   self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(16)),
                                   self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(16))]
        self.spin_lightIntens = [self.UI.spinBox(False, 0, 1, 0, 0.05, lambda: self.controlAction(20, True))]
        self.slid_lightIntens = self.UI.SliderWidget(Qt.Horizontal, 0, 0, 100, lambda: self.controlAction(20, False))
        # light_Position
        ViewLay.addLayout(self.UI.MultiColOpt("Position", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_lightPosition))
        # light_FocalPoint
        ViewLay.addLayout(self.UI.MultiColOpt("Focal Point", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=text_POS, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_lightFocalPoint))
        # light_color
        ViewLay.addLayout(self.UI.MultiColOpt("Colour", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=("R", "G", "B"), optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_lightColor))
        # light_Diffcolor
        ViewLay.addLayout(self.UI.MultiColOpt("Diffuse", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=("R", "G", "B"), optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_lightDiffColor))
        # light_Ambcolor
        ViewLay.addLayout(self.UI.MultiColOpt("Ambient", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=("R", "G", "B"), optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_lightAmbColor))
        # light_Speccolor
        ViewLay.addLayout(self.UI.MultiColOpt("Specular", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=("R", "G", "B"), optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_lightSpecColor))
        # light_intensity
        ViewLay.addLayout(self.UI.MultiColOpt("Intensity", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_lightIntens, slider=self.slid_lightIntens))
        # Property
        ViewLay.addWidget(self.UI.TextLabel("Property", colorBG='darkblue', colorFG='white', align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=35))
        self.spin_propDiff = [self.UI.spinBox(False, 0, 1, 0.9, 0.05, lambda: self.controlAction(21, True))]
        self.slid_propDiff = self.UI.SliderWidget(Qt.Horizontal, 90, 0, 100, lambda: self.controlAction(21, False))
        self.spin_propAmb = [self.UI.spinBox(False, 0, 1, 0.1, 0.05, lambda: self.controlAction(22, True))]
        self.slid_propAmb = self.UI.SliderWidget(Qt.Horizontal, 10, 0, 100, lambda: self.controlAction(22, False))
        self.spin_propSpec = [self.UI.spinBox(False, 0, 1, 0.2, 0.05, lambda: self.controlAction(23, True))]
        self.slid_propSpec = self.UI.SliderWidget(Qt.Horizontal, 20, 0, 100, lambda: self.controlAction(23, False))
        self.spin_propSpecP = [self.UI.spinBox(True, 0, 20, 10.0, 1, lambda: self.controlAction(24, True))]
        self.slid_propSpecP = self.UI.SliderWidget(Qt.Horizontal, 10, 0, 20, lambda: self.controlAction(24, False))
        # Prop_Diff
        ViewLay.addLayout(self.UI.MultiColOpt("Diffuse", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_propDiff, slider=self.slid_propDiff))
        # Prop_Amb
        ViewLay.addLayout(self.UI.MultiColOpt("Ambient", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_propAmb, slider=self.slid_propAmb))
        # Prop_Spec
        ViewLay.addLayout(self.UI.MultiColOpt("Specular", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_propSpec, slider=self.slid_propSpec))
        # Prop_SpecPower
        ViewLay.addLayout(self.UI.MultiColOpt("Specular Power", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=None, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=self.spin_propSpecP, slider=self.slid_propSpecP))
        # Colour
        ViewLay.addWidget(self.UI.TextLabel("Colour", colorBG='darkblue', colorFG='white', align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=35))
        self.pointRGBBtn = [self.UI.textBtn("Add", lambda: self.controlAction(26, True), font=("Bold Tahoma", 11), height=30),
                          self.UI.textBtn("Remove", lambda: self.controlAction(26, False), font=("Bold Tahoma", 11), height=30)]
        ViewLay.addLayout(self.UI.MultiButOpt("Colour Point Editing", subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, btn=self.pointRGBBtn))
        self.colorLay = QVBoxLayout()
        self.colorWidget = []

        self.setupColourWidget(True)
        ViewLay.addLayout(self.colorLay)

        return btn_change

    def setupColourWidget(self, flag, default=True):

        if flag:
            textOPT = ['X', 'R', 'G', 'B']
            colorOPT = self.spin_colorPointV
        else:
            textOPT = ['X', 'H', 'S', 'V', 'A']
            colorOPT = self.spin_colorPointS
        if default:
            if self.colorWidget:
                for color in self.colorWidget:
                    color.setParent(None)
            self.colorWidget.clear()
            self.setDefinedColor(flag)
            for i, spinner in enumerate (colorOPT):
                self.colorWidget.append(self.UI.MultiColOptWidget("Point {}".format(i+1), subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=textOPT, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=spinner))
                self.colorLay.addWidget(self.colorWidget[i])
        else:
            print(len(colorOPT))
            if flag:
                colorOPT.append([self.UI.spinBox(True, -10000, 10000, 0, 1, lambda: self.controlAction(27)),
                                              self.UI.spinBox(False, 0, 1, 1, 0.05, lambda: self.controlAction(27)),
                                              self.UI.spinBox(False, 0, 1, 1, 0.05, lambda: self.controlAction(27)),
                                              self.UI.spinBox(False, 0, 1, 1, 0.05, lambda: self.controlAction(27))])
            else:
                colorOPT.append([self.UI.spinBox(True, -10000, 10000, 0, 1, lambda: self.controlAction(27)),
                                              self.UI.spinBox(False, 0, 1, 1, 0.05, lambda: self.controlAction(27)),
                                              self.UI.spinBox(False, 0, 1, 1, 0.05, lambda: self.controlAction(27)),
                                              self.UI.spinBox(False, 0, 1, 1, 0.05, lambda: self.controlAction(27)),
                                              self.UI.spinBox(False, 0, 1, 1, 0.05, lambda: self.controlAction(27))])
            self.colorWidget.append(self.UI.MultiColOptWidget("Point {}".format(len(colorOPT)), subAlign=Qt.AlignLeft, subfont=("Bold Tahoma", 12), height=30, optText=textOPT, optAlign=Qt.AlignCenter, optFont=("Tahoma", 11), spin=colorOPT[-1]))
            self.colorLay.addWidget(self.colorWidget[-1])

    def controlAction(self, flag, btn=None):
        if flag==1: #3D axis
            if btn.isChecked():
                self.VTK.axes_setup(self.iren)
            else:
                self.VTK.axes.SetEnabled(0)
                # self.VTK.renderer.GetRenderWindow().Render()
        elif flag==2:   # 3D box
            if btn.isChecked():
                self.VTK.boxWidget.On()
            else:
                self.VTK.boxWidget.Off()
        elif 3<=flag<=10 or flag==19 or 32<=flag<=33:   # Cam settings
            cam = self.VTK.renderer.GetActiveCamera()
            if flag==3:
                cam.SetViewUp(self.spin_camViewUp[0].value(), self.spin_camViewUp[1].value(), self.spin_camViewUp[2].value())
            elif flag==4:
                cam.SetPosition(self.spin_camPosition[0].value(), self.spin_camPosition[1].value(), self.spin_camPosition[2].value())
            elif flag==5:
                cam.SetFocalPoint(self.spin_camFocalPoint[0].value(), self.spin_camFocalPoint[1].value(), self.spin_camFocalPoint[2].value())
            elif flag==6:
                cam.SetClippingRange(self.spin_camClip[0].value(), self.spin_camClip[1].value())
            elif flag==7:
                if btn:
                    self.slid_camAngle.setValue(self.spin_camAngle[0].value())
                else:
                    self.spin_camAngle[0].setValue(self.slid_camAngle.value())
                cam.SetViewAngle(self.spin_camAngle[0].value())
            elif flag==8:
                if btn:
                    self.slid_camAzimuth.setValue(self.spin_camAzimuth[0].value())
                else:
                    self.spin_camAzimuth[0].setValue(self.slid_camAzimuth.value())
                cam.Azimuth(self.spin_camAzimuth[0].value())
            elif flag==9:
                if btn:
                    self.slid_camElevation.setValue(self.spin_camElevation[0].value())
                else:
                    self.spin_camElevation[0].setValue(self.slid_camElevation.value())
                cam.Elevation(self.spin_camElevation[0].value())
            elif flag==10:
                if btn:
                    self.slid_camRoll.setValue(self.spin_camRoll[0].value())
                else:
                    self.spin_camRoll[0].setValue(self.slid_camRoll.value())
                cam.SetRoll(self.spin_camRoll[0].value())
            elif flag==19:
                if btn:
                    self.slid_camYaw.setValue(int(self.spin_camYaw[0].value()*100))
                else:
                    self.spin_camYaw[0].setValue(int(self.slid_camYaw.value()/100))
                cam.Yaw(self.spin_camYaw[0].value())
            elif flag == 32:  # reset cam
                self.zoomy = 100
                self.spin_camZoom[0].setValue(100)
                self.VTK.renderer.ResetCameraClippingRange()
                self.VTK.renderer.ResetCamera()
                self.setupCamera(cam)
            elif flag==33:
                if btn:
                    self.slid_camZoom.setValue(int(self.spin_camZoom[0].value()))
                else:
                    self.spin_camZoom[0].setValue(int(self.slid_camZoom.value()))
                diff = self.spin_camZoom[0].value() - self.zoomy
                if diff>0:
                    for i in range(diff):
                        cam.Zoom(1.01)
                elif diff<0:
                    for i in range(diff*-1):
                        cam.Zoom(0.99)
                self.zoomy = self.spin_camZoom[0].value()





            # self.VTK.renderer.GetRenderWindow().Render()
        elif flag==11:  # bg color
            self.VTK.renderer.SetBackground(self.spin_bgColor[0].value(), self.spin_bgColor[1].value(), self.spin_bgColor[2].value())
        elif flag==12:  # Light enable (input all settings)
            if btn.isChecked():
                self.VTK.lighting(self.spin_lightColor, self.spin_lightDiffColor, self.spin_lightAmbColor, self.spin_lightSpecColor, self.spin_lightPosition, self.spin_lightFocalPoint, self.spin_lightIntens)
                self.light = True
                self.VTK.volumeProperty.ShadeOff()
            else:
                self.VTK.renderer.RemoveLight(self.VTK.light)
                self.light = False
                self.VTK.volumeProperty.ShadeOn()
                ################ havent solve !!!
                # self.VTK.volume.SetProperty(self.VTK.volProperty())
                # self.VTK.renderer.SetAutomaticLightCreation(True)
        elif 13<=flag<=18 and self.light:
            if flag==13:  # Light color
                self.VTK.light.SetColor(self.spin_lightColor[0].value(), self.spin_lightColor[1].value(), self.spin_lightColor[2].value())
            elif flag==14:  # Light Diffuse color
                self.VTK.light.SetDiffuseColor(self.spin_lightDiffColor[0].value(), self.spin_lightDiffColor[1].value(), self.spin_lightDiffColor[2].value())
            elif flag==15:  # Light Ambient color
                self.VTK.light.SetDiffuseColor(self.spin_lightAmbColor[0].value(), self.spin_lightAmbColor[1].value(), self.spin_lightAmbColor[2].value())
            elif flag==16:  # Light Specular color
                self.VTK.light.SetDiffuseColor(self.spin_lightSpecColor[0].value(), self.spin_lightSpecColor[1].value(), self.spin_lightSpecColor[2].value())
            elif flag==17:  # Light Position
                self.VTK.light.SetPosition(self.spin_lightPosition[0].value(), self.spin_lightPosition[1].value(), self.spin_lightPosition[2].value())
            elif flag==18:  # Focal Position
                self.VTK.light.SetPosition(self.spin_lightFocalPoint[0].value(), self.spin_lightFocalPoint[1].value(), self.spin_lightFocalPoint[2].value())
        elif flag==20:  # Light intensity
            if btn:
                self.slid_lightIntens.setValue(self.spin_lightIntens[0].value() * 100)
            else:
                self.spin_lightIntens[0].setValue(self.slid_lightIntens.value() / 100)
            if self.light:
                self.VTK.light.SetIntensity(self.spin_lightIntens[0].value())
        elif flag==21:  #prop_Diff
            if btn:
                self.slid_propDiff.setValue(self.spin_propDiff[0].value() * 100)
            else:
                self.spin_propDiff[0].setValue(self.slid_propDiff.value() / 100)
            self.VTK.volume.GetProperty().SetDiffuse(self.spin_propDiff[0].value())
        elif flag==22:  #prop_Amb
            if btn:
                self.slid_propAmb.setValue(self.spin_propAmb[0].value() * 100)
            else:
                self.spin_propAmb[0].setValue(self.slid_propAmb.value() / 100)
            self.VTK.volume.GetProperty().SetAmbient(self.spin_propAmb[0].value())
        elif flag==23:  #prop_Spec
            if btn:
                self.slid_propSpec.setValue(self.spin_propSpec[0].value() * 100)
            else:
                self.spin_propSpec[0].setValue(self.slid_propSpec.value() / 100)
            self.VTK.volume.GetProperty().SetSpecular(self.spin_propSpec[0].value())
        elif flag==24:  #prop_SpecP
            if btn:
                self.slid_propSpecP.setValue(self.spin_propSpecP[0].value())
            else:
                self.spin_propSpecP[0].setValue(self.slid_propSpecP.value())
            self.VTK.volume.GetProperty().SetSpecularPower(self.spin_propSpecP[0].value())
        elif flag == 25:        # switch
            self.renderMode = btn
            self.renderBtn[btn].setStyleSheet("background-color: darkorange; color: black")
            self.renderBtn[btn].setEnabled(False)
            self.renderBtn[abs(btn - 1)].setStyleSheet("background-color: lightgrey")
            self.renderBtn[abs(btn - 1)].setEnabled(True)
            if btn == 0:
                # self.VTK.colourSurf = self.tempColorPointS
                # self.VTK.volumeUpdateColor()
                self.VTK.renderer.AddVolume(self.VTK.volume)
                for actor in self.VTK.actor_surf:
                    self.VTK.renderer.RemoveActor(actor)
                self.setupColourWidget(True)
            else:
                for actor in self.VTK.actor_surf:
                    self.VTK.renderer.AddActor(actor)
                self.VTK.renderer.RemoveVolume(self.VTK.volume)
                self.setupColourWidget(False)

        elif flag==26:  # rgb point add/remove
            if btn: #Add
                if self.renderMode==0:
                    self.setupColourWidget(True, False)
                    spin = self.spin_colorPointV[-1]
                    self.VTK.colourVol.append((spin[0].value(), spin[1].value(), spin[2].value(), spin[3].value()))
                    self.VTK.volumeUpdateColor()
                else:
                    self.setupColourWidget(False, False)
                    spin = self.spin_colorPointS[-1]
                    self.VTK.colourSurf.append((spin[0].value(), spin[1].value(), spin[2].value(), spin[3].value(), spin[4].value()))
                    self.VTK.surfaceUpdate()
            else:   #Remove
                if self.renderMode==1 and len(self.VTK.actor_surf)==1:
                    return
                if self.colorWidget:
                    self.colorWidget[-1].setParent(None)
                    if self.renderMode == 0:
                        self.spin_colorPointV.pop(-1)
                        self.VTK.colourVol.pop(-1)
                        self.VTK.volumeUpdateColor()
                    else:
                        self.spin_colorPointS.pop(-1)
                        self.VTK.colourSurf.pop(-1)
                        self.VTK.renderer.RemoveActor(self.VTK.actor_surf[-1])
                        self.VTK.actor_surf.pop(-1)
                    self.colorWidget.pop(-1)

        elif flag==27:
            if self.renderMode == 0:
                for i,spin in enumerate(self.spin_colorPointV[btn]):
                    self.VTK.colourVol[btn][i] = spin.value()
                self.VTK.volumeUpdateColor()
            else:
                for i, spin in enumerate(self.spin_colorPointS[btn]):
                    self.VTK.colourSurf[btn][i] = spin.value()
                self.VTK.renderer.RemoveActor(self.VTK.actor_surf[btn])
                self.VTK.surfaceUpdate(btn)

                self.VTK.renderer.AddActor(self.VTK.actor_surf[btn])
        elif 28<=flag<=31:
            transform_t = vtkTransform()
            transform_t.SetMatrix(self.VTK.volume.GetMatrix())
            if flag==28:        # Position (translate)
                self.VTK.volume.SetPosition(self.spin_renderPosition[0].value(), self.spin_renderPosition[1].value(), self.spin_renderPosition[2].value())
            elif flag==29:      # Rotation
                self.VTK.volume.RotateX(self.spin_renderRotation[0].value())
                self.VTK.volume.RotateY(self.spin_renderRotation[1].value())
                self.VTK.volume.RotateZ(self.spin_renderRotation[2].value())
                # self.VTK.volume.SetOrientation(self.spin_renderRotation[0].value(), self.spin_renderRotation[1].value(), self.spin_renderRotation[2].value())
            elif flag==30:
                self.VTK.volume.SetScale(self.spin_renderScale[0].value(), self.spin_renderScale[1].value(), self.spin_renderScale[2].value())
            elif flag == 31:
                print(self.VTK.volume.GetMatrix())
                transform_t = vtkTransform()
                self.VTK.volume.SetPosition(0,0,0)  #reset
                self.VTK.volume.SetOrientation(0,0,0)
                self.VTK.volume.SetScale(1,1,1)
                for i in range(3):
                    self.spin_renderPosition[i].setValue(0)
                    self.spin_renderRotation[i].setValue(0)
                    self.spin_renderScale[i].setValue(1)
            self.VTK.volume.SetUserTransform(transform_t)
            # transform_t = vtkTransform()
            if not flag==31:
                transform_t.SetMatrix(self.VTK.volume.GetMatrix())
            self.VTK.boxWidget.SetTransform(transform_t)

        self.VTK.renderer.GetRenderWindow().Render()

