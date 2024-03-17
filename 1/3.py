zero = 0
x = input('Enter number: ')
num =int(x)
def factorial(num):
    if num <= 1:
        return 1
    else:
        return (num * factorial(num-1))
        
result = factorial(num)

result = str(result)
result = result[::-1]
for i in result :
    if i == "0":
        zero = zero+1
    else :
        break
print(zero)