## 관세청과제 성능평가 프로그램 설치 및 사용방법
* 어니컴 및 자체 테스트용 ip 정보는 포함되어있지 않습니다.
* 명령어를 실행하는 위치에 도면 및 현품 이미지가 저장됩니다.
<br>

## 명령어
### 어니컴 테스트용 명령어 <br>
- image_verify {model} {number_of_tests} {ip_path}
- image_acc {model} {number_of_tests} {ip_path}

### 자체 테스트용 명령어 <br>
- image_verify_test {model} {number_of_tests} {ip_path} {test_type}
- image_acc_test {model} {number_of_tests} {ip_path} 
<br>

### 1. 필요 라이브러리 설치
- python3 version 3.8.10 환경
- opencv-python, requests, numpy, onnxruntime 
- 필요한 경우 pytorch 등 설치. (추후 기관별로 사용하는 D/L 라이브러리 확정필요)
<br>

### 2. 압축파일 복사 및 설치
- home 위치에 압축파일 다운로드 및 압축해제
- custom_bash.sh 실행권한 부여 (755 권한도 괜찮습니다)

`~/neo_custom$ chmod +x custom_bash.sh` 

- sh파일 실행 (sh파일과 python 파일은 동일한 path에 위치해야 함)
- :warning: python 코드 업데이트 시 sh 파일을 다시 실행하여 /bin 폴더에 python 파일을 최신화해야 함 
- :warning: sh파일을 여러번 실행한 경우, /home/user/위치의 .bashrc 파일 수정 필요

`~/neo_custom$ custom_bash.sh`

- NeoCustom 폴더 내 models 폴더를 home 위치로 복사
<br>

### 3. 명령어 실행
`image_verify {model} {number_of_tests} {ip_path}`
<br>

`image_acc {model} {number_of_tests} {ip_path}`
<br>

- *model* : "NW" 입력 (기관별로 입력값 달라질 수 있음)
- *number_of_tests* : 테스트 횟수 (현재 최대 10까지 가능)
- *ip_path* :  ip_path.txt 파일 위치
<br>

### 4. 자체 평가 테스트 명령어
`image_verify_test {model} {number_of_tests} {ip_path} {test_type}`
<br>

`image_acc_test {model} {number_of_tests} {ip_path}`
<br>

- 매일 아침 9시 30분에 이미지가 업데이트 됩니다.
- *model* : "neo", "tsn", "gcu" 입력 (기관별로 입력값 달라질 수 있음)
- *number_of_tests* : 테스트 횟수 (현재 최대 85까지 가능)
- *ip_path* :  ip_path.txt 파일 위치
- *test_type* : 0 : Random 1 : Same (기본값은 0 입니다.)
