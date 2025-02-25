from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("EVM_PRIVATE_KEY"))