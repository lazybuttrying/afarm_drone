from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.url = "https://better-rat-41.hasura.app/v1/graphql"
        self.headers = {
            'x-hasura-admin-secret': os.environ.get("HASURA_KEY"),
            'Content-Type': 'application/json'
        }

    def getUser(self, userid):
        query = ["{\"query\":\"query getUser {\\n                      afarm_user(where: {user_id: {_eq: \\\"",
            userid,
            "\\\"}}) {\\n                          pw\\n                      }\\n                  }\",\"variables\":{}}"
        ]
        return "".join(query)

    def getDrone(self, userid):
        query=["{\"query\":\"query getDrones {\\n                      afarm_user(where: {user_id: {_eq: \\\"",
            userid,
            "\\\"}}) {\\n                          drones {\\n product_name\\n                              start_time\\n                              id\\n                          }\\n                      }\\n                  }\",\"variables\":{}}"]
        return "".join(query)

    def getFlight(self, userid):
        query = ["{\"query\":\"query MyQuery {\\n  afarm_drone(where: {user_id: {_eq: \\\"",
            userid,
            "\\\"}}) {\\n    flight {\\n      init_x\\n      init_y\\n      width\\n      height\\n      interval\\n      sight_range\\n      grape_height\\n    }\\n    id\\n    zone\\n    product_name\\n    start_time\\n  }\\n}\\n\",\"variables\":{}}"]
        return "".join(query)
    
    def getFlightOne(self, droneid):
        query =["{\"query\":\"query MyQuery2 {\\n  afarm_drone_by_pk(id: ",
            str(droneid),
            "{\\n    start_time\\n    flight {\\n      init_x\\n      init_y\\n      width\\n      height\\n      interval\\n      sight_range\\n      grape_height\\n    }\\n  }\\n}\\n\",\"variables\":{}}"]
        return "".join(query)
        
    def sendQuality(self, droneid, userid, date):
        query = ["{\"query\":\"  mutation MyMutation {\\n    insert_afarm_quality_one(object: {drone_id: ",
            str(droneid),  ", user_id: \\\"",
            str(userid), "\\\", date: \\\"",
            str(date), "\\\"}) {\\n      id\\n    }\\n  }\\n\",\"variables\":{}}" ]
        return "".join(query)
