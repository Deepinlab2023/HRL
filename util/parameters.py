import math
import torch as th

class SharedParams:
    def __init__(self):
        self.device = th.device('cuda' if th.cuda.is_available() else 'cpu')
        self.show_testing = False  # set to True to render test episodes
        self.render_delay = 20  # set an episode delay for rendering test episodes
        self.switch_goal = True  # switches goal halfway between total_train_episodes
        self.starting_goal = 62  # East doorway in FourRooms

        self.num_trials = 5
        self.total_train_episodes = 2000
        self.t_max = 1000
        self.test_interval = 10  # test every 10 episodes
        self.test_episodes = 10  # test 10 episodes and get average results


class ParametersPPO(SharedParams):
    def __init__(self):
        super(ParametersPPO, self).__init__()

        # training loop hyperparameters
        self.buffer_episodes = 10  # num episodes in batch buffer
        self.opt_epochs = 10    #num optimization epochs per batch buffer
        self.mini_batch_size = 64
        self.train_iterations = math.ceil(self.total_train_episodes / self.buffer_episodes) #top-lvl loop index

        # training value hyperparameters
        self.actor_hidden_dim = 128
        self.critic_hidden_dim = 128
        self.actor_lr = 3e-4
        self.critic_lr = 1e-3
        self.gamma = 0.99
        self.gae_lambda = 0.99
        self.entropy_coef = 0.01
        self.eps_clip = 0.2

class ParametersDAC(SharedParams):
    def __init__(self):
        super(ParametersDAC, self).__init__()


        # training loop hyperparameters
        self.num_options = 4
        self.buffer_episodes = 10  # num episodes in batch buffer
        self.opt_epochs = 10  # num optimization epochs per batch buffer
        self.mini_batch_size = 64
        self.train_iterations = math.ceil(self.total_train_episodes / self.buffer_episodes)  # top-lvl loop index

        # training value hyperparameters
        self.actor_hidden_dim = 128
        self.critic_hidden_dim = 128
        self.beta_hidden_dim = 64
        self.lr_ha = 3e-4       #high actor learning rate
        self.lr_la = 3e-4       #low actor learning rate
        self.lr_critic = 3e-3       #critic learning rate
        self.lr_beta = 3e-4     #beta network learning rate
        self.eps_clip = 0.2     #ppo clipping parameter
        self.gamma = 0.99
        self.gae_lambda = 0.99
        self.entropy_coef = 0.01


class ParametersOC(SharedParams):
    def __init__(self):
        super(ParametersOC, self).__init__()

        # training loop hyperparameters
        self.buffer_size = 20000 #max timesteps stored in buffer
        self.batch_size = 32
        self.target_update_freq = 200    #number of timesteps between hard critic updates
        self.critic_optim_freq = 4       #number of timesteps between critic SGD optimizations

        # training value and network hyperparameters
        self.phi_hidden_dim = 32
        self.phi_output_dim = 64
        self.lr = 5e-4
        self.gamma = 0.99
        self.beta_reg = 0.01    #Regularization to decrease termination prob
        self.entropy_coef = 0.01 #Regularization to increase policy entropy
        self.num_options = 4
        self.temp = 1.0   #Action distribution softmax tempurature param

        # exploration epsilon decay from 'start' to 'end' in 'decay' timesteps
        self.eps_start = 1.0
        self.eps_end = 0.1
        self.eps_decay = 20000
        self.eps_test = 0.01

        self.t_tot = 0  # timestep counter for epsilon calculation
        """"""

    @property
    def epsilon(self):
        """dynamically compute epsilon based on current step as params attribute"""
        epsilon = self.eps_end + (self.eps_start - self.eps_end) * \
                  math.exp(-1. * self.t_tot / self.eps_decay)
        return epsilon