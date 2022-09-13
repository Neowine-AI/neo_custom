import os

enroll_directory = os.path.join(os.path.expanduser('~'), "NW")

for root, dirs, files in os.walk(enroll_directory) :
    if root != enroll_directory :
        continue
    if dirs is None :
        continue
files.sort()
product_number = []
design_num = []
temp_num = 0
for file in files:
    if file[:-7] not in product_number :
        design_num.append(temp_num)
        temp_num = 0
        product_number.append(file[:-7])
    temp_num += 1
design_num.append(temp_num)
design_num.pop(0)

for i in range(len(product_number)):
    print(product_number[i], design_num[i])
print()
print("Total {} design rights enrolled".format(len(product_number)))

    

