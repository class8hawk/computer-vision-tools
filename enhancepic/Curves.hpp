/*
 * Adjust Curves
 *
 * Author: JoStudio
 */

#ifndef OPENCV2_PS_CURVES_HPP_
#define OPENCV2_PS_CURVES_HPP_

#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
using namespace std;
using namespace cv;

namespace cv {

/**
 * Class of Curve for one channel
 */
class Curve {
protected:
	Scalar color;
	Scalar back_color;
	int tolerance; //鼠标按下或移动时，捕获曲线点的误差范围
	bool is_mouse_down;
	vector<Point> points;  //control points 曲线的所有控制点
	vector<Point>::iterator current;  //pointer to current point 当前控制点的指针

	vector<Point>::iterator  find(int x);
	vector<Point>::iterator  find(int x, int y);
	vector<Point>::iterator  add(int x, int y);

public:
	Curve();
	virtual ~Curve();

	int calcCurve(double *z); //供内部调用的方法：计算曲线

	void draw(Mat &mat);  //将曲线画在mat上
	void mouseDown(int x, int y); //当鼠标按下，请调用mouseDown()方法
	bool mouseMove(int x, int y); //当鼠标移动，请调用mouseMove()方法
	void mouseUp(int x, int y); //当鼠标抬起，请调用mouseUp()方法

	//以下方法用于：用编程方式生成曲线
	void clearPoints(); //清除曲线上所有的点
	int  addPoint(const Point &p); //增加一个点
	int  deletePoint(const Point &p); //删除一个点
	int  movePoint(const Point &p, int x, int y); //移动一个点
};

/**
 * Class of Curves for all channels
 */
class Curves {
protected:
	void createColorTables(uchar colorTables[][256]);
public:
	Curves();
	virtual ~Curves();

	Curve RGBChannel;   //RGB总通道
	Curve RedChannel;   //Red通道
	Curve GreenChannel; //Green通道
	Curve BlueChannel;  //Blue通道

	Curve * CurrentChannel; //当前通道的指针

	void draw(Mat &mat);  //将曲线画在mat上
	void mouseDown(int x, int y); //当鼠标按下，请调用mouseDown()方法
	bool mouseMove(int x, int y); //当鼠标移动，请调用mouseMove()方法
	void mouseUp(int x, int y); //当鼠标抬起，请调用mouseUp()方法
	uchar colorTables[3][256];
	//实施曲线调整
	int adjust(InputArray src, OutputArray dst, InputArray mask = noArray());
	int computtables();
	int fastadjust(InputArray src, OutputArray dst, InputArray mask = noArray());
};

//画一条虚线
void dot_line(Mat &mat, Point &p1, Point &p2, Scalar &color, int step = 8);

} /* namespace cv */

#endif /* OPENCV2_PS_CURVES_HPP_ */
