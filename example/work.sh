bam2html -b demo.1_985460.bam 1:985460 -r /data/www/data/genomes/b37/b37.fa
bam2html -b demo.1_985460.bam 1:985460,985463,985469 -r /data/www/data/genomes/b37/b37.fa
bam2html -b demo.1_985460.bam 1:985461-985465 -r /data/www/data/genomes/b37/b37.fa
bam2html -bl bam_list pos_list -r /data/www/data/genomes/b37/b37.fa 
bam2html -bl bam_list pos_list -r /data/www/data/genomes/b37/b37.fa -s
bam2html -bl bam_list pos_list -r /data/www/data/genomes/b37/b37.fa -s -x zip
