[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4005608.svg)](https://doi.org/10.5281/zenodo.4005608)


# Generate Highlighted HTML of Bam
> highlight the specific sites of html which output by `samtools tview`


## Dependencies
- Linux/Unix
- Samtools
- Python2/Python3


## Usage
```bash
bam2html -b <input.bam> chrom:pos           # single position
bam2html -b <input.bam> chrom:pos1,pos2...  # multiple positions
bam2html -b <input.bam> chrom:start-end     # a region of positions
bam2html -b <input.bam> chrom:pos -r /path/to/reference.fa # with reference
bam2html -b <input.bam> chrom:pos -c 300    # set the width of window
bam2html -b <input.bam> chrom:pos -color pink -bg green    # set colors
bam2html -bl bam_list pos_list                             # batch
```



### Example Results
- single position: [demo.1_985460.html](https://suqingdong.github.io/bam2html/example/demo.1_985460.html)
- multiple positions: [demo.1_985460,985463,985469.html](https://suqingdong.github.io/bam2html/example/demo.1_985460,985463,985469.html)
- region positions: [demo.1_985461-985465.html](https://suqingdong.github.io/bam2html/example/demo.1_985461-985465.html)

## Meaning of Base's Colors
| Color | Mapping Quality | Selector |
| - | - | - |
| Blue | 0-9 | .tviewcu1 |
| Green | 10-19 | .tviewc2 |
| Yellow | 20-29 | .tviewc3 |
| Black |>=30 | .tviewc4 |

> Underline: Secondary or orphan

## Documents
https://bam2html.readthedocs.io
