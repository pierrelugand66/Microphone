import pyqtgraph as pg
import numpy as np
from collections import deque

# Style global des graphes
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class GraphManager:
    def __init__(self, widget_signal, widget_fft=None, widget_samples=None, max_points=256):
        self.max_points = max_points
        self._has_fft = widget_fft is not None
        self._has_samples = widget_samples is not None
        
        # Buffer circulaire pour le signal temporel
        self.buffer_signal = deque([0.0] * max_points, maxlen=max_points)
        
        # --- Graphe signal temporel ---
        self.plot_signal = pg.PlotWidget()
        self.plot_signal.setTitle("Signal temporel")
        self.plot_signal.setLabel('left', 'Amplitude', units='LSB')
        self.plot_signal.setLabel('bottom', 'Temps', units='ms')
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

        # Intègre le graphe signal dans le widget Qt Designer
        layout_signal = widget_signal.layout()
        if layout_signal is None:
            from PySide6.QtWidgets import QVBoxLayout
            layout_signal = QVBoxLayout(widget_signal)
            widget_signal.setLayout(layout_signal)
        layout_signal.addWidget(self.plot_signal)

        # --- Graphe FFT (optionnel) ---
        if self._has_fft:
            self.plot_fft = pg.PlotWidget()
            self.plot_fft.setTitle("Spectre FFT")
            self.plot_fft.setLabel('left', 'Amplitude')
            self.plot_fft.setLogMode(False, False)
            self.plot_fft.setYRange(0, 1)
            self.plot_fft.showGrid(x=True, y=True, alpha=0.3)
            self.courbe_fft = self.plot_fft.plot(
                pen=pg.mkPen(color='#378ADD', width=1.5),
                fillLevel=0,
                brush=pg.mkBrush(color=(55, 138, 221, 80))
            )
            layout_fft = widget_fft.layout()
            if layout_fft is None:
                from PySide6.QtWidgets import QVBoxLayout
                layout_fft = QVBoxLayout(widget_fft)
                widget_fft.setLayout(layout_fft)
            layout_fft.addWidget(self.plot_fft)
        
        if self._has_samples:
            self.plot_samples = pg.PlotWidget()
            self.plot_samples.setTitle("Signal audio temporel")
            self.plot_samples.setLabel('left', 'Amplitude', units='LSB')
            self.plot_samples.setLabel('bottom', 'Temps', units='min')
            self.plot_samples.showGrid(x=True, y=True, alpha=0.3)
            self.plot_samples.setYRange(-32768, 32768)
            self.courbe_samples = self.plot_samples.plot(
                pen=pg.mkPen(color='#378ADD', width=1.0)
            )
            layout_samples = widget_samples.layout()
            if layout_samples is None:
                from PySide6.QtWidgets import QVBoxLayout
                layout_samples = QVBoxLayout(widget_samples)
                widget_samples.setLayout(layout_samples)
            layout_samples.addWidget(self.plot_samples)

    def maj_signal(self, valeur):
        self.buffer_signal.append(valeur)
        self.courbe_signal.setData(list(self.buffer_signal))

    def maj_signal_buffer(self, valeurs):
        """Met à jour le graphe avec un buffer entier d'un coup"""
        for v in valeurs:
            self.buffer_signal.append(v)
        self._dirty = True

    def rafraichir(self):
        if self._dirty:
            n = len(self.buffer_signal)
            t_ms = np.linspace(0, n / 16000 * 1000, n)
            self.courbe_signal.setData(t_ms, list(self.buffer_signal))
            self._dirty = False

    def maj_fft(self, data, fmax=5000):
        if not self._has_fft:
            return
        arr = np.array(data, dtype=np.float32)
        freqs = np.linspace(0, fmax, len(arr))
        self.courbe_fft.setData(freqs, arr)

    def set_seuils(self, seuil_min, seuil_max):
        """Met à jour les lignes de seuil"""
        self.ligne_seuil_max.setValue(seuil_max)
        self.ligne_seuil_min.setValue(seuil_min)

    def reset(self):
        """Remet les graphes à zéro"""
        self.buffer_signal = deque([0.0] * self.max_points, maxlen=self.max_points)
        self.courbe_signal.setData(list(self.buffer_signal))
        if self._has_fft:
            self.courbe_fft.setData([], [])
        if self._has_samples:
            self.courbe_samples.setData([], [])