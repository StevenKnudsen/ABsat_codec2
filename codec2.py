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
import sys, getopt
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import vocoder
from gnuradio.vocoder import codec2



from gnuradio import qtgui

class loopback_codec2(gr.top_block, Qt.QWidget):

    # Avaialable bit rates: 3200, 2400, 1600, 1400, 1300, 1200 bps
    # Sample rate needs to be a multiple of 8000 sps
    # Mode of operation can be either 'e' or 'd'

    def __init__(self, mode, audio_file="people_call_me_steve_Au48k.wav", samp_rate=48000, bit_rate=2400, output_filename='sample_output'): 
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
        self.mode = mode
        self.scale = scale = 2**13
        self.samp_rate = samp_rate
        if samp_rate % 8000 != 0: 
            print(">>>> samp_rate is not a multiple of 8000 sps. Audacity can be used to resample the audio file.")
            print('python codec2.py [-e <audiofile.wav> samp_rate bit_rate <encodedfilename>] OR [-d <encodedfilename> samp_rate bit_rate <decodedaudiofile.wav>]')
            exit()
        self.bit_rate = bit_rate
        self.buf_size = 0
        self.play_encoded = play_encoded = True

        # Description of CODEC2 Vocoder Codec2 encoder:
        #   /*!
        # * \brief CODEC2 Vocoder Encoder
        # * \ingroup audio_blk
        # *
        # * Input: Speech (audio) signal as 16-bit shorts, sampling rate 8 kHz.
        # *
        # * Output: Vector of unpacked bits, forming one Codec2 frame, per 160
        # *         input samples (in 2400 and 3200 bps modes) or per 320 input
        # *         samples (in 1200, 1300, 1400 and 1600 bps modes).
        # *
        # */
        # Taken from: https://www.gnuradio.org/doc/doxygen/codec2__encode__sp_8h_source.html
        # Consequently the following buffer sizes are used in converting between the output and the bit stream:
        match bit_rate:
            case 3200:
                self.bit_rate_mode = codec2.MODE_3200
                self.buf_size = 64
            case 2400:
                self.bit_rate_mode = codec2.MODE_2400
                self.buf_size = 48
            case 1600:
                self.bit_rate_mode = codec2.MODE_1600
                self.buf_size = 64
            case 1400:
                self.bit_rate_mode = codec2.MODE_1400
                self.buf_size = 56
            case 1300:
                self.bit_rate_mode = codec2.MODE_1300
                self.buf_size = 52
            case 1200:
                self.bit_rate_mode = codec2.MODE_1200
                self.buf_size = 48
            case _:
                print('>>>> bit_rate value is missing or not supported.')
                print('codec2.py [-e <audiofile.wav> samp_rate bit_rate <encodedfilename>] OR [-d <encodedfilename> samp_rate bit_rate <decodedaudiofile.wav>]')
                exit()
            


        ##################################################
        # Blocks
        ##################################################
        # _play_encoded_check_box = Qt.QCheckBox("Encode Audio")
        # self._play_encoded_choices = {True: 1, False: 0}
        # self._play_encoded_choices_inv = dict((v,k) for k,v in self._play_encoded_choices.items())
        # self._play_encoded_callback = lambda i: Qt.QMetaObject.invokeMethod(_play_encoded_check_box, "setChecked", Qt.Q_ARG("bool", self._play_encoded_choices_inv[i]))
        # self._play_encoded_callback(self.play_encoded)
        # _play_encoded_check_box.stateChanged.connect(lambda i: self.set_play_encoded(self._play_encoded_choices[bool(i)]))
        # self.top_layout.addWidget(_play_encoded_check_box)

        if self.mode == 'd':
            import pmt
            ##################################################
            # Blocks
            self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, audio_file, False, 0, 0)
            self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
            self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_LSB_FIRST)
            self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, self.buf_size)
            self.vocoder_codec2_decode_ps_0 = vocoder.codec2_decode_ps(self.bit_rate_mode)
            self.blocks_short_to_float_0 = blocks.short_to_float(1, scale)
            self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=int(self.samp_rate/8000),
                decimation=1,
                taps=[],
                fractional_bw=0.4)
            self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
                output_filename,
                1,
                samp_rate,
                blocks.FORMAT_WAV,
                blocks.FORMAT_PCM_16,
                False
            )

            ##################################################
            # Connections
            self.connect((self.blocks_file_source_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
            self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
            self.connect((self.blocks_stream_to_vector_0, 0), (self.vocoder_codec2_decode_ps_0, 0))
            self.connect((self.vocoder_codec2_decode_ps_0, 0), (self.blocks_short_to_float_0, 0))
            self.connect((self.blocks_short_to_float_0, 0), (self.rational_resampler_xxx_1, 0))
            self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_wavfile_sink_0, 0))

        elif self.mode == 'e':
            ##################################################
            # Blocks
            self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=int(self.samp_rate/8000),
                taps=[],
                fractional_bw=0.4)
            self.blocks_wavfile_source_0 = blocks.wavfile_source(audio_file, False) # inputing file for being encoded
            self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, output_filename, False)
            self.blocks_file_sink_0.set_unbuffered(False)
            self.blocks_float_to_short_0 = blocks.float_to_short(1, scale)
            self.vocoder_codec2_encode_sp_0 = vocoder.codec2_encode_sp(self.bit_rate_mode)
            self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_char*1, self.buf_size)
            self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_LSB_FIRST)

            ##################################################
            # Connections
            self.connect((self.blocks_wavfile_source_0, 0), (self.rational_resampler_xxx_0, 0))
            self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_float_to_short_0, 0))
            self.connect((self.blocks_float_to_short_0, 0), (self.vocoder_codec2_encode_sp_0, 0))
            self.connect((self.vocoder_codec2_encode_sp_0, 0), (self.blocks_vector_to_stream_0, 0))
            self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
            self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        else:
            print("There's something terribly wrong.")
            exit()

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "loopback_codec2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()



def main(argv, top_block_cls=loopback_codec2, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    try:
        opts, args = getopt.getopt(argv,"he:d:",["efile=","dfile="])
    except getopt.GetoptError:
        print('python codec2.py [-e <audiofile.wav> samp_rate bit_rate <encodedfilename>] OR [-d <encodedfilename> samp_rate bit_rate <decodedaudiofile.wav>]')
        sys.exit(2)
    opt, arg = opts[0]
    if opt == '-e': # encoding mode
        if not arg.endswith(".wav"):
            print('python codec2.py [-e <audiofile.wav> samp_rate bit_rate <encodedfilename>] OR [-d <encodedfilename> samp_rate bit_rate <decodedaudiofile.wav>]')
            exit()
        if not args[2]: encoded = 'encoded'
        else: encoded = args[2]

        tb = top_block_cls('e', audio_file=arg, samp_rate=int(args[0]), bit_rate=int(args[1]), output_filename=encoded)

    elif opt == '-d': # decoding mode
        if arg.endswith(".wav") or arg.endswith(".txt"):
            print('>>>> For decoding only binary files without extensions are accepted.')
            print('python codec2.py [-e <audiofile.wav> samp_rate bit_rate <encodedfilename>] OR [-d <encodedfilename> samp_rate bit_rate <decodedaudiofile.wav>]')
            exit()
        if not args[2]: decoded = 'decoded.wav'
        elif not args[2].endswith(".wav"): decoded = args[2] + ".wav"
        else: decoded = args[2]
        tb = top_block_cls('d', audio_file=arg, samp_rate=int(args[0]), bit_rate=int(args[1]), output_filename=decoded)

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
    main(sys.argv[1:])
