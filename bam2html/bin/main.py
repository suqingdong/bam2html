import argparse

from bam2html import Bam2HTML


def main():

    parser = argparse.ArgumentParser(
        prog='bam2html',
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    
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
    parser.add_argument('-size', '--font-size',
                        help='the font size of body [%(default)s]', default=13, type=int)
    parser.add_argument('-samtools', '--samtools',
                        help='the executable path of samtools [%(default)s]', default='samtools')

    args = parser.parse_args()

    if not (args.bam and args.positions):
        parser.print_help()
        exit()


    Bam2HTML(**vars(args)).highlight()


if __name__ == '__main__':
    main()
