#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Codec2 WAV encode
# Author: Steven Knudsen
# Copyright: University of Alberta 2022
# GNU Radio version: 3.9.7.0

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

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import vocoder
from gnuradio.vocoder import codec2



from gnuradio import qtgui

class NS_codec2_encode_v01(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Codec2 WAV encode", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Codec2 WAV encode")
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

        self.settings = Qt.QSettings("GNU Radio", "NS_codec2_encode_v01")

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
        self.wav_audio_samp_rate = wav_audio_samp_rate = 8000
        self.scale = scale = 2**13
        self.samp_rate = samp_rate = 48000
        self.codec2_rate_scale = codec2_rate_scale = 25
        self.codec2_rate = codec2_rate = 1300

        ##################################################
        # Blocks
        ##################################################
        self.vocoder_codec2_encode_sp_0 = vocoder.codec2_encode_sp(codec2.MODE_1300)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('female_male/male_8k.wav', False)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_char*1, int(codec2_rate/codec2_rate_scale))
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, scale)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'male_8k_1300.dat', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_short_0, 0), (self.vocoder_codec2_encode_sp_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.vocoder_codec2_encode_sp_0, 0), (self.blocks_vector_to_stream_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NS_codec2_encode_v01")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_wav_audio_samp_rate(self):
        return self.wav_audio_samp_rate

    def set_wav_audio_samp_rate(self, wav_audio_samp_rate):
        self.wav_audio_samp_rate = wav_audio_samp_rate

    def get_scale(self):
        return self.scale

    def set_scale(self, scale):
        self.scale = scale
        self.blocks_float_to_short_0.set_scale(self.scale)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_codec2_rate_scale(self):
        return self.codec2_rate_scale

    def set_codec2_rate_scale(self, codec2_rate_scale):
        self.codec2_rate_scale = codec2_rate_scale

    def get_codec2_rate(self):
        return self.codec2_rate

    def set_codec2_rate(self, codec2_rate):
        self.codec2_rate = codec2_rate




def main(top_block_cls=NS_codec2_encode_v01, options=None):

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
