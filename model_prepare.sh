#!/bin/bash

TEST_CAFFE=/data/test_caffe
PREBUILTS_LIB=prebuilts
CAFFE_ON_ACL_LIBRARY=$PREBUILTS_LIB/CaffeOnACL
COMPUTE_LIBRARY=$PREBUILTS_LIB/ComputeLibrary

adb wait-for-device
adb root
adb remount

# prepare libraries
adb shell "mkdir -p $TEST_CAFFE"
adb push $CAFFE_ON_ACL_LIBRARY/lib/libcaffe.so $TEST_CAFFE
adb push $COMPUTE_LIBRARY/lib/libOpenCL.so $TEST_CAFFE

# prepare test data for classification
TEST_DATA=$TEST_CAFFE/test_data
adb shell "mkdir -p $TEST_DATA"
adb push CaffeOnACL/data/ilsvrc12/imagenet_mean.binaryproto $TEST_DATA
adb push CaffeOnACL/data/ilsvrc12/synset_words.txt $TEST_DATA
adb push CaffeOnACL/examples/images/cat.jpg $TEST_DATA

# prepare AlexNet
ALEX_NET=$TEST_CAFFE/alexnet
adb shell "mkdir -p $ALEX_NET"
adb push CaffeOnACL/models/bvlc_alexnet/deploy.prototxt $ALEX_NET
adb push CaffeOnACL/models/bvlc_alexnet/bvlc_alexnet.caffemodel $ALEX_NET

# prepare GoogLeNet
GOOGLE_NET=$TEST_CAFFE/googlenet
adb shell "mkdir -p $GOOGLE_NET"
adb push CaffeOnACL/models/bvlc_googlenet/deploy.prototxt $GOOGLE_NET
adb push CaffeOnACL/models/bvlc_googlenet/bvlc_googlenet.caffemodel $GOOGLE_NET

# prepare SquezzeNet
SQUEZZE_NET=$TEST_CAFFE/squezzenet
adb shell "mkdir -p $SQUEZZE_NET"
adb push CaffeOnACL/models/SqueezeNet/SqueezeNet_v1.1/squeezenet.1.1.deploy.prototxt $SQUEZZE_NET
adb push CaffeOnACL/models/SqueezeNet/SqueezeNet_v1.1/squeezenet_v1.1.caffemodel $SQUEZZE_NET

# prepare MobileNet
MOBILE_NET=$TEST_CAFFE/mobilenet
adb shell "mkdir -p $MOBILE_NET"
adb push CaffeOnACL/models/MobileNet/mobilenet_deploy.prototxt $MOBILE_NET
adb push CaffeOnACL/models/MobileNet/mobilenet.caffemodel $MOBILE_NET

# prepare classification binary
adb push $CAFFE_ON_ACL_LIBRARY/bin/classification_profiling $TEST_CAFFE
adb push $CAFFE_ON_ACL_LIBRARY/bin/classification_profiling_gpu $TEST_CAFFE

# prepare spinning robot
adb install -r prebuilts/BasicGLSurfaceView.apk

adb shell sync
