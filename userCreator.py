# name (id) and (password)

class User:

    def __init__(self,name,password):
        if len(name) >= 2 :
            self.name = name
        else:
            print("The name is not appropriate")
        if len(password) > 5:
            self.password = password
        else:
            print("Password Must contain at least 5 characters")

    def user_login(self):
        self.id = input("Enter User name: ")
        self.password_in = input("Enter password: ")
        self.user_authentication()

    def user_authentication(self):
        if self.name == self.id and self.password_in == self.password:
            print("authenticated user")
        else:
            print("you are not authorized the service")
            self.user_login()

    def change_password(self):
        name = input("Enter your Id")
        password = input("Enter your old password")
        if name == self.name and password == self.password :
            self.password = input("enter a new password")
        else:
            self.change_password()

user1 = User("gyan","general")
user1.change_password()
user1.user_login()