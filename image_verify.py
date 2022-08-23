
import json
import requests
import cv2
import numpy as np
import onnxruntime as ort
import sys
import os

##
## One To One Match
##

institute_name = sys.argv[1]
number_of_tests = int(sys.argv[2])
ip_path_list = sys.argv[3]

## Read ip:port from ip_path.txt
f = open(ip_path_list, 'r')
guanse_ip_address = f.readline()
f.close()

# print(os.path.expanduser('~'))
# test_path = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.expanduser('~')

files = os.listdir("{}/models".format(test_path))
OTOMsess = None
flag = 0

## AI Model Name Rule : OneToOne_<Company Name>.onnx
if("neo" in files[0]) :
    OTOMsess = ort.InferenceSession("{}/models/verify_neo.onnx".format(test_path), providers=['CPUExecutionProvider'])
elif("tsn" in  files[0]) :
    OTOMsess = ort.InferenceSession("{}/models/verify_tsn.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 1
else : 
    OTOMsess = ort.InferenceSession("{}/models/verify_gcu.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 2

OTOMreq_keyList = []
for test_id in range(0, number_of_tests) :
    print("===== Test_id : {} =====".format(test_id))
    # First Step - Get the image count from the server
    
    OTOMreponse = requests.get('{}/image/one/download/{}/{}/copyright/'.format(guanse_ip_address, test_id, institute_name))
    planCount = json.loads(OTOMreponse.text)['count']
    print("image Count : {}".format(planCount))

    # Second Step - Get the image from the server
    OTOMimageList = []
    for i in range(0, int(planCount)) :
        imageResponse = requests.get('{}/image/one/download/{}/{}/copyright/{}'.format(guanse_ip_address, test_id, institute_name, i))
        OTOMimageList.append(imageResponse.content)

    OTOMrealImage = requests.get('{}/image/one/download/{}/{}/real'.format(guanse_ip_address, test_id, institute_name))
    OTOMreq_keyList.append(OTOMrealImage.headers['req_key'])
    print("test_id real img req_key : {}".format(OTOMreq_keyList[test_id]))
    OTOMrealImageData = OTOMrealImage.content
    with open("{}_real.jpg".format(test_id), 'wb') as f :
                f.write(OTOMrealImageData)

    #Third Setp - Inference the image

    # TODO : Each Comapny Give me Code
    
    ## NEOWINE Inference(example)
    if(flag == 0) :
        resultDataJson = None
        for i in range(0, int(planCount)) :
            with open("{}_{}.jpg".format(test_id,i), 'wb') as f :
                f.write(OTOMimageList[i])
            image = cv2.imread("{}_{}.jpg".format(test_id,i), cv2.IMREAD_GRAYSCALE)
            print("Verify image {} shape  : {}".format(i, image.shape))
            # data = np.frombuffer(OTOMimageList[i], dtype=np.uint8)

            # TODO : resize input data
            image = cv2.resize(image, dsize=(28, 28))
            image = image.reshape(1, 1, 28, 28).astype(np.float32) # / 255

            # image_real = cv2.imread(OTOMrealImage)
            # image_real = cv2.resize(image_real, dsize=(28, 28))
            # image_real = image_real[None][None].astype(np.float32) / 255.

            # Inference the image
            result = OTOMsess.run(None, {OTOMsess.get_inputs()[0].name : image})[0]
            
            ## delete downloaded image
            # os.remove("{}.jpg".format(i))
            
            # result_real_image = OTOMsess.run(None, {OTOMsess.get_inputs()[0].name : image})[0]
            # result = OTOMsess.run(None, {OTOMsess.get_inputs()[0].name : image, OTOMsess.get_inputs()[1].name : image_real})[0]            
            
            ensemble = float(max(result[0]))
            # Last Step : Post the result to the server
            resultDataJson = {'req_key' : OTOMreq_keyList[test_id], "model" : "{}".format(institute_name), "test_id" :test_id, 'similarity' : ensemble}

        postResponse = requests.post('{}/image/one/result'.format(guanse_ip_address), json=resultDataJson)
        responseStatus = postResponse.status_code
        print("OTOM POST Result(Success : 201) : " + str(responseStatus))
        print("")
    
    ## TODO : TSN LAB Inference
    elif(flag == 1) :
        print("tsn")
        
        # Last Step : Post the result to the server
        # resultDataJson = {'req_key' : OTOMreq_keyList[test_id], "model" : "{}".format(institute_name), "test_id" :test_id, 'similarity' : ensemble}
        # postResponse = requests.post('{}/image/one/result'.format(guanse_ip_address), json=resultDataJson)
        # responseStatus = postResponse.status_code
        # print("OTOM POST Result(Success : 201) : " + str(responseStatus))
        # print("")

    ## TODO : Gachon Inference
    else : 
        print("Gachon")

        # Last Step : Post the result to the server
        # resultDataJson = {'req_key' : OTOMreq_keyList[test_id], "model" : "{}".format(institute_name), "test_id" :test_id, 'similarity' : ensemble}
        # postResponse = requests.post('{}/image/one/result'.format(guanse_ip_address), json=resultDataJson)
        # responseStatus = postResponse.status_code
        # print("OTOM POST Result(Success : 201) : " + str(responseStatus))
        # print("")
    
    

