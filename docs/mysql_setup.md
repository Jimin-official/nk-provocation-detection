# MySQL Setup Guide
이 문서는 해당 프로젝트의 대시보드가
MySQL 데이터베이스(`att_db`)와 연동되도록 설정하는 과정을 설명합니다.

## 1. 루트 계정으로 MySQL 접속
```bash
mysql -u root -p
# 비밀번호 입력 (예: passwd)
```

## 2. 외부 접속 가능한 계정 생성 (first)
```sql
CREATE USER 'first'@'%' IDENTIFIED BY '1emddlwh';
GRANT ALL PRIVILEGES ON *.* TO 'first'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

## 3. MySQL Workbench 연결 설정
### 1) Workbench 실행 → Connections 옆의 + 버튼 클릭
### 2) 아래 정보 입력:
    - Connection Name: First Group
    - Username: first
    - Password: 저장 (Store in Vault → 1emddlwh 입력)
    - Advanced 탭 → Others 항목에 다음 옵션 추가:
        ```ini
        allowLoadLocalInfile=true
        ```
### 3) OK 클릭 후 연결 확인

## 4. 스키마 생성
```sql 
CREATE DATABASE att_db DEFAULT CHARACTER SET utf8;
```
## 5. 권한 부여
```sql
GRANT ALL PRIVILEGES ON att_db.* TO 'first'@'%';
FLUSH PRIVILEGES;
```

## 6. 새로 만든 계정으로 접속
```bash
# 터미널 재실행 후
mysql -u first -p
# 비밀번호: 1emddlwh
```

## 7. 스키마 선택
```sql
USE att_db;
```

## 8. 테이블 생성
```sql
CREATE TABLE provocation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100),
    date DATE,
    case_description TEXT,
    latitude FLOAT,
    longitude FLOAT,
    year INT,
    n_gov VARCHAR(100),
    s_gov VARCHAR(100)
);
```

## 9. CSV 업로드 설정
```bash
# 루트 계정으로 다시 접속
mysql -u root -p
```
```sql
SET GLOBAL local_infile = 1;
```

이제 새 터미널에서 `first`계정으로 다시 접속: 
```bash
mysql --local-infile=1 -u first -p att_db
```

## 10. CSV 데이터 불러오기
```sql
LOAD DATA LOCAL INFILE '/workspaces/Hanwha-Aerospace-DataAnalysis/nk-provocation-detection/data/provocation.csv'
INTO TABLE provocation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(type, date, case_description, latitude, longitude, year, n_gov, s_gov);
```
