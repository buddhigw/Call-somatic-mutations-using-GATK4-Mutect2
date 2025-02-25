import subprocess
import os
import sys
import shlex

#Tumor | Normal 
#Given a matched normal, Mutect2 is designed to call somatic variants only. The tool includes logic to skip emitting variants that are clearly present in the germline based on provided evidence, e.g. in the matched normal. 
#command='gatk --java-options "-Xmx62G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true>" Mutect2 -R /gatk/somatic/resources/Homo_sapiens_assembly38.fasta -I /gatk/somatic/sample/normal/RB121_recal.bam -normal RB121_sample -I /gatk/somatic/sample/tumor/SC93652_recal.bam -tumor SC93652_sample --germline-resource /gatk/somatic/gnomad/gatk/somatic-hg38_af-only-gnomad.hg38.vcf.gz -pon /gatk/somatic/pon_final/pon.vcf.gz -ip 100 -L /gatk/somatic/capture_kits/merge_newSort.bed --f1r2-tar-gz /gatk/somatic/SC93652_results/SC93652_f1r2.tar.gz  -O /gatk/somatic/SC93652_results/SC93652_unfiltered.vcf'
#splits1=shlex.split(command)
#print(splits1)
#with open('output.txt','wb') as output, open('err.txt','wb') as err:
#    subprocess.run(splits1,stdout=output,stderr=err)
#    output.close()
#    err.close()
#    os.wait
#
#
#
####Tumor Only Mode#######
#This mode runs on a single type of sample, e.g. the tumor or the normal. 
command='gatk --java-options "-Xmx62G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true>" Mutect2 -R /gatk/somatic/resources/Homo_sapiens_assembly38.fasta -I /gatk/somatic/sample/tumor/tumor_recal.bam --germline-resource /gatk/somatic/gnomad/gatk/somatic-hg38_af-only-gnomad.hg38.vcf.gz -pon /gatk/somatic/pon_final/pon.vcf.gz -ip 100 -L /gatk/somatic/capture_kits/merge_newSort.bed --f1r2-tar-gz /gatk/somatic/results/tumor_sample_f1r2.tar.gz  -O /gatk/somatic/results/tumor_sample_unfiltered.vcf'
splits1=shlex.split(command)
print(splits1)
with open('output.txt','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait

#Generate an artifact prior table for each tumor sample for FilterMutectCalls to use.
command='gatk --java-options "-Xmx56G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true>" LearnReadOrientationModel -I /gatk/somatic/SC93652_results/SC93652_f1r2.tar.gz  -O /gatk/somatic/SC93652_results/SC93652_read-orientation-model.tar.gz'
splits1=shlex.split(command)
print(splits1)
with open('output.txt','wb') as output, open('err.txt','wb') as err:
        subprocess.run(splits1,stdout=output,stderr=err)
        output.close()
        err.close()
        os.wait

#Summarizes counts of reads that support reference, alternate and other alleles for given sites. Results can be used with CalculateContamination.
command='gatk --java-options "-Xmx56G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true>" GetPileupSummaries -I /gatk/somatic/sample/tumor/SC93652_recal.bam -V /gatk/somatic/gnomad/gatk/somatic-hg38_af-only-gnomad.hg38.vcf.gz -L /gatk/somatic/capture_kits/merge_newSort.bed -O /gatk/somatic/SC93652_results/SC93652_pileup.table'
splits1=shlex.split(command)
print(splits1)
with open('output.txt','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait 


#Calculates the fraction of reads coming from cross-sample contamination.
command='gatk --java-options "-Xmx56G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true>" CalculateContamination -tumor-segmentation segments.table -I /gatk/somatic/SC93652_results/SC93652_pileup.table -O /gatk/somatic/SC93652_results/SC93652_calculatecontamination.table'
splits1=shlex.split(command)
print(splits1)
with open('output.txt','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait 

#Filter variants in a Mutect2 VCF callset.
command='gatk --java-options "-Xmx56G -DGATK_STACKTRACE_ON_USER_EXCEPTION=true>" FilterMutectCalls -R /gatk/somatic/resources/Homo_sapiens_assembly38.fasta -V /gatk/somatic/SC93652_results/SC93652_unfiltered.vcf --contamination-table /gatk/somatic/SC93652_results/SC93652_calculatecontamination.table --ob-priors /gatk/somatic/SC93652_results/SC93652_read-orientation-model.tar.gz --filtering-stats /gatk/somatic/SC93652_results/SC93652_unfiltered.vcf.stats -O /gatk/somatic/SC93652_results/SC93652_filtered.vcf'
splits1=shlex.split(command)
print(splits1)
with open('output.txt','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait

#Annotate using DBs
###Clinvar
command='java -Xmx29G -jar /gatk/somatic/tools/snpEff/SnpSift.jar annotate -name clinvar_ /gatk/somatic/resource_bundle_GATK/clinvar/clinvar_20191007_with_chr.vcf /gatk/somatic/SC93652_results/SC93652_filtered.vcf'  
splits1=shlex.split(command)
print(splits1)
with open('/gatk/somatic/SC93652_results/SC93652_filtered_clinvar.vcf','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait

##Cosmic
command='java -Xmx29G -jar /gatk/somatic/tools/snpEff/SnpSift.jar annotate -name cosmic_ /gatk/somatic/Cosmic/CosmicCodingMuts.normal.vcf /gatk/somatic/SC93652_results/SC93652_filtered_clinvar.vcf'  
splits1=shlex.split(command)
print(splits1)
with open('/gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic.vcf','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait
#
####dbSNP
command='java -Xmx29G -jar /gatk/somatic/tools/snpEff/SnpSift.jar annotate -name dbSNP /gatk/somatic/add_resource_bundlt_GATK/dbsnp_151.vcf.gz /gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic.vcf'  
splits1=shlex.split(command)
print(splits1)
with open('/gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic_dbsnp.vcf','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait
##
###dbSNP4
command='java -jar /gatk/somatic/tools/snpEff/SnpSift.jar dbnsfp -v -db /gatk/somatic/add_resource_bundlt_GATK/dbNSFP4.1.txt.gz /gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic_dbsnp.vcf'
splits1=shlex.split(command)
print(splits1)
with open('/gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic_dbsnp_dbsnp4.vcf','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait
#
###vartype
command='java -jar /gatk/somatic/tools/snpEff/SnpSift.jar varType /gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic_dbsnp_dbsnp4.vcf' 
splits1=shlex.split(command)
print(splits1)
with open('/gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic_dbsnp_dbsnp4-varType.vcf','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait
####
####SIFT
command='java -jar /gatk/somatic/tools/SIFT/SIFT4G_Annotator.jar -c -i /gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic_dbsnp_dbsnp4-varType.vcf -d /gatk/somatic/tools/SIFT/GRCh38.83.chr -r /gatk/wes/somatic/SC93652_results/'
splits1=shlex.split(command)
print(splits1)
with open('output.txt','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait

#extract essential fields for further analysis
command='java -Xmx29G -jar /gatk/somatic/tools/snpEff/SnpSift.jar extractFields -s "," -e "." /gatk/somatic/SC93652_results/SC93652_filtered_clinvar_cosmic_dbsnp_dbsnp4-varType.vcf CHROM POS ID REF ALT QUAL FILTER clinvar_CLNDN clinvar_CLNHGVS clinvar_CLNSIG clinvar_GENEINFO cosmic_AA cosmic_CDS cosmic_CNT cosmic_GENE cosmic_HGVSC cosmic_HGVSG cosmic_LEGACY_ID dbNSFP_MutationTaster_pred dbNSFP_PROVEAN_pred dbNSFP_Polyphen2_HDIV_pred dbNSFP_Polyphen2_HVAR_pred dbNSFP_SIFT_pred VARTYPE'  
splits1=shlex.split(command)
print(splits1)
with open('/gatk/somatic/SC93652_results/SC93652_sample_new.txt','wb') as output, open('err.txt','wb') as err:
    subprocess.run(splits1,stdout=output,stderr=err)
    output.close()
    err.close()
    os.wait

