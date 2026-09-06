from werkzeug.security import generate_password_hash
import secrets

print(secrets.token_hex(32))

password = input("Enter admin password: ")
print(generate_password_hash(password))