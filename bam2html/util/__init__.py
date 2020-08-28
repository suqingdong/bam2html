# -*- coding=utf-8 -*-
import os
import re
import sys
import subprocess
from collections import defaultdict


def safe_open(filename, mode='r'):
    if 'w' in mode:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return open(filename, mode=mode)


def run_cmd(cmd):
    print('>>> run cmd: \x1b[32m{}\x1b[0m'.format(cmd))
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout = res.stdout.read().decode()
    stderr = res.stderr.read().strip()

    if stdout:
        return stdout
    elif stderr:
        print('ERROR: {}'.format(stderr))
        exit(1)


def check_samtools(samtools):
    cmd = samtools + ' --version'
    res = run_cmd(cmd)
    if res:
        print('use samtools: {} (version: {})'.format(samtools, res.split('\n')[0]))
    else:
        print('samtools not exists, please check!')

        
def check_bam_index(bam, samtools):
    bam_index = bam + '.bai'
    if not os.path.exists(bam_index):
        cmd = '{samtools} index {bam}'.format(**locals())
        print('bam index not exists. creating with cmd: {}'.format(cmd))
        assert not os.system(cmd)


def samtools_tview(bam, chrom, pos, reference=None, samtools='samtools', column=None):
    cmd = '{samtools} tview -d H -p {chrom}:{pos} {bam} '
    if reference:
        cmd += reference
    if column:
        cmd = 'COLUMNS={column} ' + cmd

    cmd = cmd.format(**locals())

    
    res = run_cmd(cmd)
    if res:
        return res


def parse_position(position, column):
    """
        - chrom:pos
        - chrom:start-end
        - chrom:pos1,pos2,pos3
    """
    chrom, pos_info = position.split(':')
    if pos_info.isdigit():
        pos = int(pos_info)
        start_pos = pos - column / 2
        pos_list = [pos]
    else:
        if '-' in pos_info:
            start, end = map(int, pos_info.split('-'))
            pos_list = range(start, end + 1)
        elif ',' in pos_info:
            pos_list = map(int, pos_info.split(','))
            start = min(pos_list)
            end = max(pos_list)
        else:
            print('bad position format, use with: chrom:pos or chrom:start-end or chrom:pos1,pos2,...')
            exit(1)

        if end - start > column:
            print('your region({start}-{end}) is larger than column({column})!'.format(**locals()))
            exit(1)

        start_pos = start - (column - end + start) / 2
        
    return chrom, start_pos, pos_list


def get_relative_index(ref_span, position, first_position):

    highlight_index = int(position) - int(first_position)
    linelist = re.split(r'<.*?>', ref_span)
    total_len = 0
    indel_len = 0
    for part in linelist:
        if part:
            if re.match(r'^\*+$', part):
                indel_len += len(part)
                continue
            total_len += len(part)
            if total_len > highlight_index:
                relative_index = highlight_index + indel_len
                return relative_index


def add_highlight_class(seq, index, n, base_stat, is_ref):
    base = seq[index]
    if not is_ref:
        base_stat[n][base.upper()] += 1

    highlight_base = '<i class="highlight" index="{}">{}</i>'.format(n, base)
    new_seq = seq[:index] + highlight_base + seq[index + 1:]

    return new_seq


def highlight_span(span, relative_index, n, base_stat, is_ref):

    linelist = re.split(r'(<.*?>)', span)

    total_len = 0
    for idx, each in enumerate(linelist):
        if not re.match(r'^<.*?>$', each):
            total_len += len(each)
            if total_len > relative_index:
                real_index = relative_index - (total_len - len(each))
                linelist[idx] = add_highlight_class(linelist[idx], real_index, n, base_stat, is_ref)
                break
    return ''.join(linelist)


def parse_html(html, pos_list, new_title, css=None):
    out_html = ''
    for line in html.strip().split('\n'):
        if not line.startswith('</style>'):
            out_html += line
            continue
        if css:
            out_html += css

        prefix = re.findall(r"(</style>.+?<pre class='tviewpre'>)", line)[0]
        out_html += prefix
        suffix = '</pre></div></body></html>'

        # the left position in html, it might be different with input when there are insertions
        origin_title = re.findall(r"<div class='tviewtitle'>(.*?:\d+?)</div>", prefix)[0]
        first_position = origin_title.split(':')[1]

        
        spans = re.findall(r'(<span.*?)<br/>', line)

        # the last span has no <br/>
        last_span = re.findall(r'<br/>(<span[^(br)]*?</span>)</pre>', line)[-1]

        # the first span is position information
        position_line = spans[0] + '<br/>'
        out_html += position_line

        # ref_span might exist *(insertion)
        ref_span = spans[1]
        relative_indexes = [get_relative_index(ref_span, pos, first_position) for pos in pos_list]

        new_spans = []
        base_stat = {}
        for i, span in enumerate(spans[1:] + [last_span]):
            is_ref = True if i == 0 else False
            for n, relative_index in enumerate(relative_indexes, 1):
                if n not in base_stat:
                    base_stat[n] = defaultdict(int)
                span = highlight_span(span, relative_index, n, base_stat, is_ref)
            new_spans.append(span)

        out_html += '<br/>'.join(new_spans) + '<br/>'
        for n in range(1, len(relative_indexes) + 1):
            for base in ('A', 'T', 'C', 'G'):
                if base not in base_stat[n]:
                    base_stat[n][base] = 0
            total = sum(v for k,v in base_stat[n].items() if k != ' ')
            base_stat[n]['deletion'] = base_stat[n]['*']
            base_stat[n]['total'] = total
            # print(base_stat[n])
            title = 'title="total reads: {total}&#10;mutations: A={A} T={T} C={C} G={G}&#10;deletions: {deletion}"'
            title = title.format(**base_stat[n])
            # print(title)
            out_html = out_html.replace('index="{}"'.format(n), title)
    
    # remove the last span's <br/>
    out_html = out_html[:-5]
    out_html += suffix
    out_html = out_html.replace(origin_title, new_title)

    return out_html




if __name__ == '__main__':
    
    # print(parse_position('1:100', 80))
    # print(parse_position('1:100', 200))
    # print(parse_position('chr1:100', 80))

    # print(parse_position('1:100-105', 80))
    # print(parse_position('1:100-200', 80))


    bam = 'example/demo.1_985460.bam'
    position = '1:985460'
    position = '1:985460-985463'
    column = 500

    chrom, start_pos, pos_list = parse_position(position, column)
    print(position)
    print(chrom, start_pos)
    print(pos_list)

    color = 'red'
    background = 'yellow'
    bold = 'none'
    highlight_css = '.highlight {{color:{color};background:{background};font-weight:{bold};font-style:normal;}}\n'.format(**locals())

    html = samtools_tview(bam, chrom, start_pos, column=column)
    out_html = parse_html(html, pos_list, position, css=highlight_css)
    with open('out.html', 'w') as out:
        out.write(out_html)