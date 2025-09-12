import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, make_scorer, accuracy_score, precision_score, \
    recall_score, f1_score, roc_curve, roc_auc_score

from typing import Optional, List


def plot_bar_list_features(df: pd.DataFrame, feature_list: List[str]):
    fig, axes = plt.subplots(4, 2, figsize=(15, 5 * 3))
    fig.suptitle('TOP 10 : Quantidade de heróis por features', fontsize=14)

    axes = axes.flatten()
    for i, column in enumerate(feature_list):

        hero_counts = df.groupby(f'{column}').count()['name'].sort_values(ascending=False).reset_index(
            name='hero_count')[0:10]
        hero_counts[f'{column}'] = hero_counts[f'{column}'].astype(str)
        # colors = hero_counts[f'{column}'].map({'False': 'lightgreen', 'True': 'green'})
        bars = axes[i].bar(hero_counts[f'{column}'], hero_counts['hero_count'], color='green')
        for bar in bars:
            yval = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom')

        axes[i].set_title(f'{column}', fontsize=12)
        # axes[i].set_xlabel('Cluster', fontsize=10)
        # axes[i].set_ylabel(column, fontsize=10)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].set_ylim(0, max(hero_counts['hero_count']) + 100)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def plot_hist(df: pd.DataFrame, numeric_features: List[str]):
    plt.figure(figsize=(15, 10))
    for i, feature in enumerate(numeric_features, 1):
        plt.subplot(3, 3, i)
        sns.histplot(df[feature], kde=True, bins=20, color='royalblue')
        plt.title(f'Distribution of {feature}')
    plt.tight_layout()
    plt.show()


def plot_by_column(df, column_name):
    """
    Plots the distribution of values in a specified column of a DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_name (str): The column name to plot.

    Returns:
        None
    """
    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Check the data type of the column
    if df[column_name].dtype == 'object' or df[column_name].dtype.name == 'category':
        # Categorical data: Use a count plot
        plt.figure(figsize=(8, 6))
        ax = sns.countplot(data=df, y=column_name, order=df[column_name].value_counts().index)
        plt.title(f"Distribution of {column_name}")
        plt.xlabel("Count")
        plt.ylabel(column_name)

        # Add values to the bars
        for container in ax.containers:
            ax.bar_label(container)
    else:
        # Numerical data: Use a histogram
        plt.figure(figsize=(10, 6))
        ax = sns.histplot(df[column_name], kde=True)
        plt.title(f"Distribution of {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")

        # Add values to the bars if histogram
        for container in ax.containers:
            labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in container]
            ax.bar_label(container, labels=labels)

    plt.tight_layout()
    plt.show()


def plot_by_columns(df, column_names):
    """
    Plots the distribution of values for a list of columns in a DataFrame, with up to 8 plots in a single figure.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_names (list of str): The list of column names to plot.

    Returns:
        None
    """
    # Check if all columns exist in the DataFrame
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Set up the figure
    num_columns = len(column_names)
    num_rows = (num_columns + 3) // 4  # Up to 4 columns per row
    fig, axes = plt.subplots(num_rows, 4, figsize=(20, 5 * num_rows))
    axes = axes.flatten()

    for i, column_name in enumerate(column_names):
        ax = axes[i]
        # Check the data type of the column
        if df[column_name].dtype == 'object' or df[column_name].dtype.name == 'category':
            # Categorical data: Use a count plot
            sns.countplot(data=df, y=column_name, order=df[column_name].value_counts().index, ax=ax)
            ax.set_title(f"Distribution of {column_name}")
            ax.set_xlabel("Count")
            ax.set_ylabel(column_name)
            # Add values to the bars
            for container in ax.containers:
                labels = [int(v.get_width()) if v.get_width() > 0 else '' for v in container]
                ax.bar_label(container, labels=labels)
        else:
            # Numerical data: Use a histogram
            sns.histplot(df[column_name], kde=True, bins=30, ax=ax)
            ax.set_title(f"Distribution of {column_name}")
            ax.set_xlabel(column_name)
            ax.set_ylabel("Frequency")
            # Add values to the bars if histogram
            for container in ax.containers:
                labels = [int(v.get_height()) if v.get_height() > 0 else '' for v in container]
                ax.bar_label(container, labels=labels)

    # Remove any unused subplots
    for j in range(len(column_names), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def plot_boxplots_by_columns(df, column_names):
    """
    Plots boxplots for a list of columns in a DataFrame, with up to 8 plots in a single figure.
    Annotates each plot with mean, median, max, and min values.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_names (list of str): The list of column names to plot.

    Returns:
        None
    """
    # Check if all columns exist in the DataFrame
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    numeric_features = df.select_dtypes(['float', 'int']).columns.tolist()
    sets = [set(lst) for lst in [numeric_features, column_names]]

    column_names = list(set.intersection(*sets))

    # Set up the figure
    num_columns = len(column_names)
    num_rows = (num_columns + 3) // 4  # Up to 4 columns per row
    fig, axes = plt.subplots(num_rows, 4, figsize=(20, 5 * num_rows))
    axes = axes.flatten()

    for i, column_name in enumerate(column_names):
        ax = axes[i]
        if df[column_name].dtype != 'object' and df[column_name].dtype.name != 'category':
            # Plot boxplot for numerical data
            sns.boxplot(data=df, y=column_name, ax=ax)
            ax.set_title(f"Boxplot of {column_name}")
            ax.set_ylabel(column_name)

            # Calculate statistics
            column_data = df[column_name].dropna()
            mean_val = column_data.mean()
            median_val = column_data.median()
            max_val = column_data.max()
            min_val = column_data.min()

            # Add annotations for mean, median, max, and min
            ax.axhline(mean_val, color='blue', linestyle='--', linewidth=1, label=f"Mean: {mean_val:.2f}")
            ax.axhline(median_val, color='green', linestyle='--', linewidth=1, label=f"Median: {median_val:.2f}")
            ax.axhline(max_val, color='red', linestyle='--', linewidth=1, label=f"Max: {max_val:.2f}")
            ax.axhline(min_val, color='purple', linestyle='--', linewidth=1, label=f"Min: {min_val:.2f}")

            ax.legend(loc='upper right')
        else:
            ax.axis('off')  # Skip categorical data for boxplots

    # Remove any unused subplots
    for j in range(len(column_names), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def plot_boxplots_by_columns_hue(df, column_names, hue):
    """
    Plots boxplots for a list of columns in a DataFrame, with up to 8 plots in a single figure.
    Annotates each plot with mean, median, max, and min values.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column_names (list of str): The list of column names to plot.

    Returns:
        None
    """
    # Check if all columns exist in the DataFrame
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    numeric_features = df.select_dtypes(['float', 'int']).columns.tolist()
    sets = [set(lst) for lst in [numeric_features, column_names]]

    column_names = list(set.intersection(*sets))

    # Set up the figure
    num_columns = len(column_names)
    num_rows = (num_columns + 3) // 4
    fig, axes = plt.subplots(num_rows, 4, figsize=(20, 5 * num_rows))
    axes = axes.flatten()
    fig.suptitle('Features númericas: boxplot', fontsize=20)
    for i, column_name in enumerate(column_names):
        ax = axes[i]
        if df[column_name].dtype != 'object' and df[column_name].dtype.name != 'category':
            # Plot boxplot for numerical data
            sns.boxplot(data=df, y=column_name, ax=ax, hue=hue, palette='Blues')
            ax.set_title(f"{column_name}")
            ax.set_ylabel(column_name)

            ax.legend(loc='upper right')
        else:
            ax.axis('off')  # Skip categorical data for boxplots

    # Remove any unused subplots
    for j in range(len(column_names), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(y_test, y_pred):
    conf_matrix = confusion_matrix(y_test, y_pred)

    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=np.unique(y_test),
                yticklabels=np.unique(y_test))
    plt.title('Matriz de Confusão')
    plt.xlabel('Predito')
    plt.ylabel('Verdadeiro')
    plt.show()


def plot_bar_list_features(df: pd.DataFrame, feature_list: list[str], column_name='diabetes'):
    fig, axes = plt.subplots(1, 2, figsize=(15, 2 * 3))
    fig.suptitle('Features: quantidade de observações ', fontsize=20)

    axes = axes.flatten()
    for i, column in enumerate(feature_list):

        df_counts = df.groupby(f'{column}').count()[column_name].sort_values(ascending=False).reset_index(name='count')[
                    0:10]
        df_counts[f'{column}'] = df_counts[f'{column}'].astype(str)
        bars = axes[i].bar(df_counts[f'{column}'], df_counts['count'], color='lightskyblue', edgecolor='black')
        for bar in bars:
            yval = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom')
        axes[i].set_xticklabels(df_counts[f'{column}'], rotation=45, ha='right')
        axes[i].set_title(f'{column}', fontsize=12)

        axes[i].tick_params(axis='x', rotation=45)
        axes[i].set_ylim(0, max(df_counts['count']) + 10000)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def calculate_correlation_matrix(dataframe, variables):
    """
    Calculates the correlation matrix for multiple binary variables.

    Args:
      dataframe: A pandas DataFrame containing the data.
      binary_variables: A list of names of the binary variable columns (0 or 1).

    Returns:
      A pandas DataFrame representing the correlation matrix.
      Returns None if variables are not found.
    """
    if all(var in dataframe.columns for var in variables):
        correlation_matrix = dataframe[variables].corr(method='pearson')
        return correlation_matrix
    else:
        print("Warning: One or more binary variables not found in the DataFrame.")
        return None