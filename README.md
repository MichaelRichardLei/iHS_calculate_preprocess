# iHS_calculate_preprocess
This is my first time using github, so there will definitely be many problems，I will keep updating, suggestion is welcomed.

This is just a record of my project. If anyone are interested but have problems to use, just contact me.

###############################################################################################

This project use python, preprocess data before calculating iHS by R package rehh(https://github.com/cran/rehh).

Transform Data to "Example 2" in rehh, (SHAPIT2-like)

1.map file(Ancestral allele).

  Download vcf.gz file from 1000 Genome project, and use extract_AA_from_vcf_gz.py to extract Ancestral allele.

2.thap file(hap file).

  Download hap/legend file from SHAPIT2, and use generate_thap_inp.py to transform hap$legend file to thap/inp file.

3.calculate iHS.

  Use R with rehh.
