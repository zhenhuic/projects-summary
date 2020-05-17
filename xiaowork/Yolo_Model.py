from __future__ import division

from models import *
from Yolo_utils.utils import *

import argparse
from PIL import Image
import cv2

import torch
import torchvision.transforms.functional as TF

import datetime


class Yolo_Model():

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--image_folder", type=str, default="data/samples", help="path to dataset")
        parser.add_argument("--model_def", type=str, default="config/yolov3.cfg", help="path to model definition file")
        parser.add_argument("--weights_path", type=str, default="weights/yolov3.weights", help="path to weights file")
        parser.add_argument("--class_path", type=str, default="data/coco.names", help="path to class label file")
        parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
        parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
        parser.add_argument("--batch_size", type=int, default=1, help="size of the batches")
        parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
        parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
        parser.add_argument("--checkpoint_model", type=str, help="path to checkpoint model")
        opt = parser.parse_args()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # os.makedirs("output", exist_ok=True)

        # Set up model
        self.model = Darknet(opt.model_def, img_size=opt.img_size).to(self.device)

        if opt.weights_path.endswith(".weights"):
            # Load darknet weights
            self.model.load_darknet_weights(opt.weights_path)
        else:
            # Load checkpoint weights
            self.model.load_state_dict(torch.load(opt.weights_path))

        self.model.eval()  # Set in evaluation mode

    def getModel_Device(self):
        return self.model, self.device

    def transform(self, img_array, input_size):
        """

        :param img_array:
        :param input_size:
        :return:
        """
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img_array)

        width, height = img.size
        img = TF.resize(img, int(height / width * input_size))  # the smaller edge will be matched to input_size
        img = TF.pad(img, (0, int((img.size[0] - img.size[1]) / 2)))

        tensor = TF.to_tensor(img)
        # tensor = TF.normalize(tensor, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        return tensor

    def inference(self, model, input_tensor, device, num_classes, conf_thres=0.8, nms_thres=0.4):
        try:
            torch.cuda.empty_cache()  # 修复 RuntimeError: cuDNN error: CUDNN_STATUS_EXECUTION_FAILED
            input_tensor = input_tensor.to(device)
            # print(input_tensor.shape)

            output = model(input_tensor)
            preds = non_max_suppression(output, conf_thres, nms_thres)
        except RuntimeError as e:
            torch.cuda.empty_cache()
            preds = [None for _ in range(input_tensor.shape[0])]
            print(e)
        # preds = non_max_suppression(output, num_classes, conf_thres, nms_thres)
        return preds

    def stack_tensors(self, tensors):
        stacked = torch.stack(tensors)
        return stacked

    def detect_person(self, img):
        tensor_list = []
        tensor = self.transform(img, 416)
        tensor_list.append(tensor)

        tensor_list = self.stack_tensors(tensor_list)
        preds = self.inference(self.model, tensor_list, self.device, 80, 0.8, 0.4)

        if preds[0] is not None:
            for x1, y1, x2, y2, _, _, cls in preds[0]:
                if int(cls) == 0:
                    return True, int(x1), int(y1), int(x2), int(y2)
        return False, -1, -1, -1, -1


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# if __name__ == '__main__':
#     yolo_Model = Yolo_Model()
#
#     status_LUP = [0] * 20
#     status_LDOWN = [0] * 20
#
#     import os
#
#     path = "tiaoshi/失败"
#     file_list = os.listdir(path)
#     for files in file_list:
#         olddir = os.path.join(path, files)
#
#         print("视频路径为：{}".format(olddir))
#         # 2.2：开始加载视频
#         cap = cv2.VideoCapture(olddir)
#         # cap = cv2.VideoCapture("tiaoshi/ch11_20171219141909 00_13_55-00_14_50.mp4")
#         ret, frame = cap.read()
#         # 2.3：控制检测频率
#         start_time = time.time()
#
#         # 2.4：控制检测变量
#         isPersonUP = False
#         isActionStartUP = False
#
#         isPersonDOWN = False
#         isActionStartDOWN = False
#
#         while ret:
#
#             # 整体坐标
#             # frame = frame[120:550, 340:970]
#
#             # 下方坐标
#             frameDown = frame[250:500, 680:970]
#
#             # 上方坐标
#             frameUP = frame[140:400, 540:800]
#
#             # 根据队列进行检测
#             current_time = time.time()
#             if current_time - start_time >= 0.2:
#                 isPersonUP, x1UP, y1UP, x2UP, y2UP = yolo_Model.detect_person(frameUP)
#                 if isPersonUP:
#                     status_LUP.append(1)
#                 else:
#                     status_LUP.append(0)
#                 status_LUP.pop(0)
#
#                 isPersonDOWN, X1Down, X1DWON, X2DOWN, Y2DOWN = yolo_Model.detect_person(frameDown)
#                 if isPersonDOWN:
#                     status_LDOWN.append(1)
#                 else:
#                     status_LDOWN.append(0)
#                 status_LDOWN.pop(0)
#
#                 start_time = current_time
#
#             if sum(status_LUP) > 15 and isActionStartUP is False:
#                 print(get_time(), "：上方动作开始")
#                 isActionStartUP = True
#
#             if sum(status_LUP) == 0 and isActionStartUP is True:
#                 print(get_time(), "：上方动作结束")
#                 isActionStartUP = False
#
#             if sum(status_LDOWN) > 15 and isActionStartDOWN is False:
#                 print(get_time(), ":下方检测开始")
#                 isActionStartDOWN = True
#
#             if sum(status_LDOWN) == 0 and isActionStartDOWN is True:
#                 print(get_time(), ":下方检测结束")
#                 isActionStartDOWN = False
#
#             # 可视化展示预处理
#             # img = Image.fromarray(frameUP)
#             # width, height = img.size
#             # img = TF.resize(img, int(height / width * 416))  # the smaller edge will be matched to input_size
#             # img = TF.pad(img, (0, int((img.size[0] - img.size[1]) / 2)))
#             # frameUP = np.asarray(img)
#
#             # if isPersonUP:
#             #     cv2.rectangle(frameUP, (x1UP, y1UP), (x2UP, y2UP), (255, 0, 0), 2)
#             # cv2.imshow("detection", frame)
#             cv2.waitKey(25)
#             ret, frame = cap.read()
