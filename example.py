from retroachievements import RAClient

username = input("Your username on RetroAchievements: ")
api_key = input("Your web API key: ")

auth = RAClient(username, api_key)

user_profile = auth.get_user_profile("dudmacedo")

print(user_profile)
