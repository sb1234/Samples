import os
import redis
from dotenv import load_dotenv
    
load_dotenv()

def connectToRedis():
  return redis.Redis(
    host= os.getenv("REDIS_HOST"),
    port=10280,
    password=os.getenv("REDIS_PWD"))

def createSessionData(sessionID, customerID, fname, lname, pmtType, pmtAmount):
  message = 'User Session Data Created Successfully'
  try:
    redisConnection = connectToRedis()
    redisConnection.hset(sessionID, mapping={
        'customerId': customerID,
        "firstName": fname,
        "lastName": lname,
        "paymentType": pmtType,
        "paymentAmount": pmtAmount
      })
  except:
    message = 'Error Creating User Session Data'
  return message

def getSessionData(sessionID):
  message = ''
  try:
    redisConnection = connectToRedis()
    userData = redisConnection.hgetall(sessionID)

    customerName = ''
    paymentType = ''
    for key, value in userData.items():
      keyDecoded = key.decode("utf-8")

      if keyDecoded == 'firstName' or keyDecoded == 'lastName':
        customerName += value.decode("utf-8") + ' '
      elif keyDecoded == 'paymentType':
        paymentType += value.decode("utf-8")
    
    if(customerName == '' and paymentType == ''):
      message = 'Unable to find User Session Data'
    else:
      message = f"Customer {customerName} recently paid with {paymentType}"
  except:
    message = 'Error Retreiving User Session Data'  
  return message  


sessionIds = {
  'user-payment-session:12345',
  'user-payment-session:6789',
  'user-payment-session:92394'
}

for sessionId in sessionIds:
  results = getSessionData(sessionId)
  print(results)