test_string=str("2024-01-09 15:52:16,859 # � X -43 X 0Data reception started")

test_string=test_string.replace("Data","")
test_string=test_string.split(" ")
del test_string[2:5]
#del test_string[3]
#del test_string[4]
#del test_string[5]
#del test_string[5]

#test_string=test_string.split(" ")
#test_string=test_string[0:3]#,1,3,5,7]
print(test_string)
