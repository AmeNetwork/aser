from core.social.twitter import TwitterClient
client = TwitterClient()
# client.post("Hello World @aw_builder")
client.get_mentions()

# client.get_me()

# client.comment("1894645071603273792","thanks")