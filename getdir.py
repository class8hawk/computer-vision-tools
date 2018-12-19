import os

srcdir=r'原始库'
distdir=r'bigimg'


l1srcdirs=os.listdir(srcdir)

for l1srcdir in l1srcdirs:
    l1fullpath=os.path.join(srcdir,l1srcdir)
    if(os.path.isdir(l1fullpath)):
        if not os.path.exists(os.path.join(distdir,l1srcdir)):
            os.makedirs(os.path.join(distdir,l1srcdir))
        l2srcdirs=os.listdir(l1fullpath)
        for l2srcdir in l2srcdirs:
            l2fullpath=os.path.join(l1fullpath,l2srcdir)
            if os.path.isdir(l2fullpath):
                if not os.path.exists(os.path.join(distdir,l1srcdir,l2srcdir)):
                    os.makedirs(os.path.join(distdir,l1srcdir,l2srcdir))