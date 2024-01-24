from node import NodeUpsample, NodeDownsample, NodeDownsampleUpsample, NodeIntermediateScale
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, SeparableConv2D
from tensorflow.keras.models import Model

"""
Feature Aggregator Classes for Multi-Scale Neural Networks

This script provides a framework for creating your own custom feature aggregators for multi-scale neural networks. 
Additionally, it offers pre-made aggregators for your convenience.

1) How to Create Your Own Aggregator:
   Follow the format in the pre-made aggregators below

   Summary:
   - Define a new Python class that inherits from 'tf.keras.models.Model.'
   - In the constructor, specify the parameters and nodes for your aggregator.
   - Define the node connection design in the 'call' method.
   - Use the 'get_config' method for configuration details (necessary for saving/loading the model).
   - Integrate your custom aggregator into your network architecture.

2) Pre-Made Aggregators:
   This script includes several pre-made feature aggregator classes:
   - BiFPN (Bilateral Feature Pyramid Network)
   - FPN (Feature Pyramid Network)
   - PANet (Path Aggregation Network)
   - SEN_1 (Scale Encoder Network with N=1)
   - SEN_2 (Scale Encoder Network with N=2)

Usage:
1) Import the custom aggregator classes from this script into your multi-scale neural network project.
2) Initialize the desired aggregator class with the required parameters.
3) Include these custom aggregators in your network architecture as needed.
4) During training and inference, the custom aggregators will efficiently combine features from different network layers.

Example:
```python
import tensorflow as tf
from CustomAggregatorClasses import YourCustomAggregator, BiFPN, FPN, PANet, SEN_1, SEN_2

# Initialize the pre-made or your custom aggregator classes with appropriate parameters.
custom_aggregator = YourCustomAggregator(f=64, k=3)
bifpn = BiFPN(f=64, k=3)
fpn = FPN(f=64, k=3)
panet = PANet(f=64, k=3)
sen1 = SEN_1(f=64, k=3)
sen2 = SEN_2(f=64, k=3)

# Build your multi-scale neural network model and add these aggregators as layers.
"""



class BiFPN(Model):
    def __init__(self, f, k):
        """
        Constructor for the BiFPN class.

        Args:
            f (int): Number of filters for convolution.
            k (int): Size of the convolution kernel.
            last (bool): Whether this is the last BiFPN in the network.

        Initializes the BiFPN with the specified parameters and creates the necessary nodes.
        """
        super(BiFPN, self).__init__()
        self.f = f
        self.k = k

        self.P2_1 = NodeUpsample(f, k)
        self.P1 = NodeUpsample(f, k)
        self.P2_2 = NodeDownsample(f, k)
        self.P3 = NodeDownsample(f, k)

    def call(self, conv_outputs):
        """
        Call method for the BiFPN class.

        Args:
            conv_outputs (list of tf.Tensor): List of convolution outputs from different layers.

        Performs data flow as illustrated below:

        # C3 ------------> P3 --->
        # ^   ____|______   ^
        # |  /    v      \  |
        # C2 --> P2_1 --> P2_2 -->
        # ^       |        ^
        # |       v        |
        # C1 -----------> P1 ---->

        Returns the final feature map or a list of feature maps if 'last' is set to False.
        """
        P2_1 = self.P2_1([conv_outputs[-2], conv_outputs[-1]])
        P1 = self.P1([conv_outputs[-3], P2_1])
        P2_2 = self.P2_2([P2_1, P1, conv_outputs[-2]])
        P3 = self.P3([conv_outputs[-1], P2_2])

        return [P1, P2_2, P3]

    def get_config(self):
        return {"f": self.f, "k": self.k}


class FPN(Model):
    def __init__(self, f, k):
        """
        Constructor for the FPN class.

        Args:
            f (int): Number of filters for convolution.
            k (int): Size of the convolution kernel.

        Initializes the FPN with the specified parameters and creates the necessary nodes.
        """
        super(FPN, self).__init__()
        self.f = f
        self.k = k
        self.conv_C3 = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last')
        self.P2_node = NodeUpsample(f, k)
        self.P1_node = NodeUpsample(f, k)

    def call(self, conv_outputs):
        """
        Call method for the FPN class.

        Args:
            conv_outputs (list of tf.Tensor): List of convolution outputs from different layers.

        Performs data flow as illustrated below:

        # C3 ---conv(C3)--->
        # ^        |
        # |        v
        # C2 ---> P2 ------>
        # ^        |
        # |        v
        # C1 ---> P1 ------>

        Returns a list of feature maps.
        """
        conv_C3 = self.conv_C3(conv_outputs[-1])
        P2_tensor = self.P2_node([conv_outputs[-2], conv_C3])
        P1_tensor = self.P1_node([conv_outputs[-3], P2_tensor])

        return [P1_tensor, P2_tensor, conv_C3]

    def get_config(self):
        return {"f": self.f, "k": self.k}


class PANet(Model):
    def __init__(self, f, k):
        """
        Constructor for the PANet class.

        Args:
            f (int): Number of filters for convolution.
            k (int): Size of the convolution kernel.

        Initializes the PANet with the specified parameters and creates the necessary nodes.
        """
        super(PANet, self).__init__()
        self.f = f
        self.k = k
        self.P1 = NodeUpsample(f, k)
        self.P2_1 = NodeUpsample(f, k)
        self.P2_2 = NodeDownsample(f, k)
        self.P3 = NodeDownsample(f, k)
        self.conv_C3 = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last')
        self.conv_P1 = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last')

    def call(self, conv_outputs):
        """
        Call method for the PANet class.

        Args:
            conv_outputs (list of tf.Tensor): List of convolution outputs from different layers.

        Performs data flow as illustrated below:

        # C3 -- conv(C3) -->  P3   ----->
        # ^       |            ^
        # |       v            |
        # C2 --> P2_1  ----> P2_2  ----->
        # ^       |            ^
        # |       v            |
        # C1 --> P1 -------> conv(P1) -->

        Returns a list of feature maps.
        """
        conv_C3 = self.conv_C3(conv_outputs[-1])
        P2_1 = self.P2_1([conv_outputs[-2], conv_C3])
        P1 = self.P2_1([conv_outputs[-3], P2_1])
        conv_P1 = self.conv_P1(P1)
        P2_2 = self.P2_2([P2_1, conv_P1])
        P3 = self.P3([conv_C3, P2_2])

        return [conv_P1, P2_2, P3]

    def get_config(self):
        return {"f": self.f, "k": self.k}


class SEN1(Model):
    def __init__(self, f, k):
        """
        Constructor for the SEN_1 class.

        Args:
            f (int): Number of filters for convolution.
            k (int): Size of the convolution kernel.

        Initializes the Scale Encoder Network (N=1) with the specified parameters and creates the necessary nodes.
        """
        super(SEN1, self).__init__()
        self.f = f
        self.k = k
        self.P1 = NodeIntermediateScale(f, k)
        self.P2 = NodeIntermediateScale(f, k)
        self.P3 = NodeDownsampleUpsample(f, k)

    def call(self, conv_outputs):
        """
        Call method for the SEN_1 class.

        Args:
            conv_outputs (list of tf.Tensor): List of convolution outputs from different layers.

        Performs data flow as illustrated below:

        # C3
        # ^ \
        # |  P2
        # | /  \
        # C2 -> P3 ->
        # ^ \  /
        # |  P1
        # | /
        # C1

        Returns a feature map.
        """
        P1 = self.P1([conv_outputs[0], conv_outputs[1]])
        P2 = self.P2([conv_outputs[1], conv_outputs[2]])
        P3 = self.P3([conv_outputs[1], P1, P2])
        return P3

    def get_config(self):
        return {"f": self.f, "k": self.k}


class SEN2(Model):
    def __init__(self, f, k):
        """
        Constructor for the SEN_2 class.

        Args:
            f (int): Number of filters for convolution.
            k (int): Size of the convolution kernel.

        Initializes the Scale Encoder Network (N=2) with the specified parameters and creates the necessary nodes.
        """
        super(SEN2, self).__init__()
        self.k = k
        self.f = f
        self.node = NodeDownsampleUpsample(f, k)

    def call(self, conv_outputs):
        """
        Call method for the SEN_2 class.

        Args:
            conv_outputs (list of tf.Tensor): List of convolution outputs from different layers.

        Performs data flow as illustrated below:

        # C3
        # ^  \
        # |   \
        # C2-> P -->
        # ^   /
        # |  /
        # C1

        Returns a feature map.
        """
        return self.node([conv_outputs[-3], conv_outputs[-2], conv_outputs[-1]])

    def get_config(self):
        return {"f": self.f, "k": self.k}
