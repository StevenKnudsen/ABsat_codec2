# Northern SPIRIT Voice Recording Support

This repository contains GNU Radio-based support for encoding and decoding speech using [Codec2](https://en.wikipedia.org/wiki/Codec_2).

There are examples using GNU Radio Companion (GRC) for encoding WAV files to create Codec2-compressed data files, and to decode those files to recreate similar WAV files. Of course, the decoded WAV files are at best similar due to compression artefacts, but in general they are pretty similar to the original files.

The GRC flows have support for Audio Sink blocks so that the user can listen to the input file in the case of encoding, and the resulting decoded audio as the output WAV file is written to disk.

There is a standalone Python program that is based on GNU Radio and supports standalone encoding of WAV files and decoding of encoded files.

The following Codec2 Rates are supported:
   * 3200
   * 2400
   * 1600
   * 1400
   * 1300
   * 1200
   
## Sample WAV files

The WAV files included provide examples of various male and female speakers.

## GNU Radio Companion Flow files

There example flows demonstrate how to configure encoding and decoding at two different rates; 2400 bps and 1300 bps.

Each flow has a Note that provides help to set up for a specific Codec2 rate, which is set using a dropdown menu in the `CODEC2 Audio Encoder` or `CODEC2 Audio Decoder` blocks. Since there is no convenient variable from those blocks that can be used to determine the CODEC2 block size, we must set our own variables,
   * `codec2_rate`, which is the bps value set in the `CODEC2 Audio xxx` block
   * `codec2_rate_scale`, which is a divisor used to determine the CODEC2 block size
      * it is 50 for rates 3200 and 2400 bps
      * it is 25 for rates 1600, 1400, 1300, and 1200 bps
      
## Standalone Encoding and Decoding

This code was developed as a part of [AlbertaSat](https://albertasat.ca/) under the guidance of Dr. Steven Knudsen.

Example of usage:<br>
&nbsp;&nbsp;&nbsp;&nbsp;python codec2.py -e male_8k.wav 8000 2400 encoded_male <em>(encoding)</em><br>
&nbsp;&nbsp;&nbsp;&nbsp;python codec2.py -d encoded_male 8000 2400 decoded_male <em>(decoding)</em><br>
https://obsidian.md/

## Important Notes

### Encoded Data Errors

Codec2 was developed to support compression of audio data for wireless packet data transmission. There are two main kinds of errors we expect with packet systems, which are loss of packets and corruption of packet data (bit errors).

Codec2 is resilient to bit errors. You can check this by editing the `.dat` file resulting from encoding and then using the changed file as input to the decoding GRC flow. Do not change the file length, just replace random bytes with new values. 

Codec2 is not tolerant of incorrect block lengths. For example, for the bit rate of 2400 bps, the block length is 48 (see above; 2400/50 = 48 bytes). Files encoded using this software comprise concatenated blocks of 48 bytes. If, for example, we remove the first byte from the file, the decoding operation does not work since each group of 48 bytes in the file is off by 1 byte (i.e., contains the first byte of the next block).

These considerations are important when considering how to transmit Codec2-encoded files. 

For example, in a packet based system, we must ensure that whole Codec2 blocks are sent in a packet because if a packet is dropped, the last partial block in the previous packet will either have to be dropped or will "take" part of the first block of the next packet received, causing rubbish decoding. 