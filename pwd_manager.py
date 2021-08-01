from cryptography.fernet import Fernet
import pickle

class PasswordManager:

    def __init__(self,pwd,id,msg):

        self.id = id
        self.password = pwd
        self.msg = msg
        cred = self.create_binary(self.id,self.password,self.msg)
        self.encrypt(cred[0],cred[1],cred[2])



    def create_binary(self,in_id,in_pwd,in_msg):

        b_id = in_id.encode('ascii')
        b_pwd =in_pwd.encode('ascii')
        b_msg = in_msg.encode('ascii')

        return b_id,b_pwd,b_msg

    def encrypt(self,b_in_id,b_in_pwd,b_in_msg):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        ciphered_id = cipher_suite.encrypt(b_in_id)
        ciphered_pwd = cipher_suite.encrypt(b_in_pwd)
        ciphered_msg = cipher_suite.encrypt(b_in_msg)

        data = {
            "key": key,
            "id": ciphered_id,
            "pwd": ciphered_pwd,
            "msg": ciphered_msg
        }

        with open("./bin/usage.bin","ab+") as file:

            pickle.dump(data,file,pickle.HIGHEST_PROTOCOL)
            file.seek(0)


    def decrypt(self):
        pass
        # with open("./bin/usage.bin","rb") as file:
        #     data = pickle.load(file)
        # print(data)
        # for entry in data:
        #     print(entry)
            # cipher_suite = Fernet(entry['key'])
            # id = cipher_suite.decrypt(entry['id'])
            # pwd = cipher_suite.decrypt(entry['pwd'])
            # msg = cipher_suite.decrypt(entry['msg'])
            #
            # print(id,pwd,msg)



