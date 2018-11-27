from hashlib import md5


#a = 'admin'

b = md5('amine@123'.encode('utf-8')).hexdigest()

print(b)
