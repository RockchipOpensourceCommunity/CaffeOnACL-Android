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
SQUEEZE_NET_MODEL=$CAFFE_ON_ACL/models/SqueezeNet/SqueezeNet_v1.1/squeezenet_v1.1.caffemodel
if [ -s $SQUEEZE_NET_MODEL ]; then
  echo "SqueezeNet model already exists, not getting it."
else
  wget -c https://github.com/DeepScale/SqueezeNet/raw/master/SqueezeNet_v1.1/squeezenet_v1.1.caffemodel -O /tmp/squeezenet_v1.1.caffemodel.temp && mv /tmp/squeezenet_v1.1.caffemodel.temp $SQUEEZE_NET_MODEL
fi

# download MobileNet
if [ -d $CAFFE_ON_ACL/models/MobileNet ]; then
  echo "MobileNet model already exists, not getting it."
else
  git clone https://github.com/finley-/MobileNet-Caffe $CAFFE_ON_ACL/models/MobileNet
fi
