from Node import Node_upsample, Node_downsample, Node_downsample_and_upsample
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, SeparableConv2D
from tensorflow.keras.models import Model


class BiFPN(Model):
    def __init__(self, f, k, last=True):
        super(BiFPN, self).__init__()

        self.last = last  
        self.f = f
        self.k = k      

        self.P2_1 = Node_upsample(f, k)
        self.P1   = Node_upsample(f, k)
        self.P2_2 = Node_downsample(f, k, num_inputs=3)
        self.P3   = Node_downsample(f, k) 

    def call(self, conv_outputs):
        # C3 ------------> P3 ---> 
        # ^   ____|______   ^          
        # |  /    v      \  |          
        # C2 --> P2_1 --> P2_2 -->
        # ^       |        ^          
        # |       v        |          
        # C1 -----------> P1 ---->

        P2_1 = self.P2_1([conv_outputs[-2], conv_outputs[-1]])
        P1   = self.P1(  [conv_outputs[-3], P2_1])
        P2_2 = self.P2_2([P2_1, P1, conv_outputs[-2]])
        P3   = self.P3(  [conv_outputs[-1], P2_2])

        if self.last:
            return P3
        else:
            return [P1, P2_2 , P3]
            
    def get_config(self):
        return {"f":self.f, "k":self.k, "last":self.last}



class FPN(Model):
    def __init__(self, f, k):
        super(FPN, self).__init__()

        # self.conv_C3 = Conv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last') 
        self.conv_C3 = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last') 
        self.P2_node = Node_upsample(f, k)
        self.P1_node = Node_upsample(f, k)

    def call(self, conv_outputs):
        # C3 ---conv(C3)--->  
        # ^        |        
        # |        v        
        # C2 ---> P2 ------> 
        # ^        |          
        # |        v          
        # C1 ---> P1 ------>
        
        conv_C3   = self.conv_C3(conv_outputs[-1])
        P2_tensor = self.P2_node([conv_outputs[-2], conv_C3])
        P1_tensor = self.P1_node([conv_outputs[-3], P2_tensor])

        return [P1_tensor, P2_tensor , conv_C3]
        # return P1_tensor

    def get_config(self):
        return {"f":self.f, "k":self.k}



class PANet(Model):
    def __init__(self, f, k):
        super(PANet, self).__init__()

        self.P1   = Node_upsample(f, k)
        self.P2_1 = Node_upsample(f, k)
        self.P2_2 = Node_downsample(f, k)
        self.P3   = Node_downsample(f, k)
        
        # self.conv_C3 = Conv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last') 
        # self.conv_P1 = Conv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last') 
        self.conv_C3 = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last') 
        self.conv_P1 = SeparableConv2D(filters=f, kernel_size=k, padding='same', data_format='channels_last') 

    def call(self, conv_outputs):
        # C3 -- conv(C3) -->  P3   -----> 
        # ^       |            ^          
        # |       v            |          
        # C2 --> P2_1  ----> P2_2  ----->
        # ^       |            ^
        # |       v            |
        # C1 --> P1 -------> conv(P1) -->
        
        conv_C3 = self.conv_C3(conv_outputs[-1])
        P2_1    = self.P2_1([conv_outputs[-2], conv_C3])
        P1      = self.P2_1([conv_outputs[-3], P2_1])
        conv_P1 = self.conv_P1(P1)
        P2_2    = self.P2_2([P2_1, conv_P1])
        P3      = self.P3([conv_C3, P2_2])

        return [conv_P1, P2_2 , P3]
        # return P3
        
    def get_config(self):
        return {"f":self.f, "k":self.k}



class SEN(Model):
    def __init__(self, f, k):
        super(SEN, self).__init__()
        self.node = Node_downsample_and_upsample(f, k)

    def call(self, conv_outputs):
        # C3  
        # ^  \
        # |   \           
        # C2-> P --> 
        # ^   /
        # |  /
        # C1
        
        return self.node([conv_outputs[-3], conv_outputs[-2], conv_outputs[-1]])
        
    def get_config(self):
        return {"f":self.f, "k":self.k}
