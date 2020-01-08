# ISWC-performance
Reports of how our wikifier system performs on the ISWC challenge files

The reports for each file in each round of the challenge have been classified into one of 4 categories based on our performance on them
so we can focus on those files that we have performed poorly on.

## evaluate.py 

The script used to evaluate files.

Before running this script, you will need to install the wikidata wikifier service provided in the link below

https://github.com/usc-isi-i2/wikidata-wikifier

### Usage: 

python evaluate.py -f '<'file_paths'>' -c <'column_names'> -r <'round_numbers'> -g<'gt_path'> -o <'output_path'>

file_paths: space seperated file names

column_names: space seperated corresponding column names

round_numbers: space seperated corresponding round numbers (ISWC challenge rounds). If using files only from one round, do not have to repeat the round numbers. (As shown in example 2 below, both files belong to round 1)

gt_path: Path to directory containing all GT's (Path to data folder)

output_path: Output directory path

Usage examples: 

python evaluate.py -f '8468806_0_4382447409703007384.csv' -c 'Name' -r '1' -g '/Users/narendivvala/ISI' -o '/Users/narendivvala/ISI/Tests'

python evaluate.py -f '8468806_0_4382447409703007384.csv /Users/narendivvala/ISI/9475172_1_1023126399856690702.csv' -c 'Name Title' -r '1' -g '/Users/narendivvala/ISI/' -o '/Users/narendivvala/ISI/Tests'
