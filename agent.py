from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, Convolution2D, MaxPooling2D
import random
import numpy as np

class DQNAgent:

    def __init__(self, state_shape, num_actions,
                       model_filename = None,
                       double_dqn = True, gamma = 0.95,
                       epsilon_base=0.15, epsilon_add=0.85, epsilon_decay=0.999999,
                       training_epochs=1, training_batch_size=32, target_model_lifetime=1000):

        self.state_shape = state_shape
        self.num_actions = num_actions

        self.double_dqn = double_dqn
        self.gamma = gamma

        self.epsilon_base = epsilon_base
        self.epsilon_add = epsilon_add
        self.epsilon_decay = epsilon_decay

        self.training_epochs = training_epochs
        self.training_batch_size = training_batch_size

        # set up the structure of the neural networks
        if model_filename is not None:
            self.policy_model = load_model(model_filename)
        else:
            self.policy_model = self._create_model()
            self.policy_model.compile(loss='mse', optimizer='adam') # <-- this is the model we train

        self.target_model = self._create_model()
        # target model starts out as a copy of policy model
        self._reset_target_model()
        self.target_model_lifetime = target_model_lifetime
        self.training_counter = 0
        # no need to compile the target model, since we only use it for prediction and not for training


    def store_model(self, filename):
        self.policy_model.save(filename)


    def _reset_target_model(self):
        self.target_model.set_weights(self.policy_model.get_weights())


    def _create_model(self):
        new_model = Sequential()
        new_model.add(Convolution2D(input_shape=self.state_shape, filters=64, \
                                    kernel_size=(4,4), strides=(2,2), activation='relu'))
        new_model.add(MaxPooling2D(pool_size=(2,2)))
        new_model.add(Flatten())
        new_model.add(Dense(64, activation='relu'))
        new_model.add(Dense(64, activation='relu'))
        new_model.add(Dense(self.num_actions, activation='linear'))
        return new_model


    @property
    def epsilon(self):
        return self.epsilon_base + self.epsilon_add


    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0,self.num_actions-1)
        else:
            # feed the state through the policy model to get the predicted q(s,a)
            q = self.policy_model.predict(np.expand_dims(state, 0))
            # best action = a for which q(s,a) is largest
            return np.argmax(q)


    def train(self, replaybuffer):

        if len(replaybuffer) < self.training_batch_size:
            return

        # grab a sample of the replay buffer ...
        states, actions, rewards, finished, next_states = replaybuffer.sample(self.training_batch_size)
        # ... and check if everything is in the format we need
        assert      states.shape == tuple([self.training_batch_size] + [s for s in self.state_shape])
        assert     actions.shape == (self.training_batch_size,)
        assert     rewards.shape == (self.training_batch_size,)
        assert    finished.shape == (self.training_batch_size,)
        assert next_states.shape == tuple([self.training_batch_size] + [s for s in self.state_shape])

        # estimate q(s',a) using the target model (s' is the state resulting from s if action a is performed)
        q_next = self.target_model.predict(next_states)
        assert q_next.shape == (self.training_batch_size, self.num_actions)

        if self.double_dqn:

            # use the policy model to determine the best action in the next state: argmax_a' q_pol(s',a')
            q_next_selector = self.policy_model.predict(next_states)
            action_next_max = np.argmax(q_next_selector, axis=1)

            # use the q value of that action from the target network: q_tgt(s', argmax_a' q_pol(s',a'))
            q_next_max = np.array([ q_next[i,action_next_max[i]] for i in range(self.training_batch_size) ])

        else:

            # compute max_a' q(s',a') (that is the q value of the best action in the next state)
            q_next_max = np.amax(q_next, axis=1)

        assert q_next_max.shape == (self.training_batch_size,)

        # estimate q(s,a) using the policy model
        q = self.policy_model.predict(states) # size: training_batch_size x num_actions
        assert q.shape == (self.training_batch_size, self.num_actions)

        # The target of our fit of the policy model is the q(s,a) we just
        # calculated, except that we replace the value for the action that was
        # actually taken with the reward observed plus the discounted future
        # reward according to the Bellman equation.
        q_target = q
        for i in range(self.training_batch_size):
            if finished[i]:
                # for finished games there is no future reward
                q_target[i,actions[i]] = rewards[i]
            else:
                q_target[i,actions[i]] = rewards[i] + self.gamma * q_next_max[i]

        # fit the policy model to reproduce the optimum q values
        self.policy_model.fit(states, q_target, batch_size=self.training_batch_size, epochs=self.training_epochs, verbose=0)

        self.training_counter += 1
        # we become more greedy after each training
        self.epsilon_add = self.epsilon_add * self.epsilon_decay
        # every number of steps we reset the target model to the same weights as the policy model
        if self.training_counter % self.target_model_lifetime == 0:
            self._reset_target_model()
