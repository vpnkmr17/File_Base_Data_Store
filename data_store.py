
import ast
import json
import sys 
import os
import time
import portalocker



class FilesystemStore:
	def __init__(self,filename="data.txt"):
		self.filename=filename
		self.data={}
		if os.path.exists(self.filename)==False:
			with open(self.filename,'w+') as fp:
				fp.write(str(self.data))


	

	def _get_size(self,obj, seen=None):
	    """Recursively finds size of objects"""
	    size = sys.getsizeof(obj)
	    if seen is None:
	        seen = set()
	    obj_id = id(obj)
	    if obj_id in seen:
	        return 0
	    # Important mark as seen *before* entering recursion to gracefully handle
	    # self-referential objects
	    seen.add(obj_id)
	    if isinstance(obj, dict):
	        size += sum([self._get_size(v, seen) for v in obj.values()])
	        size += sum([self._get_size(k, seen) for k in obj.keys()])
	    elif hasattr(obj, '__dict__'):
	        size += self._get_size(obj.__dict__, seen)
	    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
	        size += sum([self._get_size(i, seen) for i in obj])
	    return size						

	

	#Key checking if it is present or not
	def _check_key(self,key):
		with open(self.filename,'r') as fp:
			temp=fp.read()
			self.data=ast.literal_eval(temp)
			if key not in self.data:
				return False
			return True

	#Update the data
	def _update(self,key,action,value=None,ttl=0):
		with open(self.filename,'r') as rp:
			temp=rp.read()
			self.data=ast.literal_eval(temp)
		if action=="create":
			value_as_json=json.dumps(value)

			if ttl!=0:
				self.data[key]=[value_as_json,time.time()+ttl]
			else:
				self.data[key]=[value_as_json,0]

			if self._get_size(self.data)>(1024*1024*1024) or self._get_size(value_as_json)>16384:
				print("Sorry,Memory is Full!!")
				exit(1)

		elif action=="delete":
			del self.data[key]
		with open(self.filename,"w") as fp:
			fp.write(str(self.data))



	#Create key-value pair 
	def create(self,key=None,value=None,ttl=0):
		#checking if key is empty or value is empty
		if key==None or value==None:
			print("Please enter valid key or value")
			return
		#Checking if key is other than alphabetical character
		#and if len(key) is greater than the given length(32)
		if key.isalpha()==False or len(key)>32 or len(key)==0:
			print("Please Enter a Valid Key")
			return
		#Checking if key is already present or not
		if self._check_key(key):
			print("Key is already present!!")
			return

		#if everything is valid then we will create a key-value pair
		#by calling internal method _update()
		self._update(key,"create",value,ttl)

	#Read data from the data store
	def read(self,key=None):
		#Checking if key is valid or not
		if key==None or key.isalpha()==False:
			print("Enter a valid key")
		#Checking if key is already present or not
		val=self._check_key(key)
		#if already present then we will simply return the below message
		if val==False:
			return("Key is not present!!")
		#Else we would return the value of that key
		else:
			with open(self.filename,"r") as fp:
				temp=fp.read()
				self.data=ast.literal_eval(temp)
				val=self.data[key][0]
				if self.data[key][1]!=0:
					#Checking if the time-to-live period is over or not
					if time.time()>self.data[key][1]:
						#here time-to-live period of key is over
						#So we will delete that key
						self._update(key,action="delete")
						return "This key is no longer present because its time-to-live period is over!"
				return json.loads(val)


	#Delete the key from the data store
	def delete(self,key):
		#Checking if key is valid or not
		if key==None or key.isalpha()==False:
			print("Enter valid key!")
		#Checking if key is present or not
		val=self._check_key(key)
		if val==False:
			print("Key is not present!!")
		else:
			self._update(key,action="delete")
			print("Deleted successfully!")
	
