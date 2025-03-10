import os, time, sys
import numpy as np
from util.benchmarker import Utils


class ALGO_Runner():
    def __init__(self, env, trainer):
        self.env = env
        self.trainer = trainer

    def run_experiment(self, params, load_save_result=False):
        """Change load_save_result to True to plot from existing test/train rewards"""
        start = time.time()
        if load_save_result is False or not os.path.isfile('all_train_returns.npy') or not os.path.isfile(
                'all_test_returns.npy') or not os.path.isfile('all_test_lengths.npy'):
            all_train_returns = []
            all_test_returns = []
            all_test_lengths = []

            for trial in range(params.num_trials):
                print(f"Trial: {trial + 1}")
                trainer = self.trainer()

                #ensure trials start with same goal.
                if "FourRoom" in params.env_name: self.env.choose_goal(params.starting_goal)

                train_rewards, test_rewards, test_episode_lengths = trainer.train(self.env, params)

                all_train_returns.append(train_rewards)
                all_test_returns.append(test_rewards)
                all_test_lengths.append(test_episode_lengths)

            print(f"Experiment completed in {(time.time() - start):.2f} seconds")
            np.save('all_train_returns.npy', all_train_returns)
            np.save('all_test_returns.npy', all_test_returns)
            np.save('all_test_lengths.npy', all_test_lengths)
        else:
            all_train_returns = np.load('all_train_returns.npy')
            all_test_returns = np.load('all_test_returns.npy')
            all_test_lengths = np.load('all_test_lengths.npy')

        utils = Utils()
        average_returns, max_return, max_return_ci, individual_returns, g1g2_ret, g1g2_ci = utils.benchmark_plot(all_train_returns,
                                                                                              all_test_returns, all_test_lengths,
                                                                                              params.test_interval)
        print(f"Average Return: {np.round(average_returns, 2)}")
        print(f"Overall Max Return w/ 95% CI: {max_return:.3f} +- {max_return_ci:.3f}")
        print(f"Individual Run Overall Max Returns: {np.round(individual_returns, 3)}")
        print(f"Max Return for Goal 1 w/ 95% CI: {g1g2_ret[0]:.3f} +- {g1g2_ci[0]:.3f}")
        print(f"Max Return for Goal 2 w/ 95% CI: {g1g2_ret[1]:.3f} +- {g1g2_ci[1]:.3f}")
        print("Completed experiment")