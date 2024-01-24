import tensorflow as tf
from tensorflow.keras.layers import (Layer, SeparableConv2D, Conv2D, 
                                     MaxPooling2D, UpSampling2D, 
                                     BatchNormalization)
from weighted_average_layer import WeightedAverage  # You might need to adjust the import path based on your project structure.
from tensorflow.keras.models import Model


"""
Node Classes for feature aggregation in TensorFlow.

Nodes for different type of resampling are split to improve efficiency and reduce the need for 
repeated tensor size comparisons during aggregation operations.

Custom Node Classes:
- NodeUpsample: Performs upsample, weighted averaging, convolution, and batch normalization. 
The inputs are upsampled to the size of the first input tensor.

- NodeDownsample: A subclass of NodeUpsample, performs downsample, weighted averaging, convolution, and batch normalization. 
The inputs are downsampled to the size of the first input tensor.

- NodeDownsampleUpsample: A subclass of NodeUpsample, performs both downsample and upsample operations, weighted averaging, convolution, and batch normalization. 
Adjusts input tensors to match the size of the first input tensor.

- NodeIntermediateScale: A subclass of NodeUpsample, performs resizing, weighted averaging, convolution, and batch normalization. 
Adjusts input tensors to an intermediate scale based on the average of their sizes.

Usage:
1. Import the custom node classes from this script.
2. Initialize the desired node class with the required parameters (e.g., number of filters, kernel size, number of inputs).
3. Include these custom nodes in your SELD neural network architecture as needed.

Example:
```python
import tensorflow as tf
from CustomNodeClasses import NodeUpsample, NodeDownsample, NodeDownsampleUpsample, NodeIntermediateScale

# Initialize the custom node classes with appropriate parameters
upsample_node = Nod_Upsample(f=64, k=3, num_inputs=3)
downsample_node = NodeDownsample(f=64, k=3, num_inputs=3)
downsample_upsample_node = NodeDownsampleUpsample(f=64, k=3, num_inputs=3)
intermediate_scale_node = NodeIntermediateScale(f=64, k=3, num_inputs=2)

# Build your neural network and add these custom nodes as layers.
# Compile and train your model as needed."""


class NodeUpsample(Model):
    def __init__(self, f, k, num_inputs=2):
        """
        Constructor for the NodeUpsample class.

        Args:
            f (int): Number of filters for convolution.
            k (int): Size of the convolution kernel.
            num_inputs (int): Number of input tensors to the node.

        Initializes the NodeUpsample with the specified parameters and creates the necessary layers.
        """
        super(NodeUpsample, self).__init__()
        self.f = f
        self.k = k
        self.w_ave = WeightedAverage(num_inputs)  # Weighted Average Layer
        self.conv = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last')
        self.norm = BatchNormalization()
        self.num_inputs = num_inputs

    def call(self, inputs):
        """
        Call method for the NodeUpsample class.

        Args:
            inputs (list of tf.Tensor): List of input tensors to be processed.

        Performs upsample, weighted averaging, convolution, and batch normalization operations.
        Returns the normalized convolution result.
        """
        # Upsample all input tensors to the size of the first tensor
        final_shape = inputs[0].shape[2]
        for i in range(1, self.num_inputs):
            sample_factor = int(final_shape / inputs[i].shape[2])
            if sample_factor:
                inputs[i] = UpSampling2D(size=(1, sample_factor), interpolation='bilinear')(tf.identity(inputs[i]))

        # Weighted average
        w_ave = self.w_ave(inputs)
        # Convolution
        w_conv = self.conv(w_ave)
        # Return normalized convolution
        return self.norm(w_conv)

    def get_config(self):
        return {"f": self.f, "k": self.k, "num_inputs": self.num_inputs}


class NodeDownsample(NodeUpsample):
    def call(self, inputs):
        """
        Call method for the NodeDownsample class, which is a subclass of NodeUpsample.

        Args:
            inputs (list of tf.Tensor): List of input tensors to be processed.

        Performs downsample, weighted averaging, convolution, and batch normalization operations.
        Returns the normalized convolution result.
        """
        final_shape = inputs[0].shape[2]
        for i in range(1, self.num_inputs):
            sample_factor = int(inputs[i].shape[2] / final_shape)
            if sample_factor > 1:
                inputs[i] = MaxPooling2D(pool_size=(1, sample_factor), data_format='channels_last')(tf.identity(inputs[i]))

        # Weighted average
        w_ave = self.w_ave(inputs)
        # Convolution
        w_conv = self.conv(w_ave)
        # Return normalized convolution
        return self.norm(w_conv)


class NodeDownsampleUpsample(NodeUpsample):
    def call(self, inputs):
        """
        Call method for the NodeDownsampleUpsample class, which is a subclass of NodeUpsample.

        Args:
            inputs (list of tf.Tensor): List of input tensors to be processed.

        Performs both downsample and upsample operations, weighted averaging, convolution, and batch normalization.
        Returns the normalized convolution result.
        """
        for i in range(1, self.num_inputs):
            height = inputs[0].shape[1]
            width = inputs[0].shape[2]

            inputs[i] = tf.keras.layers.Resizing(height, width, interpolation='bilinear',
                                                 crop_to_aspect_ratio=False)(tf.identity(inputs[i]))

        # Weighted average
        w_ave = self.w_ave(inputs)
        # Convolution
        w_conv = self.conv(w_ave)
        # Return normalized convolution
        return self.norm(w_conv)


class NodeIntermediateScale(NodeUpsample):
    def call(self, inputs):
        """
        Call method for the NodeIntermediateScale class, which is a subclass of NodeUpsample.

        Args:
            inputs (list of tf.Tensor): List of input tensors to be processed.

        Performs resizing, weighted averaging, convolution, and batch normalization.
        Returns the normalized convolution result.
        """
        height = int(round((inputs[0].shape[1] + inputs[1].shape[1]) / 2, 0))
        width = int(round((inputs[0].shape[2] + inputs[1].shape[2]) / 2, 0))
        for i in range(2):
            inputs[i] = tf.keras.layers.Resizing(height, width, interpolation='bilinear',
                                                 crop_to_aspect_ratio=False)(tf.identity(inputs[i]))

        # Weighted average
        w_ave = self.w_ave(inputs)
        # Convolution
        w_conv = self.conv(w_ave)
        # Return normalized convolution
        return self.norm(w_conv)
