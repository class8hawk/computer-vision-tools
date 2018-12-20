/*
 * Adjust Curves
 *
 * Author: JoStudio
 */

#include "Curves.hpp"

#ifdef HAVE_OPENMP
#include <omp.h>
#endif

#define SWAP(a, b, t)  do { t = a; a = b; b = t; } while(0)
#define CLIP_RANGE(value, min, max)  ( (value) > (max) ? (max) : (((value) < (min)) ? (min) : (value)) )
#define COLOR_RANGE(value)  CLIP_RANGE((value), 0, 255)

#include <iostream>
#define DEBUG_PRINT(a)  cout << (a) << endl
#define PRINT_VAR(var)  cout << #var << " = " << (var) <<  endl

namespace cv {

/**
 * spline function
 *
 * @param x [in]  array of x-coordinate of control points
 * @param y [in]  array of y-coordinate of control points
 * @param n [in]  count of control points
 * @param t [in]  array of x-coordinate of output points
 * @param m [in]  count of output points
 * @param z [out]  array of y-coordinate of output points
 */
static double spline(double *x, double *y, int n, double *t, int m, double *z)
{
    double* dy = new double[n];
    memset(dy, 0, sizeof(double)*n);
    dy[0] = -0.5;

    double* ddy = new double[n];
    memset(ddy, 0, sizeof(double)*n);

    double h1;
    double* s = new double[n];
    double h0 = x[1] - x[0];

    s[0] = 3.0 * (y[1] - y[0]) / (2.0 * h0) - ddy[0] * h0 / 4.0;
    for( int j = 1; j <= n - 2; ++j )
    {
        h1 = x[j + 1] - x[j];
        double alpha = h0 / (h0 + h1);
        double beta = (1.0 - alpha) * (y[j] - y[j - 1]) / h0;
        beta = 3.0 * (beta + alpha * ( y[j + 1] - y[j] ) / h1);
        dy[j] = -alpha / (2.0 + (1.0 - alpha) * dy[j - 1]);
        s[j] = (beta - (1.0 - alpha) * s[j - 1]);
        s[j] = s[j] / (2.0 + (1.0 - alpha) * dy[j - 1]);
        h0 = h1;
    }
    dy[n-1] = (3.0*(y[n-1] - y[n-2]) / h1 + ddy[n-1] * h1/2.0 - s[n-2]) / (2.0 + dy[n-2]);

    for( int j = n - 2; j >= 0; --j )
    {
        dy[j] = dy[j] * dy[j + 1] + s[j];
    }

    for( int j = 0; j <= n - 2; ++j )
    {
        s[j] = x[j + 1] - x[j];
    }

    for( int j = 0; j <= n - 2; ++j )
    {
        h1 = s[j] * s[j];
        ddy[j] = 6.0 * (y[j+1] - y[j]) / h1 - 2.0 * (2.0 * dy[j] + dy[j+1]) / s[j];
    }

    h1 = s[n-2] * s[n-2];
    ddy[n-1] = 6.0 * (y[n-2] - y[n-1]) / h1 + 2.0 * (2.0 * dy[n-1] + dy[n-2]) / s[n-2];
    double g = 0.0;
    for(int i=0; i<=n-2; i++)
    {
        h1 = 0.5 * s[i] * (y[i] + y[i+1]);
        h1 = h1 - s[i] * s[i] * s[i] * (ddy[i] + ddy[i+1]) / 24.0;
        g = g + h1;
    }

    for(int j=0; j<=m-1; j++)
    {
        int i;
        if( t[j] >= x[n-1] ) {
            i = n - 2;
        } else {
            i = 0;
            while(t[j] > x[i+1]) {
                i = i + 1;
            }
        }
        h1 = (x[i+1] - t[j]) / s[i];
        h0 = h1 * h1;
        z[j] = (3.0 * h0 - 2.0 * h0 * h1) * y[i];
        z[j] = z[j] + s[i] * (h0 - h0 * h1) * dy[i];
        h1 = (t[j] - x[i]) / s[i];
        h0 = h1 * h1;
        z[j] = z[j] + (3.0 * h0 - 2.0 * h0 * h1) * y[i+1];
        z[j] = z[j] - s[i] * (h0 - h0 * h1) * dy[i+1];
    }

    delete [] s;
    delete [] dy;
    delete [] ddy;

    return(g);
}

#define WITHIN(x1, delta, x2) ( (delta) > 0 ) ? ( (x1) <= (x2) ) : ( (x1) >= (x2) )
#define EXCEED(x1, delta, x2) ( (delta) > 0 ) ? ( (x1) >= (x2) ) : ( (x1) <= (x2) )

void dot_line(Mat &mat, const Point &p1, const Point &p2,  const Scalar &color,
		int thickness = 1, int lineType = 8, int line_step = 6, int blank_step = 6 );

void dot_line(Mat &mat, const Point &p1, const Point &p2,  const Scalar &color,
		int thickness, int lineType, int line_step, int blank_step )
{
	if ( p1 == p2 ) return;

	//validate line_step
	line_step = ::abs(line_step);
	if ( line_step == 0 ) line_step = 1;

	//validate blank_step
	blank_step = ::abs(blank_step);
	if ( blank_step == 0 ) blank_step = 1;

	//dot_ratio = blank_step / line_step;
	double dot_ratio = blank_step * 1.0 / line_step;

	//calculat step_x, step_y
	double len, step_x, step_y;
	len = sqrt( (p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y) );
	step_x = (p2.x - p1.x) / len  * line_step;
	step_y = (p2.y - p1.y) / len  * line_step;

	double x1, y1, x2, y2;
	x1 = p1.x;  y1 = p1.y;  //start from Point p1

	//draw line step by step, until meet Point p2
	if ( ::abs(p1.x - p2.x) > ::abs(p1.y - p2.y) ) {
		//step in direction of x-coordination
		while ( WITHIN(x1, step_x, p2.x) ) {
			if ( EXCEED(x1 + step_x * (1 + dot_ratio), step_x, p2.x )) {
				x2 = p2.x;
				y2 = p2.y;
			} else if ( EXCEED(x1 + step_x, step_x, p2.x )) {
				x2 = p2.x;
				y2 = p2.y;
			} else {
				x2 = x1 + step_x;
				y2 = y1 + step_y;
			}
			line(mat, Point(x1, y1), Point(x2, y2), color, thickness, lineType);
			//step
			x1 = x2 + step_x * dot_ratio;
			y1 = y2 + step_y * dot_ratio;
		}

	} else {
		//step in direction of y-coordination
		while ( WITHIN(y1, step_y, p2.y) ) {
			if ( EXCEED(y1 + step_y * (1 + dot_ratio), step_y, p2.y )) {
				x2 = p2.x;
				y2 = p2.y;
			} else if ( EXCEED(y1 + step_y, step_y, p2.y )) {
				x2 = p2.x;
				y2 = p2.y;
			} else {
				x2 = x1 + step_x;
				y2 = y1 + step_y;
			}
			line(mat, Point(x1, y1), Point(x2, y2), color, thickness, lineType);
			//step
			x1 = x2 + step_x * dot_ratio;
			y1 = y2 + step_y * dot_ratio;
		}
	}
}

Curve::Curve()
{
	color = Scalar(0,0,0);
	back_color = Scalar(255,255,255);
	tolerance = 3;
	is_mouse_down = false;
	points.push_back( Point(0, 0) );
	points.push_back( Point(255, 255) );
	current = points.end();
}

Curve::~Curve()
{
}


vector<Point>::iterator  Curve::find(int x)
{
	vector<Point>::iterator iter;
	for (iter = points.begin(); iter != points.end(); ++iter ) {
		if ( ::abs(iter->x - x ) <= tolerance )
			return iter;
	}
	return points.end();
}

vector<Point>::iterator  Curve::find(int x, int y)
{
	vector<Point>::iterator iter;
	for (iter = points.begin(); iter != points.end(); ++iter ) {
		if ( ::abs(iter->x - x ) <= tolerance && ::abs(iter->y - y ) <= tolerance )
			return iter;
	}
	return points.end();
}

vector<Point>::iterator Curve::add(int x, int y)
{
	vector<Point>::iterator it = find(x);
	if ( it == points.end() ) {
		Point p(x, y);
		vector<Point>::iterator iter;
		for (iter = points.begin(); iter != points.end(); ++iter ) {

			if ( iter == points.begin() && iter->x > p.x) {
				DEBUG_PRINT("points insert at beginning");
				return points.insert( iter, p );
			}

			if ( iter->x < x &&  (iter + 1) != points.end() &&  (iter + 1)->x > p.x) {
				DEBUG_PRINT("points insert");
				return points.insert( iter + 1, p );
			}
		}
		DEBUG_PRINT("points append");
		return points.insert( points.end(), p );
	} else {
		return it;
	}
}

int Curve::calcCurve(double *output_y)
{
	//if count of control points is less than 2, return linear output
	if ( points.size() < 2) {
		for (int i = 0; i < 256; ++i )
			output_y[i] = 255 - i;
		return 0;
	}

	//if count of control points is 2, return linear output
	if ( points.size() == 2 ) {
		vector<Point>::iterator point1 = points.begin();
		vector<Point>::iterator point2 = point1 + 1;

		double delta_y = 0;
		if ( point2->x != point1->x )
			delta_y  = (point2->y - point1->y) * 1.0 / (point2->x - point1->x);

		//create output
		for ( int i = 0; i < 256; ++i ) {
			if ( i < point1->x ) {
				output_y[i] = point1->y;
			} else if ( i >= point1->x && i < point2->x ) {
				output_y[i] = COLOR_RANGE( point1->y + delta_y * (i - point1->x) );
			} else {
				output_y[i] = point2->y;
			}
		}
		return 0;
	}


	//the count of control points is greater than 2,  create spline line

	int n = points.size();  //count of points

	//create array of x-coordinate and y-coordinate of control points
	double *x =new double[n];
	double *y = new double[n];
	
	vector<Point>::iterator start_point = points.end();
	vector<Point>::iterator end_point = points.end();
    vector<Point>::iterator iter;
    int k = 0;
    for (iter = points.begin(); iter != points.end(); ++iter, ++k ) {
    	if ( k == 0 ) start_point = iter;
    	x[k] = iter->x - start_point->x;
    	y[k] = iter->y;
    	end_point = iter;
    }

    //if start_point or end_point is invalid
    if (start_point == points.end() || end_point == points.end() || start_point == end_point) {
    	for (int i = 0; i < 256; ++i )
    		output_y[i] = 255 - i;
    	return 1;
    }

    //create array of x-coordinate of output points
	int m = end_point->x - start_point->x;
	double *t = new double[m];  //array of x-coordinate of output points
	double *z = new double[m];  //array of y-coordinate of output points
	//initialize array of x-coordinate
	for ( int i = 0; i< m; ++i ) {
		t[i] = i;
	}

	//perform spline, output y-coordinate is stored in array z
	spline(x, y, n, t, m, z);

	//create output
	for ( int i = 0; i < 256; ++i ) {
		if ( i < start_point->x ) {
			output_y[i] = start_point->y;
		} else if ( i >= start_point->x && i < end_point->x ) {
			output_y[i] = CLIP_RANGE(z[i - start_point->x], 0, 255);
		} else {
			output_y[i] = end_point->y;
		}
	}
	delete[] x;
	delete[] y;
	delete[] t;
	delete[] z;
	return 0;
}

void Curve::draw(Mat &mat)
{
	int thinkness = 1;
	int n = 0;
	Point lastPoint;

	//clear background
	mat.setTo( back_color );

	vector<Point>::iterator it;
	for (it = points.begin(); it != points.end(); ++it) {
		cout << "point:  "<< it->x << ", " << it->y << endl;
	}

	//draw lines
	dot_line(mat, Point( 0, 0), Point( 255, 0), Scalar(0,0,255), 1, 8, 4, 4);
	dot_line(mat, Point( 0, 255), Point( 255, 255), Scalar(0,0,255), 1, 8, 4, 4);

	dot_line(mat, Point(63, 0), Point(63, 255), color, 1, 8, 4, 4);
	dot_line(mat, Point(127, 0), Point(127, 255), color, 1, 8, 4, 4);
	dot_line(mat, Point(191, 0), Point(191, 255), color, 1, 8, 4, 4);
	dot_line(mat, Point(0,  255 - 63), Point(255,  255 - 63), color, 1, 8, 4, 4);
	dot_line(mat, Point(0, 255 - 127), Point(255, 255 - 127), color, 1, 8, 4, 4);
	dot_line(mat, Point(0, 255 - 191), Point(255, 255 - 191), color, 1, 8, 4, 4);

	//create curve
	double z[256];
	calcCurve(z);
	for (int i = 1; i < 256; ++i ) {
		line( mat, Point(i-1, 255 - z[i-1]), Point(i, 255 - z[i]), color, 1, 8 );
	}

	//draw control points
	vector<Point>::iterator iter, iter_next;
	for (iter = points.begin(); iter != points.end(); ++iter, ++n ) {
		thinkness = (iter == current) ? -1 : 1;
		rectangle(mat, Point(iter->x - 2, 255 - iter->y + 2),
				Point(iter->x + 2, 255 - iter->y - 2), color, thinkness, 8);
	}
}


void Curve::mouseDown(int x, int y)
{
	y = 255 - y;
	current = add( x , y );
	is_mouse_down = true;
}

bool  Curve::mouseMove(int x, int y)
{
	y = 255 - y;
	if ( is_mouse_down ) {
		if (current != points.end()) {
			int prev_x = 0;
			int next_x = 255;

			if (current != points.begin()) {
				int prev_y = (current - 1)->y;
				prev_x = (current - 1)->x;

				//match the previous point
				if ( points.size() > 2 && ::abs(x - prev_x) <= tolerance && ::abs(y - prev_y) <= tolerance ) {
					current--;
					current = points.erase(current);
					DEBUG_PRINT("erase previous");
					return true;
				}

				//if x less than x of previou point
				if ( x <= prev_x) {
					//DEBUG_PRINT("less than prev_x");
					return true;
				}
			}

			if ( ( current + 1) != points.end()) {
				int next_y = (current + 1)->y;
				next_x = (current + 1)->x;

				//match the next point
				if ( points.size() > 2 && ::abs(x - next_x) <= tolerance && ::abs(y - next_y) <= tolerance ) {
					current = points.erase(current);
					DEBUG_PRINT("erase next");
					return true;
				}

				//if x great than x of next point
				if ( x >= next_x) {
					//DEBUG_PRINT("large than next_x");
					return true;
				}
			}

			current->x = CLIP_RANGE(x, 0, 255);
			current->y = CLIP_RANGE(y, 0, 255);

			return true;
		}
	}
	return false;
}

void Curve::mouseUp(int x, int y)
{
	y = 255 - y;
	is_mouse_down = false;
}


void Curve::clearPoints()
{
	points.clear();
}

int  Curve::addPoint(const Point &p)
{
	vector<Point>::iterator iter = add(p.x, p.y);
	if ( iter != points.end() )
		return 1;
	else
		return 0;
}

int  Curve::deletePoint(const Point &p)
{
	vector<Point>::iterator iter;
	iter = find( p.x, p.y );
	if ( iter != points.end() ) {
		if ( current == iter )
			current = points.end();
		points.erase(iter);
		return 1;
	}
	return 0;
}

int  Curve::movePoint(const Point &p, int x, int y)
{
	vector<Point>::iterator iter;
	iter = find( p.x, p.y );
	if ( iter != points.end() ) {
		iter->x = x;
		iter->y = y;
		return 1;
	}
	return 0;
}


//==========================================================
// Curves

Curves::Curves()
{
	CurrentChannel = &RGBChannel;
}

Curves::~Curves()
{
}

void Curves::draw(Mat &mat)
{
	if (CurrentChannel)  CurrentChannel->draw(mat);
}

void Curves::mouseDown(int x, int y)
{
	if (CurrentChannel)  CurrentChannel->mouseDown(x, y);
}

bool Curves::mouseMove(int x, int y)
{
	if (CurrentChannel)
		return CurrentChannel->mouseMove(x, y);
	return false;
}

void Curves::mouseUp(int x, int y)
{
	if (CurrentChannel)  CurrentChannel->mouseUp(x, y);
}

void Curves::createColorTables(uchar colorTables[][256])
{
	double z[256];

	BlueChannel.calcCurve(z);
	for (int i = 0; i < 256; ++i ) {
		colorTables[0][i] = z[i];
	}

	GreenChannel.calcCurve(z);
	for (int i = 0; i < 256; ++i )
		colorTables[1][i] = z[i];

	RedChannel.calcCurve(z);
	for (int i = 0; i < 256; ++i ) {
		colorTables[2][i] = z[i];
	}

	uchar value;
	RGBChannel.calcCurve(z);
	for (int i = 0; i < 256; ++i ) {
		for (int c = 0; c < 3; c++ ) {
			value = colorTables[c][i];
			colorTables[c][i] = z[value];
		}
	}
}

int Curves::adjust(InputArray src, OutputArray dst, InputArray mask)
{
	Mat input = src.getMat();
	if( input.empty() ) {
		return -1;
	}

	dst.create(src.size(), src.type());
	Mat output = dst.getMat();

	bool hasMask = true;
	Mat msk = mask.getMat();
	if (msk.empty())
		hasMask = false;

	const uchar *in;
	const uchar *pmask;
	uchar *out;
	int width = input.cols;
	int height = input.rows;
	int channels = input.channels();

	uchar colorTables[3][256];

	//create color tables
	createColorTables( colorTables );

	//adjust each pixel

	if ( hasMask ) {
		#ifdef HAVE_OPENMP
		#pragma omp parallel for
		#endif
		for (int y = 0; y < height; y ++) {
			in = input.ptr<uchar>(y);
			out = output.ptr<uchar>(y);
			pmask = msk.ptr<uchar>(y);
			for (int x = 0; x < width; x ++) {
				for (int c = 0; c < 3; c++) {
					*out = (colorTables[c][*in] * pmask[x] / 255.0)
							+ (*in) * (255 - pmask[x]) / 255.0;
					out++; in++;
				}
				for (int c = 0; c < channels - 3; c++) {
					*out++ = *in++;
				}
			}
		}
	} else {
		#ifdef HAVE_OPENMP
		#pragma omp parallel for
		#endif
		for (int y = 0; y < height; y ++) {
			in = input.ptr<uchar>(y);
			out = output.ptr<uchar>(y);
			for (int x = 0; x < width; x ++) {
				for (int c = 0; c < 3; c++) {
					*out++ = colorTables[c][*in++];
				}
				for (int c = 0; c < channels - 3; c++) {
					*out++ = *in++;
				}
			}
		}
	}

	return 0;
}

int Curves::fastadjust(InputArray src, OutputArray dst, InputArray mask)
{
	Mat input = src.getMat();
	if (input.empty()) {
		return -1;
	}

	dst.create(src.size(), src.type());
	Mat output = dst.getMat();

	bool hasMask = true;
	Mat msk = mask.getMat();
	if (msk.empty())
		hasMask = false;

	const uchar *in;
	const uchar *pmask;
	uchar *out;
	int width = input.cols;
	int height = input.rows;
	int channels = input.channels();

	

	//create color tables
	//createColorTables(colorTables);

	//adjust each pixel

	if (hasMask) {
#ifdef HAVE_OPENMP
#pragma omp parallel for
#endif
		for (int y = 0; y < height; y++) {
			in = input.ptr<uchar>(y);
			out = output.ptr<uchar>(y);
			pmask = msk.ptr<uchar>(y);
			for (int x = 0; x < width; x++) {
				for (int c = 0; c < 3; c++) {
					*out = (colorTables[c][*in] * pmask[x] / 255.0)
						+ (*in) * (255 - pmask[x]) / 255.0;
					out++; in++;
				}
				for (int c = 0; c < channels - 3; c++) {
					*out++ = *in++;
				}
			}
		}
	}
	else {
#ifdef HAVE_OPENMP
#pragma omp parallel for
#endif
		for (int y = 0; y < height; y++) {
			in = input.ptr<uchar>(y);
			out = output.ptr<uchar>(y);
			for (int x = 0; x < width; x++) {
				for (int c = 0; c < 3; c++) {
					*out++ = colorTables[c][*in++];
				}
				for (int c = 0; c < channels - 3; c++) {
					*out++ = *in++;
				}
			}
		}
	}

	return 0;
}
int Curves::computtables()
{
	createColorTables(colorTables);
	return 1;
}

} /* namespace cv */
