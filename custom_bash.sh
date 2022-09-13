echo -e "alias design_rights_enroll='python3 ${HOME}/enroll_neowine/enroll.py' \n" >> ${HOME}/.bashrc
echo -e "alias design_rights_list='python3 ${HOME}/enroll_neowine/list.py' \n" >> ${HOME}/.bashrc
echo -e "alias design_rights_delete='python3 ${HOME}/enroll_neowine/delete.py' \n" >> ${HOME}/.bashrc
echo -e "alias design_rights_clear='python3 ${HOME}/enroll_neowine/clear.py' \n" >> ${HOME}/.bashrc

sudo cp ./image_verify.py /bin
sudo cp ./image_acc.py /bin

echo -e "alias image_verify='python3 /bin/image_verify.py' \n" >> ${HOME}/.bashrc

echo -e "alias image_acc='python3 /bin/image_acc.py' \n" >> ${HOME}/.bashrc

sudo cp ./image_verify_test.py /bin
sudo cp ./image_acc_test.py /bin

echo -e "alias image_verify_test='python3 /bin/image_verify_test.py' \n" >> ${HOME}/.bashrc

echo -e "alias image_acc_test='python3 /bin/image_acc_test.py' \n" >> ${HOME}/.bashrc

source ${HOME}/.bashrc

