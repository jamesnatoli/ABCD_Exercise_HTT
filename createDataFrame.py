import os
import pandas as pd
import numpy as np
import uproot
from glob import glob

def main(args):
    input_files = [
            ifile for ifile in glob('{}/*.root'.format(args.input_dir))
        ]

    all_data = pd.DataFrame()
    for ifile in input_files:
        open_file = uproot.open(ifile)
        for ikey in open_file.iterkeys():            
            input_df = open_file[ikey].arrays( library='pd') # read all columns

            sample_name = ifile.split('/')[-1] # get file name, to save with
            input_df['sample_name'] = np.full(len(input_df), sample_name.split('.root')[0]) # add name to file
            try:
                outname = f'{sample_name.split(".root")[0]}_{args.output}'
                input_df.to_csv( outname)
                file_stats = os.stat( outname)
                print(f'Created {outname}: {file_stats.st_size / (1024 * 1024):.2f} MB')
                size = file_stats.st_size / (1024 * 1024)
                if size > 100:
                    raise Exception
            except:
                print("File Size too big for GitHiub :(")
                print("Git LFS does not work with public works :(")
            
            all_data = pd.concat( [all_data, input_df])
            
    print(all_data)
    # all_data.to_csv(args.output)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--input', '-i', action='store',
                        dest='input_dir', default=None, help='path to all input files')
    parser.add_argument('--output', '-o', action='store', dest='output',
                        default='store.csv', help='name of output file')

    main(parser.parse_args())

