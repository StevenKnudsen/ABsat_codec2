# This script was inspired by a flowgraph found in gnuradio's github repo. 
# The flowgraph was created by Martin Braun and is linked below:
# https://github.com/gnuradio/gnuradio/blob/master/gr-vocoder/examples/loopback-codec2.grc

# Title: Codec2 encoder and decoder
# Author: Shayan Khorassany
# Description: A script that could encode or decode audio recordings using command line arguments. 
#              It was created under the guidance of Dr. Steven Knudsen to be used in AlbertaSat


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
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys, getopt
from gnuradio import vocoder
from gnuradio.vocoder import codec2
from gnuradio import qtgui

class loopback_codec2(gr.top_block):

    # Avaialable bit rates: 3200, 2400, 1600, 1400, 1300, 1200 bps
    # Sample rate needs to be a multiple of 8000 sps
    # Mode of operation can be either 'e' or 'd'

    def __init__(self, mode, audio_file="people_call_me_steve_Au48k.wav", samp_rate=48000, bit_rate=2400, output_filename='sample_output'): 
        gr.top_block.__init__(self, "Codec2 Looback Test", catch_exceptions=True)

        ##################################################
        # Variables
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

        match bit_rate: # for the reasoning behind the following buffer sizes check out https://www.gnuradio.org/doc/doxygen/codec2__encode__sp_8h_source.html
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

        if self.mode == 'd': # decoding mode selected
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

        elif self.mode == 'e': # encoding mode selected
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

    tb.run()
    qapp.exit()



if __name__ == '__main__':
    main(sys.argv[1:])
