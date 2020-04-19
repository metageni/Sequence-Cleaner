# !/usr/bin/env python3

# -*- coding: utf-8 -*-

import argparse
import logging
import os

from collections import defaultdict
from pathlib import Path

from sequence_cleaner_app import version

from pysam import FastxFile

LOGGER_FORMAT = '[%(asctime)s - %(levelname)s] %(message)s'
RC_TRANS = str.maketrans('ACGTNacgtn', 'TGCANTGCAN')


def is_wanted_file(queries):
    """List with input files with aceptable extensions (.fna/.fasta/.fastq).

    Args:
        queries (list of str): List with query names.

    Returns:
        list of str: Sorted list with only .fasta/.fastq/.fna files.

    """
    queries = [query for query in queries if Path(query).suffix.lower() in [".fna", ".fasta", ".fastq"]]
    queries.sort()

    return queries


def reverse_complement(sequence):
    """This function finds the reverse complement for a given DNA sequence.


    Args:
        sequence (str): DNA sequence.

    Returns:
        str: Reverse complement.

    """
    return sequence[::-1].translate(RC_TRANS)


def write_fasta(sequences_hash, output_fasta, concatenate_duplicates=True):
    """Write FASTA file output based on sequences and ids from the hash.

    Args:
        sequences_hash (collections.defaultdict): Hash with clean sequences.
        output_fasta (str): Path to FASTA output.

    """
    with open(output_fasta, "w+") as fasta_object:
        for sequence in sequences_hash:
            if concatenate_duplicates:
                sequence_id = "__".join(sequences_hash[sequence])
                fasta_object.write(">{}\n{}\n".format(sequence_id, sequence))
            else:
                sequence_id = sequence
                sequence = sequences_hash[sequence_id][0]
                fasta_object.write(">{}\n{}\n".format(sequence_id, sequence))



def sequence_cleaner(fasta_q_file, min_length=0, percentage_n=100.0, concatenate_duplicates=True):
    """Read FASTA/FASTQ file and clean the file.

    Args:
        fasta_q_file (str): Path to FASTA/Q file.
        min_length (str): Minimum length allowed (default=0 - allows all the lengths).
        percentage_n (float): % of N is allowed (default=100).
        concatenate_duplicates (bool): Remove duplicate and keep one sequence (default: True)

    Returns:
        collections.defaultdict: Hash with clean sequences.
        int: # Sequences Processed.
        int: # Repeated Sequences.
        int: # Repeated Sequences (Reverse Complement).
        int: # Short Sequences.
        int:  # High N Sequences.

    """
    hash_sequences = defaultdict(list)

    total_sequences_processed = 0
    total_repeated_sequences = 0
    total_repeated_sequences_rc = 0
    total_short_sequences = 0
    total_high_n_sequences = 0

    with FastxFile(fasta_q_file) as fh:
        for entry in fh:
            total_sequences_processed += 1
            sequence_id = entry.name
            sequence = entry.sequence.upper()

            # remove sequences that are shorter or equal to `min_length`
            if len(sequence) <= min_length:
                total_short_sequences += 1
                continue
            # remove sequences that do noot meet the % N
            elif (float(sequence.count("N")) / float(len(sequence))) * 100 > percentage_n:
                total_high_n_sequences += 1
                continue

            elif concatenate_duplicates:
                # repeated sequence - add sequence ID to hash
                if sequence in hash_sequences:
                    hash_sequences[sequence].append(sequence_id)
                    total_repeated_sequences += 1
                else:
                    rc = reverse_complement(sequence)
                    # check if reverse complement is already in hash
                    # if so, add modified ID and flags that the sequence reverse complement was repeated
                    if rc in hash_sequences:
                        hash_sequences[rc].append("{}_RC".format(sequence_id))
                        total_repeated_sequences += 1
                        total_repeated_sequences_rc += 1

                    # if not, it means it was the first time the sequence was seen - add it to hash
                    else:
                        hash_sequences[sequence].append(sequence_id)
            else:
                hash_sequences[sequence_id].append(sequence)


    return (hash_sequences, total_sequences_processed, total_repeated_sequences, total_repeated_sequences_rc,
            total_short_sequences, total_high_n_sequences)


def parse_args():
    """Parse args entered by the user.

    Returns:
        argparse.Namespace: Parsed arguments.

    """
    parser = argparse.ArgumentParser(description="Sequence Cleaner: Remove Duplicate Sequences, etc",
                                     epilog="example > sequence_cleaner -q INPUT -o OUTPUT")
    parser.add_argument('-v', '--version', action='version', version='sequence_cleaner {}'.format(version))
    parser.add_argument("-q", "--query", help="Path to directory with FAST(A/Q) files", required=True)
    parser.add_argument("-o", "--output_directory", help="Path to output files", required=True)
    parser.add_argument("-ml", "--minimum_length", help="Minimum length allowed (default=0 - allows all the lengths)",
                        default="0")
    parser.add_argument("-mn", "--percentage_n", help="Percentage of N is allowed (default=100)", default="100")
    parser.add_argument('--concatenate_duplicates', help='Keep All Duplicate Sequences', action='store_false', required=False)
    parser.add_argument('-l', '--log', help='Path to log file (Default: STDOUT).', required=False)

    return parser.parse_args()


def main():
    args = parse_args()

    query = Path(args.query)
    output_directory = Path(args.output_directory)
    minimum_length = int(args.minimum_length)
    percentage_n = float(args.percentage_n)
    concatenate_duplicates = args.concatenate_duplicates
    print(">>>>>>>> ", concatenate_duplicates)

    if args.log:
        logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO, filename=args.log)
    else:
        logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO)

    logger = logging.getLogger(__name__)

    logger.info("Sequence_Cleaner: Remove Duplicate Sequences, etc - version {}".format(version))

    # check if output_directory is exists - if not, creates it
    if not output_directory.exists():
        Path(output_directory).mkdir(parents=True, mode=511)
        logger.info("OUTPUT: {} does not exist - just created it :)".format(output_directory))

    # check if at least one of the queries is valid
    if not query.is_dir():
        logger.critical("QUERY: {} is not a directory".format(query))

    query_files = is_wanted_file([temp_query for temp_query in os.listdir(query)])

    for counter, fasta_q_file in enumerate(query_files):
        logger.info("1.{}) Cleaning input: {}/{}".format(counter + 1, query, fasta_q_file))
        (hash_sequences, total_sequences_processed, total_repeated_sequences, total_repeated_sequences_rc,
         total_short_sequences, total_high_n_sequences) = sequence_cleaner("{}/{}".format(query, fasta_q_file), minimum_length, percentage_n,
                                                                           concatenate_duplicates)

        output_path = "{}/clean_{}".format(output_directory, fasta_q_file)
        logger.info("1.{}) Writing Results: {}".format(counter + 1, output_path))
        write_fasta(hash_sequences, output_path, concatenate_duplicates)

        logger.info("1.{}) Stats for: {}".format(counter + 1, output_path))
        logger.info("1.{}) - # Sequences Processed: {}".format(counter + 1, total_sequences_processed))
        logger.info("1.{}) - # Repeated Sequences: {}".format(counter + 1, total_repeated_sequences))
        logger.info(
            "1.{}) - # Repeated Sequences (Reverse Complement): {}".format(counter + 1, total_repeated_sequences_rc))
        logger.info("1.{}) - # Short Sequences: {}".format(counter + 1, total_short_sequences))
        logger.info("1.{}) - # High N Sequences: {}".format(counter + 1, total_high_n_sequences))

    logger.info('Done :)')


if __name__ == "__main__":
    main()
