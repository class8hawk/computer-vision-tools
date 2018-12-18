import os
import os.path
rootdir=r"F:\work"
savedir=r"E:\backupework20171214" #千万不要放同一个盘下面 不然走远



index=0
for parent,dirnames,filenames in os.walk(rootdir):
	for filename in filenames:
		index=index+1
		#if index<1180000:
		#	continue
		if index%10000==0:
			logfile=open('logflie.txt','a')
			logfile.write(str(index)+'\n')
			logfile.close()
		#print("processing %d file in total " % (index))
		ext=os.path.splitext(filename)[1]
		#print(ext)
		if ext==".cpp" or ext==".h" or ext==".c" or ext==".cxx" or ext==".py":
			saveparent=parent.replace(rootdir,savedir)
			orgfilename=os.path.join(parent,filename)
			copyfilename=os.path.join(saveparent,filename)
			print("org:%s" % orgfilename)
			print(copyfilename)
			#print(os.path.join(saveparent,filename))
			if not os.path.exists(saveparent):
				os.makedirs(saveparent)
			os.system ("copy %s %s" % (os.path.join(parent,filename), os.path.join(saveparent,filename)))
			if os.path.isfile (os.path.join(saveparent,filename)):
				print ("Success")
