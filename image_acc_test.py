import requests
import cv2
import numpy as np
import onnxruntime as ort
import sys
import os

##
## Top N Acc
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

f = open(ip_path_list, 'r')
guanse_ip_address = f.readline()
f.close()
# guanse_ip_address = "http://localhost:8080"

test_path = os.path.expanduser('~')

files = os.listdir("{}/models".format(test_path))
TopAccsess = None
flag = 0

download_path = "{}/download/top3/".format(test_path)
os.makedirs(download_path + "same", exist_ok=True)
os.makedirs(download_path + "random", exist_ok=True)


if("neo" in files[0]) :
    TopAccsess = ort.InferenceSession("{}/models/accuracy_neo.onnx".format(test_path), providers=['CPUExecutionProvider'])
elif("tsn" in  files[0]) :
    TopAccsess = ort.InferenceSession("{}/models/accuracy_tsn.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 1
else : 
    TopAccsess = ort.InferenceSession("{}/models/accuracy_gcu.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 2

if(int(test_type) == 0) :
    for test_id in range(0, number_of_tests) :

        print("===== Test_id : {} =====".format(test_id))
        
        # First Step - Get the image from the server
        imageResponse = requests.get('{}/image/acc/download/{}/{}/'.format(guanse_ip_address,test_id, institute_name))
        TOPACCimage = imageResponse.content
        req_key = imageResponse.headers['req_key']
        
        print("test_id real img req_key : {}".format(req_key))
        #Third Setp - Inference the image

        # TODO : Each Comapny Give me Code
        os.makedirs(download_path + "random/" + str(test_id), exist_ok=True)
        ## NEOWINE Inference(example)
        if(flag == 0) :
            with open("{}random/{}/{}.jpg".format(download_path, test_id, req_key), 'wb') as f :
                f.write(TOPACCimage)
                        
            image = cv2.imread("{}random/{}/{}.jpg".format(download_path, test_id, req_key), cv2.IMREAD_GRAYSCALE)
            print("Acc image shape  : {}".format(image.shape))

            # TODO : resize input data
            image = cv2.resize(image, dsize=(28, 28))
            image = image.reshape(1, 1, 28, 28).astype(np.float32) # / 255

                # image_real = cv2.imread(TopAccrealImage)
                # image_real = cv2.resize(image_real, dsize=(28, 28))
                # image_real = image_real[None][None].astype(np.float32) / 255.

            # Inference the image
            result = TopAccsess.run(None, {TopAccsess.get_inputs()[0].name : image})[0]
            
            ## delete downloaded image
            #os.remove("{}.jpg".format(test_id))

            # Sorting result(example)

            # Last Step : Post the result to the server
            # resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : float(result[0][0]), 'reg2' : float(result[0][1]), 'reg3' : float(result[0][2])}
            resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : "32032032002", 'reg2' : "32032032ASDB124", 'reg3' : "A12324BD22214", "check" : 0}
            postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("TOPN POST Result(Success : 200) : " + str(responseStatus))
            print("")

        ## TODO : TSN LAB Inference
        elif(flag == 1) :
            print("tsn")
            
            # Last Step : Post the result to the server
            resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : "32032032002", 'reg2' : "32032032ASDB124", 'reg3' : "A12324BD22214", "check" : 0}
            postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("TOPN POST Result(Success : 200) : " + str(responseStatus))
            print("")

        ## TODO : Gachon Inference
        else : 
            print("Gachon")

            # Last Step : Post the result to the server
            resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : "32032032002", 'reg2' : "32032032ASDB124", 'reg3' : "A12324BD22214", "check" : 0}
            postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("TOPN POST Result(Success : 200) : " + str(responseStatus))
            print("")

else :
    for test_id in range(0, number_of_tests) :
        print("===== Test_id : {} =====".format(test_id))
        
        # First Step - Get the image from the server
        imageResponse = requests.get('{}/image/acc/download/{}/{}/same'.format(guanse_ip_address,test_id, institute_name))
        TOPACCimage = imageResponse.content
        req_key = imageResponse.headers['req_key']
        
        print("test_id real img req_key : {}".format(req_key))
        #Third Setp - Inference the image

        # TODO : Each Comapny Give me Code
        
        os.makedirs(download_path + "same/" + str(test_id), exist_ok=True)
        ## NEOWINE Inference(example)
        if(flag == 0) :
            with open("{}same/{}/{}.jpg".format(download_path, test_id, req_key), 'wb') as f :
                f.write(TOPACCimage)
                        
            image = cv2.imread("{}same/{}/{}.jpg".format(download_path, test_id, req_key), cv2.IMREAD_GRAYSCALE)
            print("Acc image shape  : {}".format(image.shape))

            # TODO : resize input data
            image = cv2.resize(image, dsize=(28, 28))
            image = image.reshape(1, 1, 28, 28).astype(np.float32) # / 255

                # image_real = cv2.imread(TopAccrealImage)
                # image_real = cv2.resize(image_real, dsize=(28, 28))
                # image_real = image_real[None][None].astype(np.float32) / 255.

            # Inference the image
            result = TopAccsess.run(None, {TopAccsess.get_inputs()[0].name : image})[0]
            
            ## delete downloaded image
            #os.remove("{}.jpg".format(test_id))

            # Sorting result(example)

            # Last Step : Post the result to the server
            # resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : float(result[0][0]), 'reg2' : float(result[0][1]), 'reg3' : float(result[0][2])}
            resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : "32032032002", 'reg2' : "32032032ASDB124", 'reg3' : "A12324BD22214", "check" : 1}
            postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("reg1 : {}".format(resultDataJson['reg1']))
            print("reg2 : {}".format(resultDataJson['reg2']))
            print("reg3 : {}".format(resultDataJson['reg3']))
            print("TOPN POST Result(Success : 200) : " + str(responseStatus))
            print("")

        ## TODO : TSN LAB Inference
        elif(flag == 1) :
            print("tsn")
            
            # Last Step : Post the result to the server
            resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : "32032032002", 'reg2' : "32032032ASDB124", 'reg3' : "A12324BD22214", "check" : 1}
            postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("TOPN POST Result(Success : 200) : " + str(responseStatus))
            print("")

        ## TODO : Gachon Inference
        else : 
            print("Gachon")

            # Last Step : Post the result to the server
            resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : "32032032002", 'reg2' : "32032032ASDB124", 'reg3' : "A12324BD22214", "check" : 1}
            postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
            responseStatus = postResponse.status_code
            print("TOPN POST Result(Success : 200) : " + str(responseStatus))
            print("")    
    
    

