# Generate Highlighted HTML of Bam
> highlight the specific sites of html which output by `samtools tview`


## Dependencies
- Linux/Unix
- Samtools
- Python2/Python3


## Usage
```bash
bam2html <input.bam> chrom:pos           # single position
bam2html <input.bam> chrom:pos1,pos2...  # multiple positions
bam2html <input.bam> chrom:start-end     # a region of positions
bam2html <input.bam> chrom:pos -r /path/to/reference.fa # with reference
```

## Meaning of Base's Colors
| Color | Mapping Quality | Selector |
| - | - | - |
| Blue | 0-9 | .tviewcu1 |
| Green | 10-19 | .tviewc2 |
| Yellow | 20-29 | .tviewc3 |
| Black |>=30 | .tviewc4 |

> Underline: Secondary or orphan

