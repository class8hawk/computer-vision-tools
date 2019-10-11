convert_imageset --resize_height=30 --resize_width=90 --shuffle ./ train_size3090_d0925.txt  testlmdb3090_0925.lmdb

convert_imageset --resize_height=120 --resize_width=120 --shuffle ./ trainbighead0709.txt  trainlmdbbighead0709
convert_imageset --resize_height=88 --resize_width=88 --shuffle ./ test0523.txt  testlmdb0523
caffe train --solver=solver.prototxt 2>&1|tee train0711.log
./caffe train --solver=solver_liveness_mobilenet_half_0524.prototxt 2>&1|tee trainm18half524.log