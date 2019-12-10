cmake_minimum_required(VERSION 2.8)
project(dcf-c++)

# setup tensorRT flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g")	# -std=gnu++11

set(BUILD_DEPS "NO" CACHE BOOL "If YES, will install dependencies into sandbox.  Automatically reset to NO after dependencies are installed.")

# if this is the first time running cmake, perform pre-build dependency install script (or if the user manually triggers re-building the dependencies)
if( ${BUILD_DEPS} )
	message("Launching pre-build dependency installer script...")

	execute_process(COMMAND sh ../CMakePreBuild.sh
				WORKING_DIRECTORY ${PROJECT_BINARY_DIR}
				RESULT_VARIABLE PREBUILD_SCRIPT_RESULT)

	set(BUILD_DEPS "NO" CACHE BOOL "If YES, will install dependencies into sandbox.  Automatically reset to NO after dependencies are installed." FORCE)
	message("Finished installing dependencies")
endif()

# setup CUDA
find_package(CUDA)

set(
	CUDA_NVCC_FLAGS
	${CUDA_NVCC_FLAGS}; 
    -O3 
	-gencode arch=compute_53,code=sm_53
	-gencode arch=compute_62,code=sm_62
)

MESSAGE(STATUS "This is SOURCE dir " ${PROJECT_SOURCE_DIR})
MESSAGE(STATUS "This is BINARY dir " ${PROJECT_BINARY_DIR})

find_package(OpenCV)

message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")

#-------------------------------------------------------------------
# 定义头文件的路径变量
SET(INCLUDE_PATH ${PROJECT_SOURCE_DIR}/include
				 /usr/local/cuda-9.0/targets/aarch64-linux/include
) 
MESSAGE(STATUS "Include Path, ${INCLUDE_PATH}")

# 定义源文件路径变量
SET(SOURCE_PATH ${PROJECT_SOURCE_DIR}/src) 
MESSAGE(STATUS "Source Path , ${SOURCE_PATH}")

# 定义库文件路径
SET(LIB_PATH ${PROJECT_SOURCE_DIR}/libs
			 
)
MESSAGE(STATUS "Libs Path, ${LIB_PATH}")

# 包含头文件搜索路径
INCLUDE_DIRECTORIES(${INCLUDE_PATH}
					${OpenCV_INCLUDE_DIRS}
					#${PROJECT_SOURCE_DIR}/thirdparty/NE10/include
					${PROJECT_SOURCE_DIR}/3rdParty/include
					${PROJECT_SOURCE_DIR}/3rdParty/include/ncnn/src
                    ${PROJECT_SOURCE_DIR}/3rdParty/src/YT_TensorRT2Yolo3.0_C++/include
)

# 包含库搜索路径
LINK_DIRECTORIES(${LIB_PATH}
				 #${PROJECT_SOURCE_DIR}/thirdparty/NE10/lib
				 ${PROJECT_SOURCE_DIR}/3rdParty/library_tx2_gpu
				 /usr/local/cuda/lib64
				 
)

# 添加源文件路径下所有源文件存放到变量中(*.c && *.cpp)，也可以手动一个个文件添加进来
#AUX_SOURCE_DIRECTORY(${SOURCE_PATH} SRC_LIST)
set(SRC_LIST 
    ${SOURCE_PATH}/computescore.cpp
	# ${SOURCE_PATH}/fftTool.cpp
	# ${SOURCE_PATH}/gpu_kernel.cu
	# ${SOURCE_PATH}/dcf.cpp
	# ${SOURCE_PATH}/unittest.cpp
)

# 设置动态库输出路径
SET(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/libs)
MESSAGE(STATUS "Library Output Path, " ${LIBRARY_OUTPUT_PATH})

# 生成动态库(libmymath.so)
#ADD_LIBRARY(mymath SHARED ${SRC_LIST})

# 生成静态库（libmymath.a，target名字只能有一个，所以不能与动态库的名字一样）
#ADD_LIBRARY(yt_tensorrt_yolo STATIC ${SRC_LIST})
#CUDA_ADD_LIBRARY(yt_tensorrt_yolo STATIC ${SRC_LIST})

#------------------------------------
# 链接静态库
#SET(LIBS_LIST libmymath.a)
#SET(LIBS_LIST nvcaffe_parser nvinfer nvinfer_plugin cudart ncnn cusolver openblas  gfortran ${OpenCV_LIBS})
SET(LIBS_LIST cudart cublas ${OpenCV_LIBS})
#SET(LIBS_LIST ${OpenCV_LIBS})

# 设置生成可执行文件的输出路径
SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR})

# 设置生成可执行文件的名称
SET(EXECUTABLE_FILE_NAME dcf_demo)


# 生成可执行文件
CUDA_ADD_EXECUTABLE(${EXECUTABLE_FILE_NAME} ${SRC_LIST})
#ADD_EXECUTABLE(${EXECUTABLE_FILE_NAME} ${SRC_LIST})

# 设置可执行文件链接的库名称
TARGET_LINK_LIBRARIES(${EXECUTABLE_FILE_NAME} ${LIBS_LIST})

MESSAGE(STATUS "Link__Librarys, " ${LIBS_LIST})
