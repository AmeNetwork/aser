from aser.agent import Agent
from aser.text2sql import Text2SQL,SQLiteConnector
agent = Agent(name="aser agent", description="aser agent",
              model="gpt-4.1-mini")
#You can custom Connector by inherit aser.text2sql DatabaseConnector class
db_connector = SQLiteConnector()
text2sql = Text2SQL(agent,db_connector,"data/database/users.db")
response=text2sql.chat("query all users")
print(response)

