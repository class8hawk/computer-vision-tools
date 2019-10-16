import os
import os.path
rootdir=r"langguang1015part1"
savedir=r"langguang1015part1ir" #no one path

if not os.path.exists(savedir):
	os.makedirs(savedir)

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
