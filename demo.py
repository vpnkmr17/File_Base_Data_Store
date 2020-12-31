
from data_store import FilesystemStore

#Create object of class FilesystemStore

#Provide filename or it will take the default filename(data.txt)
obj=FilesystemStore("new_data.txt")

#Create key-value pair
obj.create("dummy",{"x":1,"y":2})
obj.create("newdummy",{"x":2,"y":3})
obj.create("Color",{"sky":"Blue"},50) #Here the third value is time-to-live period
obj.create("newcolor",{"blood":"Red"},70)

#Read the values from data_store
val=obj.read("dummy")
print(val)
val=obj.read("dummyone") #output key is not present
print(val)
val=obj.read("Color")
print(val)

#Delte the key from data_store
obj.delete("newcolor")
obj.delete("dummy")
