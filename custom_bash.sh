sudo cp ./image_verify.py /bin
sudo cp ./image_acc.py /bin

echo -e "alias image_verify='python3 /bin/image_verify.py' \n" >> ${HOME}/.bashrc

echo -e "alias image_acc='python3 /bin/image_acc.py' \n" >> ${HOME}/.bashrc

source ${HOME}/.bashrc

