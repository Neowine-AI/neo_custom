import requests
import cv2
import numpy as np
import onnxruntime as ort
import sys
import os

##
## Top N Acc
##

institute_name = sys.argv[1]
number_of_tests = int(sys.argv[2])
ip_path_list = sys.argv[3]
## AI Model Name Rule : OneToOne_<Company Name>.onnx
f = open(ip_path_list, 'r')
guanse_ip_address = f.readline()
f.close()

test_path = os.path.expanduser('~')

files = os.listdir("{}/models".format(test_path))
TopAccsess = None
flag = 0
if("neo" in files[0]) :
    TopAccsess = ort.InferenceSession("{}/models/topacc_neo.onnx".format(test_path), providers=['CPUExecutionProvider'])
elif("tsn" in  files[0]) :
    TopAccsess = ort.InferenceSession("{}/models/topacc_tsn.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 1
else : 
    TopAccsess = ort.InferenceSession("{}/models/topacc_gachon.onnx".format(test_path), providers=['CPUExecutionProvider'])
    flag = 2

for test_id in range(0, number_of_tests) :
    print("===== Test_id : {} =====".format(test_id))
    
    # First Step - Get the image from the server
    imageResponse = requests.get('{}/image/acc/download/{}/{}/'.format(guanse_ip_address,test_id, institute_name))
    TOPACCimage = imageResponse.content
    req_key = imageResponse.headers['req_key']
    
    print("test_id real img req_key : {}".format(req_key))
    #Third Setp - Inference the image

    # TODO : Each Comapny Give me Code
    
    ## NEOWINE Inference(example)
    if(flag == 0) :
        with open("{}.jpg".format(test_id), 'wb') as f :
            f.write(TOPACCimage)
                    
        image = cv2.imread("{}.jpg".format(test_id), cv2.IMREAD_GRAYSCALE)
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
        resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : "32032032002", 'reg2' : "32032032ASDB124", 'reg3' : "A12324BD22214"}
        postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
        responseStatus = postResponse.status_code
        print("TOPN POST Result(Success : 201) : " + str(responseStatus))
        print("")

    ## TODO : TSN LAB Inference
    elif(flag == 1) :
        print("tsn")
        
        # Last Step : Post the result to the server
        resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : float(result[0][0]), 'reg2' : float(result[0][1]), 'reg3' : float(result[0][2])}
        postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
        responseStatus = postResponse.status_code
        print("TOPN POST Result(Success : 201) : " + str(responseStatus))
        print("")

    ## TODO : Gachon Inference
    else : 
        print("Gachon")

        # Last Step : Post the result to the server
        resultDataJson = {'req_key' : req_key, "model" : "{}".format(institute_name), "test_id" : "{}".format(test_id), 'reg1' : float(result[0][0]), 'reg2' : float(result[0][1]), 'reg3' : float(result[0][2])}
        postResponse = requests.post('{}/image/acc/result'.format(guanse_ip_address), json=resultDataJson)
        responseStatus = postResponse.status_code
        print("TOPN POST Result(Success : 201) : " + str(responseStatus))
        print("")
    
    

