#模块"aspa_json_file_reader"，功能为读取3d_data.json来计算角度，根据中心关节坐标可信度，在角度计算时会忽略一些可信度低的帧

import os
import json
import cv2

dir_path = os.path.dirname(os.path.realpath(__file__))
path_3d_data = dir_path+"/3d-pose-baseline/maya/3d_data.json"
jfile_3d_data = open(path_3d_data, 'r', encoding='utf8')
jdict_3d_data = json.load(jfile_3d_data)

import math
import numpy as np
import matplotlib.pyplot as plt

#该函数功能是计算夹角BAC的度数
def calculate_angle(A, B, C):
    # 计算向量AB和向量AC
    vector_AB = [B[0] - A[0], B[1] - A[1], B[2] - A[2]]
    vector_AC = [C[0] - A[0], C[1] - A[1], C[2] - A[2]]

    # 计算向量AB和向量AC的内积
    dot_product = vector_AB[0] * vector_AC[0] + vector_AB[1] * vector_AC[1] + vector_AB[2] * vector_AC[2]

    # 计算向量的模长
    magnitude_AB = math.sqrt(vector_AB[0] ** 2 + vector_AB[1] ** 2 + vector_AB[2] ** 2)
    magnitude_AC = math.sqrt(vector_AC[0] ** 2 + vector_AC[1] ** 2 + vector_AC[2] ** 2)

    # 避免除以零的情况
    if magnitude_AB == 0 or magnitude_AC == 0:
        return 0

    # 计算夹角的弧度值
    angle_rad = math.acos(dot_product / (magnitude_AB * magnitude_AC))

    # 将弧度转换为度数
    angle_deg = math.degrees(angle_rad)

    return angle_deg

# 打开视频文件
video_path = "Resources/Videos/" + input()
video_base_name = os.path.basename(video_path)
video_name = video_base_name.split('.')[0]
video_extension_name = video_base_name.split('.')[1]
cap = cv2.VideoCapture(video_path)
# 检查视频是否成功打开
if not cap.isOpened():
    print("无法打开视频文件")
    exit()

# 循环读取和输出
frame = 0
angles_valid = []
while True:
    # 读取视频帧
    ret, frame_image = cap.read()

    # 检查是否到达视频末尾
    if (not ret) or (frame_image is None):
        break

    sframe = str(frame)
    if (len(sframe) < 12):
        path_frame_confidence_data = "OutputFiles/Videos/" + video_name + "/" + "JsonFiles" + "/" + video_name + "_" + sframe.zfill(12) + "_keypoints.json"
    else:
        path_frame_confidence_data = "OutputFiles/Videos/" + video_name + "/" + "JsonFiles" + "/" + video_name + "_" + sframe + "_keypoints.json"

    jfile_frame_confidence_data = open(path_frame_confidence_data, 'r', encoding='utf8')
    jdict_frame_confidence_data = json.load(jfile_frame_confidence_data)
    print("FRAME"+sframe)
    if(len(jdict_frame_confidence_data["people"]) > 0):
        ignore_limit=0.1
        elbow_confidence=jdict_frame_confidence_data["people"][0]["pose_keypoints_2d"][11]
        wrist_confidence=jdict_frame_confidence_data["people"][0]["pose_keypoints_2d"][14]
        shoulder_confidence=jdict_frame_confidence_data["people"][0]["pose_keypoints_2d"][8]
        if(elbow_confidence > ignore_limit) :
            elbow_3d = jdict_3d_data[sframe]["18"]["translate"]
            wrist_3d = jdict_3d_data[sframe]["19"]["translate"]
            shoulder_3d = jdict_3d_data[sframe]["17"]["translate"]
            angle=calculate_angle(elbow_3d, wrist_3d, shoulder_3d)
            print(angle)
            angles_valid.append(angle)
        else:
            print("Low confidence, ignored.")
    else:
        print("No target detected in tis frame, ignored.")

    frame += 1
length=len(angles_valid)
x=np.arange(0, length, 1)
y=np.array(angles_valid)
z1=np.polyfit(x, y, 18)
p1=np.poly1d(z1)
yvals=p1(x)
angle_plot=plt.plot(x, yvals, 'r')
plt.plot(x, y, color='blue')
plt.scatter(x, y)
plt.xlabel("Valid Frame")
plt.ylabel("Angle (Degrees)")
print(p1)
plt.show()
cap.release()