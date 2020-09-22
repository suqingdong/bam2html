# -*- coding=utf-8 -*-
import os
import colorama

from bam2html import util

colorama.init()


__version__ = '1.0.1'

__author__ = 'suqingdong'
__author_email__ = 'suqingdong@novogene.com'

__epilog__ = '''\x1b[34m
examples:
    %(prog)s
    %(prog)s -b input.bam 1:1234 -r /path/to/reference.fa
    %(prog)s -b input.bam 1:1234 2:4567
    %(prog)s -b input.bam 1:1234,1236,1238
    %(prog)s -b input.bam 1:1234-1238
    %(prog)s -b input.bam 1:1234-1238
    %(prog)s -bl bam_list.txt pos_list.txt
\x1b[36m
contact: {__author__} <{__author_email__}>\
\x1b[0m'''.format(**locals())


class Bam2HTML(object):
    def __init__(self, positions, bam=None, bam_list=None, reference=None,
                 column=80, color='red', background='yellow',
                 samtools='samtools', outdir='.', prefix=None,
                 **kwargs):
        self.bam = bam
        self.bam_list = bam_list
        self.positions = positions
        self.reference = reference
        self.column = column
        self.color = color
        self.background = background
        self.samtools = samtools
        self.outdir = outdir
        self.prefix = prefix

    def highlight(self):

        bam_list = []
        position_list = []

        if self.bam_list and os.path.isfile(self.bam_list):
            bam_list += util.safe_open(self.bam_list).read().strip().split('\n')
        else:
            bam_list += self.bam.split(',')

        for pos in self.positions:
            if os.path.isfile(pos):
                position_list += util.safe_open(pos).read().strip().split('\n')
            else:
                position_list += [pos]

        print(bam_list)
        print(position_list)

        for bam in bam_list:
            util.check_samtools(self.samtools)
            util.check_bam_index(bam, self.samtools)

            css = '.highlight {{color:{color};background:{background};font-style:normal;}}\n'
            css = css.format(**self.__dict__)

            sample = self.prefix or os.path.basename(bam).split('.')[0]

            for position in position_list:
                chrom, start_pos, pos_list = util.parse_position(position, self.column)
                html = util.samtools_tview(bam, chrom, start_pos, column=self.column, reference=self.reference)
                out_html = util.parse_html(html, pos_list, position, css=css)

                outfile = '{}/{}.{}.html'.format(self.outdir, sample, position.replace(':', '_'))
                with util.safe_open(outfile, 'w') as out:
                    out.write(out_html)

                print('save file: {}'.format(outfile))
