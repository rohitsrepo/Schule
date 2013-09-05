import string
from random import choice

def GenVigKey():
  '''Generates Vigilance key for a user.'''
  chars = string.letters + string.digits
  newpasswd =''
  for i in range(8):
    newpasswd = newpasswd+choice(chars)
  return newpasswd
