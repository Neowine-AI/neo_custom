
import json
from site import getuserbase
import requests
import cv2
import numpy as np
import onnxruntime as ort
import sys
import os

##
## One To One Match
##


if(len(sys.argv) < 4 or len(sys.argv) > 5) :
    print("Usage : image_verify_test <institute_name> <number_of_tests> <ip_path_list> <test_type{ 0(default) : random, 1 : same }>")
    exit()
test_type = 0
institute_name = sys.argv[1]
number_of_tests = int(sys.argv[2])
ip_path_list = sys.argv[3]
if(len(sys.argv) == 5) :
    test_type = sys.argv[4]

## Read ip:port from ip_path.txt
f = open(ip_path_list, 'r')
guanse_ip_address = f.readline()
f.close()
# guanse_ip_address = "http://localhost:8080"
# print(os.path.expanduser('~'))
# test_path = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.expanduser('~')

files = os.listdir("{}/models".format(test_path))
OTOMsess = None
flag = 0

os.makedirs("{}/download/similar/copyright".format(test_path), exist_ok=True)
os.makedirs("{}/download/similar/real".format(test_path), exist_ok=True)

## AI Model Name Rule : OneToOne_<Company Name>.onnx
if("neo" in institute_name) :
    OTOMsess = ort.InferenceSession("{}/models/verify_neo.onnx".format(test_path), providers=['CPUExecutionProvider'])
elif("tsn" in  institute_name) :
    OTOMsess = ort.InferenceSession("{}/models/verify_tsn.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 1
else : 
    OTOMsess = ort.InferenceSession("{}/models/verify_gcu.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 2
if(int(test_type) == 0) :
    OTOMreq_keyList = []
    for test_id in range(0, number_of_tests) :
        print("===== Test_id : {} =====".format(test_id))
        # First Step - Get the image count from the server
        
        OTOMreponse = requests.get('{}/image/one/download/{}/{}/copyright/'.format(guanse_ip_address, test_id, institute_name))
        planCount = json.loads(OTOMreponse.text)['data']['count']
        randomImageNum = json.loads(OTOMreponse.text)['data']['imageNum']
        print("Random image Num : {}".format(randomImageNum))
        print("image Count : {}".format(planCount))

        # Second Step - Get the image from the server
        OTOMimageList = []
        for i in range(0, int(planCount)) :
            imageResponse = requests.get('{}/image/one/download/{}/{}/copyright/{}/{}'.format(guanse_ip_address, test_id, institute_name, i, randomImageNum))
            OTOMimageList.append(imageResponse.content)

        OTOMrealImage = requests.get('{}/image/one/download/{}/{}/real'.format(guanse_ip_address, test_id, institute_name))
        OTOMreq_keyList.append(OTOMrealImage.headers['req_key'])
        print("test_id real img req_key : {}".format(OTOMreq_keyList[test_id]))
        OTOMrealImageData = OTOMrealImage.content
        
        dir_path_copyright = "{}/download/similar/copyright/random/{}".format(test_path, test_id)
        dir_path_real = "{}/download/similar/real/random/{}".format(test_path, test_id)
        os.makedirs(dir_path_copyright, exist_ok=True)
        os.makedirs(dir_path_real, exist_ok=True)

        with open("{}/{}_real.jpg".format(dir_path_real,OTOMreq_keyList[test_id]), 'wb') as f :
            f.write(OTOMrealImageData)
        #Third Setp - Inference the image

        # TODO : Each Comapny Give me Code
        
        ## NEOWINE Inference(example)
        if(flag == 0) :
            resultDataJson = None
            for i in range(0, int(planCount)) :
                os.makedirs(dir_path_copyright, exist_ok=True)
                with open("{}/{}_{}.jpg".format(dir_path_copyright,randomImageNum,i), 'wb') as f :
                    f.write(OTOMimageList[i])
                image = cv2.imread("{}/{}_{}.jpg".format(dir_path_copyright,randomImageNum,i), cv2.IMREAD_GRAYSCALE)
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
                resultDataJson = {'copyright_key' : randomImageNum, 'req_key' : OTOMreq_keyList[test_id], "model" : "{}".format(institute_name), "test_id" :test_id, 'similarity' : ensemble, "check" : 0}

            postResponse = requests.post('{}/image/one/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("OTOM POST Result(Success : 201) : " + str(responseStatus))
            print("result : {}".format(resultDataJson['similarity'])) 
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

else : 
    OTOMreq_keyList = []
    for test_id in range(0, number_of_tests) :
        print("===== Test_id : {} =====".format(test_id))
        # First Step - Get the image count from the server
        
        OTOMreponse = requests.get('{}/image/one/download/{}/{}/copyright/same'.format(guanse_ip_address, test_id, institute_name))
        planCount = json.loads(OTOMreponse.text)['data']['count']
        specifiedImageNum = json.loads(OTOMreponse.text)['data']['imageNum']
        print("Same image Num : {}".format(specifiedImageNum))
        print("image Count : {}".format(planCount))

        # Second Step - Get the image from the server
        OTOMimageList = []
        for i in range(0, int(planCount)) :
            imageResponse = requests.get('{}/image/one/download/{}/{}/copyright/{}/{}'.format(guanse_ip_address, test_id, institute_name, i, specifiedImageNum))
            OTOMimageList.append(imageResponse.content)

        OTOMrealImage = requests.get('{}/image/one/download/{}/{}/real/same'.format(guanse_ip_address, test_id, institute_name, test_id))
        OTOMreq_keyList.append(OTOMrealImage.headers['req_key'])
        print("test_id real img req_key : {}".format(OTOMreq_keyList[test_id]))
        OTOMrealImageData = OTOMrealImage.content
        
        dir_path_copyright = "{}/download/similar/copyright/same/{}".format(test_path, test_id)
        dir_path_real = "{}/download/similar/real/same/{}".format(test_path, test_id)
        os.makedirs(dir_path_copyright, exist_ok=True)
        os.makedirs(dir_path_real, exist_ok=True)

        os.makedirs(dir_path_real, exist_ok=True)
        with open("{}/{}_real.jpg".format(dir_path_real,test_id), 'wb') as f :
            f.write(OTOMrealImageData)
        #Third Setp - Inference the image

        # TODO : Each Comapny Give me Code
        
        ## NEOWINE Inference(example)
        if(flag == 0) :
            resultDataJson = None
            for i in range(0, int(planCount)) :
                os.makedirs(dir_path_copyright, exist_ok=True)
                with open("{}/{}_{}.jpg".format(dir_path_copyright,specifiedImageNum,i), 'wb') as f :
                    f.write(OTOMimageList[i])
                image = cv2.imread("{}/{}_{}.jpg".format(dir_path_copyright,specifiedImageNum,i), cv2.IMREAD_GRAYSCALE)
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
                resultDataJson = {'copyright_key' : test_id ,'req_key' : OTOMreq_keyList[test_id], "model" : "{}".format(institute_name), "test_id" :test_id, 'similarity' : ensemble, "check" : 1}

            postResponse = requests.post('{}/image/one/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("OTOM POST Result(Success : 201) : " + str(responseStatus))
            print("result : {}".format(resultDataJson['similarity'])) 
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

