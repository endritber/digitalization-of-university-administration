# Digitalization of University Administration

DUA is a web-based solution which covers some aspects of universities. It is developed for conducting, monitoring & analyzing complex activities of the University and its affiliated colleges like Centralized Admission, Centralized Examination, and much more.
#
Server side tests:
```
docker-compose run app sh -c "python3 manage.py test"
```

Server side run web-server:
```
docker-compose up
```

Server side endpoints:
```
<b>localhost:8000/api/user/create</b> # administrator can add new user to the system such as prof and student
<b>localhost:8000/api/user/list</b> # list of students with their personal info, administrator, professors can see this
<b>localhost:8000/api/user/me</b> # profile with personal info of the currently logged in user such as administrator, student and proffesor
<b>localhost:8000/api/user/token</b> # login page, a token gets generated
<b>localhost:8000/api/update/<int:pk> </b> #only administrator can update personal info for their students
<b>localhost:8000/api/administratiom/progress</b> # proffesors can view students progress, administrator can add student progress info.
<b>localhost:8000/api/administration/grade/<int:pk></b> #professors can add student grade to transcript
<b>localhost:8000/api/administration/course</b> #professors can view courses
<b>localhost:8000/api/administration/course/<int:pk>/ #professors can view detailed course

more to come...

```
