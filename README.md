CaffeOnACL-Android
===============
## Goal
Porting [CaffeOnACL](https://github.com/OAID/CaffeOnACL) to RK3399 Android platform

### Support
The release is based on [Rockchip RK3399](http://www.rock-chips.com/plus/3399.html) Platform
* ACL/NEON
* ACL/GPU(OpenCL)
* OpenBLAS
* Mixed Mode

## Build
Tested with Android [NDK](https://developer.android.com/ndk/downloads/index.html) r15c and cmake 3.5.1 on Ubuntu 16.04

```shell
# Install some dependencies
sudo apt-get install python-dev python-pip git cmake
sudo pip install pyyaml six

# Download source code and prebuilts
git clone --recursive https://github.com/RockchipOpensourceCommunity/CaffeOnACL-Android.git

cd CaffeOnACL-Android
export NDK_ROOT=<path/to/your/ndk/root>

# build caffe
./build_caffe.sh

# download network
./model_download.sh

# prepare data for RK3399 device
./model_prepare.sh

# Running SquezzeNet network (default is AlexNet, support AlexNet, GoogLeNet, SquezzeNet, MobileNet)
./model_runner.py SquezzeNet

```

## Prebuilts
* Arm Compute Library : ver. 17.09
* OpenBLAS            : ver. 0.2.20
* Boost               : ver. 1.65
* glog                : ver. 0.3.3
* gflags              : ver. 2.2.0
* protobuf            : ver. 3.1.0
* lmdb                : ver. 0.9.21
* OpenCV              : ver. 3.3.0

