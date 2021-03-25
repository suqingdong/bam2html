[![DOI](https://zenodo.org/badge/291003590.svg)](https://doi.org/10.5281/zenodo.4005607)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/suqingdong/bam2html)

# Generate Highlighted HTML of Bam
> highlight the specific sites of bam with `samtools tview`


## Dependencies
- Linux/Unix
- Python2/Python3
- samtools
- tar/gzip/zip [optional for compressing]


## Installation
```bash
pip install bam2html
```


## Usage
```bash
bam2html -b <input.bam> chrom:pos           # single position
bam2html -b <input.bam> chrom:pos1,pos2...  # multiple positions
bam2html -b <input.bam> chrom:start-end     # a region of positions
bam2html -b <input.bam> chrom:pos -r /path/to/reference.fa # with reference
bam2html -b <input.bam> chrom:pos -c 300    # set the width of window
bam2html -b <input.bam> chrom:pos -color pink -bg green    # set colors
bam2html -bl bam_list pos_list                             # batch mode
bam2html -bl bam_list pos_list -s                          # generate summary.html
bam2html -bl bam_list pos_list -s -x zip                   # compress the result with zip
bam2html -bl bam_list pos_list -s -x tar.gz                # compress the result with tar/gzip
```


### Example Results
- single position: [demo.1_985460.html](https://suqingdong.github.io/bam2html/example/demo.1_985460.html)
- multiple positions: [demo.1_985460,985463,985469.html](https://suqingdong.github.io/bam2html/example/demo.1_985460,985463,985469.html)
- region positions: [demo.1_985461-985465.html](https://suqingdong.github.io/bam2html/example/demo.1_985461-985465.html)
- summary result: [summary.html](https://suqingdong.github.io/bam2html/example/summary.html)


## Meaning of Base's Colors
| Color | Mapping Quality | Selector |
| - | - | - |
| Blue | 0-9 | .tviewcu1 |
| Green | 10-19 | .tviewc2 |
| Yellow | 20-29 | .tviewc3 |
| Black |>=30 | .tviewc4 |

> Underline: Secondary or orphan

---
## Documents
https://bam2html.readthedocs.io
