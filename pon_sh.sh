#!/bin/bash
#1.Run Mutect2 in tumor-only mode on each normal sample
gatk --java-options "-Xmx20G" Mutect2 -R /gatk/new_wes/resources/Homo_sapiens_assembly38.fasta -I normal.bam -tumor normal --disable-read-filter MateOnSameContigOrNoMappedMateReadFilter -L Agilent_SureSelect_v7_post_GRCh38-Edited-sorted.interval_list -O normal.vcf.gz
        
#2.Collate all the normal V into a single callset with CreateSomaticPanelOfNormals
gatk --java-options "-Xmx20G" GenomicsDBImport -R /gatk/somatic/resources/Homo_sapiens_assembly38.fasta 
gatk --java-options "-Xmx20G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true" CreateSomaticPanelOfNormals -vcfs /gatk/somatic/pon/tumor1.vcf.gz -vcfs /gatk/somatic/pon/tumor2.vcf.gz -vcfs /gatk/somatic/pon/tumor3.vcf.gz -vcfs /gatk/somatic/pon/tumor4.vcf.gz -vcfs /gatk/somatic/pon/tumor5.vcf.gz -vcfs /gatk/somatic/pon/tumor6.vcf.gz -vcfs /gatk/somatic/pon/tumor7.vcf.gz -vcfs /gatk/somatic/pon/tumor8.vcf.gz -vcfs /gatk/somatic/pon/tumor9.vcf.gz -vcfs /gatk/somatic/pon/tumor10.vcf.gz -vcfs /gatk/somatic/pon/tumor11.vcf.gz -vcfs /gatk/somatic/pon/tumor12.vcf.gz -vcfs /gatk/somatic/pon/tumor13.vcf.gz -vcfs /gatk/somatic/pon/tumor14.vcf.gz -vcfs /gatk/somatic/pon/tumor15.vcf.gz -O /gatk/somatic/pon/15_samplepon.vcf.gz

input_dir=/gatk/somatic/bams
output_dir=/gatk/somatic/pon
for item in $input_dir/*_recal.bam
    do
       s=$(basename $item)
       f_name=${s%_recal.bam}
       echo "$f_name"
       #In tumor-only mode, a single case sample is analyzed with the -tumor flag without an accompanying matched control -normal sample. For the tutorial, we run this command only for sample.
       gatk --java-options "-Xmx20G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true" Mutect2 -R /gatk/somatic/resources/Homo_sapiens_assembly38.fasta -I $input_dir/"$f_name"_recal.bam --max-mnp-distance 0 -O $output_dir/"$f_name".vcf.gz
    done
exit

gatk --java-options "-Xmx56G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true" GenomicsDBImport -R /gatk/somatic/resources/Homo_sapiens_assembly38.fasta -L /gatk/somatic/capture_kits/merge_newSort.bed --genomicsdb-workspace-path pon_db --tmp-dir /gatk/pon_db/tmp --genomicsdb-shared-posixfs-optimizations true --batch-size 16 -V /gatk/somatic/pon/tumor1.vcf.gz -V /gatk/somatic/pon/tumor2.vcf.gz -V /gatk/somatic/pon/tumor3.vcf.gz -V /gatk/somatic/pon/tumor4.vcf.gz -V /gatk/somatic/pon/tumor5.vcf.gz -V /gatk/somatic/pon/tumor6.vcf.gz -V /gatk/somatic/pon/SC3tumor76876.vcf.gz -V /gatk/somatic/pon/tumor7.vcf.gz -V /gatk/somatic/pon/tumor9.vcf.gz -V /gatk/somatic/pon/tumor9.vcf.gz -V /gatk/somatic/pon/tumor10.vcf.gz -V /gatk/somatic/pon/tumor11.vcf.gz -V /gatk/somatic/pon/tumor12.vcf.gz -V /gatk/somatic/pon/tumor14.vcf.gz -V /gatk/somatic/pon/tumor14.vcf.gz -V /gatk/somatic/pon/tumor15.vcf.gz

gatk --java-options "-Xmx56G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true" CreateSomaticPanelOfNormals -R /gatk/somatic/resources/Homo_sapiens_assembly38.fasta --germline-resource /gatk/somatic/gnomad/hg38/gnomad.exomes.r2.1.1.sites.liftover_grch38.vcf.bgz -V gendb:///gatk/somatic/ponbase1 -O /gatk/somatic/pon_final/pon.vcf.gz

