#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 Jan Krämer.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks, digital, analog, trellis
import celec_swig as celec
import numpy


fsm_args = {"awgn1o2_8": (2, 8, 4,
        (0, 4, 0, 4, 1, 5, 1, 5, 2, 6, 2, 6, 3, 7, 3, 7),
        (0, 3, 3, 0, 1, 2, 2, 1, 3, 0, 0, 3, 2, 1, 1, 2),
        ), 
      "awgn1o2_16": ( 2,16,4,
        (0, 8, 0, 8, 1, 9, 1, 9, 2, 10, 2, 10, 3, 11, 3, 11, 4, 12, 4, 12, 5, 13, 5, 13, 6, 14, 6, 14, 7, 15, 7, 15),
        (0, 3, 3, 0, 1, 2, 2, 1, 1, 2, 2, 1, 0, 3, 3, 0, 2, 1, 1, 2, 3, 0, 0, 3, 3, 0, 0, 3, 2, 1, 1, 2)),
        }  

class qa_gen_viterbi_fi (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # Trellislength
        K = 3072               # Bit in one packet
        n = 2                  # Bit in codeword
        k = 5                  # Constraint length
        start_state = 0
        end_state = -1         # Endstate not defined 
        fsm = fsm_args["awgn1o2_16"]

        ## setup dummy data
        os = numpy.array(fsm[4], dtype=int) # Encoder output matrix
        data = numpy.random.randint(0,2,K) # Create 0s and 1s

        sym_table = digital.constellation_qpsk()

        # Setup blocks
        data_src = blocks.vector_source_s(map(int, data))
        src_head = blocks.head(gr.sizeof_short*1, K)
        
        # TX Sim
        encoder = trellis.encoder_ss(trellis.fsm(*fsm), 0)
        modulator = digital.chunks_to_symbols_sc(sym_table.points(), 1)

        # Decoder
        viterbi_cel = celec.gen_viterbi_fi(n, k, K, start_state, end_state, 
                                           sym_table.points(), os)

        # Sinks
        rx_sink = blocks.vector_sink_b(1)
        
        # Connections
        self.tb.connect(data_src, src_head, encoder)
        self.tb.connect(encoder, modulator)
        self.tb.connect(modulator, viterbi_cel)
        self.tb.connect(viterbi_cel, rx_sink)
        self.tb.run ()
        
        # # Check data
        rx_output = numpy.array(rx_sink.data())
        for k in range(0, K):
            self.assertEqual(int(rx_output[k]), int(data[k]))

if __name__ == '__main__':
    gr_unittest.run(qa_gen_viterbi_fi, "qa_gen_viterbi_fi.xml")
