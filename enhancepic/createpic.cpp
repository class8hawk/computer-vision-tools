// createpic.cpp : Defines the entry point for the console application.
//



#include "Dir.hpp"
#include <list>
//饱和度(S)
#if 0  
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include "HSL.hpp"

using namespace std;
using namespace cv;

static string window_name = "photo";
static Mat src;

static HSL hsl;
static int color = 0;
static int hue = 180;
static int saturation = 100;
static int brightness = 100;

static void callbackAdjust(int, void *)
{
	Mat dst;

	hsl.channels[color].hue = hue - 180;
	hsl.channels[color].saturation = saturation - 100;
	hsl.channels[color].brightness = brightness - 100;

	hsl.adjust(src, dst);

	imshow(window_name, dst);
}

static void callbackAdjustColor(int, void *)
{
	hue = hsl.channels[color].hue + 180;
	saturation = hsl.channels[color].saturation + 100;
	brightness = hsl.channels[color].brightness + 100;

	setTrackbarPos("hue", window_name, hue);
	setTrackbarPos("saturation", window_name, saturation);
	setTrackbarPos("brightness", window_name, brightness);
	callbackAdjust(0, 0);
}


int main()
{
	src = imread("cartype.jpg");

	if (!src.data) {
		cout << "error read image" << endl;
		return -1;
	}

	namedWindow(window_name);
	createTrackbar("color", window_name, &color, 6, callbackAdjustColor);
	createTrackbar("hue", window_name, &hue, 2 * hue, callbackAdjust);
	createTrackbar("saturation", window_name, &saturation, 2 * saturation, callbackAdjust);
	createTrackbar("brightness", window_name, &brightness, 2 * brightness, callbackAdjust);
	callbackAdjust(0, 0);

	waitKey();
	return 0;

}



#endif

//亮度 对比度
#if 0
#define M_PI        3.14159265358979323846

#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <opencv.hpp>
using namespace std;
using namespace cv;


#define SWAP(a, b, t)  do { t = a; a = b; b = t; } while(0)
#define CLIP_RANGE(value, min, max)  ( (value) > (max) ? (max) : (((value) < (min)) ? (min) : (value)) )
#define COLOR_RANGE(value)  CLIP_RANGE(value, 0, 255)

/**
* Adjust Brightness and Contrast
*
* @param src [in] InputArray
* @param dst [out] OutputArray
* @param brightness [in] integer, value range [-255, 255]
* @param contrast [in] integer, value range [-255, 255]
*
* @return 0 if success, else return error code
*/
int adjustBrightnessContrast(InputArray src, OutputArray dst, int brightness, int contrast)
{
	Mat input = src.getMat();
	if (input.empty()) {
		return -1;
	}

	dst.create(src.size(), src.type());
	Mat output = dst.getMat();

	brightness = CLIP_RANGE(brightness, -255, 255);
	contrast = CLIP_RANGE(contrast, -255, 255);

	/**
	Algorithm of Brightness Contrast transformation
	The formula is:
	y = [x - 127.5 * (1 - B)] * k + 127.5 * (1 + B);

	x is the input pixel value
	y is the output pixel value
	B is brightness, value range is [-1,1]
	k is used to adjust contrast
	k = tan( (45 + 44 * c) / 180 * PI );
	c is contrast, value range is [-1,1]
	*/

	double B = brightness / 255.;
	double c = contrast / 255.;
	double k = tan((45 + 44 * c) / 180 * M_PI);

	Mat lookupTable(1, 256, CV_8U);
	uchar *p = lookupTable.data;
	for (int i = 0; i < 256; i++)
		p[i] = COLOR_RANGE((i - 127.5 * (1 - B)) * k + 127.5 * (1 + B));

	LUT(input, lookupTable, output);

	return 0;
}


//=====主程序开始====

static string window_name = "photo";
static Mat src;
static int brightness = 255;
static int contrast = 255;

static void callbackAdjust(int, void *)
{
	Mat dst;
	adjustBrightnessContrast(src, dst, brightness - 255, contrast - 255);
	imshow(window_name, dst);
}


int main()
{
	src = imread("cartype.jpg");
	
	if (!src.data) {
		cout << "error read image" << endl;
		return -1;
	}

	namedWindow(window_name);
	createTrackbar("brightness", window_name, &brightness, 2 * brightness, callbackAdjust);
	createTrackbar("contrast", window_name, &contrast, 2 * contrast, callbackAdjust);
	callbackAdjust(0, 0);

	waitKey();

	return 0;

}


#endif

#if 0  //曲线
/*
* test_Curves.cpp
*
*  Created on: 2016年9月11日
*      Author: Administrator
*/


#include <cstdio>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "Curves.hpp"

using namespace std;
using namespace cv;

static string window_name = "Photo";
static Mat src;

static string curves_window = "Adjust Curves";
static Mat curves_mat;
static int channel = 0;
Curves  curves;

static void invalidate()
{
	curves.draw(curves_mat);
	imshow(curves_window, curves_mat);

	Mat dst;
	curves.adjust(src, dst);
	imshow(window_name, dst);

	int y, x;
	uchar *p;

	y = 150; x = 50;
	p = dst.ptr<uchar>(y) +x * 3;
	cout << "(" << int(p[2]) << ", " << int(p[1]) << ", " << int(p[0]) << ")  ";

	y = 150; x = 220;
	p = dst.ptr<uchar>(y) +x * 3;
	cout << "(" << int(p[2]) << ", " << int(p[1]) << ", " << int(p[0]) << ")  ";

	y = 150; x = 400;
	p = dst.ptr<uchar>(y) +x * 3;
	cout << "(" << int(p[2]) << ", " << int(p[1]) << ", " << int(p[0]) << ")  " << endl;
}

static void callbackAdjustChannel(int, void *)
{
	switch (channel) {
	case 3:
		curves.CurrentChannel = &curves.BlueChannel;
		break;
	case 2:
		curves.CurrentChannel = &curves.GreenChannel;
		break;
	case 1:
		curves.CurrentChannel = &curves.RedChannel;
		break;
	default:
		curves.CurrentChannel = &curves.RGBChannel;
		break;
	}


	invalidate();
}

static void callbackMouseEvent(int mouseEvent, int x, int y, int flags, void* param)
{
	switch (mouseEvent) {
	case CV_EVENT_LBUTTONDOWN:
		curves.mouseDown(x, y);
		invalidate();
		break;
	case CV_EVENT_MOUSEMOVE:
		if (curves.mouseMove(x, y))
			invalidate();
		break;
	case CV_EVENT_LBUTTONUP:
		curves.mouseUp(x, y);
		invalidate();
		break;
	}
	return;
}


int main()
{
	//read image file
	src = imread("cartype.jpg");
	if (!src.data) {
		cout << "error read image" << endl;
		return -1;
	}

	//create window
	namedWindow(window_name);
	imshow(window_name, src);

	//create Mat for curves
	curves_mat = Mat::ones(256, 256, CV_8UC3);

	//create window for curves
	namedWindow(curves_window);
	setMouseCallback(curves_window, callbackMouseEvent, NULL);
	createTrackbar("Channel", curves_window, &channel, 3, callbackAdjustChannel);


	// 范例：用程序代码在RedChannel中定义一条曲线
	//curves.RGBChannel.clearPoints();
	//curves.RGBChannel.addPoint(Point(0, 0));
	//curves.RGBChannel.addPoint(Point(180, 125));
	//curves.RGBChannel.addPoint(Point(255, 255));
	//Mat dst;
	//curves.adjust(src, dst);
	//imshow(window_name, dst);
	invalidate();

	waitKey();

	return 0;
}




#endif

//曲线批量
#if 0 //曲线批量
/*
* test_Curves.cpp
*
*  Created on: 2016年9月11日
*      Author: Administrator
*/


#include <cstdio>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "Curves.hpp"
#include <list>
#include "Dir.hpp"

using namespace std;
using namespace cv;


int main(int argc, char **argv)
{
	//read image file
	if (argc == 1)
	{
		cout << "hah" << endl;
	}
	char path_buffer[_MAX_PATH];
	char drive[_MAX_DRIVE];
	char mydir[_MAX_DIR];
	char fname[_MAX_FNAME];
	char ext[_MAX_EXT];
	Curves  curves;
	curves.CurrentChannel = &curves.RGBChannel;
	curves.RGBChannel.clearPoints();
	curves.RGBChannel.addPoint(Point(0, 0));
	curves.RGBChannel.addPoint(Point(190, 128));//185 170 
	curves.RGBChannel.addPoint(Point(255, 255));

	Curves  curves2;
	curves2.CurrentChannel = &curves2.RGBChannel;
	curves2.RGBChannel.clearPoints();
	curves2.RGBChannel.addPoint(Point(0, 0));
	curves2.RGBChannel.addPoint(Point(170, 128));//192 160 
	curves2.RGBChannel.addPoint(Point(255, 255));

	Curves  curves3;
	curves3.CurrentChannel = &curves3.RGBChannel;
	curves3.RGBChannel.clearPoints();
	curves3.RGBChannel.addPoint(Point(0, 0));
	curves3.RGBChannel.addPoint(Point(128, 160));//192 160 
	curves3.RGBChannel.addPoint(Point(255, 255));

	Curves  curves4;
	curves4.CurrentChannel = &curves4.RGBChannel;
	curves4.RGBChannel.clearPoints();
	curves4.RGBChannel.addPoint(Point(0, 0));
	curves4.RGBChannel.addPoint(Point(128, 190));//192 160 
	curves4.RGBChannel.addPoint(Point(255, 255));

	char file_Name[256] = "G:\\work\\2018\\活体检测\\posres";
	char save_Name[256] = "G:\\work\\2018\\活体检测\\posrescure";
	char savec1[320];
	char savec2[320];
	char savec3[320];
	char savec4[320];
	list<string> posfiles;
	dir::listFiles(posfiles, file_Name, "", true);
	int iPoCount = posfiles.size();
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();

		_splitpath(hah, drive, mydir, fname, ext);
		/*printf("Path extracted with _splitpath:\n");
		printf("  Drive: %s\n", drive);
		printf("  Dir: %s\n", mydir);
		printf("  Filename: %s\n", fname);
		printf("  Ext: %s\n", ext);*/
		Mat src = imread(hah, 1);
		if (!src.data) {
			cout << "error read image" << endl;
			continue;
		}

		//create window
		namedWindow("src");
		imshow("src", src);

		//create Mat for curves
		//curves_mat = Mat::ones(256, 256, CV_8UC3);

		//create window for curves
		//namedWindow(curves_window);
		//setMouseCallback(curves_window, callbackMouseEvent, NULL);
		//createTrackbar("Channel", curves_window, &channel, 3, callbackAdjustChannel);
		//_splitpath

		// 范例：用程序代码在RedChannel中定义一条曲线
		
		Mat dst;
		curves.adjust(src, dst);
		//imshow("dst", dst);
		//invalidate();
		sprintf_s(savec1, "%s\\%s%s%s", save_Name, fname, "curve1", ext);
		imwrite(savec1,dst);
		
		Mat dst2;
		curves2.adjust(src, dst2);
		sprintf_s(savec2, "%s\\%s%s%s", save_Name, fname, "curve2", ext);
		imwrite(savec2, dst2);

		
		Mat dst3;
		curves3.adjust(src, dst3);
		sprintf_s(savec3, "%s\\%s%s%s", save_Name, fname, "curve3", ext);
		imwrite(savec3, dst3);

		
		Mat dst4;
		curves4.computtables();
		curves4.fastadjust(src, dst4);
		//curves4.adjust(src, dst4);
		sprintf_s(savec4, "%s\\%s%s%s", save_Name, fname, "curve4", ext);
		imwrite(savec4, dst4);



		//waitKey();
	}
	return 0;
}




#endif


//饱和度(S) 批量
#if 0 
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include<list>
#include "HSL.hpp"
using namespace std;
using namespace cv;

static string window_name = "photo";
static Mat src;

static HSL hsl;
static int color = 0;




static void callbackAdjust(int, void *)
{
	
}




int main()
{
	

	HSL hsl;
	hsl.channels[color].hue = 0;
	hsl.channels[color].saturation = 108 - 100;
	hsl.channels[color].brightness = 0;


	HSL hsl2;
	hsl2.channels[color].hue = 0;
	hsl2.channels[color].saturation = 90 - 100;
	hsl2.channels[color].brightness = 0;


	HSL hsl3;
	hsl3.channels[color].hue = 0;
	hsl3.channels[color].saturation = 70 - 100;
	hsl3.channels[color].brightness = 0;

	char path_buffer[_MAX_PATH];
	char drive[_MAX_DRIVE];
	char mydir[_MAX_DIR];
	char fname[_MAX_FNAME];
	char ext[_MAX_EXT];


	char file_Name[256] = "G:\\work\\2018\\活体检测\\negres";
	char save_Name[256] = "G:\\work\\2018\\活体检测\\negreshsl";
	char savec1[320];
	char savec2[320];
	char savec3[320];
	


	list<string> posfiles;
	dir::listFiles(posfiles, file_Name, "", true);
	int iPoCount = posfiles.size();
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();

		_splitpath(hah, drive, mydir, fname, ext);
		/*printf("Path extracted with _splitpath:\n");
		printf("  Drive: %s\n", drive);
		printf("  Dir: %s\n", mydir);
		printf("  Filename: %s\n", fname);
		printf("  Ext: %s\n", ext);*/
		Mat src = imread(hah, 1);




		if (!src.data) {
			cout << "error read image" << endl;
			return -1;
		}

		namedWindow(window_name);
		//static int saturation = 80;//80 90 108
		Mat dst;

		hsl.adjust(src, dst);
		sprintf_s(savec1, "%s\\%s%s%s", save_Name, fname, "hsl1", ext);
		imwrite(savec1, dst);

		Mat dst2;

		hsl2.adjust(src, dst2);
		sprintf_s(savec2, "%s\\%s%s%s", save_Name, fname, "hsl2", ext);
		imwrite(savec2, dst2);

		Mat dst3;

		hsl3.adjust(src, dst3);
		sprintf_s(savec3, "%s\\%s%s%s", save_Name, fname, "hsl3", ext);
		imwrite(savec3, dst3);


		
	}
	return 0;

}



#endif

//亮度 对比度 批量
#if 1
#define M_PI        3.14159265358979323846

#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace std;
using namespace cv;


#define SWAP(a, b, t)  do { t = a; a = b; b = t; } while(0)
#define CLIP_RANGE(value, min, max)  ( (value) > (max) ? (max) : (((value) < (min)) ? (min) : (value)) )
#define COLOR_RANGE(value)  CLIP_RANGE(value, 0, 255)

/**
* Adjust Brightness and Contrast
*
* @param src [in] InputArray
* @param dst [out] OutputArray
* @param brightness [in] integer, value range [-255, 255]
* @param contrast [in] integer, value range [-255, 255]
*
* @return 0 if success, else return error code
*/
int adjustBrightnessContrast(InputArray src, OutputArray dst, int brightness, int contrast)
{
	Mat input = src.getMat();
	if (input.empty()) {
		return -1;
	}

	dst.create(src.size(), src.type());
	Mat output = dst.getMat();

	brightness = CLIP_RANGE(brightness, -255, 255);
	contrast = CLIP_RANGE(contrast, -255, 255);

	/**
	Algorithm of Brightness Contrast transformation
	The formula is:
	y = [x - 127.5 * (1 - B)] * k + 127.5 * (1 + B);

	x is the input pixel value
	y is the output pixel value
	B is brightness, value range is [-1,1]
	k is used to adjust contrast
	k = tan( (45 + 44 * c) / 180 * PI );
	c is contrast, value range is [-1,1]
	*/

	double B = brightness / 255.;
	double c = contrast / 255.;
	double k = tan((45 + 44 * c) / 180 * M_PI);

	Mat lookupTable(1, 256, CV_8U);
	uchar *p = lookupTable.data;
	for (int i = 0; i < 256; i++)
		p[i] = COLOR_RANGE((i - 127.5 * (1 - B)) * k + 127.5 * (1 + B));

	LUT(input, lookupTable, output);

	return 0;
}


//=====主程序开始====

static string window_name = "photo";






int main()
{
	int brightness ;
	int contrast;//-50 -70 30



	double B ;
	double c;
	double k ;

	char path_buffer[_MAX_PATH];
	char drive[_MAX_DRIVE];
	char mydir[_MAX_DIR];
	char fname[_MAX_FNAME];
	char ext[_MAX_EXT];


	char file_Name[256] = "G:\\work\\2018\\活体检测\\saveimg_pos";
	char save_Name[256] = "G:\\work\\2018\\活体检测\\saveimg_posadd\\";
	char savec1[320];
	char savec2[320];
	char savec3[320];
	char savec4[320];
	list<string> posfiles;
	dir::listFiles(posfiles, file_Name, "", true);
	int iPoCount = posfiles.size();
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();

		_splitpath(hah, drive, mydir, fname, ext);
		/*printf("Path extracted with _splitpath:\n");
		printf("  Drive: %s\n", drive);
		printf("  Dir: %s\n", mydir);
		printf("  Filename: %s\n", fname);
		printf("  Ext: %s\n", ext);*/
		Mat src = imread(hah, 1);

		if (!src.data) {
			cout << "error read image" << endl;
			return -1;
		}


		

		brightness = 0;
		B = brightness / 255.;
		Mat lookupTable(1, 256, CV_8U);
		uchar *p = lookupTable.data;
		
		
		contrast = -50;//-50 -70 30	
		c = contrast / 255.;
		k = tan((45 + 44 * c) / 180 * M_PI);
		for (int i = 0; i < 256; i++)
			p[i] = COLOR_RANGE((i - 127.5 * (1 - B)) * k + 127.5 * (1 + B));
		Mat dst;
		dst.create(src.size(), src.type());
		LUT(src, lookupTable, dst);
		sprintf_s(savec1, "%s%s%s%s", save_Name, fname, "lut1", ext);
		imwrite(savec1, dst);


		contrast = -90;//-50 -70 30	
		c = contrast / 255.;
		k = tan((45 + 44 * c) / 180 * M_PI);
		for (int i = 0; i < 256; i++)
			p[i] = COLOR_RANGE((i - 127.5 * (1 - B)) * k + 127.5 * (1 + B));
		Mat dst2;
		dst2.create(src.size(), src.type());
		LUT(src, lookupTable, dst2);
		sprintf_s(savec2, "%s%s%s%s", save_Name, fname, "lut2", ext);
		imwrite(savec2, dst2);


		contrast = 30;//-50 -70 30	
		c = contrast / 255.;
		k = tan((45 + 44 * c) / 180 * M_PI);
		for (int i = 0; i < 256; i++)
			p[i] = COLOR_RANGE((i - 127.5 * (1 - B)) * k + 127.5 * (1 + B));
		Mat dst3;
		dst3.create(src.size(), src.type());
		LUT(src, lookupTable, dst3);
		sprintf_s(savec3, "%s%s%s%s", save_Name, fname, "lut3", ext);
		imwrite(savec3, dst3);

		contrast = 15;//-50 -70 30	
		c = contrast / 255.;
		k = tan((45 + 44 * c) / 180 * M_PI);
		for (int i = 0; i < 256; i++)
			p[i] = COLOR_RANGE((i - 127.5 * (1 - B)) * k + 127.5 * (1 + B));
		Mat dst4;
		dst4.create(src.size(), src.type());
		LUT(src, lookupTable, dst4);
		sprintf_s(savec4, "%s%s%s%s", save_Name, fname, "lut4", ext);
		imwrite(savec4, dst4);







		
	}
	return 0;

}


#endif

// 批量文件名
#if 0
#define M_PI        3.14159265358979323846

#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <Windows.h>
using namespace std;
using namespace cv;


#define SWAP(a, b, t)  do { t = a; a = b; b = t; } while(0)
#define CLIP_RANGE(value, min, max)  ( (value) > (max) ? (max) : (((value) < (min)) ? (min) : (value)) )
#define COLOR_RANGE(value)  CLIP_RANGE(value, 0, 255)

/**
* Adjust Brightness and Contrast
*
* @param src [in] InputArray
* @param dst [out] OutputArray
* @param brightness [in] integer, value range [-255, 255]
* @param contrast [in] integer, value range [-255, 255]
*
* @return 0 if success, else return error code
*/


void savetxt(const char* orgfilename, char* save_Name, char * fname, char *addname, char *ext)
{
	char savename[320];
	sprintf_s(savename, "%s%s%s%s", save_Name, fname, addname, ext);
	CopyFile(orgfilename, savename, true);
}



int main()
{
	



	

	char path_buffer[_MAX_PATH];
	char drive[_MAX_DRIVE];
	char mydir[_MAX_DIR];
	char fname[_MAX_FNAME];
	char ext[_MAX_EXT];


	char file_Name[256] = "G:\\图片视频\\汽车车标\\图片和标注\\newlable\\0901\\yolo0901\\txt";
	char save_Name[256] = "G:\\图片视频\\汽车车标\\图片和标注\\newlable\\0901\\yolo0901\\txtadd\\";





	list<string> posfiles;
	dir::listFiles(posfiles, file_Name, "", true);
	int iPoCount = posfiles.size();
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();

		_splitpath(hah, drive, mydir, fname, ext);
		printf("Path extracted with _splitpath:\n");
		printf("  Drive: %s\n", drive);
		printf("  Dir: %s\n", mydir);
		printf("  Filename: %s\n", fname);
		printf("  Ext: %s\n", ext);
		
		savetxt(hah, save_Name, fname, "curve1", ext);
		savetxt(hah, save_Name, fname, "curve2", ext);
		savetxt(hah, save_Name, fname, "curve3", ext);
		savetxt(hah, save_Name, fname, "curve4", ext);
		savetxt(hah, save_Name, fname, "hsl1", ext);
		savetxt(hah, save_Name, fname, "hsl2", ext);
		savetxt(hah, save_Name, fname, "hsl3", ext);
		savetxt(hah, save_Name, fname, "hut1", ext);
		savetxt(hah, save_Name, fname, "hut2", ext);
		savetxt(hah, save_Name, fname, "hut3", ext);
		
	}
	return 0;

}


#endif

//测试yolo格式
#if 0//



#include<iostream>
#include <fstream>
#include <istream>
#include<time.h>
#include "Dir.hpp"
#include<vector>
#include<opencv2/opencv.hpp>

using namespace std;
using namespace cv;
int main(int argc, char* argv[])
{

	char filename[256] = "G:\\图片视频\\汽车车标\\图片和标注\\newlable\\0901\\part3ed";
	//char savefilename[256]="E:\\work\\python\\20161217\\testout";
	char filenamesave[256];
	list<string> posfiles;
	dir::listFiles(posfiles, filename, "", true);
	int iPosCount = posfiles.size();

	const char *d = ".";
	int index = 463;
	int saveindex = 0;
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();

		const char *show;
		char *txtstr = ".txt";
		//cout<<hah<<endl;
		show = strstr(hah, txtstr);
		if (show != NULL)
		{
			continue; //txt跳过
		}
		Mat posMat;
		posMat = imread(hah, 1);
		if (posMat.cols<20 || posMat.rows<20)
		{
			continue;
		}
		//imshow("posMat",posMat);
		//waitKey(1);
		char normalhah[240];
		strcpy_s(normalhah, hah);
		char *p;
		p = strtok(normalhah, d);
		if (p)
		{
			strcat(p, ".txt");
			ifstream fin(p, ios::in);
			//char savetxtfilename[320];
			//char savejpgfilename[320];
			//sprintf(savejpgfilename,"%s/new%d.jpg",savefilename,index);
			//sprintf(savetxtfilename,"%s/new%d.txt",savefilename,index);
			//imwrite(savejpgfilename,posMat);

			index++;
			//ofstream fout(savetxtfilename, ios::out);
			if (!fin){
				printf("The file is not exist!");
				cout << hah << endl;
				continue;
			}
			int  hasin = 0;
			while (!fin.eof())
			{
				int  lable;
				float mx, my, w, h;
				fin >> lable >> mx >> my >> w >> h;
				if (w<0.17&&h<0.17)
				{
					if (hasin == 0)
					{
						cout << "small:" << hah << endl;

						//getchar();
						//return 0;
					}


				}
				if (mx == 0 && my == 0 && w == 0 && h == 0)
				{
					if (hasin == 0)
					{
						cout << hah << endl;
						getchar();
						return 0;
					}

					break;
				}
				//if(w<0.11||h<0.15)
				//{
				//	if(hasin==0)
				//	{
				//		cout<<hah<<endl;	
				//		getchar();
				//		//return 0;
				//	}
				//	//break;

				//}
				hasin++;
				//Mat showmat;
				//posMat.copyTo(showmat);
				Rect temprect;
				temprect.x = mx*posMat.cols - (w*posMat.cols / 2);
				temprect.y = my*posMat.rows - (h*posMat.rows / 2);
				temprect.width = w*posMat.cols;
				temprect.height = h*posMat.rows;
				rectangle(posMat, temprect, Scalar(255, 0, 0), 3, 8, 0);

				resize(posMat, posMat, Size(posMat.size().width, posMat.size().height));
				//int classlable=1;
				// float mx,my,w,h;
				// mx=(float)(lefttop.x+rightbottom.x)/posMat.size().width/2;
				//my=(float)(lefttop.y+rightbottom.y)/posMat.size().height/2;
				// w=(float)(abs(rightbottom.x-lefttop.x))/posMat.size().width;
				//h=(float)(abs(rightbottom.y-lefttop.y))/posMat.size().height;
				//fout<<classlable<<" "<<mx<<" "<<my<<" "<<w<<" "<<h<<" "<<endl;
				//imwrite(savejpgfilename,posMat);

				//fin >> a[cnt][0]>>a[cnt][1]>>a[cnt][2];
				//int sum = a[cnt][0] + a[cnt][1] + a[cnt][2];
				//fout<<sum<<"\n";
				//cnt++;
			}
			imshow("showmat", posMat);
			waitKey(0);

			fin.close();
			//fout.close();


			//printf("%s\n",p);  
		}


	}

	//getchar();

	return 0;
}
#endif


//sobel
#if 0//



#include<iostream>
#include <fstream>
#include <istream>
#include<time.h>
#include "Dir.hpp"
#include<vector>
#include<opencv2/opencv.hpp>

using namespace std;
using namespace cv;
double Thenengrad(Mat &img)
{
	double Grad_value = 0;
	double Sx, Sy;
	float T = 0;
	for (int i = 1; i < img.rows-1; i++)
	{
		//定义行指针
		uchar *current_ptr = (uchar*)img.data + i * img.cols;//当前行
		uchar *pre_ptr = (uchar*)img.data + (i - 1)*img.cols;//上一行
		uchar *next_ptr= (uchar*)img.data + (i +1)*img.cols;//下一行
		for (int j = 1; j < img.cols-1; j++)
		{
			Sx = pre_ptr[j - 1] * (-1) + pre_ptr[j + 1] + current_ptr[j - 1] * (-2) + current_ptr[j + 1] * 2 + next_ptr[j - 1] * (-1) + next_ptr[j + 1];//x方向梯度
			Sy = pre_ptr[j - 1] + 2 * pre_ptr[j] + pre_ptr[j + 1] - next_ptr[j - 1] - 2 * next_ptr[j] - next_ptr[j + 1];//y方向梯度
			//求总和
			double sobel = sqrtl(Sx * Sx + Sy * Sy);
			if (sobel>T)
			{
				Grad_value += sobel;
			}
		}
	}
	return Grad_value / (img.cols - 2) / (img.rows - 2);
}


int main(int argc, char* argv[])
{
	 
	char file_Name[256] = "G:\\work\\2018\\活体检测\\respos9696\\";
	





	list<string> posfiles;
	dir::listFiles(posfiles, file_Name, "", true);
	int iPoCount = posfiles.size();
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();
		Mat src = imread(hah, 0);
		double res = Thenengrad(src);
		cout << "res::" << res << endl;
		imshow("src", src);
		waitKey(0);


	}

	return 0;
}
#endif

//LBP show
#if 0
#include <opencv2/opencv.hpp>
#include <iostream>
#include "math.h"

using namespace cv;
using namespace std;

Mat  gray_src;

const char* output_tt = "LBP Result";

int main(int argc, char** argv) {
	gray_src = imread("11182930952_157_overall.jpg", 0);
	if (gray_src.empty()) {
		printf("could not load image...\n");
		return -1;
	}

	namedWindow("input image", CV_WINDOW_AUTOSIZE);
	namedWindow(output_tt, CV_WINDOW_AUTOSIZE);
	imshow("input image", gray_src);

	// convert to gray
	//cvtColor(src, gray_src, COLOR_BGR2GRAY);
	int width = gray_src.cols;
	int height = gray_src.rows;

	// 基本LBP演示
	Mat lbpImage = Mat::zeros(gray_src.rows - 2, gray_src.cols - 2, CV_8UC1);//3*3窗口，边界有左右各1个像素不处理
	for (int row = 1; row < height - 1; row++) {
		for (int col = 1; col < width - 1; col++) {
			uchar c = gray_src.at<uchar>(row, col);//获取中心像素值
			uchar code = 0;//特征码
			code |= (gray_src.at<uchar>(row - 1, col - 1) > c) << 7;
			code |= (gray_src.at<uchar>(row - 1, col) > c) << 6;
			code |= (gray_src.at<uchar>(row - 1, col + 1) > c) << 5;
			code |= (gray_src.at<uchar>(row, col + 1) > c) << 4;
			code |= (gray_src.at<uchar>(row + 1, col + 1) > c) << 3;
			code |= (gray_src.at<uchar>(row + 1, col) > c) << 2;
			code |= (gray_src.at<uchar>(row + 1, col - 1) > c) << 1;
			code |= (gray_src.at<uchar>(row, col - 1) > c) << 0;
			lbpImage.at<uchar>(row - 1, col - 1) = code;//原图1，1=效果图0，0
		}
	}
	imshow(output_tt, lbpImage);

	waitKey(0);
	return 0;
}
#endif

//flip
#if 0
/*
* test_Curves.cpp
*
*  Created on: 2016年9月11日
*      Author: Administrator
*/


#include <cstdio>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "Curves.hpp"
#include <list>
#include "Dir.hpp"

using namespace std;
using namespace cv;


int main(int argc, char **argv)
{
	//read image file
	if (argc == 1)
	{
		cout << "hah" << endl;
	}
	char path_buffer[_MAX_PATH];
	char drive[_MAX_DRIVE];
	char mydir[_MAX_DIR];
	char fname[_MAX_FNAME];
	char ext[_MAX_EXT];

	char file_Name[256] = "G:\\work\\2018\\活体检测\\svm\\1207NEG";
	char save_Name[256] = "G:\\work\\2018\\活体检测\\svm\\neg-flip";
	char savec1[320];

	list<string> posfiles;
	dir::listFiles(posfiles, file_Name, "", true);
	int iPoCount = posfiles.size();
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();

		_splitpath(hah, drive, mydir, fname, ext);
		/*printf("Path extracted with _splitpath:\n");
		printf("  Drive: %s\n", drive);
		printf("  Dir: %s\n", mydir);
		printf("  Filename: %s\n", fname);
		printf("  Ext: %s\n", ext);*/
		Mat src = imread(hah, 1);
		if (!src.data) {
			cout << "error read image" << endl;
			continue;
		}

		//create window
		namedWindow("src");
		imshow("src", src);

		//create Mat for curves
		//curves_mat = Mat::ones(256, 256, CV_8UC3);

		//create window for curves
		//namedWindow(curves_window);
		//setMouseCallback(curves_window, callbackMouseEvent, NULL);
		//createTrackbar("Channel", curves_window, &channel, 3, callbackAdjustChannel);
		//_splitpath

		// 范例：用程序代码在RedChannel中定义一条曲线

		Mat dst;
		flip(src, dst, 1);
		//imshow("dst", dst);
		//invalidate();
		sprintf_s(savec1, "%s\\%s%s%s", save_Name, fname, "flip1", ext);
		imwrite(savec1, dst);





		//waitKey();
	}
	return 0;
}




#endif


//YCRCB show
#include <opencv2/opencv.hpp>
#include <iostream>
#include "math.h"

using namespace cv;
using namespace std;

Mat  gray_src;

const char* output_tt = "LBP Result";

static void getlbpfeature(Mat& gray_src, Mat& lbpImage)
{
	int width = gray_src.cols;
	int height = gray_src.rows;


	lbpImage = Mat::zeros(gray_src.rows - 2, gray_src.cols - 2, CV_8UC1);
	for (int row = 1; row < height - 1; row++) {
		for (int col = 1; col < width - 1; col++) {
			uchar c = gray_src.at<uchar>(row, col);
			uchar code = 0;
			code |= (gray_src.at<uchar>(row - 1, col - 1) > c) << 7;
			code |= (gray_src.at<uchar>(row - 1, col) > c) << 6;
			code |= (gray_src.at<uchar>(row - 1, col + 1) > c) << 5;
			code |= (gray_src.at<uchar>(row, col + 1) > c) << 4;
			code |= (gray_src.at<uchar>(row + 1, col + 1) > c) << 3;
			code |= (gray_src.at<uchar>(row + 1, col) > c) << 2;
			code |= (gray_src.at<uchar>(row + 1, col - 1) > c) << 1;
			code |= (gray_src.at<uchar>(row, col - 1) > c) << 0;
			lbpImage.at<uchar>(row - 1, col - 1) = code;
		}
	}






}
Size ProcSize(128, 128);
static void get3cfeature(Mat& srcImage, vector<float>& lbpfeatures)
{
	if (srcImage.size() != ProcSize)
	{
		resize(srcImage, srcImage, ProcSize);
	}
	
	vector<Mat> channels;
	
	split(srcImage, channels);
	int histBinNum = 255;
	float range[] = { 0, 255 };
	const float* histRange = { range };
	bool uniform = true;
	bool accumulate = false;


	Mat Y, CR, CB;

	getlbpfeature(channels[0], Y);
	getlbpfeature(channels[1], CR);
	getlbpfeature(channels[2], CB);

	Mat Y_hist, CR_hist, CB_hist;



	calcHist(&Y, 1, 0, Mat(), Y_hist, 1, &histBinNum, &histRange, uniform, accumulate);
	calcHist(&CR, 1, 0, Mat(), CR_hist, 1, &histBinNum, &histRange, uniform, accumulate);
	calcHist(&CB, 1, 0, Mat(), CB_hist, 1, &histBinNum, &histRange, uniform, accumulate);

	normalize(Y_hist, Y_hist, 1, NORM_L1);
	normalize(CR_hist, CR_hist, 1, NORM_L1);
	normalize(CB_hist, CB_hist, 1, NORM_L1);

	for (int i = 0; i < Y_hist.rows; i++)
	{ 
		//lbpfeatures.push_back(Y_hist.at<float>(i, 0));
	}

	for (int i = 0; i < CR_hist.rows; i++)
	{
		lbpfeatures.push_back(CR_hist.at<float>(i, 0));
	}

	for (int i = 0; i < CR_hist.rows; i++)
	{
		lbpfeatures.push_back(CR_hist.at<float>(i, 0));
	}


}

void Writeimgtomat(int& offset, vector<vector<float>>& posfiles, Mat& feature_vec_mat, Mat& res_mat, int mark)
{
	for (int i = 0; i < posfiles.size(); i++)
	{



		for (int j = 0; j < posfiles[i].size(); j++)
		{
			feature_vec_mat.at<float>(offset, j) = posfiles[i][j];
			//把特征值复制到mat中  
		}
		res_mat.at<float>(offset, 0) = mark;
		//res_mat->data.fl[offset] = 1;//正样本标记为0
		offset++;

	}



}






//train
#if 0
int main(int argc, char** argv) {
   
	char posfile[256] = "G:\\work\\2018\\活体检测\\svm\\1207POS";
	char negfile[256] = "G:\\work\\2018\\活体检测\\svm\\1207NEG";
	char Svm_Save_Path[256] = "G:\\work\\2018\\活体检测\\svm\\noy.xml";
	list<string> posfiles;
	dir::listFiles(posfiles, posfile, "", true);
	int iPosCount = posfiles.size();
	int offset = 0;
	vector<vector<float>> posres;
	vector<vector<float>> negres;
	
	cout << "begin get pos features | num:" << iPosCount << endl;
	for (list<string>::iterator it = posfiles.begin(); it != posfiles.end(); it++)
	{
		const char *hah = it->c_str();
		Mat src = imread(hah);
		if (!src.data) {
			cout << "error read image" << hah << endl;
			return -1;
		}
		vector<float> res;
		get3cfeature(src, res);
		posres.push_back(res);

	}
	
	

	
	list<string> negfiles;
	dir::listFiles(negfiles, negfile, "", true);
	int inegCount = negfiles.size();
	cout << "begin get neg features | num:" << inegCount << endl;
	for (list<string>::iterator it = negfiles.begin(); it != negfiles.end(); it++)
	{
		const char *hah = it->c_str();
		Mat src = imread(hah);

		if (!src.data) {
			cout << "error read image" << hah << endl;
			return -1;
		}
		resize(src, src, Size(128, 128));
		vector<float> res;
		get3cfeature(src, res);
		negres.push_back(res);

	}
	Mat feature_vec_mat = Mat::zeros(iPosCount + inegCount, posres[0].size(), CV_32FC1);
	//CvMat *feature_vec_mat;//所有样本特征向量
	Mat res_mat = Mat::zeros(iPosCount + inegCount, 1, CV_32FC1); //样本标识
	
	Writeimgtomat(offset, posres, feature_vec_mat, res_mat, 1);

	Writeimgtomat(offset, negres, feature_vec_mat, res_mat, 0);

	cout << "feature_vec_mat size:" << feature_vec_mat.size() << endl;

	CvSVMParams params;
	params.svm_type = CvSVM::C_SVC;
	params.kernel_type = CvSVM::RBF;
	//params.kernel_type = CvSVM::LINEAR;
	//params.term_crit = cvTermCriteria(CV_TERMCRIT_ITER, 1000, 1e-6);
	params.term_crit = cvTermCriteria(CV_TERMCRIT_ITER, 50000, FLT_EPSILON); //线性
	//params.term_crit = cvTermCriteria(CV_TERMCRIT_ITER, 5000, FLT_EPSILON);
	params.C = 1;//10
	params.gamma = 1;//old 0.035 0.09


	//CvSVMParams param;//这里是参数  
	//  CvTermCriteria criteria;      
	//  criteria = cvTermCriteria( CV_TERMCRIT_EPS, 1000, FLT_EPSILON );      
	// param = CvSVMParams( CvSVM::C_SVC, CvSVM::RBF, 10.0, 0.09, 1.0, 10.0, 0.5, 1.0, NULL, criteria );      

	//CvSVMParams param(CvSVM::C_SVC, CvSVM::LINEAR, 0, 1, 0, 0.01, 0, 0, 0, criteria);  
	SVM svm;
	CvTermCriteria criteria;
	//criteria = cvTermCriteria( CV_TERMCRIT_EPS, 50000, FLT_EPSILON ); 
	criteria = cvTermCriteria(CV_TERMCRIT_EPS, 5000, FLT_EPSILON);
	double t_train = (double)getTickCount();
	CvParamGrid getC = CvSVM::get_default_grid(CvSVM::C);
	//svm.train_auto(feature_vec_mat, res_mat, NULL, NULL, params);

	svm.train(feature_vec_mat, res_mat, Mat(), Mat(), params);
	//svm.train( feature_vec_mat, res_mat, NULL, NULL, CvSVMParams(CvSVM::C_SVC,CvSVM::RBF,10.0,0.09,1.0,10.0,0.5,1.0,NULL,criteria) ); 
	//svm.train_auto(feature_vec_mat,res_mat,Mat(),Mat(),params);
	t_train = (double)getTickCount() - t_train;
	cout << "训练成功，训练时间：" << t_train << endl;

	svm.save(Svm_Save_Path);

	//cvReleaseMat(&feature_vec_mat);
	//cvReleaseMat(&res_mat);

	int v = svm.get_support_vector_count();
	cout << "支撑向量个数：" << v << endl;


	//waitKey(0);
	return 0;
}

#endif
#if 0
int main(int argc, char** argv) {
	int featurelenth = 765/3*2;
	char PREDICT_Name[128] = "G:\\work\\2018\\活体检测\\saveimg_posadd";//设置待分类图片加载目录
	char RESULT_Name[128] = "G:\\work\\2018\\活体检测\\svm\\respos";
	list<string> predictfiles;
	dir::listFiles(predictfiles, PREDICT_Name, "", true);
	int PrCount = predictfiles.size();

	

	SVM svm;
	
	
	svm.load("G:\\work\\2018\\活体检测\\svm\\noy.xml");
	int sptvectorcount = svm.get_support_vector_count();
	assert(svm.get_support_vector_count() != 0);

	//CvMat *feature_vec_mat;//样本特征向量
	//Mat feature_vec_mat;
	Mat feature_vec_mat = Mat::zeros(1, featurelenth, CV_32FC1);
	int index = 1;
	for (list<string>::iterator it = predictfiles.begin(); it != predictfiles.end(); it++)
	{
		const char *hah = it->c_str();
		Mat imgbgr = imread(hah, 1);
		

		if (imgbgr.empty())
		{
			continue;
		}

		resize(imgbgr, imgbgr, Size(128, 128));
		//缩放 

		


		//if( img.height!=36||img.height!=36 )
		//{

		//}

		vector<float> descriptors;
		//Mat fliterout;
		//bilateralFilter ( img, fliterout, 3, 3*2, 3/2 );

		get3cfeature(imgbgr, descriptors);




		for (int j = 0; j < featurelenth; j++)
		{
			//CV_MAT_ELEM( *feature_vec_mat, float, 0, j ) = descriptors[j];
			float* tempfloat = feature_vec_mat.ptr<float>(0);
			tempfloat[j] = descriptors[j];
			//把特征值复制到mat中  
		}
		double  t = cvGetTickCount();
		int ret = svm.predict(feature_vec_mat);
		t = cvGetTickCount() - t;
		index++;
		std::cout << "detect times: " << t / (cvGetTickFrequency() * 1000) << "ms" << std::endl;
		char result_filename[128];
		switch (ret)
		{
		case 0:
		{
				  sprintf(result_filename, "%s\\%s-%d.jpg", RESULT_Name,"neg", index);
				  break;
		}
		case 1:
		{
				  sprintf(result_filename, "%s\\%s-%d.jpg", RESULT_Name,"pos", index);
				  break;
		}
	


		default:
			break;
		}


		/*if(ret==1)
		{

		sprintf(result_filename,"%s\\%s\\%d-%s.jpg",RESULT_Name,"姿势中",index,"姿势中");

		}
		else if(ret==2)
		{

		sprintf(result_filename,"%s\\%s\\%d-%s.jpg",RESULT_Name,"无",index,"无");
		}*/

		cout << "识别第:" << index << "张图片" << endl;
		imwrite(result_filename, imgbgr);
		
	}






	return 0;
}
#endif