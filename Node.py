import tensorflow as tf
from tensorflow.keras.layers import Layer, SeparableConv2D, Conv2D, MaxPooling2D, AveragePooling2D, UpSampling2D, BatchNormalization
from Weighted_Average_Layer import Weighted_Average
from tensorflow.keras.models import Model

# Node performs resampling, weighted averaging, convolution, batch normalization
# Node is split into Node_Upsample, Node_Downsample, Node_Downsample_Upsample
# this is to reduce repetitive operations during training process

class Node_Upsample(Model):
    def __init__(self, f, k, num_inputs=2):        
        super(Node_upsample, self).__init__()
        self.f = f
        self.k = k

        # create weighted layers when initializing
        self.w_ave = Weighted_Average(num_inputs)
        self.conv   = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last') 
        self.norm   = BatchNormalization()
        self.num_inputs = num_inputs

    def call(self, inputs):        
        # upsample all input tensors to size of first tensor
        final_shape = inputs[0].shape[2]

        for i in range(1, self.num_inputs):
            sample_factor = int(final_shape / inputs[i].shape[2])

            # interpolation for upsample
            # types = "area", "bicubic", "bilinear", "gaussian", "lanczos3", "lanczos5", "mitchellcubic", "nearest"
            # bicubic good but expensive
            if sample_factor:
                inputs[i] = UpSampling2D(size = (1, sample_factor),
                                         interpolation ='bilinear')(inputs[i])
        # weighted average
        w_ave = self.w_ave(inputs)
        # convolution
        w_conv = self.conv(w_ave)
        # return normalized convolution
        return self.norm(w_conv)
        
    def get_config(self):
        return {"f":self.f, "k":self.k, "num_inputs":self.num_inputs}


class Node_Downsample(Node_Upsample):
    def call(self, inputs):        

        # downsample all input tensors to size of first tensor
        final_shape = inputs[0].shape[2]
        for i in range(1, self.num_inputs):
            sample_factor = int(inputs[i].shape[2] / final_shape)
            
            # pooling2D to downsample
            if sample_factor:
                inputs[i] = MaxPooling2D(pool_size=(1, sample_factor), 
                                           data_format='channels_last')(inputs[i])
        # weighted average
        w_ave = self.fusion(inputs)
        # convolution
        w_conv = self.conv(w_ave)
        # return normalized convolution
        return self.norm(w_conv)


class Node_Downsample_Upsample(Node_Upsample):
    def call(self, inputs):        
        final_shape = inputs[0].shape[2]

        for i in range(1, self.num_inputs):
        
            # upsample
            if final_shape.shape[2] > inputs[i].shape[2]:
                upsample_factor = int(final_shape / inputs[1].shape[2])
                inputs[i] = UpSampling2D(size = (1, sample_factor),
                                           interpolation ='bilinear')(inputs[i])

            elif final_shape.shape[2] < inputs[i].shape[2]:
                downsample_factor = int(inputs[2].shape[2] / final_shape)
                inputs[1] = MaxPooling2D(pool_size=(1, sample_factor), data_format='channels_last')(inputs[1])

        # weighted average
        w_ave = self.fusion(inputs)
        # convolution
        w_conv = self.conv(w_ave)
        # return normalized convolution
        return self.norm(w_conv)
