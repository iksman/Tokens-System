import uuid

# A simple system to create tokens in place of userId's
# These tokens can be used to prove identity
# allowing safe access to the database



class ReturnIntersceptor: #Used for easy reading of interactions between database and user
                          #To see what information is shared and seen between the simulated connection
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
                 "tokens":    #Here, the authorization tokens will be shared
                 []
                }

  def checkName(self,name):   #Name is checked for existence, then result plus the id is returned
    for item in self.data["users"]:
      if name == item["name"]:
        return [True,item["id"]]
    return [False,0]

  def generateToken(self,id): #A token is generated at random and then inserted into DB
                              #Token is then returned with result
    token = uuid.uuid4().hex
    self.data["tokens"] += [{"id" : id, "token": token}]
    return token

  def login(self,name):       #Combined sequence of searching userId and then making and returning token
    result = self.checkName(name)
    if result[0] == True:
      return [True, self.generateToken(result[1])]
    else:
      return [False, 0]

  def getData(self,token):    #Returns data for user with supplied token, if not found will return empty string
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
  text = input("Naam: ")                              #Log in with name
                                                      #If name is found in database, return true and token


  result =    i.interscept("DB", "User",              #Log return interaction of DB to User
              i.send("User", "DB", text, db.login))   #Log initial interaction of User to DB
  if result[0] == True:
    break
  else:
    print("Not found\n")
    i.log = []                                        #Clear Log

print(i.interscept("DB", "User", i.send("User", "DB", result[1],db.getData))) #Print data with token

i.prettyPrint()                                       #Print Log
#print()
#print(db.data)                                        #Print entire database again


