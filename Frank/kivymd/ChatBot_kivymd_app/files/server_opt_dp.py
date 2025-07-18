
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConfigurationError
import random


# serverSelectionTimeoutMS=5000
uri = "mongodb+srv://Frankkwizigira:J4W3K3q997jUlOsv@grimecluster0.py6uoj0.mongodb.net/?retryWrites=true&w=majority&appName=grimeCluster0"
cluster = MongoClient(uri,serverSelectionTimeoutMS=5000,server_api=ServerApi('1'))
try:
    cluster.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except ConfigurationError:
    print("Yess we got the mf")
except Exception as e:
    print(e)

db = cluster["grime_server"]
collection= db["user_chats_and_profile"]


def add_user_sign_in_data(username:str,full_name:str,email:str,gender:str,password:str):
    client_id_number = random.randint(6000090,90000000)
    save_success=False
    user_data = {"username":username,
                 "client_name":full_name ,
                 "client_id":client_id_number,
                 "email":email,
                 "gender":gender,
                 "password": password,
                 "converstion":[]
                 }
    try:
      collection.update_one({"_id":100},{"$push":{"core.user":user_data}})
      save_success = True
      print('data added success')
    except Exception as err:
       print(err)

    return save_success


def check_user_login(username:str,password:str):
    data_to_find = {"username":username,'password':password}
    DataFound = False
    doc = collection.find_one({"core.user":{"$elemMatch":data_to_find}})
    if doc:
        DataFound = True
        print("\n\n Found \n\n")
    else:
        DataFound = False
        print("\n\n not Found \n\n")
    return DataFound


def check_if_exist(username:str):
    data = {"username":username}
    it_true = False
    doc = collection.find_one({"core.user":{"$elemMatch":data}})

    if doc:
      it_true = True
      print('\nFound\n')
    else:
       print(f"\n not found \n")

    return it_true

def get_user_id_num(username:str):
    data_to_find ={"username":username}
    doc = collection.find_one({"core.user":{"$elemMatch":data_to_find}},{"core.user.$":1,"_id":0})
    v = None
    if doc:
     v = doc["core"]["user"][0]['client_id']
    else:
        print("no found")

    return v

class Load_user_data:
    def __init__(self,username:str,user_id:int):
           self.data = {"username":username,"client_id":user_id}

    def get_user_name(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        value = ""
        try:
            if doc:
                value = doc["core"]["user"][0]["client_name"]

        except Exception as e:
            value = "connection error"

        return value
    def get_user_email(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        value = ""
        try:
            if doc:
                value = doc["core"]["user"][0]["email"]
        except Exception as e:
            value = "connection error"

        return value

    def get_user_username(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        value = ""
        try:
            if doc:
                value = doc["core"]["user"][0]["username"]
        except Exception as e:
            value = "connection error"

        return value

    def get_user_conversation(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        v = None
        try:
            if doc:
                v = doc["core"]["user"][0]["converstion"]

        except Exception as e:
            value = "connection error"

        return  v

    def get_chat_length(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        value = None
        try:
            if doc:
                v = doc["core"]["user"][0]["converstion"]
                if len(v) >= 1:
                    value = True
                else:
                    value = False
        except Exception as err:
           print(err)
        return value

    def get_user_id(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        value = None
        try:
            if doc:
                value = doc["core"]["user"][0]["client_id"]
                print(value)
        except Exception as e:
            value = "connection error"

        return value

    def save_client_chat(self,chat:dict):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        try:
            if doc:
                v = doc["core"]["user"][0]["username"]
                collection.update_one({"core.user.username":v},{"$push":{"core.user.$.converstion":chat}})
                print("Data added")
        except Exception as err:
            print(err)
        return chat


    def delete_user_conversation(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        try:
            if doc:
                v = doc["core"]["user"][0]["username"]
                # vx = doc["core"]["user"][0]["converstion"]
                collection.update_one({"core.user.username":v},{"$pull":{"core.user.$.converstion":{}}})
                print("\n \n Data found\n \n")
            else:
                print("not foud")
        except Exception as err:
            print(f"error:{err}")

    def delete_account(self):
        doc = collection.find_one({"core.user":{"$elemMatch":self.data}},{"core.user.$":1,"_id":0})
        try:
            if doc:
              v = doc["core"]["user"][0]["username"]
              idd = doc["core"]["user"][0]["client_id"]
              collection.update_one({"core.user.username":v},{"$pull":{"core.user":{"username":v,"client_id":idd}}})
              print("deleted")
            else:
                print("it aint right")
        except Exception as err:
            print(err)

    def get_login_info(self,username:str,password:str):
        doc = collection.find_one({"core.user":{"$elemMatch":{'username':username,'password':password}}},{"core.user.$":1,"_id":0})
        value = False
        try:
            if doc:
                print("\n\n\nFOUND\n\n\n")
                value = True
            else:
                print("\n\n\n\nNOT FOUND\n\n\n")
        except Exception as e:
           print(e)


# p = Load_user_data("kita200@",25735868).get_user_conversation()
# print(p)

# print(*map(lambda d: d["Question"],p))
# print("\n")
# print(*map(lambda d: d["Reply"],p))
# print("\n")
# print(*map(lambda d: d["Time"],p))
# c = (*map(lambda d: d["Time"],p),)
# print(type(c))