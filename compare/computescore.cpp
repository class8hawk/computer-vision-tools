#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include "cublas_v2.h"
#include <iostream>
#include <dirent.h>
#include <vector>
#include <list>
#include <string.h>
#include<fstream>

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/io.h>

#include <string>
using namespace std;

int getAbsoluteFiles(string directory, list<string>& filesAbsolutePath) //参数1[in]要变量的目录  参数2[out]存储文件名
{
    DIR* dir = opendir(directory.c_str()); //打开目录   DIR-->类似目录句柄的东西 
    if ( dir == NULL )
    {
        cout<<directory<<" is not a directory or not exist!"<<endl;
        return -1;
    }

    struct dirent* d_ent = NULL;       //dirent-->会存储文件的各种属性
    char fullpath[128] = {0};
    char dot[3] = ".";                //linux每个下面都有一个 .  和 ..  要把这两个都去掉
    char dotdot[6] = "..";

    while ( (d_ent = readdir(dir)) != NULL )    //一行一行的读目录下的东西,这个东西的属性放到dirent的变量中
    {
        if ( (strcmp(d_ent->d_name, dot) != 0)&&
               (strcmp(d_ent->d_name, dotdot) != 0) )   //忽略 . 和 ..
        {
            if ( d_ent->d_type == DT_DIR ) //d_type可以看到当前的东西的类型,DT_DIR代表当前都到的是目录,在usr/include/dirent.h中定义的
            {

                string newDirectory = directory + string("/") + string(d_ent->d_name); //d_name中存储了子目录的名字
                if( directory[directory.length()-1] == '/')
                {
                    newDirectory = directory + string(d_ent->d_name);
                }
                           
                if ( -1 == getAbsoluteFiles(newDirectory, filesAbsolutePath) )  //递归子目录
                {
                    return -1;
                }
            }
            else   //如果不是目录
            {
                string absolutePath = directory + string("/") + string(d_ent->d_name);  //构建绝对路径
                if( directory[directory.length()-1] == '/')  //如果传入的目录最后是/--> 例如a/b/  那么后面直接链接文件名
                {
                    absolutePath = directory + string(d_ent->d_name); // /a/b/1.txt
                }
                filesAbsolutePath.push_back(absolutePath);
                if(filesAbsolutePath.size()%10000==0)
                {
                  cout<<"readfile:"<<filesAbsolutePath.size()<<endl;

                }
            }
        }
    }

    closedir(dir);
    return 0;
}




static void Split_string(const string& strSrc, const string& splitCh, vector<string>& splitString)
{
	splitString.clear();

	if (strSrc.size() == 0)
	{
		return;
	}

	size_t startpos = 0;
	size_t found = strSrc.find_first_of(splitCh.c_str());
	if (found == string::npos)
	{
		splitString.push_back(strSrc);
		return;
	}

	while (found != string::npos)
	{
		splitString.push_back(strSrc.substr(startpos, found - startpos));
		startpos = found + 1;
		found = strSrc.find_first_of(splitCh.c_str(), startpos);
	}

	if (strSrc.size() != startpos)
	{
		splitString.push_back(strSrc.substr(startpos, strSrc.size() - startpos));
	}

}

void readfeaturefromtxt(float* A,list<string>& file,int k,vector<string>& idstring)
{
           int A_index=0;

           for(list<string>::iterator it = file.begin();it!=file.end();it++) //readtxt
           {
              vector<string> splits;
              const string dirname=*it;
              Split_string(dirname,"/",splits);
              //cout<<splits[splits.size()-2]<<endl;
              idstring.push_back(splits[splits.size()-2]);
              
              ifstream readFile(*it);



              //cout<<*it<<endl;
               float temp;
               for(int kindex=0;kindex<k;kindex++)
               {
                 readFile >>temp;   
                 A[A_index*k+kindex]=temp;
                 


               }
              readFile.close();
              
              
              A_index++;

           }






}






int main(void)
{
   int batchsize=30000;

    int const m = batchsize;
    int const n = batchsize;
    int const k =512;
    float *A ,*B,*C;
    float *d_A,*d_B,*d_C;
    A = (float*)malloc(sizeof(float)*m*k);  
    B = (float*)malloc(sizeof(float)*n*k);  
    C = (float*)malloc(sizeof(float)*m*n); 
    
    float alpha = 1.0;
    float beta = 0.0;
    cudaMalloc((void**)&d_A,sizeof(float)*m*k);
    cudaMalloc((void**)&d_B,sizeof(float)*n*k);
    cudaMalloc((void**)&d_C,sizeof(float)*m*n);
    cublasHandle_t handle;
    cublasCreate(&handle);


   string leftdir="/media/hasx/DATA3/facedata/res/resr";
   //string leftdir="/media/hasx/DATA3/facedata/test/resl";
   string rightdir = "/media/hasx/DATA3/facedata/test/resr";
   bool self=true;
   list<string> leftfiles;
   cout<<"getfile------------------>"<<endl;
   getAbsoluteFiles(leftdir,leftfiles);
   
   int lefttotal=leftfiles.size();
   cout<<"lefttotal file:"<<lefttotal<<endl; 
   //recursion_scan_dir_file(leftdir.c_str(),1);
    if(self)
    {
        int index=0;
        int leftdirnum=lefttotal/batchsize+1;
        vector<list<string>> leftdirproc;
        list<string> each;
        for(list<string>::iterator it = leftfiles.begin();it!=leftfiles.end();it++)
        {
            index++;
            

            if(index%100000==0)
            {
                cout<<"split:cur:"<<index<<"  total:"<<lefttotal<<endl;
            }
            
            
            if(each.size()==batchsize)
            {
                leftdirproc.push_back(each);
                each.clear();
            }


            each.push_back(*it);

            if(index==lefttotal)
            {
                leftdirproc.push_back(each);
                each.clear();

            }
        }
        for(int i=0;i<leftdirproc.size();i++)
        {
           cout<<i<<"   total:"<<leftdirproc.size()<<endl;
           vector<string> Aidstring;
           
           readfeaturefromtxt(A,leftdirproc[i],k,Aidstring);
           //return 0;
           for (int j=i;j<leftdirproc.size();j++)
           {
             cout<<"L2:"<<j<<"   total:"<<leftdirproc.size()<<endl;
               vector<string> Bidstring;
               readfeaturefromtxt(B,leftdirproc[j],k,Bidstring);
                
               cudaMemcpy(d_A,A,sizeof(float)*m*k,cudaMemcpyHostToDevice);
               cudaMemcpy(d_B,B,sizeof(float)*n*k,cudaMemcpyHostToDevice);

              
               cublasSgemm(handle, CUBLAS_OP_T, CUBLAS_OP_N, m, n, k, &alpha, d_A, k, d_B, k, &beta, d_C, m);//<测试二>
               //cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_T, m, n, k, &alpha, d_A, m, d_B, n, &beta, d_C, n);
               cudaMemcpy(C,d_C,sizeof(float)*m*n,cudaMemcpyDeviceToHost);
               for (int i = 0; i< m*n;i++){
                //std::cout <<C[i]<<"\t";
                if(C[i]>0.5)
                {
                    int aindex=i%m;
                    int bindex=i/m;
                    if(aindex>=Aidstring.size()||bindex>=Bidstring.size())
                    {
                        continue;
                    }
                    if(Aidstring[aindex]==Bidstring[bindex])
                    {
                        continue;
                    }
                    string saveresname="res/"+Aidstring[aindex]+"_"+Bidstring[bindex]+"_"+to_string(int(C[i]*100))+".txt";
                    ofstream OutFile(saveresname); //利用构造函数创建txt文本，并且打开该文本

                    OutFile << Aidstring[aindex]<<"    "<<Bidstring[bindex]<<"    "<<C[i]<<endl;;  //把字符串内容"This is a Test!"，写入Test.txt文件

                    OutFile.close();         

                   
                }
               }

           }

        }
    }
    
   


   
  
    free(A);
    free(B);
    free(C);
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    cublasDestroy(handle);
}
