import os
import cv2
import torch
import sys
import filetype
import numpy as np
from time import time

# dependencies : pip install pytorch, torchvision, onnx2torch, filetype, opencv-python==4.2, onnxruntime

def resize_with_pad_for_square(src_img, tgt_size=512):
    if src_img.shape[0] == tgt_size and src_img.shape[1] == tgt_size:
        return src_img

    if src_img.shape[0] > src_img.shape[1]:
        resize_ratio = tgt_size / src_img.shape[0]
        pad_array = [0, int(tgt_size - src_img.shape[1] * resize_ratio + 1) // 2]
    else:
        resize_ratio = tgt_size / src_img.shape[1]
        pad_array = [int(tgt_size - src_img.shape[0] * resize_ratio + 1) // 2, 0]

    tgt_img = cv2.resize(src_img, dsize=(0, 0), fx=resize_ratio, fy=resize_ratio, interpolation=cv2.INTER_AREA)
    tgt_img = np.pad(tgt_img, ((pad_array[0], (tgt_size - tgt_img.shape[0] - pad_array[0])),
                               (pad_array[1], (tgt_size - tgt_img.shape[1] - pad_array[1])), (0, 0)),
                     constant_values=255)

    return tgt_img

def image_normalization(img, img_min=0, img_max=255, epsilon=1e-12):
    img = np.float32(img)
    img = (img - np.min(img)) * (img_max - img_min) / \
          ((np.max(img) - np.min(img)) + epsilon) + img_min
    return img

def edge_detection_from_numpy(edge_detection_model, original_img: np.ndarray, resize=(1024, 1024)):
    """
    Downsizing image (with ratio) and generate edge image
    :param original_img:
    :return:
    """

    if original_img.shape[1] > original_img.shape[0]:  # larger width
        fx_ratio = 1.0
        fy_ratio = original_img.shape[0] / original_img.shape[1]
    else:
        fx_ratio = original_img.shape[1] / original_img.shape[0]
        fy_ratio = 1.0

    input_image = original_img.copy()
    normalization_value = 3.5 if 128 / input_image.mean() > 3.5 else 128 / input_image.mean()  # _MS_ normalization
    input_image = np.clip(input_image * normalization_value, 0, 255).astype(np.uint8)  # _MS_ normalization
    input_image = cv2.resize(input_image, dsize=resize)
    input_image = np.array(input_image, dtype=np.float32)  # .astype(np.float32)
    input_image -= [103.939, 116.779, 123.68]
    input_image = input_image.transpose(2, 0, 1)[None]
    input_tensor = torch.from_numpy(input_image)

    # input_tensor = self.edge_detection_tensor(torch.from_numpy(input_image))

    output = edge_detection_model(input_tensor)
    output = output[-1].detach().cpu().numpy()
    output = 1 / (1 + np.exp(-output))
    output = np.uint8(image_normalization(output[0][0]))
    output = cv2.bitwise_not(output).astype(np.uint8)
    output = cv2.resize(output, dsize=(0, 0), fx=fx_ratio, fy=fy_ratio)
    output = np.expand_dims(output, axis=2)

    return np.concatenate([output, output, output], axis=2)

def get_total_process_to_do(source_directory : str):
    total_processing = 0
    for root, dirs, files in os.walk(source_directory):
        if root != source_directory:  # ONLY REGISTER ROOT DIRECTORY
            continue
        for file in files:
            if filetype.is_image(os.path.join(root, file)) is False:
                continue
            total_processing += 1

    return total_processing

if __name__ == "__main__":
    startTime = time()

    # source_directory : picture_path 등록할 사진들이 들어 있는 폴더 경로 
    source_directory = sys.argv[1]
    
    # TODO : 회사명, enroll 폴더명 등 자유롭게 변경해주세요
    # target_directory : 변환된 사진이 저장 될 폴더 경로
    # enroll_directory : enroll에 필요한 모델들과 python 파일이 있는 곳
    target_directory = os.path.join(os.path.expanduser('~'), "NW")
    enroll_directory = os.path.join(os.path.expanduser('~'), "enroll_neowine")
    print(enroll_directory)
    os.makedirs(target_directory, exist_ok=True)

    total_processing = get_total_process_to_do(source_directory)
    print("Total Design Drawing Number is : ", total_processing)

    edge_detection_model = torch.load(enroll_directory + "/utils/model_edge_detection.pt")
    feature_extractor_model = torch.load(enroll_directory + "/result_model/model_resnet50_dim64_group.pt")
    edge_detection_model.eval()
    feature_extractor_model.eval()

    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    edge_detection_model.to(device=torch.device("cpu"))
    feature_extractor_model.to(device=device)
    product_number = []
    for root, dirs, files in os.walk(source_directory):
        if root != source_directory: # ONLY REGISTER ROOT DIRECTORY
            continue
        files.sort()
        for file in files:
            if filetype.is_image(os.path.join(root, file)) is False:
                continue

            input_image = cv2.imread(os.path.join(root, file), cv2.IMREAD_COLOR)
            input_image = edge_detection_from_numpy(edge_detection_model, input_image, resize=(1024, 1024))
            input_image = resize_with_pad_for_square(input_image, tgt_size=512)
            input_numpy = (input_image.transpose(2, 0, 1) / 255.).astype(np.float32)[None]
            input_tensor = torch.from_numpy(input_numpy).to(device)

            _, _, feature, _ = feature_extractor_model(input_tensor, input_tensor)

            feature_numpy = feature.detach().cpu().numpy()

            # Some Classification For Robust Retrieval

            # END
            product_directory = os.path.join(target_directory, os.path.basename(file[:-7]))
            print(file[:-4])
            if product_directory.split("/")[-1] not in product_number:
                product_number.append(product_directory.split("/")[-1])
            np.save(os.path.join(target_directory, os.path.basename(file.split(".")[0]) + ".npy"), feature_numpy)

                
    endTime = time()
    print("Enrolled {} Design Rights".format(len(product_number)))
    print("time elapsed : ", endTime - startTime)

