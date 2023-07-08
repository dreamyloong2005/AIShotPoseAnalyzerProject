import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '/openpose/build/python/openpose/Release')
os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/openpose/build/x64/Release;' + dir_path + '/openpose/build/bin;'

import pyopenpose as op
import cv2
import json

# 设置OpenPose参数
params = dict()
model_folder = os.path.join(dir_path, 'openpose', 'models')
params["model_folder"] = model_folder
params["number_people_max"] = 1  # 设置最大人数为1，即只分析一个主要人物

# 初始化OpenPose对象
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

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
while True:
    # 读取视频帧
    ret, frame_image = cap.read()

    # 检查是否到达视频末尾
    if (not ret) or (frame_image is None):
        break

    # 姿势估计
    datum = op.Datum()
    datum.cvInputData = frame_image
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    keypoints = datum.poseKeypoints

    # 初始化json字典
    jdict = {}
    jdict["version"] = 1.3
    jdict["people"] = []

    # 如果检测到人物，插入json字典
    if keypoints is not None and len(keypoints) > 0:
        person_info = {}
        person_info["person_id"] = [-1]
        person_info["pose_keypoints_2d"] = [float(0)] * 75
        person_info["face_keypoints_2d"] = []
        person_info["hand_left__keypoints_2d"] = []
        person_info["hand_right_keypoints_2d"] = []
        person_info["pose_keypoints_3d"] = []
        person_info["face_keypoints_3d"] = []
        person_info["hand_left_keypoints_3d"] = []
        person_info["hand_right_keypoints_3d"] = []

        # 将关节数据传入json字典，严格按照OpenPoseDemo的格式
        for i in range(25):
            if (keypoints[0][i][0] == 0):
                person_info["pose_keypoints_2d"][3 * i] = 0
            else:
                person_info["pose_keypoints_2d"][3 * i] = round(float(keypoints[0][i][0]), 3)

            if (keypoints[0][i][1] == 0):
                person_info["pose_keypoints_2d"][3 * i + 1] = 0
            else:
                person_info["pose_keypoints_2d"][3 * i + 1] = round(float(keypoints[0][i][1]), 3)

            if (keypoints[0][i][2] == 0):
                person_info["pose_keypoints_2d"][3 * i + 2] = 0
            else:
                person_info["pose_keypoints_2d"][3 * i + 2] = round(float(keypoints[0][i][2]), 6)

        jdict["people"].append(person_info)

    # 文件名按照OpenPoseDemo的输出格式：视屏文件名_十二位帧序数_keypoints.json
    sframe = str(frame)
    if (len(sframe) < 12):
        jfile_path = "OutputFiles/Videos/" + video_name + "/" + "JsonFiles" + "/" + video_name + "_" + sframe.zfill(12) + "_keypoints.json"
        rendered_frame_image_path = "OutputFiles/Videos/" + video_name + "/FrameImageFiles/Rendered/" + video_name + "_" + sframe.zfill(12) + "_rendered.png"
    else:
        jfile_path = "OutputFiles/Videos/" + video_name + "/" + "JsonFiles" + "/" + video_name + "_" + sframe + "_keypoints.json"
        rendered_frame_image_path = "OutputFiles/Videos/" + video_name + "/FrameImageFiles/Rendered/" + video_name + "_" + sframe + "_rendered.png"

    try:
        with open(jfile_path, 'w', encoding='utf-8') as jfile:
            json.dump(jdict, jfile, ensure_ascii=False, separators=(',', ':'))
        print("数据成功写入文件" + jfile_path)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(jfile_path), exist_ok=True)
        with open(jfile_path, 'x', encoding='utf-8') as jfile:
            json.dump(jdict, jfile, ensure_ascii=False, separators=(',', ':'))
        print("数据成功写入文件" + jfile_path)
    except PermissionError:
        print("没有权限访问文件" + jfile_path + "，请检查文件的读写权限。")

    window_title = "Reading Video File: " + video_base_name + " ......"
    cv2.imshow(window_title, datum.cvOutputData)
    if not os.path.exists(os.path.dirname(rendered_frame_image_path)):
        print("写入失败，正在创建渲染图目录......成功！开始尝试再次写入图片。")
        os.makedirs(os.path.dirname(rendered_frame_image_path))
    cv2.imwrite(rendered_frame_image_path, datum.cvOutputData)
    print("图片" + rendered_frame_image_path + "写入成功")
    cv2.setWindowProperty(window_title, cv2.WND_PROP_TOPMOST, 1)

    frame += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()

# 停止OpenPose
opWrapper.stop()
