import os

enroll_directory = os.path.join(os.path.expanduser('~'), "NW")
os.system("rm -rf {}".format(enroll_directory))
print("entire list cleared!")
