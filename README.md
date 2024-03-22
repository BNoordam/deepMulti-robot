# Research project adaptation

An anaconda virtual environment is used for running this program with the right dependencies. First, install anaconda by following the instructions in https://conda.io/projects/conda/en/latest/user-guide/install/linux.html. Then create a conda environment with Python version 3.6, and install the required dependencies in this environment: 

```
conda create -n "myNNenv" python=3.6.0
conda activate myNNenv
sudo apt-get update
Pip install pip=20.1.1
Pip install tensorflow==2.1.2
Pip install h5py==2.10.0
python3 -m pip install Pillow
Pip3 install statistics
Conda install opencv
```

It should also be possible to flash this model on the AI deck, and run it on-board. An older version of the gap_SDK (version 3.8) is likely needed to this end.  

Demo.py is the script performing image predictions. The trained model is retrieved from https://tubcloud.tu-berlin.de/s/Sa5rN5JK7poGawr (IMRC lab Berlin). This research used the pre-trained model: models/loca_net_models/locanet/random-flight-filter1. In line 70 this file should be read. Make sure that the Conda environment is activated when using the Python script.

The  results can be found in Google drive. In the final paper in chapter 5.4. The raw images captured during flight, which are not yet classified, are listed in Google Drive under data/raw images.
 

# locaNet - Monocular Multi-robot Relative Localization with Deep Neural Networks

This project proposes a locaNet for multi-robot localization by predicting the pixel position of the robot center and its distance from the camera, which can be transformed to inertial 3D relative positions using the intrinsic parameter. The implementation contains several code projects: 1) Blender code for synthetic dataset generation; 2) TensorFlow-based network of the locaNet and training; 3) Onboard deep network code on the AIdeck; 4) Quadrotor control code based on Crazyflie firmware.

## Contents

    .
    ├── aideck-locaNet          # deep network on the AI edge chip - GAP8
    ├── dataset                 # 
        ├── AIdeck-dataset      # flight images and relative positions
        ├── Other files         # synthetic images rendered by Blender
        
    ├── Otherfiles      # neural network, training, and testing
    └── README.md

<!-- <p align="center">
  <img width="400" height="260" src="./plot.png">
</p> -->

Paper: [PDF on arXiv](https://arxiv.org/abs/2105.12797).

Video: [Real-world flight on Youtube](abc).

## Requirements

 - locaNet & locaAIdeck (Python 3.6, pip=20.1.1, tensorflow==2.1.2, h5py==2.10.0)
 - dataset (Blender, numpy, csv, statistics)

    
