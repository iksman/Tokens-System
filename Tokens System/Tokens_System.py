import uuid

# A simple system to create tokens in place of userId's
# These tokens can be used to prove identity
# allowing safe access to the database



class ReturnIntersceptor:
  def __init__(self):
    self.log = []
  def interscept(self,senderName, sendeeName, data):
    self.log += [str(senderName + " -> '" + str(data) + "' -> " + sendeeName)]
    return data
  def send(self, senderName, sendeeName , data, method):
    self.log += [str(senderName + " -> '" + str(data) + "' -> " + sendeeName)]
    return method(data)

  def prettyPrint(self):
    itern = 0
    print()
    for item in self.log:
      itern += 1
      
      print(str(itern) + ". " + str(item))

class Database():
  def __init__(self):
    self.data = {"users": 
                  [
                    {"id": 1, "name": "Frank", "age": 15, "gender": "male"}, 
                    {"id": 2, "name": "Willem", "age": 20, "gender": "female"},
                    {"id": 3, "name": "Grizelda", "age": 21, "gender": "female"}
                  ],
                 "tokens":
                 []
                }

  def checkName(self,name):
    for item in self.data["users"]:
      if name == item["name"]:
        return [True,item["id"]]
    return [False,0]

  def generateToken(self,id):
    token = uuid.uuid4().hex
    self.data["tokens"] += [{"id" : id, "token": token}]
    return token

  def login(self,name):
    result = self.checkName(name)
    if result[0] == True:
      return [True, self.generateToken(result[1])]
    else:
      return [False, 0]

  def getData(self,token):
    id = 0
    for item in self.data["tokens"]:
      if item["token"] == token:
        id = item["id"]

    if id != 0:
      for item in self.data["users"]:
        if item["id"] == id:
          return item
    return "''"

i = ReturnIntersceptor()
db = Database()
print(db.data['users'])

while True:
  text = input("Naam: ")
  result = i.interscept("DB", "User", i.send("User", "DB", text, db.login))
  if result[0] == True:
    break
  else:
    print("Not found\n")
    i.log = []

print(i.interscept("DB", "User", i.send("User", "DB", result[1],db.getData)))

i.prettyPrint()
print()
print(db.data)


