# Parameters used in the feature extraction, neural network model, and training the SELDnet can be changed here.
#
# Ideally, do not change the values of the default parameters. Create separate cases with unique <task-id> as seen in
# the code below (if-else loop) and use them. This way you can easily reproduce a configuration on a later time.

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


def get_params(argv):
    print("SET: {}".format(argv))
    # ########### default parameters ##############
    params = dict(
        quick_test = False, #True, # To do quick test. Trains/test on small subset of dataset
        azi_only   = True,      # Estimate Azimuth only

        # Dataset loading parameters
        dataset= 'real', #'ansim',    # Dataset to use: ansim, resim, cansim, cresim, real, mansim or mreal
        overlap=1,         # maximum number of overlapping sound events [1, 2, 3]
        split=1,           # Cross validation split [1, 2, 3]
        db=30,             # SNR of sound events.
        nfft=512,          # FFT/window length size

        # DNN Model parameters
        sequence_length=512,        # Feature sequence length
        batch_size=16,              # Batch size
        dropout_rate=0.0,           # Dropout rate, constant for all layers
        nb_cnn2d_filt=64,           # Number of CNN nodes, constant for each layer
        pool_size=[8, 8, 2],        # CNN pooling, length of list = number of CNN layers, list value = pooling per layer
        rnn_size=[128, 128],        # RNN contents, length of list = number of layers, list value = number of nodes
        fnn_size=[128],             # FNN contents, length of list = number of layers, list value = number of nodes
        loss_weights=[1., 50.],     # [sed, doa] weight for scaling the DNN outputs
        xyz_def_zero=True,          # Use default DOA Cartesian value x,y,z = 0,0,0
        nb_epochs=1000,             # Train for maximum epochs

        # Not important
        mode='regr',        # Only regression ('regr') supported as of now
        nb_cnn3d_filt=32,   # For future. Not relevant for now
        cnn_3d=False,       # For future. Not relevant for now
        weakness=0          # For future. Not relevant for now
    )
    params['patience'] = int(0.1 * params['nb_epochs'])     # Stop training if patience reached

    # ########### User defined parameters ##############
    if argv == '1':
        print("USING DEFAULT PARAMETERS\n")

    # Quick test
    elif argv == '999':
        print("QUICK TEST MODE\n")
        params['quick_test'] = True
        params['nb_epochs'] = 2

    # Different datasets
    elif argv == '2':  # anechoic simulated Ambisonic data set
        params['dataset'] = 'ansim'
        params['sequence_length'] = 512

    elif argv == '3':  # reverberant simulated Ambisonic data set
        params['dataset'] = 'resim'
        params['sequence_length'] = 256

    elif argv == '4':  # anechoic simulated circular-array data set
        params['dataset'] = 'cansim'
        params['sequence_length'] = 256

    elif argv == '5':  # reverberant simulated circular-array data set
        params['dataset'] = 'cresim'
        params['sequence_length'] = 256

    elif argv == '6':  # real-life Ambisonic data set
        params['dataset'] = 'real'
        params['sequence_length'] = 512

    # anechoic circular array data set split 1, overlap 3
    elif argv == '7':  #
        params['dataset'] = 'cansim'
        params['overlap'] = 3
        params['split'] = 1

    # anechoic Ambisonic data set with sequence length 64 and batch size 32
    elif argv == '8':  #
        params['dataset'] = 'ansim'
        params['sequence_length'] = 64
        params['batch_size'] = 32

    else:
        print('ERROR: unknown argument {}'.format(argv))
        exit()

    for key, value in params.items():
        print("{}: {}".format(key, value))
    return params
