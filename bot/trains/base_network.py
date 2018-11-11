from keras import layers
from keras.models import Sequential

class BaseNetwork(object):
    def __init__(self, width, height, action_num, *args, **kwargs):
        self.width = width
        self.height = height
        self.action_num = action_num

        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(layers.Conv2D(16, (5,5), input_shape=(self.width, self.height, 4)))
        model.add(layers.Activation('relu'))
        model.add(layers.Conv2D(32, (3,3)))
        model.add(layers.Activation('relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(128))
        model.add(layers.Activation('relu'))
        model.add(layers.Dense(self.action_num))
        model.add(layers.Activation('softmax'))
        
        return model
    
    def forward(self, x):
        return self.model(x)
    
    
