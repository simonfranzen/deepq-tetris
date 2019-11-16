from keras.models import Sequential
from keras.layers import Dense
import random
import numpy as np

class DQNAgent:

    def __init__(self, state_size, num_actions,
                       gamma = 0.999,
                       epsilon_base=0.02, epsilon_add=0.98, epsilon_decay=0.99999,
                       training_epochs=3, training_batch_size=300, target_model_lifetime=1000):

        self.state_size = state_size
        self.num_actions = num_actions

        self.gamma = gamma

        self.epsilon_base = epsilon_base
        self.epsilon_add = epsilon_add
        self.epsilon_decay = epsilon_decay

        self.training_epochs = training_epochs
        self.training_batch_size = training_batch_size

        # set up the (identical) structure of the neural networks
        self.policy_model = self._create_model()
        self.target_model = self._create_model()
        # target model starts out as a copy of policy model
        self._reset_target_model()
        self.target_model_lifetime = target_model_lifetime
        self.training_counter = 0

        self.policy_model.compile(loss='mse', optimizer='adam') # <-- this is the model we train
        # (no need to compile the target model, since we only use it for prediction and not for training)


    def _reset_target_model(self):
        self.target_model.set_weights(self.policy_model.get_weights())


    def _create_model(self):
        new_model = Sequential()
        new_model.add(Dense(32, input_dim=self.state_size, activation='relu'))
        new_model.add(Dense(32, activation='relu'))
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
            q = self.policy_model.predict(state)
            # best action = a for which q(s,a) is largest
            return np.argmax(q)


    def train(self, replaybuffer):

        if len(replaybuffer) < self.training_batch_size:
            return

        # grab a sample of the replay buffer ...
        states, actions, rewards, finished, next_states = replaybuffer.sample(self.training_batch_size)
        # ... and check if everything is in the format we need
        assert      states.shape == (self.training_batch_size, self.state_size)
        assert     actions.shape == (self.training_batch_size,)
        assert     rewards.shape == (self.training_batch_size,)
        assert    finished.shape == (self.training_batch_size,)
        assert next_states.shape == (self.training_batch_size, self.state_size)

        # estimate q(s,a) using the policy model
        q = self.policy_model.predict(states) # size: training_batch_size x num_actions
        assert q.shape == (self.training_batch_size, self.num_actions)

        # estimate q(s',a) using the target model (s' is the state resulting from s if action a is performed)
        q_next = self.target_model.predict(next_states)
        assert q.shape == (self.training_batch_size, self.num_actions)

        # compute max_a' q(s',a') (that is the q value of the best action in the next state)
        q_next_max = np.amax(q_next, axis=1)
        assert q_next_max.shape == (self.training_batch_size,)
        # if s' is the final state, the above is garbage since there is no action a' to be performed in s'
        # we should set all max_a' q(s',a') to zero if s' is the final state ...
        for i in range(self.training_batch_size):
            if finished[i]: q_next_max[i] = 0.0

        # the Bellman equation gives us the optimum values for q(s,a):
        # q_opt(s,a) = r + gamma * max_a' q(s',a')
        q_opt = rewards + self.gamma * q_next_max

        # fit the policy model to reproduce the optimum q values
        self.policy_model.fit(states, q_opt, batch_size=self.training_batch_size, epochs=self.training_epochs, verbose=0)

        self.training_counter += 1
        # we become more greedy after each training
        self.epsilon_add = self.epsilon_add * self.epsilon_decay
        # every number of steps we reset the target model to the same weights as the policy model
        if self.training_counter % self.target_model_lifetime == 0:
            self._reset_target_model()
