#!/bin/bash

CAFFE_ON_ACL=CaffeOnACL

chmod a+x $CAFFE_ON_ACL/data/ilsvrc12/get_ilsvrc_aux.sh
chmod a+x $CAFFE_ON_ACL/scripts/download_model_binary.py

# download data
$CAFFE_ON_ACL/data/ilsvrc12/get_ilsvrc_aux.sh

# download AlexNet
$CAFFE_ON_ACL/scripts/download_model_binary.py $CAFFE_ON_ACL/models/bvlc_alexnet

# download GoogLeNet
$CAFFE_ON_ACL/scripts/download_model_binary.py $CAFFE_ON_ACL/models/bvlc_googlenet

# download SqueezeNet
wget -c https://github.com/DeepScale/SqueezeNet/raw/master/SqueezeNet_v1.1/squeezenet_v1.1.caffemodel -P $CAFFE_ON_ACL/models/SqueezeNet/SqueezeNet_v1.1

# download MobileNet
git clone https://github.com/shicai/MobileNet-Caffe.git $CAFFE_ON_ACL/models/MobileNet
# mobilenet.caffemodel download from https://github.com/shicai/MobileNet-Caffe
