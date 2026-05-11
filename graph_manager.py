import pyqtgraph as pg
import numpy as np
from collections import deque

# Style global des graphes
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class GraphManager:
    def __init__(self, widget_signal, widget_fft, max_points=256):
        self.max_points = max_points
        
        # Buffer circulaire pour le signal temporel
        self.buffer_signal = deque([0.0] * max_points, maxlen=max_points)
        
        # --- Graphe signal temporel ---
        self.plot_signal = pg.PlotWidget()
        self.plot_signal.setTitle("Signal temporel")
        self.plot_signal.setLabel('left', 'Valeur')
        self.plot_signal.setLabel('bottom', 'Échantillons')
        self.plot_signal.showGrid(x=True, y=True, alpha=0.3)
        self.plot_signal.setYRange(-32768, 32768) 
        self.courbe_signal = self.plot_signal.plot(
            pen=pg.mkPen(color='#378ADD', width=1.5)
        )
        
        # Indique si le buffer a changé
        self._dirty = False

        # Lignes de seuil
        self.ligne_seuil_max = pg.InfiniteLine(
            angle=0, pen=pg.mkPen(color='r', width=1, style=pg.QtCore.Qt.DashLine)
        )
        self.ligne_seuil_min = pg.InfiniteLine(
            angle=0, pen=pg.mkPen(color='r', width=1, style=pg.QtCore.Qt.DashLine)
        )
        self.plot_signal.addItem(self.ligne_seuil_max)
        self.plot_signal.addItem(self.ligne_seuil_min)

        # --- Graphe FFT ---
        self.plot_fft = pg.PlotWidget()
        self.plot_fft.setTitle("Spectre FFT")
        self.plot_fft.setLabel('left', 'Amplitude')
        self.plot_fft.setLabel('bottom', 'Fréquence (Hz)')
        self.plot_fft.showGrid(x=True, y=True, alpha=0.3)
        self.courbe_fft = self.plot_fft.plot(
            pen=pg.mkPen(color='#378ADD', width=1.5),
            fillLevel=0,
            brush=pg.mkBrush(color=(55, 138, 221, 80))
        )

        # Intègre les graphes dans les widgets Qt Designer
        layout_signal = widget_signal.layout()
        if layout_signal is None:
            from PySide6.QtWidgets import QVBoxLayout
            layout_signal = QVBoxLayout(widget_signal)
            widget_signal.setLayout(layout_signal)
        layout_signal.addWidget(self.plot_signal)

        layout_fft = widget_fft.layout()
        if layout_fft is None:
            from PySide6.QtWidgets import QVBoxLayout
            layout_fft = QVBoxLayout(widget_fft)
            widget_fft.setLayout(layout_fft)
        layout_fft.addWidget(self.plot_fft)

    def maj_signal(self, valeur):
        self.buffer_signal.append(valeur)
        self.courbe_signal.setData(list(self.buffer_signal))

    
    def maj_signal_buffer(self, valeurs):
        """Met à jour le graphe avec un buffer entier d'un coup"""
        for v in valeurs:
            self.buffer_signal.append(v)
        self._dirty = True  # Indique que le buffer a changé, rafraîchissement différé
    
    def rafraichir(self):
        if self._dirty:
            self.courbe_signal.setData(list(self.buffer_signal))
            self._dirty = False

    
    def maj_fft(self, data, fmax=5000):
        """Met à jour le graphe FFT avec un buffer de points"""
        freqs = np.linspace(0, fmax, len(data))
        self.courbe_fft.setData(freqs, data)

    def set_seuils(self, seuil_min, seuil_max):
        """Met à jour les lignes de seuil"""
        self.ligne_seuil_max.setValue(seuil_max)
        self.ligne_seuil_min.setValue(seuil_min)

    def reset(self):
        """Remet les graphes à zéro"""
        self.buffer_signal = deque([0.0] * self.max_points, maxlen=self.max_points)
        self.courbe_signal.setData(list(self.buffer_signal))
        self.courbe_fft.setData([], [])