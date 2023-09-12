"""
COMP20008 Semester 1
Assignment 1 Task 5
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Union, List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer


# Task 5 - Dimensionality Reduction (3 marks)
def task5(bow_df: pd.DataFrame, tokens_plot_filename: str, distribution_plot_filename: str) -> Dict[str, Union[List[str], List[float]]]:
    # bow_df is the output of Task 3, for this task you 
    # should generate a bag of words, normalisation of the 
    # data perform PCA decomposition to 2 components, and 
    # then plot all URLs in a way which helps you answer
    # the discussion questions. If you would like to verify 
    # your PCA results against the sample data, you can return
    # the PCA weights - containing the list of most positive
    # weighted words, most negatively weighted words and the 
    # weights in the PCA decomposition for each respective word.
    # Implement Task 5 here
    result = {}

    # Get bag-of-words representation of words across all pages
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform(bow_df['words'])
    words = vectorizer.get_feature_names_out()
    bow = pd.DataFrame(bow.toarray(), columns=words)

    # Normalize using max norm fit to the dataframe
    normalizer = Normalizer(norm='max')
    bow_normalized = normalizer.fit_transform(bow)
    bow_normalized = pd.DataFrame(bow_normalized, columns=words)

    # Perform Principal Component Analysis using 2 components
    pca = PCA(n_components=2, random_state=535)
    pca_components = pca.fit_transform(bow_normalized)
    # list of the proportion of the variance explained by each principal component.
    explained_var = pca.explained_variance_ratio_
    # sorts the components in descending order of explained variance.
    sorted_components  = (-explained_var).argsort()

    # Store the PCA results in a dictionary
    for i in sorted_components :
        weight = pca.components_[i]  
        index = weight.argsort()
        # Get the positive and negative weights 
        positive_weights = weight[index[-10:]]
        negative_weights = weight[index[:10]]
        negative = words[index[:10]]
        positive = words[index[-10:]]

        result[str(i)] = {
            "positive": positive[::-1],
            "negative": negative[::-1],
            "positive_weights": positive_weights[::-1],
            "negative_weights": negative_weights[::-1]
        }

    fig, axis = plt.subplots(1, 2, figsize=(20, 10))
    # For each principal component, plot the top 10 most positively and negatively weighted tokens and their weights
    for i in sorted_components :
        ax = axis[i]
        # Get the positive and negative weights and tokens for the i-th component from the result dictionary
        positive_weights = result[str(i)]['positive_weights']
        negative_weights = result[str(i)]['negative_weights']
        positive = result[str(i)]['positive']
        negative = result[str(i)]['negative']
        # Concatenate the positive and negative tokens and weights
        words = np.concatenate([positive, negative])
        weights = np.concatenate([positive_weights, negative_weights])
        # Create a horizontal bar plot with the tokens on the y-axis and the weights on the x-axis
        ax.barh(range(len(words)), weights, align='center')
        # Set the y-ticks and labels to the tokens
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words)
        # Invert the y-axis so that the most important tokens are on top
        ax.invert_yaxis()
        # Set the title of the plot to the name of the principal component
        ax.set_title(f'PCA Component {i+1}')
    fig.suptitle("top 10 most positively and negatively weighted tokens and their weights for each component.")
    fig.tight_layout()
    fig.savefig(tokens_plot_filename)

    
    # Create a scatter plot of seed URLs based on their PCA components
    fig, ax = plt.subplots(figsize=(10, 10))
    for seed_url in bow_df['seed_url'].unique():
        index = bow_df['seed_url'] == seed_url
        pca_x = pca_components[index, 0]
        pca_y = pca_components[index, 1]
        ax.scatter(pca_x, pca_y, label=seed_url)

    # Set the axis labels and title, and show a legend
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_title('PCA Plot of Seed URLs')
    ax.legend()

    # Save the plot to a file
    fig.savefig(distribution_plot_filename)

    return result

