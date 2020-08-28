"""\x1b[1;32m\
====================================================
 _                     ____  _     _             _ 
| |__   __ _ _ __ ___ |___ \| |__ | |_ _ __ ___ | |
| '_ \ / _` | '_ ` _ \  __) | '_ \| __| '_ ` _ \| |
| |_) | (_| | | | | | |/ __/| | | | |_| | | | | | |
|_.__/ \__,_|_| |_| |_|_____|_| |_|\__|_| |_| |_|_|

                    -- View Bam in Highlighted HTML
====================================================
\x1b[0m"""


import argparse

from bam2html import Bam2HTML, __epilog__, __version__


def main():

    parser = argparse.ArgumentParser(
        prog='bam2html',
        description=__doc__,
        epilog=__epilog__,
        formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-v', '--version', help='show program\'s version number and exit', action='version', version=__version__)

    parser.add_argument('bam', help='the input bamfile', nargs='?')
    parser.add_argument('positions', help='the positions or regions to highlight', nargs='*')

    parser.add_argument('-r', '--reference', help='the reference genome')
    parser.add_argument('-c', '--column',
                        help='the size of column window [%(default)s]', type=int, default=200)

    parser.add_argument('-O', '--outdir',
                        help='the output directory [%(default)s]', default='.')
    parser.add_argument('-o', '--prefix', help='the prefix of output file')

    parser.add_argument('-color', '--color',
                        help='the color highlighted base [%(default)s]', default='red')
    parser.add_argument('-bg', '--background',
                        help='the background color of highlighted base [%(default)s]', default='yellow')

    parser.add_argument('-samtools', '--samtools',
                        help='the executable path of samtools [%(default)s]', default='samtools')

    args = parser.parse_args()

    if not (args.bam and args.positions):
        parser.print_help()
        exit()

    Bam2HTML(**vars(args)).highlight()


if __name__ == '__main__':
    main()
