#Program:
	#Extract Ancestral Allele from vcf gz file according to position
	#files: 1). 1.vcf.gz	2). position.txt
#History:
#	2019/01/08	MichaelLei	Haven't Release
#	2019/01/11	MichaelLei	Add get_file_name_from_dir()/Modify extract_AA()
#	2019/01/15	MichaelLei	Add Main Function: 1).filedir 2).output dir 3).filename


import sys
import os
import re
import gzip

def get_file_mother_dir(filedir:str):
	#Function:
	#	input a file directory, output motherdirectory of that file.
	#Format:
	# 	inputed file directory should be absolute directory.
	motherdir = ""
	list1 = filedir.split("/")
	list1.pop() # Remove last element of list.
	for i in list1:
		if i == '':
			continue
		else:
			motherdir = motherdir + "/" + i
	print("Mother directory is: "+motherdir)
	return motherdir

def get_filename_from_dir(filedir:str):
	#Function
	#	input a file directory, return file name.
	#Format:
	#	Inputed file directory should be absolute directory
	list1 = filedir.split("/")

	if list1[-1] != "":
		list2 = list1[-1].split(".")
		list2.pop(-1)
	else:
		list2 = list1[-2].split(".")
		list2.pop(-1)

	filename = ""
	for i in list2:
		filename = filename + "." + i
	filename = filename[1:]
	return filename

def extract_from_vcf_gz(posdir:str, vcfgzdir:str, chromosome:int):
	#Function:
	#	input 1).position txt file directory, 2).vcf file directory 3).chromosome number
	#	extract rsID INFO from vcf.gz file by position
	f1 = open(posdir)
	f2 = open(vcfgzdir,'w')
	os.chdir(get_file_mother_dir(vcfgzdir))
	for pos in f1:
		pos=pos.replace("\n","")
#		print(pos)
		os.system("tabix ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 22:"+pos+"-"+pos+" | awk '{print $3 \"\t\"$8}' >> /home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/chr22.vcf")
		#f2.write(os.environ["var"]+"\n")

#Since extract_from_vcf_gz file is too slow as it use tabix, I decide to write a new function.
#2019/01/09	MichaelLei
def extract_from_vcf_gz_2(filedir:str, outputdir:str, filename:str):
	#Function:
	#	input vcfgz file directory.
	#	output vcf information. Output is .vcf
	
	#############################
	print("Creating vcf file.......")
	#############################

	#gzip read gz file
	vcffile = gzip.open(filedir)
#	vcf_dict = dict()
	newvcf = open(outputdir+"/"+filename+".vcf",'w')
	#skip vcf head and match information to dictionary by key(position)
	for line2 in vcffile:
		line2 = str(line2)[2:-1] #binary file read out is b'<something>', transform to regular string
		list2 = line2.split("\\t") # During transform, tab becames chracter, use double backslash to identify it.
		if re.match(r'#.',line2) == None:
			#print(line2)
#			vcf_dict[list2[1]] = list2[0]+"\t"+list2[1]+"\t"+list2[2]+"\t"+list2[3]+"\t"+list2[4]+"\t"+list2[5]+"\t"+list2[6]+"\t"+list2[7]+"\t"+list2[8]+"\n"
			newvcf.write(list2[0]+"\t"+list2[1]+"\t"+list2[2]+"\t"+list2[3]+"\t"+list2[4]+"\t"+list2[5]+"\t"+list2[6]+"\t"+list2[7]+"\t"+list2[8]+"\n")


def exclude_sv(vcffiledir:str):
	#Function:
	#	exclude structure variant from file generated from extract_from_vcf_gz()
	#2019/01/09	MichaelLei	
		#As this function is to exclude structure variants, I delete the funciton.
	###############################
	print("Exclude Structure Variants............")
	###############################
	pattern1 = re.compile(r'rs\d+')
	pattern2 = re.compile(r'END=\d+')
	file1 = open(vcffiledir)
	file2 = open(get_file_mother_dir(vcffiledir)+"/"+get_filename_from_dir(vcffiledir)+"_exclude_sv.vcf",'w')
	for line1 in file1:
#		list1 = line1.split()
#		list1 = list1[0].split(":")
		if re.findall(pattern1,line1) == None:
			print(line1)
			continue
		else:
			'''#2019/01/09 MichaelLei
			list1 = line1.split()
			list2 = list1[1].split(":")
#			END = re.match(pattern2,list1[1])
#			print(list1[1])
#			pos = END.replace("END=","")
			file2.write(list1[0]+"\t")
			for i in list2:
				file2.write(i+"\t")
			file2.write("\n")
			'''
			file2.write(line1)

def extract_AA(vcffiledir:str):
	#Function:
	#	extract ancestral allele from file generated by exclude_sv().
	#####################################
	print("Extracting Ancestral Alleles...........")
	#####################################
	pattern = re.compile(r'AA=.')
	file1 = open(vcffiledir)
	file2 = open(get_file_mother_dir(vcffiledir)+"/"+get_filename_from_dir(vcffiledir)+".AA",'w')
	file2.write("rsid position Ancestral_allele\n")
	file3 = open(get_file_mother_dir(vcffiledir)+"/"+get_filename_from_dir(vcffiledir)+"_withoutAA.txt",'w')
	file3.write("#This is file writes snp that without Ancestal allele in vcf file\n")
	for line1 in file1:
		list1 = line1.split()
		if re.findall(pattern,list1[7]) == None:
			file3.write(list1[2]+"\t"+list1[1]+"\n")
		else:
#			print(re.findall(pattern,list1[1]))
			output = str(re.findall(pattern,list1[7]))
			output = output.replace("[\'AA=","")
			output = output.replace("\']","")
			if output == "." or output == "|" or output == "[]" or output == "-" or output == "N":
				file3.write(list1[2]+"\t"+list1[1]+"\n")
				continue
			else:
				file2.write(list1[2]+"\t"+list1[1]+"\t"+output.upper()+"\n")

##########################################################################################
##########################   Not   used function     #####################################
def match_gens_transform(gensfile:str, AAfile:str): #No use 2019/01/09 Michael Lei
	#Function:
	#	1).match snp in AA file with gens file.
	#	2).transform gens to .inp and .thap(0,1 to N,N)
	gensf = open(gensfile)
	AAf = open(AAfile)
	inpf = open(get_file_dir(gensfile)+"/chr22_exclude_sv.inp",'w')
	thapf = open(get_file_dir(gensfile)+"/chr22_exclude_sv.thap",'w')
	notmatchf = open(get_file_dir(gensfile)+"/chr22_exclude_sv.nomatch",'w')
	AAdict = dict()
	for snp1 in AAf:
		snplist = snp1.split()
		AAdict[snplist[0]] = snplist[1]
	for line2 in gensf:
		genslist = line2.split()
		snp2 = genslist[0].split(":")[0]
		if snp2 in AAdict and (genslist[3] == AAdict[snp2] or genslist[4] == AAdict[snp2]):
		
			if genslist[3] == AAdict[snp2]:
				inpf.write(snp2+"\t"+"22"+"\t"+genslist[2]+"\t"+AAdict[snp2]+"\t"+genslist[4]+"\n")
			elif genslist[4] == AAdict[snp2]:
				inpf.write(snp2+"\t"+"22"+"\t"+genslist[2]+"\t"+AAdict[snp2]+"\t"+genslist[3]+"\n")
#			else:
#				print("Warning:Ancestral Allele is not matched, snp is :" + snp2)
#				notmatchf.write(snp2+"\t"+AAdict[snp2]+"\t"+genslist[3]+"\t"+genslist[4]+"\n")
			ref = genslist[3]
			alt = genslist[4]
			genslist.pop(0);genslist.pop(0);genslist.pop(0);genslist.pop(0);genslist.pop(0)
			# To delete other infomation
			for i in genslist:
				i = i.replace("0",ref)
				i = i.replace("1",alt)
				thapf.write(i+" ")
			thapf.write("\n")
		elif snp2 in AAdict:
			print("Warning:Ancestral Allele is not matched, snp is :" + snp2)
			notmatchf.write(snp2+"\t"+AAdict[snp2]+"\t"+genslist[3]+"\t"+genslist[4]+"\n")

def extract_pop_from_thap(thapfile:str, popfile:str): # No use 2019/01/09 Michael Lei
	#Function
	#	extract thap haplotype file from thap file according to population file
	thapf = open(thapfile)
	popf = open(popfile)
	newthapf = open(get_file_dir(thapfile)+"/CHS_chr22.thap",'w')
	popcollist = list()
	for line1 in popf:
		list1 = line1.split()
		popcollist.append(list1[0])
	for line2 in thapf:
		list2 = line2.split()
		for i in popcollist:
			i = int(i)
			column = i-1
			newthapf.write(list2[column]+" ")
		newthapf.write("\n")
#######################################Not Used Function##################################################
##########################################################################################################

#Test
#extracr_from_vcf_gz_2("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/position.txt","/home/data/1000G_phase3_v5a/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz")
#exclude_sv("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/test.vcf")
#extract_AA("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/test_exclude_sv.vcf")
#match_gens_transform("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/new_2.gens","/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/chr22_exclude_sv.AA")
#extract_pop_from_thap("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/chr22_exclude_sv.thap","/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/CHS.pop")

def Main():
	filedir = sys.argv[1]
	print("vcfgz file direction (absolute directory) is:"+filedir)
	outputdir = sys.argv[2]
	print("output dir is:"+outputdir)
	filename = sys.argv[3]
	print("out file name is:"+filename)
	if not os.path.exists(outputdir):
		os.makedirs(outputdir)
	extract_from_vcf_gz_2(filedir, outputdir, filename)
	vcffiledir = outputdir+"/"+filename+".vcf"
	exclude_sv(vcffiledir)
	vcffiledir2 = get_file_mother_dir(vcffiledir)+"/"+get_filename_from_dir(vcffiledir)+"_exclude_sv.vcf"
	extract_AA(vcffiledir2)

Main()
