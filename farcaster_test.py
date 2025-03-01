# import os
# from farcaster import Warpcast
# from dotenv import load_dotenv # can be installed with `pip install python-dotenv`

# load_dotenv()

# mnemonic=os.getenv("FARCASTER_MNEMONIC")
# client = Warpcast(mnemonic=mnemonic)

# print(client.get_me().fid)
# result=client.get_casts(fid=374889)
# print(result)


from core.social.farcaster import FarcasterClient
client = FarcasterClient()
result=client.get_mentions()
print(result)

# client.comment(374889,"0x4c9a4943ba502167c341fb162e14a0108bdfc69e","test again")
# client.get_cast("0x4c9a4943ba502167c341fb162e14a0108bdfc69e")

# client.post("test again111")