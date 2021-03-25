# -*- coding=utf-8 -*-
import os
import json

from bam2html import util, version_info
from bam2html.util.template import TEMPLATE


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

    def highlight(self, summary=False, compress=None):

        bam_list = []
        position_list = []
        summary_data = []

        if self.bam_list and os.path.isfile(self.bam_list):
            bam_list += util.safe_open(self.bam_list).read().strip().split('\n')
        else:
            bam_list += self.bam.split(',')

        for pos in self.positions:
            if os.path.isfile(pos):
                position_list += util.safe_open(pos).read().strip().split('\n')
            else:
                position_list += [pos]

        print('>>> input bam:\n{}'.format('\n'.join(bam_list)))
        print('>>> input pos:\n{}'.format('\n'.join(position_list)))

        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

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
                html = "<a target='_blank' href='{0}'>{0}</a>".format('{}.{}.html'.format(sample, position.replace(':', '_')))
                summary_data.append({'sample': sample, 'site':position, 'html': html})

        if summary:
            summary_file = os.path.join(self.outdir, 'summary.html')
            with util.safe_open(summary_file, 'w') as out:
                out.write(TEMPLATE.safe_substitute(DATA=json.dumps(summary_data)))
            print('save summary: {}'.format(summary_file))

        if compress is None:
            return
        elif compress == 'tar.gz':
            cmd = 'tar -zcvf {0}.tar.gz {0}'.format(self.outdir)
        elif compress == 'zip':
            cmd = 'zip -r {0}.zip {0}'.format(self.outdir)
        else:
            exit('unaccepted compress method.')

        assert not os.system(cmd)
        print('save compress file: {}.{}'.format(self.outdir, compress))
