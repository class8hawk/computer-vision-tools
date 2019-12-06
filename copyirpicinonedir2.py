import os
import os.path



def copypictodir(rootdir,savedir):
	index=0
	for parent,dirnames,filenames in os.walk(rootdir):
		for filename in filenames:
			index=index+1
			#if index<1180000:
			#	continue
			#if index>10: #test
			#break
			if index%10000==0:
				logfile=open('logflie.txt','a')
				logfile.write(str(index)+'\n')
				logfile.close()
			#print("processing %d file in total " % (index))
			#ext=os.path.splitext(filename)[1]
				#print(ext)
			if filename=="viewImageInfrared.jpg":
				
				orgfilename=os.path.join(parent,filename)
				copyfilename=os.path.join(savedir,str(index)+'_'+filename)
				#print("org:%s" % orgfilename)
				#print(copyfilename)
				#print(os.path.join(saveparent,filename))
				#if not os.path.exists(saveparent):
					#os.makedirs(saveparent)
				#linux
				#cmd="cp \"%s\" \"%s\"" % (os.path.join(parent,filename), os.path.join(saveparent,filename))
				#print(cmd)
				#os.system (cmd)
				#windows
				os.system ("copy %s %s" % (orgfilename, copyfilename))
				if os.path.isfile (copyfilename):
					print ("Success")
####功能：将list对象N等分
def div_list(ls,n):
	if not isinstance(ls,list) or not isinstance(n,int):
		return []
	ls_len = len(ls)
	if n<=0 or 0==ls_len:
		return []
	if n > ls_len:
		return []
	elif n == ls_len:
		return [[i] for i in ls]
	else:
		j = int(ls_len/n)+1
		k = ls_len%n
		print(j,k)
		### j,j,j,...(前面有n-1个j),j+k
		#步长j,次数n-1
		ls_return = []
		for i in range(0,(n-1)*j,j):
			ls_return.append(ls[i:i+j])
		#算上末尾的j+k
		ls_return.append(ls[(n-1)*j:])
		return ls_return

					
def splitdir(srcdir,name,split_num):
	dirs=os.listdir(srcdir)
	list_dirs=div_list(dirs,split_num)
	jpgnameindex=0
	for index,eachlist in enumerate(list_dirs):
		each_savedir=name+'_part'+str(index)
		if not os.path.exists(each_savedir):
			os.makedirs(each_savedir)
		for each_jpg_dir in eachlist:
			jpgnameindex+=1
			jpgfullname=os.path.join(srcdir,each_jpg_dir,'viewImageInfrared.jpg')
			cmd="copy %s %s" % (jpgfullname, os.path.join(each_savedir,'ir'+str(jpgnameindex)+'.jpg'))
			print(cmd)
			os.system (cmd)
	#print(list_dirs)
					
srcdir='1017'
name='langguang1017kuangdongtai'
splitdir(srcdir,name,2)
#rootdir=r"langguang1015part1"
#savedir=r"langguang1015part1ir" #no one path
#if not os.path.exists(savedir):
	#os.makedirs(savedir)