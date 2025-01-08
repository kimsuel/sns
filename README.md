# F-lab 프로젝트 - sns

---

### Version
Python : 3.11 <br>
Django : 5.1.4 <br>
Postgresql (psycopg2-binary) : 2.9.10


---
### 기술 스택 선택 이유
1. PostgreSQL vs MySQL
    - PostgreSQL
      - Django에서 PostgreSQL를 위한 많은 기능을 제공
      - Django 공식문서에서도 PostgreSQL에 대한 좋은 평가를 볼 수 있음 <br>
        -> PostgreSQL은 스키마 지원 측면에서 모든 데이터베이스 중에 가장 유능하다. <br>
           (https://docs.djangoproject.com/en/4.2/topics/migrations/#postgresql)
      - Django는 PostgreSQL에서만 작동하는 다양한 데이터 유형을 제공
    - MySQL
      - Django에서 PostgreSQL 만큼의 기능을 제공하지 않음
      - Django 공식문서에서 MySQL에 대한 평가는 부정적 <br>
        -> MySQL은 스키마 변경 작업과 관련된 트랜잭션에 대한 지원이 부족하다. <br>
           (https://docs.djangoproject.com/en/4.2/topics/migrations/#mysql)
    - 이런 이유로 PostgreSQL을 선택
2. secrets.json vs django-environ
   - secrets.json
     - 민감한 정보를 JSON 파일로 관리하는 방법
     - 장점
       - 추가 라이브러리가 필요 없음
       - JSON 포맷은 읽기 쉽고 직관적
     - 단점
       - 파일이 git에 커밋되거나 유출될 가능성이 있어 정보가 노출될 수 있음
       - 환경마다 다른 설정을 적용하려면 여러 JSON 파일을 관리해야함
       - 파일 기반 설정은 Docker나 Kubernetes와 같은 컨테이너 환경에 비효율적
   - django-environ
     - 환경 변수를 기반으로 설정을 관리하도록 돕는 라이브러리
       - 장점
         - 운영 환경(<ex> Docker, Kubernetes)에서 환경 변수는 표준적인 방법. 배포환경에 적합
         - .env 파일로 로컬 개발 환경에서도 간편하게 사용 가능
         - 환경 변수는 운영체제 수준에서 관리되므로 git에 커밋될 일이 없음
         - 개발, 테스트, 운영 환경에 따라 쉽게 설정을 변경할 수 있음
       - 단점
         - 환경 변수 기반 설정에 익숙하지 않은 경우 초기 학습 필요
         - 잘못된 환경 변수 설정은 디버깅이 어려움
         - 추가 라이브러리 필요
   - 개인 프로젝트이므로 secrets.json도 충분하지만 확장성을 위해 django-environ 사용