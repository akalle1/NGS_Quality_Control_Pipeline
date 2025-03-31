# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os
import sys
from quality_analyzer import analyze_fastq_quality

# 1. Quality Score Distribution Plot
def plot_score_distribution(quality_distribution):
    plt.figure(figsize=(10, 6))
    scores = list(quality_distribution.keys())
    counts = list(quality_distribution.values())
    plt.bar(scores, counts, color='blue', alpha=0.7, edgecolor='black')
    # Set x-axis labels and title
    plt.xlabel('Quality Score')
    plt.ylabel('Frequency')
    plt.title('Quality Score Distribution')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.show()

# 2. GC Content Histogram
def plot_gc_content(gc_content):
    plt.figure(figsize=(10, 6))
    # Create histogram of GC content
    plt.hist(gc_content, bins=50, color='green', alpha=0.7, edgecolor='black')
    # Set x-axis labels and title
    plt.xlabel('GC Content (%)')
    plt.ylabel('Frequency')
    plt.title('GC Content Distribution')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.show()

# 3. Per-Base Quality Boxplots
def plot_per_base_quality(quality_stats):
    # Define positions as sorted base positions from quality_stats keys
    positions = sorted(quality_stats.keys())
    plt.figure(figsize=(12, 6))
    # Create boxplot of per-base quality scores using values for each position
    data = [list(quality_stats[pos].values()) for pos in positions]
    sns.boxplot(data=data, palette='Set3')
    # Set x-axis labels and title
    plt.xlabel('Base Position')
    plt.ylabel('Quality Score')
    plt.title('Per Base Quality Scores')
    plt.xticks(ticks=np.arange(len(positions)), labels=positions, rotation=45)
    plt.tight_layout()
    plt.show()

# 4. Sequence Length Distribution Histogram
def plot_sequence_length_distribution(basic_stats):
    plt.figure(figsize=(10, 6))
    sequence_lengths = basic_stats.get('sequence_lengths', [])
    # Create histogram of sequence lengths
    plt.hist(sequence_lengths, bins=50, color='purple', alpha=0.7, edgecolor='black')
    # Set x-axis labels and title
    plt.xlabel('Sequence Length')
    plt.ylabel('Frequency')
    plt.title('Sequence Length Distribution')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.show()

# Main function
def main(fastq_file):
    results = analyze_fastq_quality(fastq_file)
    # Call each plotting function with the loaded data.

    plot_score_distribution(results['n_content']['quality_distribution'])
    plot_gc_content(results['basic_stats']['gc_content'])
    plot_per_base_quality(results['quality_stats'])
    plot_sequence_length_distribution(results['basic_stats'])

# Run script if executed directly
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualizer.py <fastq_file>")
        sys.exit(1)
    fastq_file = sys.argv[1]
    main(fastq_file)
