from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class WidgetUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def TextLabel(self, text, align, colorBG=None, colorFG=None, font=None, height=None):
        label_Text = QLabel(self)
        label_Text.setText(text)
        if font:
            label_Text.setFont(QFont(font[0], font[1]))
        if height:
            label_Text.setFixedHeight(height)
        label_Text.setAlignment(align)
        if colorFG and colorBG:
            label_Text.setStyleSheet("background-color: {}".format(colorBG) + "; color: {}".format(colorFG))
        return label_Text

    def MultiColOpt(self, subtext, subAlign, subfont, height, optText, optAlign, optFont, spin, slider=None):
        mainLay = QVBoxLayout()
        mainLay.addWidget(self.TextLabel(subtext, subAlign, subfont, height))
        OptLay = QHBoxLayout()
        for i in range(len(spin)):
            if optText:
                OptLay.addWidget(self.TextLabel(optText[i], optAlign, optFont, height))
            if slider:
                OptLay.addWidget(slider)
            OptLay.addWidget(spin[i])
        mainLay.addLayout(OptLay)
        return mainLay

    def MultiButOpt(self, subtext, subAlign, subfont, height, btn):
        mainLay = QVBoxLayout()
        mainLay.addWidget(self.TextLabel(subtext, subAlign, subfont, height))
        OptLay = QHBoxLayout()
        for i in range(len(btn)):
            OptLay.addWidget(btn[i])
        OptLay.setSpacing(0)
        mainLay.addLayout(OptLay)
        return mainLay


    def spinBox(self, flag, min, max, value, step, action=None, width=None):
        if flag:
            spin = QSpinBox()
        else:
            spin = QDoubleSpinBox()
        spin.setSingleStep(step)
        spin.setMinimum(min)
        spin.setMaximum(max)
        spin.setValue(value)
        if width:
            spin.setMinimumWidth(width)
        if action:
            spin.valueChanged.connect(action)
        return spin

    def checkbox(self, name, action, checked, font=None, colorFG=None, colorBG=None, height=None):
        checkbox = QCheckBox(self)
        if name:
            checkbox.setText(name)
        checkbox.setChecked(checked)
        if font:
            checkbox.setFont(QFont(font[0], font[1]))
        if colorFG and colorBG:
            checkbox.setStyleSheet("background-color: {}".format(colorBG) + "; color: {}".format(colorFG))
        if height:
            checkbox.setFixedHeight(height)
        if action:
            checkbox.clicked.connect(action)
        return checkbox

    def SliderWidget(self, ott, default, min, max, action=None):
        slider = QSlider(self)
        slider.setOrientation(ott)
        slider.setValue(default)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setSingleStep(1)
        # slider.setFixedWidth(width)
        # slider.setEnabled(enable)
        slider.setStyleSheet("QSlider::groove:horizontal {border: 1px solid #bbb;background: white;height: 10px;border-radius: 4px;}"
                             "QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,stop: 0 #66e, stop: 1 #bbf);background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,stop: 0 #bbf, stop: 1 #55f);border: 1px solid #777;height: 10px;border-radius: 4px;}"
                             "QSlider::add-page:horizontal {background: #fff;border: 1px solid #777;height: 10px;border-radius: 4px;}"
                             "QSlider::handle:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #eee, stop:1 #ccc);border: 1px solid #777;width: 13px;margin-top: -2px;margin-bottom: -2px;border-radius: 4px;}"
                             "QSlider::handle:horizontal:hover {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #fff, stop:1 #ddd);border: 1px solid #444;border-radius: 4px;}"
                             "QSlider::sub-page:horizontal:disabled {background: #bbb;border-color: #999;}"
                             "QSlider::add-page:horizontal:disabled {background: #eee;border-color: #999;}"
                             "QSlider::handle:horizontal:disabled {background: #eee;border: 1px solid #aaa;border-radius: 4px;}")
        if action:
            slider.valueChanged.connect(action)
        return slider

    def textBtn(self, text, action=None, font=None, width=None, height=None, colorFG=None, colorBG=None, removeBorder=None, enable=True):
        btn = QPushButton(self)
        btn.setText(text)
        if font:
            btn.setFont(QFont(font[0], font[1]))
        if width:
            btn.setFixedWidth(width)
        if height:
            btn.setFixedHeight(height)
        if colorFG and colorBG:
            btn.setStyleSheet("background-color: {}".format(colorBG) + "; color: {}".format(colorFG))
        elif colorFG:
            btn.setStyleSheet("color: {}".format(colorFG))
        elif colorBG:
            btn.setStyleSheet("background-color: {}".format(colorBG))
        if not enable:
            btn.setEnabled(enable)
        if removeBorder:
            pass
        if action:
            btn.clicked.connect(action)
        return btn

    def MultiColOptWidget(self, subtext, subAlign, subfont, optText, optAlign, optFont, height, spin):
        mainWidget = QWidget()
        mainLay = QVBoxLayout()
        mainLay.addWidget(self.TextLabel(subtext, subAlign, subfont, height))
        optLay = QHBoxLayout()

        for i in range(len(spin)):
            if optText:
                optLay.addWidget(self.TextLabel(optText[i], optAlign, optFont, height))
            optLay.addWidget(spin[i])
        mainLay.addLayout(optLay)
        mainWidget.setLayout(mainLay)

        return mainWidget




    def fileDialog(self):
        dialog = QFileDialog(self, 'CT folder', r"Data/")
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.selectedFiles()[0]

    def mssgDialog(self, title, desc):
        reply = QMessageBox.question(self, title, desc, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False