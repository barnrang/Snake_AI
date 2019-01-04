# Implement PPO using tensorflow  

import tensorflow as tf

flags = tf.app.flags

flags.DEFINE_float('lr', 3e-4, "Learning rate")
flags.DEFINE_integer('width', 30, "Game width")
flags.DEFINE_integer('height', 40, "Game height")

SESS = tf.Session()
EPSILON = 0.2
loss_V = 0.2
BETA = 0.01
LR = 1e-4

class ACPPONetwork(object):
    def __init__(self, image_width, image_height, num_channel, num_actions):
        self.image_height = image_height
        self.image_width = image_width
        self.num_channel = num_channel
        self.num_actions = num_actions
        self.old_prob = 1
        self.optimizer = tf.train.AdamOptimizer(learning_rate=LR)


    def build_graph(self):
        self.s_t = tf.placeholder(tf.float32, shape=(None, self.image_width, 
            self.image_height, self.num_channel))
        self.a_t = tf.placeholder(tf.float32, shape=(None, self.num_actions))
        self.r_t = tf.placeholder(tf.float32, shape=(None, 1))

        with tf.variable_scope('conv_layer', reuse=tf.AUTO_REUSE):
            conv1 = tf.layers.conv2d(self.s_t, 64, (5, 5))
            conv1 = tf.nn.relu(conv1)
            conv2 = tf.layers.conv2d(conv1, 256, (3, 3))
            conv2 = tf.nn.relu(conv2)
            flatten = tf.layers.flatten(conv2)

        with tf.variable_scope('dense_layer', reuse=tf.AUTO_REUSE):
            inner1 = tf.layers.dense(flatten, 256)
            self.conv_output = tf.nn.relu(inner1)

        with tf.variable_scope('actor_layer', reuse=tf.AUTO_REUSE):
            self.actor_output = tf.nn.softmax(tf.layers.dense(self.conv_output, self.num_actions))
        
        with tf.variable_scope('critic_layer', reuse=tf.AUTO_REUSE):
            self.critic_output = tf.layers.dense(self.conv_output, 1)

        advantage = self.r_t - self.critic_output
        self.prob = self.a_t * self.actor_output + 1e-10
        r_theta = self.prob / self.old_prob
        advantage_CPI = r_theta * tf.stop_gradient(advantage)

        r_clip = tf.clip_by_value(r_theta, 1 - EPSILON, 1 + EPSILON)
        clipped_advantage_CPI = r_clip * advantage
        loss_clip = -tf.reduce_mean(tf.minimum(advantage_CPI, clipped_advantage_CPI), axis=1, keep_dims=True)

        loss_value = loss_V * advantage ** 2
        loss_entropy = BETA * tf.reduce_sum(self.actor_output * tf.log(self.actor_output + 1e-10), keep_dims=True)

        self.total_loss = tf.reduce_mean(loss_clip + loss_entropy + loss_value)
        self.minimizer = self.optimizer.minimize(self.total_loss)

    def predict_prob(self, s):
        return SESS.run(self.actor_output, {self.s_t:s})

    




class Agent(object):
    def __init__(self, image_width, image_height, num_channel, num_actions):
        raise NotImplementedError

