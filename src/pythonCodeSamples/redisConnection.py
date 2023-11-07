import json
import os
import redis
from dotenv import load_dotenv
    
load_dotenv()

def connectToRedis():
  return redis.Redis(
    host= os.getenv("REDIS_HOST"),
    port=10280,
    password=os.getenv("REDIS_PWD"))

def createSessionData(sessionId, customerID, fname, lname, pmtType, purchaseDesc, location):
  try:
    redisConnection = connectToRedis()
    redisConnection.hset(sessionId, mapping={
        'customerId': customerID,
        "firstName": fname,
        "lastName": lname,
        "paymentType": pmtType,
        "purchaseDesc": purchaseDesc,
        "location": location
      })
    return f"User Session Data Created Successfully for {sessionId}"
  except:
    return f"Error Creating User Session Data for {sessionId}"

def getSessionData(sessionId):
  message = ''
  try:
    redisConnection = connectToRedis()
    userData = redisConnection.hgetall(sessionId)
    
    if userData == {}:
      return f"Unable to find Session Data for {sessionId}"

    customerName, purchaseDesc, purchaseLocation = '', '', ''
    for key, value in userData.items():
      keyDecoded = key.decode("utf-8")

      if keyDecoded == 'firstName' or keyDecoded == 'lastName':
        customerName += value.decode("utf-8") + ' '
      elif keyDecoded == 'purchaseDesc':
        purchaseDesc += value.decode("utf-8")
      elif keyDecoded == 'location':
        purchaseLocation += value.decode("utf-8")
    
      message = f"Customer {customerName} recently bought a {purchaseDesc} within {purchaseLocation}"
  except:
    message = f"Error Retreiving User Session Data for {sessionId}"
  return message

def deleteSessionData(sessionId):
  try:
    redisConnection = connectToRedis()
    numDeletedSessions = redisConnection.delete(sessionId)

    if numDeletedSessions > 0:
      return f"Session data deleted successfully for {sessionId}"
    else:
      return f"There was no session data to delete for {sessionId}"
  except:
    return f"Error deleting session data for {sessionId}"


fileContents = open('userData.json')
sessionData = json.load(fileContents)

for sessionId in sessionData:
  createDataResults = createSessionData(sessionId,sessionData[sessionId]['customerId'],
                                        sessionData[sessionId]['firstName'],
                                        sessionData[sessionId]['lastName'],
                                        sessionData[sessionId]['paymentType'], 
                                        sessionData[sessionId]['productDesc'],
                                        sessionData[sessionId]['location'])
  sessionDataResults = getSessionData(sessionId)
  deleteDataResults = deleteSessionData(sessionId)
  print(createDataResults, sessionDataResults, deleteDataResults, sep='\n')
  print('\n')