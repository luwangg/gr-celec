/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_CELEC_GEN_VITERBI_FI_IMPL_H
#define INCLUDED_CELEC_GEN_VITERBI_FI_IMPL_H

#include <celec/gen_viterbi_fi.h>
#include <celec/viterbi.h>

namespace gr {
  namespace celec {

    class gen_viterbi_fi_impl : public gen_viterbi_fi
    {
     private:
      int d_n; // Inverse Coderate
      int d_k; // Constraint length
      int d_s; // Number of States
      int d_frame_size; 
      int d_start_state;
      int d_end_state;
      const std::vector<int> d_OS; // Output Symbols
      const std::vector<gr_complex> d_Table; // Tx Symbol Table

     public:
      gen_viterbi_fi_impl(const int n, const int k, const int frame_size,
                          const int start_state, const int end_state,
                          const std::vector<gr_complex> &Table, 
                          const std::vector<int> &OS);
      ~gen_viterbi_fi_impl();
      int rate() { return d_n; }
      int s() { return d_s; }
      int frame_size() { return d_frame_size; }
      int end_state() { return d_end_state; }
      int start_state() { return d_start_state; }

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace celec
} // namespace gr

#endif /* INCLUDED_CELEC_GEN_VITERBI_FI_IMPL_H */

