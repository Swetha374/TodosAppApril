

from todosapp.models import users,todos
session={}

def login_required(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("you must login")
    return wrapper


def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password]
    return user

class LogInView():
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"] = user[0]
            print(username,"sucessfully logged in")

        else:
            print("invalid credentials")

class ListAllView():
    @login_required
    def get(self,*args,**kwargs):
        return todos
    #for creating todos
    @login_required
    def post(self,*args,**kwargs):
        userid=session["user"]["id"]
        kwargs["userId"]=userid
        todos.append(kwargs)
        print("todo added")
        print(todos)

#list all todos created by authenticated user
class MyTodosView:
    @login_required
    def get(self,*args,**kwargs):
        userid=session["user"]["id"]
        mytodos=[user for user in todos if user["userId"]==userid]
        print(mytodos)

class TodosView():
    @login_required
    def get_object(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo

    # view for fetching detail of a specific todo
    @login_required
    def get(self,*args,**kwargs):
        todoid=kwargs.get("todoid")
        todos=self.get_object(todoid)
        return todos

    # view for updating a specific todos
    @login_required
    def put(self,*args,**kwargs):
        todoid=kwargs.get("todoid")
        data=kwargs.get("data")
        value=self.get_object(todoid)
        if value:
            todo=value[0]
            todo.update(data)
            return todo

    # deleting
    @login_required
    def delete(self,*args,**kwargs):
        todoid=kwargs.get("todoid")
        value=self.get_object(todoid)
        if value:
            todo=value[0]
            todos.remove(todo)
            print("todo removed")
            print(len(todos))
#logout
@login_required
def logout(*args,**kwargs):
    user=session.pop("user")
    username=user["username"]
    print(f"user {username} has been loged out")





login=LogInView()
login.post(username="anu",password="Password@123")
listall=ListAllView()
print(listall.get())
listall.post(todoId=9,task_name="lbill",completed=False)
mytodos=MyTodosView()
mytodos.get()
todosall=TodosView()
print(todosall.get(todoid=5))

data={
    "task_name":"mobilebill"
}
print(todosall.put(todoid=5,data=data))

print(todosall.delete(todoid=8))

