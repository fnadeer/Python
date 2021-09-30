my_list = ['Hello','Whatever']
print(id(my_list))
new_list = my_list #This is not making a copy. Its just two references to the same memory
my_list.append('Something')
print(new_list)
print(my_list)
#Strings  and numbers are immutable
