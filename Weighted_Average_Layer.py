import tensorflow as tf
from tensorflow.keras.layers import Layer

class Weighted_Average(Layer):
    def __init__(self, num_inputs):
        super(Weighted_Average, self).__init__()
        self.num_inputs = num_inputs

    def build(self, input_shapes):
        w_init = tf.random_normal_initializer()
        self.w = tf.Variable(name = 'weight',
                             initial_value = w_init(shape=(1, len(input_shapes)),
                             dtype='float32'),
                             trainable = True)

    def call(self, inputs):
        weighted_inputs = tf.tensordot(inputs, self.w[0], axes=1)
        den = tf.reduce_sum(self.w) + 0.0001
        return tf.divide(weighted_inputs, den)