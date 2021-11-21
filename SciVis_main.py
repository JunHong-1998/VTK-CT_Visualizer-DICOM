from SciVis_setting import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys


class SciVis(QMainWindow):

    def __init__(self, parent=None):
        self.viewportCount = 0
        QMainWindow.__init__(self, parent)
        self.UI = WidgetUI(self)
        self.setupUI()
        self.VTK = [Setting(self, 'Data\Pelvis')]

        self.vtkWidget[0].GetRenderWindow().AddRenderer(self.VTK[0].VTK.renderer)        # default ren can add on
        self.VTK[0].iren = self.vtkWidget[0].GetRenderWindow().GetInteractor()
        self.VTK[0].setup3DAnnotation()
        self.VTK[0].setupObserver()

        self.setup_dockWidget(self)
    def setupUI(self):
        self.setWindowTitle("CT Visualizer made by Low Jun Hong")
        self.resize(1200, 800)
        centreWidget = QFrame(self)
        self.holdVTKwidget = (QFrame(self), QFrame(self), QFrame(self), QFrame(self))
        self.vtkWidget = [QVTKRenderWindowInteractor(self.holdVTKwidget[0])]
        mainLay = QVBoxLayout()
        self.layTop = QHBoxLayout()
        self.layTop.addWidget(self.vtkWidget[0])
        self.layBot = QHBoxLayout()
        mainLay.addLayout(self.layTop)
        mainLay.addLayout(self.layBot)
        centreWidget.setLayout(mainLay)
        self.setCentralWidget(centreWidget)
        
    def addNewVTK(self, ind=None):
        folder = self.UI.fileDialog()
        if folder:
            if ind is not None:
                self.tabDelete(ind)
                self.tabby.removeTab(ind)
            self.viewportCount += 1
            self.VTK.append(Setting(self, folder))
            self.vtkWidget.append(QVTKRenderWindowInteractor(self.holdVTKwidget[self.viewportCount]))
            if self.viewportCount<2:
                self.layTop.addWidget(self.vtkWidget[self.viewportCount])
            else:
                self.layBot.addWidget(self.vtkWidget[self.viewportCount])
            self.vtkWidget[self.viewportCount].GetRenderWindow().AddRenderer(self.VTK[self.viewportCount].VTK.renderer)  # default ren can add on

            self.VTK[self.viewportCount].iren = self.vtkWidget[self.viewportCount].GetRenderWindow().GetInteractor()
            self.VTK[self.viewportCount].setup3DAnnotation()
            self.VTK[self.viewportCount].setupObserver()
            for vtk in self.VTK:
                vtk.VTK.renderer.ResetCamera()
                vtk.VTK.renderer.GetRenderWindow().Render()
            btn = self.VTK[self.viewportCount].Content(self.tabby)
            btn.clicked.connect(self.btnAction)
            return True
        else:
            return False


    def setup_dockWidget(self, win):
        dock = QDockWidget("Inspect", self)
        dock_widget = QWidget()
        dock_cont = QVBoxLayout()
        inner = QMainWindow(dock)
        inner.setWindowFlags(Qt.Widget)
        self.tabby = QTabWidget(dock)
        self.tabby.setMinimumWidth(400)
        self.tabby.setTabsClosable(True)
        self.tabby.tabCloseRequested.connect(self.tabDelete)
        self.tabby.tabBarClicked.connect(self.tabAdd)
        btn = self.VTK[0].Content(self.tabby)
        btn.clicked.connect(self.btnAction)
        self.tabby.addTab(QWidget(), "")
        AddTab_btn = self.UI.TextLabel("+", align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=25)
        self.tabby.tabBar().setTabButton(self.tabby.count()-1, self.tabby.tabBar().RightSide, AddTab_btn)

        dock_cont.addWidget(self.tabby, Qt.AlignTop)
        dock.setTitleBarWidget(QWidget(dock))
        dock_widget.setLayout(dock_cont)
        dock.setWidget(dock_widget)
        win.addDockWidget(Qt.RightDockWidgetArea, dock)

    def btnAction(self):
        check = self.addNewVTK(self.tabby.currentIndex())
        if not check:
            return
        if self.tabby.count() <= 4:
            self.tabby.addTab(QWidget(), "")
            AddTab_btn = self.UI.TextLabel("+", align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=25)
            self.tabby.tabBar().setTabButton(self.tabby.count() - 1, self.tabby.tabBar().RightSide, AddTab_btn)

    def tabDelete(self, ind):
        if self.tabby.count()>1 and not self.tabby.count()==ind+1:
            check = self.UI.mssgDialog("Delete CT", "Are you sure to remove this CT data")
            if not check:
                return
            self.tabby.removeTab(ind)
            self.viewportCount -= 1
            self.vtkWidget[ind].GetRenderWindow().RemoveRenderer(self.VTK[ind].VTK.renderer)
            self.VTK[ind].VTK.axes.SetEnabled(0)
            self.VTK.pop(ind)
            self.vtkWidget[ind].setParent(None)
            self.vtkWidget.pop(ind)


    def tabAdd(self, ind):
        if self.tabby.count()<5 and self.tabby.count() == ind + 1:
            self.tabby.removeTab(ind)
            self.addNewVTK()
            if self.tabby.count()<=4:
                self.tabby.addTab(QWidget(), "")
                AddTab_btn = self.UI.TextLabel("+", align=Qt.AlignCenter, font=("Bold Tahoma", 12), height=25)
                self.tabby.tabBar().setTabButton(self.tabby.count() - 1, self.tabby.tabBar().RightSide, AddTab_btn)

    def closeEvent(self, event):
        quit = self.UI.mssgDialog("Quit Application", "Are you sure to quit application ?")
        if quit:
            # event.accept()
            super().closeEvent(event)
            for vtk in self.vtkWidget:
                vtk.GetRenderWindow().Finalize()
                vtk.close()
            self.close()

        else:
            event.ignore()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SciVis()
    window.show()
    for set in window.VTK:
        set.iren.Initialize()
    sys.exit(app.exec_())


