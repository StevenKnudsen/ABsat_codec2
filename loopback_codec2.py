#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Codec2 Looback Test
# Author: Martin Braun
# Copyright: 2014,2019 Free Software Foundation, Inc.
# Description: An example how to use the Codec2 Vocoder
# GNU Radio version: 3.9.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import vocoder
from gnuradio.vocoder import codec2



from gnuradio import qtgui

class loopback_codec2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Codec2 Looback Test", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Codec2 Looback Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "loopback_codec2")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.scale = scale = 2**13
        self.samp_rate = samp_rate = 48000
        self.play_encoded = play_encoded = True

        ##################################################
        # Blocks
        ##################################################
        _play_encoded_check_box = Qt.QCheckBox("Encode Audio")
        self._play_encoded_choices = {True: 1, False: 0}
        self._play_encoded_choices_inv = dict((v,k) for k,v in self._play_encoded_choices.items())
        self._play_encoded_callback = lambda i: Qt.QMetaObject.invokeMethod(_play_encoded_check_box, "setChecked", Qt.Q_ARG("bool", self._play_encoded_choices_inv[i]))
        self._play_encoded_callback(self.play_encoded)
        _play_encoded_check_box.stateChanged.connect(lambda i: self.set_play_encoded(self._play_encoded_choices[bool(i)]))
        self.top_layout.addWidget(_play_encoded_check_box)
        self.vocoder_codec2_encode_sp_0 = vocoder.codec2_encode_sp(codec2.MODE_2400)
        self.vocoder_codec2_decode_ps_0 = vocoder.codec2_decode_ps(codec2.MODE_2400)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=6,
                decimation=1,
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=6,
                taps=[],
                fractional_bw=0.4)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            1024, #size
            8000, #samp_rate
            'Audio Pre-Encoding', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            8000, #samp_rate
            'Audio Post-Encoding', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\khora\\OneDrive\\Documents\\ABsat_codec2\\people-call-me-steve.wav', True)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_char*1, 48)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, 48)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, scale)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(1.0 if play_encoded  else 0.0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.0 if play_encoded  else 1.0)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, scale)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(48000, '', True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.vocoder_codec2_encode_sp_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.vocoder_codec2_decode_ps_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.vocoder_codec2_decode_ps_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.vocoder_codec2_encode_sp_0, 0), (self.blocks_vector_to_stream_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "loopback_codec2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_scale(self):
        return self.scale

    def set_scale(self, scale):
        self.scale = scale
        self.blocks_float_to_short_0.set_scale(self.scale)
        self.blocks_short_to_float_0.set_scale(self.scale)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_play_encoded(self):
        return self.play_encoded

    def set_play_encoded(self, play_encoded):
        self.play_encoded = play_encoded
        self._play_encoded_callback(self.play_encoded)
        self.blocks_multiply_const_vxx_0.set_k(0.0 if self.play_encoded  else 1.0)
        self.blocks_multiply_const_vxx_1.set_k(1.0 if self.play_encoded  else 0.0)




def main(top_block_cls=loopback_codec2, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
