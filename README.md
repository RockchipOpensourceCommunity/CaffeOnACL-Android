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

# Build Caffe
./build_caffe.sh

# Download network
./model_download.sh

# Prepare model data for RK3399 device
./model_prepare.sh

# Update binary data for RK3399 device
./binary_update.sh

# Running SqueezeNet network (default is AlexNet, support AlexNet, GoogLeNet, SqueezeNet, MobileNet)
./model_runner.py SqueezeNet

```

## Prebuilts
Library|Version
:---:|:---:
Arm Compute Library |v17.10
OpenBLAS|v0.2.20
Boost|v1.65
glog|v0.3.3
gflags|v2.2.0
protobuf|v3.1.0
lmdb|v0.9.21
OpenCV|v3.3.0
