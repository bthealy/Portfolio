# Extracts the features, labels, and normalizes the training and test split features. Make sure you update the location
# of the downloaded datasets before in the cls_feature_class.py

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

import cls_feature_class

dataset_name = 'real'  # Datasets: ansim, resim, cansim, cresim, real, mansim and mreal

# Extracts feature and labels for all overlap and splits
for ovo in [1]: #[1, 2, 3]:  # SE overlap. Change to [1] if you are only calculating the features for overlap 1.
    for splito in [1]: #[1, 2, 3]:    # all splits. Use [1, 8, 9] for 'real' and 'mreal' datasets. Change to [1] if you are only calculating features for split 1.
        for nffto in [512]: # For now use 512 point FFT. Once you get the code running, you can play around with this.
            feat_cls = cls_feature_class.FeatureClass(ov=ovo, split=splito, nfft=nffto, dataset=dataset_name)

            # Extract features and normalize them
            feat_cls.extract_all_feature()
            feat_cls.preprocess_features()

            # # Extract labels in regression mode
            feat_cls.extract_all_labels('regr', 0)
