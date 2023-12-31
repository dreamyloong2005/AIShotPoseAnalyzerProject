# AIShotPoseAnalyzerProject
## A FREE and OPENSOURCE shot pose analyzer software for basketball lovers based on OpenPose and 3d-pose-baseline.

Here is a simple tutorial to teach you how to use AIShotPoseAnalyzer.  
First make sure you have installed these softwares already:
1. Python3.7.9
2. Tensorflow (<2.0, tensorflow-gpu==1.15.5 recommanded because its the last version before v2.0)

Now let's get started.  
Step1: Clone AIShotPoseAnalyzerProject onto your computer.  
Step2: Clone OpenPose (https://github.com/CMU-Perceptual-Computing-Lab/openpose) and 3d-pose-baseline (https://github.com/ArashHosseini/3d-pose-baseline) into the project folder.  
For bug fix, make sure you are using the openpose-3dpose-sandbox.py and viz.py from AIShotPoseAnalyzerProject instead of the original ones.  
Step3: Compile OpenPose, remember to tick BUILD_PYTHON in CMake-GUI.  
Step4: Record your shot video, locate your shot, edit the video clip to a proper length, and then put it under ../AIShotPoseAnalyzerProject/Resources/Videos/  
Step5: Run aispa_video_reader.py, enter the complete file name (with extension name) of your video.  
Then you can find Json Files generated under ../AIShotPoseAnalyzerProject/OutputFiles/Videos/[VideoFileNameWithoutExtensionName]/JsonFiles/  
You can also find the rendered pictures of each frame in PNG generated under ../AIShotPoseAnalyzerProject/OutputFiles/Videos/[VideoFileNameWithoutExtensionName]/FrameImageFiles/  
Step6: Use 3d-pose-baseline to generate 2d_data.json and 3d_data.json from the folder JsonFiles.  
Command:
```
python src/openpose_3dpose_sandbox.py --camera_frame --residual --batch_norm --dropout 0.5 --max_norm --evaluateActionWise --use_sh --epochs 200 --load 4874200 --pose_estimation_json /path/to/json_directory --write_gif --gif_fps 24
```
PS: "--write_gif --gif_fps 24" is optional, if you don't want to generate a gif file, delete it.  
Step7: Run aispa_json_file_reader.py, enter the complete file name (with extension name) of your video, and you will see the visualized analysis results.

PS:
1. If tensorflow-gpu doesn't work, use tensorflow instead.
2. If errors occur when you are using 3d-pose-baseline to generate 2d_data.json and 3d_data.json, either should you use the command mkdir to create necessary directories under ../AIShotPoseAnalyzerProject/3d-pose-baseline/ or use the command python -m pip install to install the missing modules.
3. 3d-pose-baseline original repository: https://github.com/una-dinosauria/3d-pose-baseline, but we are using its OpenPose-supported fork.
4. Citing (BibTex):
```
@article{8765346,  
  author = {Z. {Cao} and G. {Hidalgo Martinez} and T. {Simon} and S. {Wei} and Y. A. {Sheikh}},  
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},  
  title = {OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields},  
  year = {2019}  
}

@inproceedings{simon2017hand,  
  author = {Tomas Simon and Hanbyul Joo and Iain Matthews and Yaser Sheikh},  
  booktitle = {CVPR},  
  title = {Hand Keypoint Detection in Single Images using Multiview Bootstrapping},  
  year = {2017}  
}

@inproceedings{cao2017realtime,  
  author = {Zhe Cao and Tomas Simon and Shih-En Wei and Yaser Sheikh},  
  booktitle = {CVPR},  
  title = {Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields},  
  year = {2017}  
}

@inproceedings{wei2016cpm,  
  author = {Shih-En Wei and Varun Ramakrishna and Takeo Kanade and Yaser Sheikh},  
  booktitle = {CVPR},  
  title = {Convolutional pose machines},  
  year = {2016}  
}

@inproceedings{martinez_2017_3dbaseline,
  title={A simple yet effective baseline for 3d human pose estimation},
  author={Martinez, Julieta and Hossain, Rayat and Romero, Javier and Little, James J.},
  booktitle={ICCV},
  year={2017}
}
```
