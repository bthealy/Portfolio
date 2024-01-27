from tensorflow.keras.layers import (Bidirectional, Dense, Flatten, Activation,
                                     SimpleRNN, Dropout, Reshape, Permute,
                                     Conv2D, MaxPooling2D, Input, GRU,
                                     TimeDistributed, BatchNormalization)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from feature_aggregators import *


"""
-----------COPYRIGHT NOTICE STARTS WITH THIS LINE------------ Copyright (c) 2017 Tampere University of Technology and its licensors All rights reserved.

Permission is hereby granted, without written agreement and without license or royalty fees, to use and copy the code for the Sound Event Localization and Detection using Convolutional Recurrent Neural Network method/architecture, present in the GitHub repository with the handle seld-net, (“Work”) described in the paper with title "Sound event localization and detection of overlapping sources using convolutional recurrent neural network" and composed of files with code in the Python programming language. This grant is only for experimental and non-commercial purposes, provided that the copyright notice in its entirety appear in all copies of this Work, and the original source of this Work, Audio Research Group, Lab. of Signal Processing at Tampere University of Technology, is acknowledged in any publication that reports research using this Work.

Any commercial use of the Work or any part thereof is strictly prohibited. Commercial use include, but is not limited to:

selling or reproducing the Work
selling or distributing the results or content achieved by use of the Work
providing services by using the Work.
IN NO EVENT SHALL TAMPERE UNIVERSITY OF TECHNOLOGY OR ITS LICENSORS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF THIS WORK AND ITS DOCUMENTATION, EVEN IF TAMPERE UNIVERSITY OF TECHNOLOGY OR ITS LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

TAMPERE UNIVERSITY OF TECHNOLOGY AND ALL ITS LICENSORS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE WORK PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE TAMPERE UNIVERSITY OF TECHNOLOGY HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

-----------COPYRIGHT NOTICE ENDS WITH THIS LINE------------
"""


def get_model(data_in, data_out, dropout_rate, nb_cnn2d_filt, pool_size,
              rnn_size, fnn_size, classification_mode, weights):
    # model definition
    spec_start = Input(shape=(data_in[-3], data_in[-2], data_in[-1]))
    spec_cnn = spec_start

    conv_outputs = []

    for i, convCnt in enumerate(pool_size):
        spec_cnn = Conv2D(filters=nb_cnn2d_filt, kernel_size=(3, 3), padding='same', data_format="channels_last")(spec_cnn)
        spec_cnn = BatchNormalization()(spec_cnn)
        spec_cnn = Activation('relu')(spec_cnn)
        spec_cnn = MaxPooling2D(pool_size=(1, pool_size[i]), data_format="channels_last")(spec_cnn)
        spec_cnn = Dropout(dropout_rate)(spec_cnn)
        conv_outputs.append(spec_cnn)

    agg_cnn = PANet(nb_cnn2d_filt, 1)(conv_outputs)

    spec_rnn = Permute((2, 1, 3))(agg_cnn[-1])
    spec_rnn = Reshape((data_in[-2], -1))(spec_rnn)

    for nb_rnn_filt in rnn_size:
        spec_rnn = Bidirectional(GRU(nb_rnn_filt, 
                                     activation='tanh', 
                                     dropout=dropout_rate, 
                                     recurrent_dropout=dropout_rate,
                                     return_sequences=True),
                                merge_mode='mul')(spec_rnn)

    shared_doa_sed = spec_rnn
    for nb_fnn_filt in fnn_size:
        shared_doa_sed = TimeDistributed(Dense(nb_fnn_filt))(shared_doa_sed)
        shared_doa_sed = Dropout(dropout_rate)(shared_doa_sed)

    doa = TimeDistributed(Dense(data_out[1][-1], activation='tanh'), name='doa_out')(shared_doa_sed)
    sed = TimeDistributed(Dense(data_out[0][-1], activation='sigmoid'), name='sed_out')(shared_doa_sed)

    model = Model(inputs=spec_start, outputs=[sed, doa])
    model.compile(optimizer=Adam(), loss=['binary_crossentropy', 'mse'], loss_weights=weights)

    model.summary()
    return model
