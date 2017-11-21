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
#adb push $COMPUTE_LIBRARY/lib/libOpenCL.so $TEST_CAFFE

# prepare classification binary
adb push $CAFFE_ON_ACL_LIBRARY/bin/classification_profiling $TEST_CAFFE
adb push $CAFFE_ON_ACL_LIBRARY/bin/classification_profiling_gpu $TEST_CAFFE

adb shell sync
