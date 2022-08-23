# neo_custom

## 관세청과제 성능평가 프로그램 설치 및 사용방법
 * 현재 어니컴의 평가서버는 임시로 오픈되어있는 상태이며, 현품 및 도면이미지도 임시 데이터가 들어있습니다.
 * 어니컴 평가서버에서 어떤 데이터들이 오는지 어떤 방식으로 명령어가 동작하는지 이해를 돕기위해 배포합니다.
 * 명령어를 실행하는 위치에 도면 및 현품 이미지가 저장됩니다.
 * 현재 image_verify, image_acc 명령어만 구현되어있습니다.
 
## 테스트 시 마다 sh 파일을 실행하여 /bin 폴더에 python 파일을 옮겨주어야 합니다!! 
 
### 1. 필요 라이브러리 설치
opencv-python, requests, numpy, onnxruntime (필요 할 경우 pytorch 등등 설치하여도 됩니다. 다만 이후에 각 기관 별로 추가한 라이브러리를 고지해주셔야합니다.)

### 2. 압축파일 복사 및 설치
- home 위치에 압축파일 다운로드 및 압축해제
- custom_bash.sh 실행권한 부여
 > ~/NeoCustom$ chmod +x custom_bash.sh (755 권한도 괜찮습니다)
- sh파일 실행 (python 파일들과 같은 위치에서 진행해 주셔야 합니다.)
 > ~/NeoCustom$ custom_bash.sh
- NeoCustom 폴더 내 models 폴더를 home 위치로 복사

### 3. 명령어 실행
- image_verify {model} {number_of_tests} {ip_path}
- image_acc {model} {number_of_tests} {ip_path}

ip_path는 ip_path 가 적힌 txt 파일 위치입니다. (ex : /home/user/ip_path.txt)


### 테스트로 인하여 sh 파일을 여러번 수정하였을 때
/home/user/ 에 존재하는 .bashrc 을 cat 을 통해 확인하면

![image](https://user-images.githubusercontent.com/68864422/186049456-63966298-3dc0-4a24-99b6-f65c85681a2a.png)

위와 같이 같은 명령어가 계속 입력됩니다. vi .bashrc 이후 지우고 싶은 줄에서 dd를 연타하시면 해당 줄이 지워집니다. 이후 :wq 로 저장해주시고 source .bashrc를 진행해주세요
