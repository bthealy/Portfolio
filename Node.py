import tensorflow as tf
from tensorflow.keras.layers import Layer, SeparableConv2D, Conv2D, MaxPooling2D, AveragePooling2D, UpSampling2D, BatchNormalization
from tensorflow.keras.models import Model

# Node is split into Node_Upsample, Node_Downsample
# this is to reduce redundant logic during training process

class Node_upsample(Model):
    def __init__(self, f, k, num_inputs=2):        
        super(Node_upsample, self).__init__()

        self.f = f
        self.k = k

        # create weighted layers when initializing
        self.fusion = Fast_normalized_fusion(num_inputs) 
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
        # fast normalize fusion
        fused = self.fusion(inputs)
        # convolution
        fused_conv = self.conv(fused)
        # return normalized convolution
        return self.norm(fused_conv)
        
    def get_config(self):
        return {"f":self.f, "k":self.k, "num_inputs":self.num_inputs}



class Node_downsample(Node_upsample):
    def call(self, inputs):        

        # downsample all input tensors to size of first tensor
        final_shape = inputs[0].shape[2]

        for i in range(1, self.num_inputs):
            sample_factor = int(inputs[i].shape[2] / final_shape)
            
            # pooling2D to downsample
            if sample_factor:
                inputs[i] = MaxPooling2D(pool_size=(1, sample_factor), 
                                           data_format='channels_last')(inputs[i])
        # fast normalize fusion
        fused = self.fusion(inputs)
        # convolution
        fused_conv = self.conv(fused)
        # return normalized convolution
        return self.norm(fused_conv)



class Node_downsample_and_upsample(Node_upsample):
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

        # fast normalize fusion
        fused = self.fusion(inputs)

        # convolution
        fused_conv = self.conv(fused)

        # return normalized convolution
        return self.norm(fused_conv)



class Fast_normalized_fusion(Layer):
    def __init__(self, num_inputs):        
        super(Fast_normalized_fusion, self).__init__()
        self.num_inputs = num_inputs

    def build(self, input_shapes):
        w_init = tf.random_normal_initializer()
        self.w = tf.Variable(name = 'weight',
                             initial_value = w_init(shape=(1, len(input_shapes)), 
                             dtype='float32'),
                             trainable = True)
    
    def call(self, inputs):
        num = tf.multiply(inputs[0], self.w[0][0])

        for i in range(1, self.num_inputs):
            num = tf.add(num, tf.multiply(inputs[i], self.w[0][i]))

        den = tf.reduce_sum(self.w) + 0.0001
        return tf.divide(num, den)
