import numpy as np
import matplotlib.pyplot as plot
import time
plot.switch_backend('agg')
import pickle
import evaluation_metrics
import cls_data_generator

#%% load training / test data


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


def load_data_gens(params):
    data_gen_train = cls_data_generator.DataGenerator(
        dataset=params['dataset'], ov=params['overlap'], split=params['split'], db=params['db'], nfft=params['nfft'],
        batch_size=params['batch_size'], seq_len=params['sequence_length'], classifier_mode=params['mode'],
        weakness=params['weakness'], datagen_mode='train', cnn3d=params['cnn_3d'], xyz_def_zero=params['xyz_def_zero'],
        azi_only=params['azi_only']
    )

    data_gen_test = cls_data_generator.DataGenerator(
        dataset=params['dataset'], ov=params['overlap'], split=params['split'], db=params['db'], nfft=params['nfft'],
        batch_size=params['batch_size'], seq_len=params['sequence_length'], classifier_mode=params['mode'],
        weakness=params['weakness'], datagen_mode='test', cnn3d=params['cnn_3d'], xyz_def_zero=params['xyz_def_zero'],
        azi_only=params['azi_only'], shuffle=False
    )

    return data_gen_train, data_gen_test


#%% load / save subtraining data
def save_subtraining_results(dic_name, dictionary):
    with open(f'{dic_name}.pkl', 'wb') as f:
        pickle.dump(dictionary, f)


def load_subtraining_results(dic_name):
    with open(f'{dic_name}.pkl', 'rb') as f:
        dictionary = pickle.load(f)
        
    return dictionary


#%% label collection, plot function
def collect_test_labels(_data_gen_test, _data_out, classification_mode, quick_test):
    # Collecting ground truth for test data
    nb_batch = 2 if quick_test else _data_gen_test.get_total_batches_in_data()

    batch_size = _data_out[0][0]
    gt_sed = np.zeros((nb_batch * batch_size, _data_out[0][1], _data_out[0][2]))
    gt_doa = np.zeros((nb_batch * batch_size, _data_out[0][1], _data_out[1][2]))

    print("nb_batch in test: {}".format(nb_batch))
    cnt = 0
    for tmp_feat, tmp_label in _data_gen_test.generate():
        gt_sed[cnt * batch_size:(cnt + 1) * batch_size, :, :] = tmp_label[0]
        gt_doa[cnt * batch_size:(cnt + 1) * batch_size, :, :] = tmp_label[1]
        cnt = cnt + 1
        if cnt == nb_batch:
            break
    return gt_sed.astype(int), gt_doa


# def plot_functions(fig_name, nb_epochs, _tr_loss, _val_loss, _sed_loss, _doa_loss, _epoch_metric_loss):
#     plot.figure()
#
#     plot.subplot(311)
#     plot.plot(range(nb_epoch), _tr_loss[:nb_epochs], label='train loss')
#     plot.plot(range(nb_epoch), _val_loss[:nb_epochs], label='val loss')
#     plot.legend()
#     plot.grid(True)
#
#     plot.subplot(312)
#     plot.plot(range(nb_epoch), _epoch_metric_loss[:nb_epochs], label='metric')
#     plot.plot(range(nb_epoch), _sed_loss[:, 0][:nb_epochs], label='er')
#     plot.plot(range(nb_epoch), _sed_loss[:, 1][:nb_epochs], label='f1')
#     plot.legend()
#     plot.grid(True)
#
#     plot.subplot(313)
#     plot.plot(range(nb_epoch), _doa_loss[:, 1][:nb_epochs], label='gt_thres')
#     plot.plot(range(nb_epoch), _doa_loss[:, 2][:nb_epochs], label='pred_thres')
#     plot.legend()
#     plot.grid(True)
#
#     plot.savefig(fig_name)
#     plot.close()

def plot_functions(fig_name, _tr_loss, _val_loss, _sed_loss, _doa_loss, _epoch_metric_loss):
    plot.figure()
    nb_epoch = len(_tr_loss)
    plot.subplot(311)
    plot.plot(range(nb_epoch), _tr_loss, label='train loss')
    plot.plot(range(nb_epoch), _val_loss, label='val loss')
    plot.legend()
    plot.grid(True)

    plot.subplot(312)
    plot.plot(range(nb_epoch), _epoch_metric_loss, label='metric')
    plot.plot(range(nb_epoch), _sed_loss[:, 0], label='er')
    plot.plot(range(nb_epoch), _sed_loss[:, 1], label='f1')
    plot.legend()
    plot.grid(True)

    plot.subplot(313)
    plot.plot(range(nb_epoch), _doa_loss[:, 1], label='gt_thres')
    plot.plot(range(nb_epoch), _doa_loss[:, 2], label='pred_thres')
    plot.legend()
    plot.grid(True)

    plot.savefig(fig_name)
    plot.close()




#%% Evaluate / Update

def epoch_evaluation(params, pred, sed_loss, epoch_cnt, sed_gt, data_gen_test, doa_loss, doa_gt, epoch_metric_loss):
    if params['mode'] == 'regr':
            sed_pred = evaluation_metrics.reshape_3Dto2D(pred[0]) > 0.5
            doa_pred = evaluation_metrics.reshape_3Dto2D(pred[1])

            sed_loss[epoch_cnt, :] = evaluation_metrics.compute_sed_scores(sed_pred, 
                                                                            sed_gt, 
                                                                            data_gen_test.nb_frames_1s())
            if params['azi_only']:
                doa_loss[epoch_cnt, :], conf_mat = evaluation_metrics.compute_doa_scores_regr_xy(doa_pred, doa_gt,
                                                                                                 sed_pred, sed_gt)
            else:
                doa_loss[epoch_cnt, :], conf_mat = evaluation_metrics.compute_doa_scores_regr_xyz(doa_pred, doa_gt,
                                                                                                  sed_pred, sed_gt)

            epoch_metric_loss[epoch_cnt] = np.mean([sed_loss[epoch_cnt, 0],
                                                    1-sed_loss[epoch_cnt, 1],
                                                    2*np.arcsin(doa_loss[epoch_cnt, 1]/2.0)/np.pi,
                                                    1 - (doa_loss[epoch_cnt, 5] / float(doa_gt.shape[0]))])
            
    return sed_loss, doa_loss, epoch_metric_loss, conf_mat


def update_best(best_metric, epoch_metric_loss, epoch_cnt, conf_mat, model, unique_name, best_conf_mat, best_epoch, patience_cnt):
    if epoch_metric_loss[epoch_cnt] < best_metric:
            best_metric   = epoch_metric_loss[epoch_cnt]
            best_conf_mat = conf_mat
            best_epoch    = model.epochs_trained
            #model.save(f'{unique_name}_model.h5')
            patience_cnt = 0

    return best_metric, best_conf_mat, best_epoch, patience_cnt



#%% Printing

def print_model_parameters(params):
    print(
        "\nMODEL:\n"
        f"\tdropout_rate: {params['dropout_rate']}\n\n"
        f"\tCNN: \n"
        f"\t  nb_cnn_filt: {params['nb_cnn3d_filt'] if params['cnn_3d'] else params['nb_cnn2d_filt']}\n"
        f"\t  pool_size: {params['pool_size']}\n\n"
        f"\trnn_size:  {params['rnn_size']}\n"
        f"\tfnn_size:  {params['fnn_size']}\n"
    )


def print_epoch_output(epoch_cnt, start, tr_loss, val_loss, sed_loss, doa_loss, sed_gt, epoch_metric_loss, best_metric, best_epoch):
    print(
            'epoch_cnt: %d, time: %.2fs, tr_loss: %.2f, val_loss: %.2f, '
            'F1_overall: %.2f, ER_overall: %.2f, '
            'doa_error_gt: %.2f, doa_error_pred: %.2f, good_pks_ratio:%.2f, '
            'error_metric: %.2f, best_error_metric: %.2f, best_epoch : %d' %
            (
                epoch_cnt, time.time() - start, tr_loss[epoch_cnt], val_loss[epoch_cnt],
                sed_loss[epoch_cnt, 1], sed_loss[epoch_cnt, 0],
                doa_loss[epoch_cnt, 1], doa_loss[epoch_cnt, 2], doa_loss[epoch_cnt, 5] / float(sed_gt.shape[0]),
                epoch_metric_loss[epoch_cnt], best_metric, best_epoch
            )
        )


def print_final_outputs(best_conf_mat, best_epoch, best_metric, doa_loss, sed_gt, sed_loss, unique_name):
    print(f'best_conf_mat : {best_conf_mat}')
    print(f'best_conf_mat_diag : {np.diag(best_conf_mat)}')
    print(f'saved model for the best_epoch: {best_epoch} with best_metric: {best_metric}')
    print(f'DOA Metrics: doa_loss_gt: {doa_loss[best_epoch, 1]}, '
          f'doa_loss_pred: {doa_loss[best_epoch, 2]}, '
          f'good_pks_ratio: {doa_loss[best_epoch, 5] / float(sed_gt.shape[0])}')
    print(f'SED Metrics: F1_overall: {sed_loss[best_epoch, 1]}, '
          f'ER_overall: {sed_loss[best_epoch, 0]}')
    print(f'unique_name: {unique_name}')


def print_input_warning(argv):
     if len(argv) != 3:
        print('\n\n')
        print('-------------------------------------------------------------------------------------------------------')
        print('The code expected two inputs')
        print('\t>> python seld.py <job-id> <task-id>')
        print('\t\t<job-id> is a unique identifier which is used for output filenames (models, training plots). '
              'You can use any number or string for this.')
        print('\t\t<task-id> is used to choose the user-defined parameter set from parameter.py')
        print('Using default inputs for now')
        print('-------------------------------------------------------------------------------------------------------')
        print('\n\n')

