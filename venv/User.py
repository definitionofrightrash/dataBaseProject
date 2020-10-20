class User:
    def __init__(self,id,name,email,land,hashed_password,image_reference):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.image_reference = image_reference
        self.id = id
        self.land = land