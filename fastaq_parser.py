#CORE FUNCTIONALITY
#create a fastaq_parser.py for reading and parsing FASTQ files
#add basic statistics functionality (read length)

#open the fastaq file
#read the file line by line
def parse_fastq(fastq_file_path):

    """
    Parse a FASTQ file  and yield tuple of (header, sequence, quality)
    Args:
    fastq_file_path: path to the FASTQ file
    Yield:
    (header, sequence, quality)
    """
    #open the file
    try:
        with open(fastq_file_path, 'r') as fastq_file:
    
            while True:
                #4 lines per record
                #read the header line
                header = fastq_file.readline().strip()
                if not header:
                    break
                #read the sequence line
                sequence = fastq_file.readline().strip()

                #read the plus (separator) line
                plus = fastq_file.readline().strip()
                #read the quality line
                quality = fastq_file.readline().strip()

                #check if header starts with @ 
                if header.startswith('@'):
                    header = header[1:]
                yield (header, sequence, quality)

    except FileNotFoundError:
        print(f'Error: {fastq_file_path} not found')
        yield from []


#caclulate thhe basic statistics for the fastq file
#calculate read length distribution- min, max, average, distribution
def calculate_basic_stats(fastq_file_path):
    #intialize variables
    read_count = 0
    total_length = 0
    min_length = float('inf') #starts with infinity for minumum comparison
    max_length = 0

    #loop through the fastq file
    for header, sequence, quality in parse_fastq(fastq_file_path):
        read_count += 1
        seq_length = len(sequence)
        #calculate the total length - calculate the sum of all the sequence lengths
        total_length += seq_length
        #calculate the min length   
        if seq_length < min_length:
            min_length = seq_length
        #calculate the max length
        if seq_length > max_length:
            max_length = seq_length

    #handles empty file cases
    if read_count == 0:
        average_length = 0
        min_length = 0
    else:
        #calculuate the average length
        average_length = total_length / read_count
    return {'read_count': read_count, 'total_length': total_length, 'min_length': min_length, 'max_length': max_length, 'average_length': average_length}

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        fastq_file_path = sys.argv[1]
    else:
        fastq_file_path = 'example.fastq'

#call the function and display results
stats = calculate_basic_stats(fastq_file_path)

print("FASTQ File Statistics:")
print(f"Total reads: {stats['read_count']}")
print(f"Total bases: {stats['total_length']}")
print(f"Minimum read length: {stats['min_length']}")
print(f"Maximum read length: {stats['max_length']}")
print(f"Average read length: {stats['average_length']:.2f}") 



    



