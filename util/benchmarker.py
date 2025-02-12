import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import seaborn as sns
import sys
#TODO: Fix confidence interval / benchmarking calculation

class Utils:
    def __init__(self):
        pass

    def benchmark_plot(self, all_train_returns, all_test_returns, all_test_lengths, test_interval, moving_avg_window=100, down_sample_factor=100):
        """Data processing and calculations"""
        num_trials = len(all_train_returns)
        num_points = len(all_test_returns[0])

        # Convert lists to numpy arrays for easier calculations
        all_train_returns = np.array(all_train_returns)
        all_test_returns = np.array(all_test_returns)
        all_test_lengths = np.array(all_test_lengths)
        # print(all_test_returns.shape)

        """Overall benchmarking"""
        # Calculate the mean and 95% confidence intervals
        mean_train_returns = all_train_returns.mean(axis=0)
        mean_test_returns = all_test_returns.mean(axis=0)
        mean_test_lengths = all_test_lengths.mean(axis=0)

        train_ci = 1.96 * all_train_returns.std(axis=0) / np.sqrt(num_trials)
        test_ci = 1.96 * all_test_returns.std(axis=0) / np.sqrt(num_trials)
        test_len_ci = 1.96 * all_test_lengths.std(axis=0) / np.sqrt(num_trials)

        # Calculate individual maximum returns from each trial
        individual_max_returns = [np.max(trial_returns) for trial_returns in all_test_returns]

        # Calculate the average maximum return
        avg_max_return = np.mean(individual_max_returns)

        # Calculate the 95% confidence interval for the average maximum return
        n = len(individual_max_returns)
        sample_std = np.std(individual_max_returns, ddof=1)
        t_value = st.t.ppf(1 - 0.025, df=n - 1)
        margin_of_error = t_value * sample_std / np.sqrt(n)
        avg_max_return_ci = margin_of_error

        """Transfer learning benchmarking"""
        #split arrays in half (before and after goal switch)
        halfway_point = num_points // 2
        test_returns_g1 = all_test_returns[:,:halfway_point]
        test_returns_g2 = all_test_returns[:,halfway_point:]

        #compute max return for each half
        max_returns_g1 = [np.max(trial_returns) for trial_returns in test_returns_g1]
        max_returns_g2 = [np.max(trial_returns) for trial_returns in test_returns_g2]

        #compute average max return
        avg_max_return_g1 = np.mean(max_returns_g1)
        avg_max_return_g2 = np.mean(max_returns_g2)
        avg_max_return_g1g2 = [avg_max_return_g1, avg_max_return_g2]

        # Calculate the 95% confidence interval
        n = len(max_returns_g1)
        sample_std_g1 = np.std(max_returns_g1, ddof=1)
        sample_std_g2 = np.std(max_returns_g2, ddof=1)
        t_value = st.t.ppf(1 - 0.025, df=n - 1)
        avg_max_return_ci_g1 = t_value * sample_std_g1 / np.sqrt(n)
        avg_max_return_ci_g2 = t_value * sample_std_g2 / np.sqrt(n)
        avg_max_return_ci_g1g2 = [avg_max_return_ci_g1, avg_max_return_ci_g2]

        """Plot test episode lengths"""
        plt.figure(figsize=(12, 6))
        episodes = np.arange(0, num_points * test_interval, test_interval)
        for i in range(num_trials):
            plt.plot(episodes, all_test_lengths[i], linestyle='dotted', alpha=0.5, label=f'Trial {i+1}')  # Individual test trials
        plt.plot(episodes, mean_test_lengths, '-o', label='Mean Episode Lengths', color='black')  # Mean test returns without error bars
        plt.fill_between(episodes, mean_test_lengths - test_len_ci, mean_test_lengths + test_len_ci, color='lightblue', alpha=0.3, label='CI')  # Fill between upper and lower bounds
        plt.xlabel('Training Episodes')
        plt.ylabel('Average Test Episode Length')
        plt.title('Test Episode Lengths with 95% Confidence Interval')
        plt.legend()
        plt.show()


        """Plot test returns"""
        plt.figure(figsize=(12, 6))
        episodes = np.arange(0, num_points * test_interval, test_interval)
        for i in range(num_trials):
            plt.plot(episodes, all_test_returns[i], linestyle='dotted', alpha=0.5, label=f'Trial {i+1}')  # Individual test trials
        plt.plot(episodes, mean_test_returns, '-o', label='Mean Test Returns', color='black')  # Mean test returns without error bars
        plt.fill_between(episodes, mean_test_returns - test_ci, mean_test_returns + test_ci, color='lightblue', alpha=0.3, label='CI')  # Fill between upper and lower bounds
        plt.xlabel('Episodes')
        plt.ylabel('Test Return')
        plt.title('Test Returns with 95% Confidence Interval')
        plt.legend()
        plt.show()

        """Plot density plot of test returns (Not in use)"""
        # plt.figure(figsize=(12, 6))
        # #sns.kdeplot(mean_test_returns, fill=True, label='Density Plot')
        # sns.kdeplot(mean_test_returns, label='Density Plot')
        # plt.xlabel('Test Return')
        # plt.ylabel('Density')
        # plt.title('Density Plot of Test Returns')
        # plt.legend()
        # plt.show()

        """Plot test rewards (Not in use)"""
        # # Plot training returns with moving average and confidence interval
        # plt.figure(figsize=(12, 6))
        # plt.plot(down_sampled_indices, down_sampled_mean_train_returns, label='Mean Training Returns (Smoothed)', color='blue')
        # plt.fill_between(down_sampled_indices, down_sampled_mean_train_returns - down_sampled_train_ci, down_sampled_mean_train_returns + down_sampled_train_ci, color='lightblue', alpha=0.3, label='CI')
        # plt.xlabel('Episodes')
        # plt.ylabel('Training Return')
        # plt.title('Training Returns with 95% Confidence Interval (Smoothed)')
        # plt.legend()
        # plt.show()

        """Plot density plot of training returns"""
        # plt.figure(figsize=(12, 6))
        # #sns.kdeplot(mean_train_returns, fill=True, label='Density Plot')
        # sns.kdeplot(mean_train_returns, label='Density Plot')
        # plt.xlabel('Training Return')
        # plt.ylabel('Density')
        # plt.title('Density Plot of Training Returns')
        # plt.legend()
        # plt.show()

        return (mean_test_returns, avg_max_return, avg_max_return_ci, individual_max_returns,
                avg_max_return_g1g2, avg_max_return_ci_g1g2)