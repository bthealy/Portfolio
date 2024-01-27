import tensorflow as tf
from tensorflow.keras.layers import Layer


"""
Feature Aggregation with Weighted Average Layer

This script defines a custom layer 'Weighted_Average' using TensorFlow/Keras. 
The purpose of this layer is to perform feature aggregation through weighted averaging. 

The 'Weighted_Average' layer takes a specified number of input elements and learns a weight parameter 'w' to perform weighted averaging. 
The weight parameter 'w' is initialized with random values and is updated during training. 
The layer's main function is to compute the weighted average of the input data based on these learned weights. 
It normalizes the result by dividing it by the sum of the weights plus a small value to prevent division by zero.

Example:
```python
import tensorflow as tf
from tensorflow.keras.layers import Layer
from your_custom_module import Weighted_Average

# Build your SELD neural network model and add the 'Weighted_Average' layer
model = tf.keras.Sequential([
    # Add your input layers and other layers here
    Weighted_Average(num_inputs),
    # Add more layers as needed
])"""


class WeightedAverage(Layer):
    def __init__(self, num_inputs):
        """
        Constructor for the Weighted_Average layer.

        Args:
            num_inputs (int): Number of input elements to be averaged.

        Initializes the Weighted_Average layer with the specified number of inputs.
        """
        super(WeightedAverage, self).__init__()
        self.num_inputs = num_inputs

    def build(self, input_shapes):
        """
        Build method for the Weighted_Average layer.

        Args:
            input_shapes (tf.TensorShape): The shape of the input data.

        This method initializes the weight parameter 'w' with random values.
        'w' is a learnable parameter used for weighted averaging.
        """
        w_init = tf.random_normal_initializer()
        self.w = self.add_weight(name='weight',
                                shape=(self.num_inputs,),
                                initializer=w_init,
                                trainable=True)

    def call(self, inputs):
        """
        Call method for the Weighted_Average layer.

        Args:
            inputs (tf.Tensor): Input data to be averaged.

        Computes the weighted average of the input data based on the learned weights.
        The result is normalized by dividing by the sum of the weights plus a small value.

        Returns:
            tf.Tensor: The weighted average of the input data.
        """
        if self.num_inputs == 2:
            weighted_inputs = tf.multiply(inputs[0], self.w[0]) + tf.multiply(inputs[1], self.w[1])

        elif self.num_inputs == 3:
            weighted_inputs = tf.multiply(inputs[0], self.w[0]) + tf.multiply(inputs[1], self.w[1]) + tf.multiply(inputs[2], self.w[2])

        den = tf.reduce_sum(self.w) + 0.0001
        return tf.divide(weighted_inputs, den)


