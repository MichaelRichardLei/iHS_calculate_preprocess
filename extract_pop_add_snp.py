#Program:	
	#Extract  population from thap file by column
	#files: 1). *thap 	2). *_popcolumns.txt

#History:
#	2019/01/09	MichaelLei	Haven't Release
#	2019/01/10	MichaelLei	Modify output file name
#	2019/01/15	MichaelLei	Add add_snp()

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

def get_filename_from_dir(filedir:str):
        #Function
        #       input a file directory, return file name.
        #Format:
        #       Inputed file directory should be absolute directory
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

########################################Not Finished#########################################################################
def add_snp(thapdir:str, inpdir:str, snpthapdir:str, rsid:str, position:int, AA:str, DA:str):
	#Function
	#	input 1).thap	2).inp	3).snpthapdir
	#	output addsnp file
	
	inpf = open(inpdir)
	newinpf = open(get_file_mother_dir(inpdir)+"/"+get_filename_from_dir(inpdir)+"_"+rsid+".inp",'w')
	poslist = list()
	i = 0
	for line1 in inpf:
		list1 = line1.split()
		poslist.append(list1[2])
		i += 1
		if int(poslist[-1]) > position and int(poslist[-2] < position):
			newinpf.write(rsid+" 22 "+str(position)+" "+AA+" "+DA+"\n")
			snpline = i
			newinpf.write(line1)
		else:
			newinpf.write(line1)
	
	thapf = open(thapdir)
	newthapf = open(get_file_mother_dir(thapdir)+"/"+get_filename_from_dir(thapdir)+"_"+rsid+".thap",'w')
	n = 0
	for line2 in thapf:
		list2 = line2.split()		
###################################################################################################################		



def extract_pop_by_column(thapdir:str, popdir:str, outputdir:str, outfilename:str):
	#Function
	#	input thap file and pop column file, output thap file of corresponding population

	thapf = open(thapdir)
	popf = open(popdir)
	popcolumnlist = list()
	for line2 in popf:
		list2 = line2.split()
		popcolumnlist.append(list2[0])
	
#	newthapf = open(get_file_mother_dir(thapdir)+"/CHS_chr22_haplotype_withoutQCremoved.thap",'w')
	##Modified	2019/01/10	MichaelLei
	newthapf = open(outputdir+"/"+outfilename+"_"+get_filename_from_dir(thapdir)+".thap",'w')
	##Modified
	for line1 in thapf:
		list1 = line1.split()
		for column in popcolumnlist:
			column = int(column) - 1
			newthapf.write(list1[2*column -1]+" "+ list1[2*column]+" ")
		newthapf.write("\n")

thapdir = "/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/CHR_22/chr22_haplotype_withoutQCremoved_withoutTriAllele.thap" 
popdir = "/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/CEU_columns.sample"
outputdir = "/home/leiyao/1000G_plink/iHS_calculate/chr22_afterQC/CHR_22"
outfilename = "CEU"
extract_pop_by_column(thapdir, popdir, outputdir, outfilename)
