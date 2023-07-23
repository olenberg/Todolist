## Todolist

---

### About

---

Todolist is a web application for working with goals.

1. Authentication
   - Django basic authentication
   - OAuth VK
2. Goals
   - basic CRUD with filters and sorting: boards, goals, categories, comments
   - user can view items related to the boards he's member of (owner, writer or reader)
   - user can create categories, goals, comments only if he's owner/writer of the related board
   - user can update, delete only if he's owner/writer of the related board
   - user can update, delete only his comments
   - when board, category is marked as is_deleted, all child categories, goals are also marked as is_deleted
3. TG bot
   - user need to verify identity using verification code
   - user could view and create goals
   - bot telegram username: @artur_olenberg_todo_bot


### Installation

---

```
$ git clone https://github.com/olenberg/todolist.git
```

### Requirements

- Python 3.10
- Pip
- Docker

---

## Usage

1. Go to the directory 'diploma'
2. Create abd activate venv
```
$ python3 -m venv venv
$ source venv/bin/activate
```
3. Install requirements
```
$ pip install -r requirements.txt
```
4. Create postgresql docker container
```
$ sudo docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```
5. Make migrations
```
$ ./manage.py makemigraitons
$ ./manage.py migrate
```
6. Run server
```
python3 manage.py runserver
```
7. Open http://127.0.0.1:8000/
