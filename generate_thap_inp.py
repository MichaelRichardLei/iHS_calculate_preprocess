#Program:
	#Generate thap inp file from hap legend file
	#files 1). *_afterQC_removed_snps.txt	2). *.AA	3). *.hap	4). *.legend
#History:
#	2019/01/09	MichaelLei	Haven'v Release
#	2019/01/10	MichaelLei	Add RemoveTriAllele()
#	2019/01/15	MichaelLei	Add Main()
#	2019/01/16	MichaelLei	import sys
import sys

def file_len(fname):
	#Function
	#	input file and return how many line file has.
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def get_file_mother_dir(filedir:str):
        #Function:
        #       input a file directory, output motherdirectory of that file.
        #Format:
        #       inputed file directory should be absolute directory.
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

def Mergehaplegend(hapdir:str, legenddir:str, outputdir:str, outfilename:str):
	#Function
	#	input hap and legend file, output merged file.
	
	#Check if hap and legend has same number of rows.
	################################################
	print("Merging hap/legend file.........")
	################################################
	if file_len(hapdir) != file_len(legenddir) -1:
		print("Error:hap file has different number of rows with legend file!")
	else:
		hapf = open(hapdir)
		legendf = open(legenddir)
		haplegendfile = open(outputdir+"/"+outfilename+"_haplotype.haplegend",'w')
		line1 = legendf.readline()
		for line1 in legendf:
			line1 = line1.replace("\n"," ")
			line2 = hapf.readline()
			line3 = line1 + line2
			haplegendfile.write(line3)

def MatchDuplicateBetweenFiles(filePath1,filePath2,keyColumn1:int,keyColumn2:int):
	#Function
	#	input 2 file directory and key column numbers, output 2 duplicate file by key.
	f1 = open(filePath1)
	f2 = open(filePath2)
	f3 = open(filePath1+".duplicate",'w')
	f4 = open(filePath2+".duplicate",'w')
	dict1 = dict(); dict2 = dict()
	key1 = list()
	key2 = list()
	for line1 in f1:
		list1 = line1.split()
		dict1[list1[keyColumn1-1]]=line1
		key1.append(list1[keyColumn1-1])
	for line2 in f2:
		list2 = line2.split()
		dict2[list2[keyColumn2-1]]=line2
		key2.append(list2[keyColumn2-1])
	if(file_len(filePath1)<=file_len(filePath2)):
		for key in key1:
			try:
				print(dict1[key]+'\n'+dict2[key])
				f3.write(dict1[key])
				f4.write(dict2[key])
			except KeyError:
				continue
	else:
		for key in key2:
			try:
				print(dict1[key]+'\n'+dict2[key])
				f3.write(dict1[key])
				f4.write(dict2[key])
			except KeyError:
				continue

def deleteQC_removed(haplegenddir:str, QC_removeddir:str, outfilename:str):
	#Function
	#	Equals to quality control, remove snp in afterQC_removed_snps according to position
	#	output haplegend file
	###########################################
	print("Quality controling................")
	###########################################
	haplegendf = open(haplegenddir)
	QC_removedf = open(QC_removeddir)
	newhaplegendf = open(get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved.haplegend",'w')
	
	posset= set()
	line2 = QC_removedf.readline()#skip head
	for line2 in QC_removedf:
		list2 = line2.split()
		posset.add(list2[2])
	print(len(posset))	

	i = 0
	j = 0
	n = 0
	haplegendset = set()
	for line1 in haplegendf:
		list1 = line1.split()
		pos = list1[1]
		n += 1
		if pos in posset:
			i += 1
			continue
		elif pos  not in haplegendset:
			newhaplegendf.write(line1)
			haplegendset.add(pos)
			j += 1
	print("pos in QCset:"+str(i))
	print("pos in haplegendset/writed:"+str(j))

def RemoveTriAllele(haplegenddir:str, outfilename:str):# 2019/01/10
	#Function
	#	Extract duplicate snp in haplegend file according to position number.
	#############################################
	print("Removing Tri-allele.................")
	#############################################
	haplegendf = open(haplegenddir)
	newhaplegendf = open(get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved_withoutTriAllele.haplegend",'w')
	TriAllelehaplegendf = open(get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved.TriAllele",'w')
	TriAllelehaplegendf.write("## This file writes tri-allele snps \n")
	
	snpset = set()
	dupset = set()
	for line1 in haplegendf:
		list1 = line1.split()
		if list1[1] in snpset:
			TriAllelehaplegendf.write(list1[0]+""+list1[1]+" "+list1[2]+" "+list1[3]+"\n")
			dupset.add(list1[1])
		else:
			snpset.add(list1[1])
	
	haplegendf = open(haplegenddir)
	for line1 in haplegendf:
		list1 = line1.split()
		if list1[1] in dupset:
			continue
		else:
			newhaplegendf.write(line1)
		
	
	

def MatchAAoutput(haplegenddir:str, AAdir:str, outfilename:str):
	#function
	#	Match snp in haplegend_withoutQCremoved.haplegend with AA file according to position.
	#	output thap file and inp file.
	##############################################
	print("MatchAAoutput:thap/inp...............")
	##############################################
	AAf = open(AAdir)
	AAdictAA = dict()
	AAdictRsid = dict()
	line1 = AAf.readline()#skip head
	for line1 in AAf:
		list1 = line1.split()
		AAdictAA[list1[1]] = list1[2]
		AAdictRsid[list1[1]] = list1[0]

	haplegendf = open(haplegenddir)
	
#	thapf = open(get_file_mother_dir(haplegenddir)+"/chr22_haplotype_withoutQCremoved.thap",'w')
#	inpf = open(get_file_mother_dir(haplegenddir)+"/chr22_haplotype_withoutQCremoved.inp",'w')
#	notmatch = open(get_file_mother_dir(haplegenddir)+"/chr22_haplotype_withoutQCremoved.nomatchAA",'w')

	## Modified at 2019/01/10	MichaelLei
	thapf = open(get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved_withoutTriAllele.thap",'w')
	inpf = open(get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved_withoutTriAllele.inp",'w')
	notmatch = open(get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved_withoutTriAllele.nomatchAA",'w')
	## Modified
	notmatch.write("#This file writes snps in haplegend file that no match in AA file\n")
	for line2 in haplegendf:
		list2 = line2.split()
		list3 = list2.copy()
#		print(line2)
		if list2[1] in AAdictAA:
			line2left = list2[0]+" "+list2[1]+" "+list2[2]+" "+list2[3] # To be stored in inp file
			print(list2[1])
			
			##Delete inp file infomation, and stored haplotype to $line2right.
			##Transform  $line2right (0,1) to (N,N) and stored to thap file.
			list3.pop(0);list3.pop(0);list3.pop(0);list3.pop(0);
			line2right=""
			for i in list3:
				line2right = line2right + " " + i
			line2right = line2right.replace("0",list2[2]); line2right = line2right.replace("1",list2[3])
			line2right = line2right[1:]
			#print(list2[1])

			##Write inp information
			print(AAdictAA[list2[1]]+" "+list2[2]+" "+list2[3])
			if AAdictAA[list2[1]] == list2[2]:
				inpf.write(AAdictRsid[list2[1]]+" 22 "+list2[1]+" "+AAdictAA[list2[1]]+" "+list2[3]+"\n")
				thapf.write(line2right+"\n")
			elif AAdictAA[list2[1]] == list2[3]:
				inpf.write(AAdictRsid[list2[1]]+" 22 "+list2[1]+" "+AAdictAA[list2[1]]+" "+list2[2]+"\n")
				thapf.write(line2right+"\n")
			else:
				notmatch.write(list2[1]+"\n")
				print("Warn: Not matched!!!")

#Mergehaplegend("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/1000GP_Phase3_chr22.hap","/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/1000GP_Phase3_chr22.legend")
#deleteQC_removed("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/chr22_haplotype.haplegend","/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/1000GP_Phase3_chr22_afterQC_removed_snps.txt")
#RemoveTriAllele("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/chr22_haplotype_withoutQCremoved.haplegend")
#MatchAAoutput("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/chr22_haplotype_withoutQCremoved_withoutTriAllele.haplegend","/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/chr22_exclude_sv.AA")

def Main():
	hapdir = sys.argv[1]
	print(".hap file directory (Absolute Path):"+hapdir)
	legenddir = sys.argv[2]
	print(".legend directory (Absolute Path):"+legenddir)
	outputdir = sys.argv[3]
	print("output dir:"+outputdir)
	outfilename = sys.argv[4]
	print("output file name:"+outfilename)
	QCfiledir = sys.argv[5]
	print("QCfile is:"+QCfiledir)
	AAfile = sys.argv[6]
	print("AA file is:"+AAfile)
#	Mergehaplegend(hapdir, legenddir, outputdir, outfilename)
	haplegenddir = outputdir+"/"+outfilename+"_haplotype.haplegend"
#	deleteQC_removed(haplegenddir, QCfiledir, outfilename)
	afterQC_haplegenddir = get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved.haplegend"
#	RemoveTriAllele(afterQC_haplegenddir, outfilename)
	TriAllele_afterQC_haplegenddir = get_file_mother_dir(haplegenddir)+"/"+outfilename+"_haplotype_withoutQCremoved_withoutTriAllele.haplegend"
	MatchAAoutput(TriAllele_afterQC_haplegenddir, AAfile, outfilename)

Main()
#MatchDuplicateBetweenFiles("/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/CHR_22/rehh_CEU_chr22.txt","/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/CHR_22/CEU_chr22.1kg.p3.allPops.iHS.txt",1,3)
