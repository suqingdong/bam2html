# -*- coding=utf-8 -*-
import os
import colorama

from bam2html import util

colorama.init()


__version__ = '1.0.0'

__author__ = 'suqingdong'
__author_email__ = 'suqingdong@novogene.com'


class Bam2HTML(object):
    def __init__(self, bam, positions, reference=None,
                 column=80, color='red', background='yellow', samtools='samtools',
                 **kwargs):
        self.bam = bam
        self.positions = positions
        self.reference = reference
        self.column = column
        self.color = color
        self.background = background
        self.samtools = samtools

    def highlight(self):

        util.check_samtools(self.samtools)
        util.check_bam_index(self.bam, self.samtools)

        css = '.highlight {{color:{color};background:{background};font-style:normal;}}\n'
        css = css.format(**self.__dict__)

        sample = os.path.basename(self.bam).split('.')[0]

        for position in self.positions:
            chrom, start_pos, pos_list = util.parse_position(position, self.column)
            html = util.samtools_tview(self.bam, chrom, start_pos, column=self.column, reference=self.reference)
            out_html = util.parse_html(html, pos_list, position, css=css)

            outfile = '{}.{}.html'.format(sample, position.replace(':', '_'))
            with util.safe_open(outfile, 'w') as out:
                out.write(out_html)

            print('save file: {}'.format(outfile))
