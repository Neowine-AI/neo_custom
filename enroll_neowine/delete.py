from ast import arg
import os
import sys

enroll_directory = os.path.join(os.path.expanduser('~'), "NW")

for root, dirs, files in os.walk(enroll_directory) :
    if root != enroll_directory :
        continue
    if dirs is None :
        continue

delete_num = len(sys.argv) - 1

delete_product = []
for i in range(delete_num):
    temp = 0
    for file in files :
        if sys.argv[i+1] in file:
            temp += 1
            os.remove(os.path.join(enroll_directory, file))
    
    delete_product.append(temp)

for i in range(delete_num):
    print("{} {}".format(sys.argv[i+1], delete_product[i]))

print()
print("{} design rights deleted".format(delete_num))
