#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Codec2 WAV decode
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

from gnuradio import audio
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
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

class NS_codec2_decode_v01(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Codec2 WAV decode", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Codec2 WAV decode")
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

        self.settings = Qt.QSettings("GNU Radio", "NS_codec2_decode_v01")

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
        self.codec2_rate = codec2_rate = 1200

        ##################################################
        # Blocks
        ##################################################
        self.vocoder_codec2_decode_ps_0 = vocoder.codec2_decode_ps(codec2.MODE_1200)
        self.rational_resampler_xxx_0_1 = filter.rational_resampler_fff(
                interpolation=int(samp_rate/wav_audio_samp_rate),
                decimation=1,
                taps=[],
                fractional_bw=.4)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            'decoded_audio_1200.wav',
            1,
            wav_audio_samp_rate,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, int(codec2_rate/codec2_rate_scale))
        self.blocks_short_to_float_0 = blocks.short_to_float(1, scale)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/knud/Development/AlbertaSat/ABsat_codec2/test_vectors/OSR_us_000_0061_8k_1200.dat', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.audio_sink_1 = audio.sink(samp_rate, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.rational_resampler_xxx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.vocoder_codec2_decode_ps_0, 0))
        self.connect((self.rational_resampler_xxx_0_1, 0), (self.audio_sink_1, 0))
        self.connect((self.vocoder_codec2_decode_ps_0, 0), (self.blocks_short_to_float_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NS_codec2_decode_v01")
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
        self.blocks_short_to_float_0.set_scale(self.scale)

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




def main(top_block_cls=NS_codec2_decode_v01, options=None):

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
