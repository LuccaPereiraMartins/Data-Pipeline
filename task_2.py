import os
import sys


def scan_directory(
    directory: str
    ) -> dict:
    """
    retrive the file stats from a given directory
    """

    # initialise the empty dictionary we will append values to
    file_stats = {}

    # walk through the directory and all its subdirectories
    for root, dirs, files in os.walk(directory):

        for file in files:

            # extract file extension (opt for os instead of slicing string)
            ext = os.path.splitext(file)[1]

            # only process files with an extension
            if ext:  
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)

                # append any new extensions to dictionary
                if ext not in file_stats:
                    file_stats[ext] = {
                        'count': 0,
                        'max_size': 0,
                        'total_size': 0
                    }

                # update file_stats for this entry
                file_stats[ext]['count'] += 1
                file_stats[ext]['max_size'] = max(file_stats[ext]['max_size'], file_size)
                file_stats[ext]['total_size'] += file_size

    return file_stats


def print_stats(file_stats):

    # print the statistics for each file extension in specified format
    for ext, stats in sorted(file_stats.items()):
        print(f"{ext} {stats['count']} {stats['max_size']} {stats['total_size']}")


def main():

    # will admit I looked online for this line
    # get the directory path from the command line argument, default to current directory
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    file_stats = scan_directory(directory)
    print_stats(file_stats)


if __name__ == "__main__":
    main()