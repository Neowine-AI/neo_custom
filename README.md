# neo_custom

## 관세청과제 성능평가 프로그램 설치 및 사용방법
 * 현재 어니컴의 평가서버는 임시로 오픈되어있는 상태이며, 현품 및 도면이미지도 임시 데이터가 들어있습니다.
 * 어니컴 평가서버에서 어떤 데이터들이 오는지 어떤 방식으로 명령어가 동작하는지 이해를 돕기위해 배포합니다.
 * 명령어를 실행하는 위치에 도면 및 현품 이미지가 저장됩니다.
<br>

## 현재 구현된 명령어
- image_verify {model} {number_of_tests} {ip_path}
- image_acc {model} {number_of_tests} {ip_path}
<br>

## 테스트 시 마다 sh 파일을 실행하여 /bin 폴더에 python 파일을 옮겨주어야 합니다!! 
<br>

### 1. 필요 라이브러리 설치
opencv-python, requests, numpy, onnxruntime (필요 할 경우 pytorch 등등 설치하여도 됩니다. 다만 이후에 각 기관 별로 추가한 라이브러리를 고지해주셔야합니다.)
<br>

### 2. 압축파일 복사 및 설치
- home 위치에 압축파일 다운로드 및 압축해제
- custom_bash.sh 실행권한 부여 (755 권한도 괜찮습니다)
<br>
`~/NeoCustom$ chmod +x custom_bash.sh` 
<br>
- sh파일 실행 (python 파일들과 같은 위치에서 진행해 주셔야 합니다.)
<br>
`~/NeoCustom$ custom_bash.sh`
<br>
- NeoCustom 폴더 내 models 폴더를 home 위치로 복사
<br>

### 3. 명령어 실행
`image_verify {model} {number_of_tests} {ip_path}`
<br>
`image_acc {model} {number_of_tests} {ip_path}`
<br>

model은 현재 NW입니다. 따라서 NW로 적어주시면됩니다.
number_of_tests 같은 경우 관세청에서 준 Swaager 링크를 참조하시면, 현재 10까지만 가능합니다.
<br>
<br>

![image](https://user-images.githubusercontent.com/68864422/186050189-32d540d2-f72a-447a-b428-49d29312ad24.png)

<br>
<br>
ip_path는 ip_path 가 적힌 txt 파일 위치입니다. (ex : /home/user/ip_path.txt)
<br>
<br>
<br>

### 테스트로 인하여 sh 파일을 여러번 수정하였을 때
/home/user/ 에 존재하는 .bashrc 을 cat 을 통해 확인하면

<br>

![image](https://user-images.githubusercontent.com/68864422/186049456-63966298-3dc0-4a24-99b6-f65c85681a2a.png)

<br>

위와 같이 같은 명령어가 계속 입력됩니다. 
<br>
`vi .bashrc`
<br>
이후 지우고 싶은 줄에서 dd를 연타하시면 해당 줄이 지워집니다. 이후 :wq 로 저장해주시고 
<br>
`source .bashrc`
<br>
를 진행해주세요
<br>

### models 폴더에 관하여
models 폴더는 항상 /home/user/ 에 존재하여야 합니다. (홈 디렉토리...)
models 내부에 onnx 모델 이름 또는 pytorch 모델 내부에는 무조건적으로 기관별 단축어를 넣어 주셔야 합니다(neo, tsn, gcu)
model 뿐만아니라 inference 하는 코드도 같이 넘겨 주셔야 합니다.(input size 를 어떻게 조절 할 것인지 등등)
<br>

### model이 파싱이 안된다면 
<br>
<br>

![image](https://user-images.githubusercontent.com/68864422/186050628-81eee638-704e-459c-8b66-31b4fc2e1f33.png)

<br>
위 사진 코드 부분에서 각 기관별로 모델을 다르게 파싱해주시면 됩니다.
