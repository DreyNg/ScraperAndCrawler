"""
COMP20008 Semester 1
Assignment 1 Task 4
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import defaultdict



# Task 4 - Plotting the Most Common Words (2 Marks)
def task4(bow: pd.DataFrame, output_plot_filename: str) -> Dict[str, List[str]]:
    # The bow dataframe is the output of Task 3, it has 
    # three columns, link_url, words and seed_url. The 
    # output plot should show which words are most common
    # for each seed_url. The visualisation is your choice,
    # but you should make sure it makes sense for what it
    # is meant to be.
    # Implement Task 4 here

    # creating a frequency dictionary for all the words
    freq_dict = defaultdict(lambda: defaultdict(int))
    for row in bow.itertuples(index=False):
        word_list = row.words.split()
        for word in word_list:
            freq_dict[row.seed_url][word] += 1

       
    # Take top 10 words for each url
    top_10_words_dict = {}
    for seed_url in freq_dict:
        top_10_words = sorted(freq_dict[seed_url].items(), key=lambda x: (-x[1], x[0]))
        top_10_words = top_10_words[:10]
        top_10_words = [word for word, freq in top_10_words]

        top_10_words_dict[seed_url] = top_10_words

    # Plotting in to figure
    fig, axes = plt.subplots(1, len(bow['seed_url'].unique()), figsize=(12, 5), dpi=100)
    # For each unique seed_url, get the top 10 most common words and their frequencies
    # Plot a horizontal bar chart for each seed_url with the top 10 words and their frequencies
    for i, seed_url in enumerate(bow['seed_url'].unique()):
        top_10_words = [word for word in top_10_words_dict[seed_url]]
        top_10_freqs = [freq_dict[seed_url][word] for word in top_10_words]
        axes[i].barh(top_10_words, top_10_freqs)
        axes[i].set_title(f'Seed Url: {seed_url}', fontsize=12)
        axes[i].set_xlabel('Frequency', fontsize=10)
        axes[i].set_ylabel('Word', fontsize=10)
        axes[i].tick_params(axis='both', labelsize=8)
        axes[i].invert_yaxis()

    fig.suptitle('Top 10 Most Common Words by Seed URL', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_plot_filename)

    return top_10_words_dict










