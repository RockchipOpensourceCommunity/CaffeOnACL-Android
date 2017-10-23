#!/usr/bin/env python

# Author: Zeng Fei <felix.zeng@rock-chips.com>

import os
import sys
import argparse

class error_to_exit(Exception):
  pass

def run_adb_cmd(cmd):
  full_cmd = 'adb shell \"' + cmd + '\"'
  os.system(full_cmd)

# show RK3399 CPU and GPU freq
def show_device_freq():
  show_cpu0 = 'cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq'
  show_cpu4 = 'cat /sys/devices/system/cpu/cpu4/cpufreq/cpuinfo_cur_freq'
  show_gpu  = 'cat /sys/devices/platform/ff9a0000.gpu/devfreq/ff9a0000.gpu/cur_freq'
  run_adb_cmd(show_cpu0)
  run_adb_cmd(show_cpu4)
  run_adb_cmd(show_gpu)

# fix RK3399 CPU and GPU freq
def fix_device_freq():
  show_device_freq()
  fix_cpu0 = 'echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor'
  fix_cpu4 = 'echo performance > /sys/devices/system/cpu/cpufreq/policy4/scaling_governor'
  fix_gpu  = 'echo performance > /sys/devices/platform/ff9a0000.gpu/devfreq/ff9a0000.gpu/governor'
  run_adb_cmd(fix_cpu0)
  run_adb_cmd(fix_cpu4)
  run_adb_cmd(fix_gpu)
  show_device_freq()

# do simple task to prevent the CPU and GPU fall into idle for maximizing the RK3399 performance
def spinning_robot():
  start_app = 'am start -S com.example.android.basicglsurfaceview/.BasicGLSurfaceViewActivity'
  lock_cpu0 = "taskset -p 1 \$(ps | grep com.example.android.basicglsurfaceview | busybox awk '{print \$2}')"
  run_adb_cmd(start_app)
  run_adb_cmd(lock_cpu0)

# model runner class for running all the network
class ModelRunner(object):

  def __init__(self, path, export_flags, task_set_cmd, caffe_bin, mean, labels, image):
    self.path = path
    self.export_flags = export_flags
    self.task_set_cmd = task_set_cmd
    self.caffe_bin = caffe_bin
    self.mean = mean
    self.labels = labels
    self.image = image

  def print_net_status(self, net_name, running_mode, status):
    print '============================================================================================'
    print ' '.join([status, net_name, '...', 'Running Mode:', running_mode])
    print '============================================================================================'

  def run_model(self, running_mode, net_name, proto_txt, caffe_model, mixed_value):

    export_flags = self.export_flags
    task_set_cmd = self.task_set_cmd
    caffe_bin = self.caffe_bin

    if (running_mode == 'ACL/NEON'):
      export_bypass_acl = 'export BYPASSACL=0x0'
    elif (running_mode == 'OpenBLAS'):
      export_bypass_acl = 'export BYPASSACL=0xffffffff'
    elif (running_mode == 'ACL/GPU'):
      export_bypass_acl = 'export BYPASSACL=0x0'
      caffe_bin = caffe_bin + '_gpu'
    elif (running_mode == 'Mixed'):
      export_bypass_acl = 'export BYPASSACL=' + mixed_value
    else:
      raise error_to_exit('Unsupported Running Mode: ' + running_mode)

    export_flags = ';'.join([export_flags, export_bypass_acl])

    command = ' '.join([export_flags + ';', task_set_cmd, caffe_bin, proto_txt, caffe_model, self.mean, self.labels, self.image])
    #print command
    fix_device_freq()
    self.print_net_status(net_name, running_mode, 'Start Running')
    run_adb_cmd(command)
    self.print_net_status(net_name, running_mode, 'End Running')

  # run AlexNet
  def run_alexnet(self, running_mode):
    net_name = 'AlexNet'
    net_dir = self.path + '/alexnet'
    proto_txt = net_dir + '/deploy.prototxt'
    caffe_model = net_dir + '/bvlc_alexnet.caffemodel'
    mixed_value = '0x14c'

    self.run_model(running_mode, net_name, proto_txt, caffe_model, mixed_value)

  # run GoogLeNet
  def run_googlenet(self, running_mode):
    net_name = 'GoogLeNet'
    net_dir = self.path + '/googlenet'
    proto_txt = net_dir + '/deploy.prototxt'
    caffe_model = net_dir + '/bvlc_googlenet.caffemodel'
    mixed_value = '0x14c'

    self.run_model(running_mode, net_name, proto_txt, caffe_model, mixed_value)

  # run SquezzeNet
  def run_squezzenet(self, running_mode):
    net_name = 'SquezzeNet'
    net_dir = self.path + '/squezzenet'
    proto_txt = net_dir + '/squeezenet.1.1.deploy.prototxt'
    caffe_model = net_dir + '/squeezenet_v1.1.caffemodel'
    mixed_value = '0x14c'

    self.run_model(running_mode, net_name, proto_txt, caffe_model, mixed_value)

  # run MobileNet
  def run_mobilenet(self, running_mode):
    net_name = 'MobileNet'
    net_dir = self.path + '/mobilenet'
    proto_txt = net_dir + '/mobilenet_deploy.prototxt'
    caffe_model = net_dir + '/mobilenet.caffemodel'
    mixed_value = '0x44'

    self.run_model(running_mode, net_name, proto_txt, caffe_model, mixed_value)


def main():

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--network', default='AlexNet', help='Input network name, support: AlexNet, googLeNet, SquezzeNet, MobileNet')
  args = parser.parse_args()

  running_mode_list = ['ACL/NEON', 'OpenBLAS', 'ACL/GPU', 'Mixed']

  test_caffe = '/data/test_caffe'
  test_data = test_caffe + '/test_data'

  binary = 'classification_profiling'
  export_library = 'export LD_LIBRARY_PATH=' + test_caffe
  export_glog_minloglevel = 'export GLOG_minloglevel=2'
  export_glog_logtostderr = 'export GLOG_logtostderr=0'
  export_openblas_num_threads = 'export OPENBLAS_NUM_THREADS=2'
  export_log_acl = 'export LOGACL=0x0'
  export_flags = ';'.join([export_library, export_glog_minloglevel, export_glog_logtostderr, export_openblas_num_threads, export_log_acl])
  task_set_cmd = 'taskset -a 30'

  caffe_bin = test_caffe + '/' + binary
  mean = test_data + '/imagenet_mean.binaryproto'
  labels = test_data + '/synset_words.txt'
  image = test_data + '/cat.jpg'

  fix_device_freq()
  spinning_robot()

  runner = ModelRunner(test_caffe, export_flags, task_set_cmd, caffe_bin, mean, labels, image)

  for running_mode in running_mode_list:
    print args.network
    if args.network.lower() == 'alexnet':
      runner.run_alexnet(running_mode)
    elif args.network.lower() == 'googlenet':
      runner.run_googlenet(running_mode)
    elif args.network.lower() == 'squeezenet':
      runner.run_squezzenet(running_mode)
    elif args.network.lower() == 'mobilenet':
      runner.run_mobilenet(running_mode)
    else:
      raise error_to_exit('Unsupported Network: ' + args.network)

if __name__ == '__main__':
    main()
