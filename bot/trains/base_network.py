from keras import layers
from keras.models import Sequential
import tensorflow as tf
from keras.optimizers import RMSprop

class BaseNetwork(object):
    def __init__(self, width, height, action_num, config, *args, **kwargs):
        self.width = width
        self.height = height
        self.action_num = action_num
        self.config = config

        self.model = self.build_model()
    
    def _huber_loss(self, target, pred, clip_delta=1.):
        error = tf.abs(target - pred)
        cond = error < clip_delta
        loss = tf.where(cond, 0.5 * tf.square(error), clip_delta * (error - 0.5 * clip_delta))
        return tf.reduce_mean(loss)

    def build_model(self):
        model = Sequential()
        model.add(layers.Conv2D(16, (5,5), input_shape=(self.width, self.height, 2)))
        model.add(layers.Activation('relu'))
        model.add(layers.Conv2D(32, (3,3)))
        model.add(layers.Activation('relu'))
        model.add(layers.GlobalAveragePooling2D())
        model.add(layers.Dense(128))
        model.add(layers.Activation('relu'))
        model.add(layers.Dense(self.action_num, activation='linear'))

        model.compile(optimizer=RMSprop(self.config.lr), loss=self._huber_loss)
        
        return model
    
    def forward(self, x):
        return self.model(x)
    
    
