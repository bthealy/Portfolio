#
# A wrapper script that trains the SELDnet. The training stops when the SELD error (check paper) stops improving.
#

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
tf.keras.backend.set_image_data_format("channels_last")
import sys
import matplotlib.pyplot as plot
import keras_model
import parameter
import utils
plot.switch_backend('agg')
from seld_functions import *


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


def main(argv):
    """
    Main wrapper for training sound event localization and detection network.
    
    :param argv: expects two optional inputs. 
        first input: job_id - (optional) all the output files will be uniquely represented with this. (default) 1
        second input: task_id - (optional) To chose the system configuration in parameters.py. 
                                (default) uses default parameters
    """
    if len(argv) != 3:
        print('\n\n\n-------------------------------------------------------------------------------------------------------')
        print('The code expected two inputs')
        print('\t>> python seld.py <job-id> <task-id>')
        print('\t\t<job-id> is a unique identifier which is used for output filenames (models, training plots). '
              'You can use any number or string for this.')
        print('\t\t<task-id> is used to choose the user-defined parameter set from parameter.py')
        print('Using default inputs for now')
        print('-------------------------------------------------------------------------------------------------------\n\n\n')

    # use parameter set defined by user
    task_id = '1' if len(argv) < 3 else argv[-1]
    params = parameter.get_params(task_id)

    job_id = 1 if len(argv) < 2 else argv[1]

    model_dir = 'models/'
    utils.create_folder(model_dir)
    
    unique_name = '{}_ov{}_split{}_{}{}_3d{}_{}'.format(
        params['dataset'], params['overlap'], params['split'], params['mode'], params['weakness'],
        int(params['cnn_3d']), job_id)

    unique_name = os.path.join(model_dir, unique_name)
    print("unique_name: {}\n".format(unique_name))

    data_gen_train, data_gen_test = load_data_gens(params)
    data_in, data_out = data_gen_train.get_data_sizes()

    print('FEATURES:\n'
          '\tdata_in: {}\n'
          '\tdata_out: {}\n'.format(data_in, data_out))

    gt = collect_test_labels(data_gen_test, data_out, params['mode'], params['quick_test'])
    sed_gt = evaluation_metrics.reshape_3Dto2D(gt[0])
    doa_gt = evaluation_metrics.reshape_3Dto2D(gt[1])

    print(
        'MODEL:\n'
        '\tdropout_rate: {}\n'
        '\tCNN: nb_cnn_filt: {}, pool_size{}\n'
        '\trnn_size: {}, fnn_size: {}\n'.format(
            params['dropout_rate'],
            params['nb_cnn3d_filt'] if params['cnn_3d'] else params['nb_cnn2d_filt'], params['pool_size'],
            params['rnn_size'], params['fnn_size']))

    model = keras_model.get_model(data_in=data_in, data_out=data_out, dropout_rate=params['dropout_rate'],
                                  nb_cnn2d_filt=params['nb_cnn2d_filt'], pool_size=params['pool_size'],
                                  rnn_size=params['rnn_size'], fnn_size=params['fnn_size'],
                                  classification_mode=params['mode'], weights=params['loss_weights'])
    best_metric = 99999
    conf_mat = None
    best_conf_mat = None
    best_epoch = -1
    patience_cnt = 0
    epoch_metric_loss = np.zeros(params['nb_epochs'])
    tr_loss = np.zeros(params['nb_epochs'])
    val_loss = np.zeros(params['nb_epochs'])
    doa_loss = np.zeros((params['nb_epochs'], 6))
    sed_loss = np.zeros((params['nb_epochs'], 2))
    nb_epoch = 2 if params['quick_test'] else params['nb_epochs']

    # Train model
    for epoch_cnt in range(nb_epoch):
        start = time.time()
        data_gen_train_samples = data_gen_train.generate()
        data_gen_test_samples = data_gen_test.generate()

        hist = model.fit(
            x=data_gen_train_samples,
            steps_per_epoch=2 if params['quick_test'] else data_gen_train.get_total_batches_in_data(),
            validation_data=data_gen_test_samples,
            validation_steps=2 if params['quick_test'] else data_gen_test.get_total_batches_in_data(),
            epochs=1,
            verbose=0
        )

        tr_loss[epoch_cnt] = hist.history['loss'][0]
        val_loss[epoch_cnt] = hist.history['val_loss'][0]

        pred = model.predict(
            x=data_gen_test_samples,
            steps=2 if params['quick_test'] else data_gen_test.get_total_batches_in_data(),
            verbose=2
        )

        if params['mode'] == 'regr':
            sed_pred = evaluation_metrics.reshape_3Dto2D(pred[0]) > 0.5
            doa_pred = evaluation_metrics.reshape_3Dto2D(pred[1])

            sed_loss[epoch_cnt, :] = evaluation_metrics.compute_sed_scores(sed_pred, sed_gt,
                                                                           data_gen_test.nb_frames_1s())
            if params['azi_only']:
                doa_loss[epoch_cnt, :], conf_mat = evaluation_metrics.compute_doa_scores_regr_xy(doa_pred, doa_gt,
                                                                                                 sed_pred, sed_gt)
            else:
                doa_loss[epoch_cnt, :], conf_mat = evaluation_metrics.compute_doa_scores_regr_xyz(doa_pred, doa_gt,
                                                                                                  sed_pred, sed_gt)
            epoch_metric_loss[epoch_cnt] = np.mean([
                sed_loss[epoch_cnt, 0],
                1 - sed_loss[epoch_cnt, 1],
                2 * np.arcsin(doa_loss[epoch_cnt, 1] / 2.0) / np.pi,
                1 - (doa_loss[epoch_cnt, 5] / float(doa_gt.shape[0]))
            ])

        plot_functions(unique_name, tr_loss, val_loss, sed_loss, doa_loss, epoch_metric_loss)

        patience_cnt += 1
        if epoch_metric_loss[epoch_cnt] < best_metric:
            best_metric = epoch_metric_loss[epoch_cnt]
            best_conf_mat = conf_mat
            best_epoch = epoch_cnt
            model.save(f'{unique_name}_model.h5')
            patience_cnt = 0

        print(f'epoch_cnt: {epoch_cnt}, time: {time.time() - start:.2f}s, tr_loss: {tr_loss[epoch_cnt]:.2f}, '
              f'val_loss: {val_loss[epoch_cnt]:.2f}, F1_overall: {sed_loss[epoch_cnt, 1]:.2f}, '
              f'ER_overall: {sed_loss[epoch_cnt, 0]:.2f}, doa_error_gt: {doa_loss[epoch_cnt, 1]:.2f}, '
              f'doa_error_pred: {doa_loss[epoch_cnt, 2]:.2f}, good_pks_ratio: {doa_loss[epoch_cnt, 5] / float(sed_gt.shape[0]):.2f}, '
              f'error_metric: {epoch_metric_loss[epoch_cnt]:.2f}, best_error_metric: {best_metric:.2f}, best_epoch: {best_epoch}')

        if patience_cnt > params['patience']:
            break

    print('best_conf_mat:', best_conf_mat)
    print('best_conf_mat_diag:', np.diag(best_conf_mat))
    print(f'saved model for the best_epoch: {best_epoch} with best_metric: {best_metric},')
    print('DOA Metrics: doa_loss_gt: {}, doa_loss_pred: {}, good_pks_ratio: {}'.format(
        doa_loss[best_epoch, 1], doa_loss[best_epoch, 2], doa_loss[best_epoch, 5] / float(sed_gt.shape[0])))
    print('SED Metrics: F1_overall: {}, ER_overall: {}'.format(sed_loss[best_epoch, 1], sed_loss[best_epoch, 0]))
    print('unique_name:', unique_name)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (ValueError, IOError) as e:
        sys.exit(e)
