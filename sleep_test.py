from util_tools.Read_Excle import read_excel


#写出0-9的数字中不同的组合，数字间不会重复
# 能重复，比如:10和01
list_sort = []
for i in range(10):
    for j in range(10):
        if i != j:
            list_sort.append(int(str(i)+str(j)))
print(list_sort)

for i in range(7):
    print("*" * i)