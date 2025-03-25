

from collections import defaultdict, Counter
import statistics
import numpy as np
from fastq_parser import parse_fastq, calculate_basic_stats

# Global function for quality score conversion
def quality_to_phred(quality_string):
    """
    Convert ASCII quality characters to Phred+33 scores.
    """
    return [ord(char) - 33 for char in quality_string]

# Per-base quality score analysis
def analyze_per_base_quality(fastq_file_path):
    """
    Analyze quality scores at each base position across all reads.

    Returns a dictionary with position-based statistics:
    {position: {'mean': float, 'median': float, 'q1': float, 'q3': float}}
    """
    # Track scores by position
    position_scores = defaultdict(list)

    # Parse FASTQ and collect scores
    for header, sequence, quality in parse_fastq(fastq_file_path):
        scores = quality_to_phred(quality)
        for pos, score in enumerate(scores):
            position_scores[pos].append(score)

    # Calculate statistics for each position
    position_stats = {}
    for pos, scores in position_scores.items():
        if scores:  # Ensure we have data
            position_stats[pos] = {
                'mean': statistics.mean(scores),
                'median': statistics.median(scores),
                'q1': np.percentile(scores, 25),
                'q3': np.percentile(scores, 75),
                'min': min(scores),
                'max': max(scores)
            }

    return position_stats

# Sequence duplication detection
def analyze_sequence_duplication(fastq_file_path, sample_size=100000):
    """
    Detect sequence duplication levels.

    Returns:
    - duplication_rate: Percentage of reads that are duplicates
    - unique_sequences: Number of unique sequences
    - sequence_counts: Dictionary of {sequence: count}
    """
    # Store all the sequence reads
    sequences = []
    read_count = 0

    # Loop through the FASTQ file
    for header, sequence, quality in parse_fastq(fastq_file_path):
        sequences.append(sequence)
        read_count += 1
        if read_count >= sample_size:
            break

    # Count the occurrence of each sequence
    sequence_counts = Counter(sequences)
    unique_sequences = len(sequence_counts)

    # Calculate the duplication rate
    duplicate_reads = read_count - unique_sequences
    duplication_rate = (duplicate_reads / read_count) * 100 if read_count > 0 else 0

    return {
        'duplication_rate': duplication_rate,
        'unique_sequences': unique_sequences,
        'total_reads': read_count,
        'sequence_counts': dict(sequence_counts.most_common(10))  # Top 10 most common
    }

# N content and quality distribution
def calculate_n_content(fastq_file_path):
    """
    Calculate N content, base composition, and quality distribution.

    Returns:
    - n_content: Percentage of N bases
    - base_content: Dictionary of {base: percentage}
    - quality_distribution: Distribution of quality scores
    """
    # Track base counts and quality scores
    base_counts = Counter()
    total_bases = 0
    quality_scores = []

    # Parse the FASTQ file
    for header, sequence, quality in parse_fastq(fastq_file_path):
        # Count bases
        base_counts.update(sequence)
        total_bases += len(sequence)

        # Count quality scores
        quality_scores.extend(quality_to_phred(quality))

    if total_bases == 0:
        return {'n_content': 0, 'base_content': {}, 'quality_distribution': {}}

    # Calculate the percentage of base counts
    base_content = {base: (count / total_bases) * 100 for base, count in base_counts.items()}

    # Calculate N content
    n_content = base_content.get('N', 0)

    # Calculate quality distribution
    quality_distribution = Counter(quality_scores)

    return {
        'n_content': n_content,
        'base_content': base_content,
        'quality_distribution': dict(quality_distribution)
    }

# Main function
def analyze_fastq_quality(fastq_file_path):
    """
    Perform comprehensive quality analysis on a FASTQ file.
    """
    # Get basic statistics
    stats = calculate_basic_stats(fastq_file_path)

    # Get quality metrics
    quality_stats = analyze_per_base_quality(fastq_file_path)
    duplication_stats = analyze_sequence_duplication(fastq_file_path)
    n_content_stats = calculate_n_content(fastq_file_path)

    return {
        'basic_stats': stats,
        'quality_stats': quality_stats,
        'duplication_stats': duplication_stats,
        'n_content_stats': n_content_stats
    }

