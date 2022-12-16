import cv2
import numpy as np
import tensorflow as tf
from locaNet import locaNet
from PIL import Image, ImageDraw, ImageFont
import config as cfg
import math
from utils import *

def image_predict(image_path, model):
    if cfg.INPUT_CHANNEL == 3:
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    else:
        original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        original_image = original_image[..., np.newaxis]
    original_image = original_image.astype('float32')
    original_image = original_image/128 - 1
    image_data = original_image[np.newaxis, ...].astype(np.float32)
    conv = model.predict(image_data)
    conf = tf.sigmoid(conv[0, :, :, 1:2])
    np.set_printoptions(linewidth=np.inf)
    # for i in range(28):
    #     print(np.round(np.array(conv[0, i, :, 1]).T))
    pos_conf_above_threshold = np.argwhere(conf > 0.33)
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 26, encoding="unic")

    dist = 5
    list_pos = pos_conf_above_threshold.tolist()
    pos_conf_above_threshold = clean_array2d(list_pos, dist)

    for xy in pos_conf_above_threshold:
        curH = (xy[0]-0.5)*8
        curW = (xy[1]+0.5)*8
        draw.ellipse((curW-4, curH-4, curW+4, curH+4), outline ='white', width=2)
        draw.ellipse((curW-7, curH-7, curW+7, curH+7), outline ='black', width=2)
        draw.text((curW-20, curH),"{:3.2f}m".format(tf.exp(conv[0, xy[0], xy[1], 0])),fill='white', stroke_fill='black', stroke_width=1, font=font)
    image.show()
    # image.save(image_path[-6]+image_path[-5]+'.png')

def pred_max_conf(image_path, model):
    if cfg.INPUT_CHANNEL == 3:
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    else:
        original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        original_image = original_image[..., np.newaxis]
    original_image = original_image.astype('float32')
    original_image = original_image/128 - 1
    image_data = original_image[np.newaxis, ...].astype(np.float32)
    conv = model.predict(image_data)   
    conf = tf.sigmoid(conv[0, :, :, 1:2])
    xy = [np.argmax(conf)//40, np.argmax(conf)%40]
    d = tf.exp(conv[0, xy[0], xy[1], 0])
    # image = Image.open(image_path)
    # draw = ImageDraw.Draw(image)
    # draw.ellipse(((xy[0]-0.5)*8-5, (xy[1]-0.5)*8-5, (xy[0]-0.5)*8+5, (xy[1]-0.5)*8+5), outline ='white')
    # image.show()
    return [(xy[1]+0.5)*8, (xy[0]+0.5)*8, float(d)]

input_size   = cfg.TRAIN_INPUT_SIZE
input_layer  = tf.keras.layers.Input([input_size[0], input_size[1], cfg.INPUT_CHANNEL])
feature_maps = locaNet(input_layer)
model = tf.keras.Model(input_layer, feature_maps)
# model.load_weights("./output-real/locaNet")
model.load_weights("./output/locanet-1")
model.summary()

## Figure in the paper
image_predict('/home/akmaral/tubCloud/Shared/cvmrs/training_dataset/synth/single/1000/img_00999.jpg', model)
# image_predict("./dataset/synImgsMulti/0037.jpg", model)
# image_predict("./dataset/synImgsMulti/0047.jpg", model)
# image_predict("./dataset/synImgs/0837.jpg", model) # sample also in AIdeck
# image_predict("./dataset/synImgs/0970.jpg", model)
# image_predict("./dataset/aideck-dataset/imageStorage/imagesH2C/img00080.ppm", model)

## Figure in the paper
# 0.23 real, 0.33 syn, weight selection
# fileNames = []
# with open('./dataset/aideck-dataset/imageStorage/test.txt', 'r') as file:
#     for row in file:
#         fileNames.append(row.split()[0])
# for file in fileNames:
#     image_predict(file, model)

## Figure in the paper
# lineAll = []
# y_err = []
# z_err = []
# d_err = []
# with open('./dataset/aideck-dataset/imageStorage/test.txt', 'r') as file:
#     for row in file:
#         lineAll.append(row.split())
# for line in lineAll:
#     imgPath = line[0]
#     y_p = float(line[2].split(',')[0])
#     z_p = float(line[2].split(',')[1])
#     d   = float(line[2].split(',')[2])/1000.0
#     predict = pred_max_conf(imgPath, model)
#     y_err.append(y_p - predict[0])
#     z_err.append(z_p - predict[1])
#     d_err.append(d   - predict[2])
# import matplotlib.pyplot as plt
# allData = [y_err, z_err]
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
# axes[0].violinplot(allData, showmeans=True, showmedians=True)
# axes[0].set_title('2D position error in image')
# axes[0].yaxis.grid(True)
# axes[0].set_xticks([y+1 for y in range(len(allData))])
# axes[0].set_ylabel('Position error in pixels', fontsize=12)
# axes[0].set_xticklabels([r'$x_{p}$',r'$y_{p}$'], fontsize=12)
# axes[1].violinplot([d_err], showmeans=True, showmedians=True)
# axes[1].set_title('Depth error')
# axes[1].yaxis.grid(True)
# axes[1].set_xticks([y+1 for y in range(len([d_err]))])
# axes[1].set_ylabel('Depth error in meters', fontsize=12)
# axes[1].set_xticklabels([r'$d$'], fontsize=12)
# fig.tight_layout(pad=3.0)
# plt.show()

# Figure (error w.r.t distance)
# import matplotlib.pyplot as plt
# lineAll = []
# y_err = []
# z_err = []
# d_err = []
# dis = []
# with open('./dataset/synImgs/test.txt', 'r') as file:
#     for row in file:
#         lineAll.append(row.split())
# for line in lineAll:
#     imgPath = line[0]
#     y_p = float(line[2].split(',')[0])
#     z_p = float(line[2].split(',')[1])
#     d   = float(line[2].split(',')[2])/1000.0
#     predict = pred_max_conf(imgPath, model)
#     y_err.append(y_p - predict[0])
#     z_err.append(z_p - predict[1])
#     d_err.append(d   - predict[2])
#     dis.append(d)
# data = np.array((dis, y_err, z_err, d_err))
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
# x = data[0, :]
# y = data[1, :]
# ax1.scatter(x, y, c='tab:blue', label='pixError x', alpha=0.3, edgecolors='none')
# y = data[2, :]
# ax1.scatter(x, y, c='tab:orange', label='pixError y', alpha=0.3, edgecolors='none')
# y = data[3, :]
# ax2.scatter(x, y, c='tab:green', label='depthError', alpha=0.3, edgecolors='none')
# ax1.legend()
# ax1.grid(True)
# ax1.set_title('Position error in image', fontsize=12)
# ax1.set_ylabel('Error (Pixels)', fontsize=12)
# ax1.set_xlabel('Distance (m)', fontsize=12)
# ax2.legend()
# ax2.grid(True)
# ax2.set_title('Depth error')
# ax2.set_ylabel('Error (m)', fontsize=12)
# ax2.set_xlabel('Distance (m)', fontsize=12)
# plt.show()

# ## Figure position error
# from numpy.linalg import inv
# lineAll = []
# px_err = []
# py_err = []
# pz_err = []
# with open('dataset/synImgs/test.txt', 'r') as file:
#     for row in file:
#         lineAll.append(row.split())
# for line in lineAll:
#     imgPath = line[0]
#     predict = pred_max_conf(imgPath, model)
#     pI = np.array([[predict[0]], [predict[1]], [1]])
#     phi = float(line[1].split(',')[0])/180*3.1415
#     theta = -float(line[1].split(',')[1])/180*3.1415
#     RxInv = np.array([[1, 0, 0], [0, np.cos(phi), np.sin(phi)], [0, -np.sin(phi), np.cos(phi)]])
#     RyInv = np.array([[np.cos(theta), 0, -np.sin(theta)], [0, 1, 0], [np.sin(theta), 0, np.cos(theta)]])
#     Intrin = np.array([[185.14, 0, 169.54], [0, 185.13, 85.76], [0, 0, 1]])   
#     pC_TL = inv(Intrin)@pI*predict[2]
#     pC = inv(np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]]))@pC_TL
#     pH = inv(RyInv@RxInv)@pC
#     pH_GT = np.array([[float(line[3].split(',')[0])], [float(line[3].split(',')[1])], [float(line[3].split(',')[2])]])   
#     px_err.append(pH[0,0] - pH_GT[0,0])
#     py_err.append(pH[1,0] - pH_GT[1,0])
#     pz_err.append(pH[2,0] - pH_GT[2,0])
# import matplotlib.pyplot as plt
# allData = [px_err, py_err, pz_err]
# fig, axe = plt.subplots(figsize=(9, 4))
# axe.violinplot(allData, showmeans=True, showmedians=True)
# # axe.set_title('2D position error in image')
# axe.yaxis.grid(True)
# axe.set_xticks([y+1 for y in range(len(allData))])
# axe.set_ylabel('3D position error in horizontal frame')
# axe.set_xticklabels([r'$y_{h}$',r'$z_{h}$',r'$x_{h}$'])
# plt.show()