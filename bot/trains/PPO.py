# Implement PPO using tensorflow  

import tensorflow as tf

flags = tf.app.flags

flags.DEFINE_float('lr', 3e-4, "Learning rate")
flags.DEFINE_integer('width', 30, "Game width")
flags.DEFINE_integer('height', 40, "Game height")