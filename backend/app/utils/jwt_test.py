from jwt import create_access_token, check_token_is_valid
import time

# Creating token valid for 2 sec
token = create_access_token({"sub": "user1"}, expires_minutes=0.033) # 2 sec
print("Generated token:", token)

#  validation (should be valid)
print ("Checking token immediately:")
check_token_is_valid(token)

# Wait for 3 sec to token expire
time.sleep(3)
print("Checking token after expiration")
check_token_is_valid(token)