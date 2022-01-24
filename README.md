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
localhost:8000/api/user/create # administrator can add new user to the system such as prof and student
localhost:8000/api/user/list # list of students with their personal info, administrator, professors can see this
localhost:8000/api/user/me # profile with personal info of the currently logged in user such as administrator, student and proffesor
localhost:8000/api/user/token # login page, a token gets generated
localhost:8000/api/update/<int:pk> #only administrator can update personal info for their students
localhost:8000/api/administratiom/progress # proffesors can view students progress, administrator can add student progress info.
localhost:8000/api/administration/grade/<int:pk> #professors can add student grade to transcript
localhost:8000/api/administration/course #professors can view courses
localhost:8000/api/administration/course/<int:pk>/ #professors can view detailed course

more to come...

```
