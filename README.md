# Generate Highlighted HTML of Bam
> highlight the specific sites of html which output by `samtools tview`


## Dependencies
- Linux/Unix
- Samtools


## Usage
```bash
bam2html -i <input.bam> [-r <ref.fa>] chrom:pos...
bam2html -i <input.bam> chrom:start-end
```


## Meaning of Base's Colors
| Color | Mapping Quality | Selector |
| - | - | - |
| Blue | 0-9 | .tviewcu1 |
| Green | 10-19 | .tviewc2 |
| Yellow | 20-29 | .tviewc3 |
| Black |>=30 | .tviewc4 |

> Underline: Secondary or orphan

