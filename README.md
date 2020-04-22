#### Sequence_Cleaner: Remove Duplicate Sequences, Short Sequences, etc
### WARNING: 
I originally created this script using [Biopython](https://biopython.org/wiki/Sequence_Cleaner) back in the day, and 
recently I decided to re-write using Pysam and Python 3. I hope you enjoy it.

* [Installation](#installation)
  * [dependencies](#dependencies)
  * [git](#git)
* [Usage](#usage)

## Installation
### Dependencies
  - [Python 3.6](http://www.python.org/download)
  - [Setuptools 36.0.1](https://setuptools.readthedocs.io/en/latest/)
  - [Pysam 0.15.3](https://pypi.org/project/pysam/)

### Git

	# these steps should install the dependencies

	# clone repo
	git clone git@github.com:metageni/Sequence-Cleaner.git

	# install tool
	cd Sequence-Cleaner && pip install -U -r requirements.txt && python setup.py install

## Usage
    usage: sequence_cleaner [-h] [-v] -q QUERY -o OUTPUT_DIRECTORY
                            [-ml MINIMUM_LENGTH] [-mn PERCENTAGE_N]
                            [--keep_all_duplicates] [-l LOG]
    
    Sequence Cleaner: Remove Duplicate Sequences, etc
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -q QUERY, --query QUERY
                            Path to directory with FAST(A/Q) files
      -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                            Path to output files
      -ml MINIMUM_LENGTH, --minimum_length MINIMUM_LENGTH
                            Minimum length allowed (default=0 - allows all the
                            lengths)
      -mn PERCENTAGE_N, --percentage_n PERCENTAGE_N
                            Percentage of N is allowed (default=100)
      --keep_all_duplicates
                            Keep All Duplicate Sequences
      -l LOG, --log LOG     Path to log file (Default: STDOUT).
    
    example > sequence_cleaner -q INPUT -o OUTPUT
