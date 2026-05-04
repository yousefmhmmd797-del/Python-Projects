#a = 47
#print(type(a)) 
#_____________________

#a = 70
#b = 3.14
#c = 'France'

#print(f'a is:', type(a) , 'b is: ', type(b) , 'c is: ' , type(c))
#___________________________________________________________________________

#je_suis_franscais = True
#print("tu est franscais?" , je_suis_franscais)
#__________________________________________________________________________

#fav_color = input("Enter your favourite color: ")
#print("You favourite color is" , fav_color)

#__________________________________________________________________________
  
#age = int(input("Waht's your age?"))
#print("Your age is: " , age) 

#__________________________________________________________________________

#age = int(input("Age: "))
#if age >= 17:
 #   print("Welcome to the Scintefic Ameture society of Natural Sciences")
#else:
#    print("sorry, your age doesn't match the age standards we are sitting. We are excited waiting for you")

#GPA = float(input("Your GPA: "))
#if GPA >= 3:
#    print("Welcome to Campus france scholarships")
#elif GPA <= 2.9:
#    print("your" , GPA , "requires an addition enhancement")
#elif GPA <= 2:
#    print("You are not eligible for effil schlarsips for this year, wish you a good luck")

#_____________________________________________________________________________________________

#for i in range(9):
   # print(i , "is eligible!")
   # if i == 3:
   #     break
   # print(i)

#count = 1
#while count <= 7:
#    print("count is: " , count)
#    count += 1


#Password = " "
#while Password != "enter123":
 #   Password = input("Enter your Password: ")
#print("Access granted!")    

#_______________________________________________

#cars = ["mercedis" , "BMW" , "Maclaryn" , "Ferarri" , "Redpull" , "Ford"]
#cars[0] = "Honday"                     # for modification
#print(cars[0])       
#cars.append("Audi")                    # to add at end 
#cars.insert(2, "Mustang")              # to add in a specific possition 'index'
#cars.remove("Ford")                    # to remove by value 
#cars.pop(4)                            # to remove by index 
#print(cars) 

#___________________________________________________

x = 10
y = 3

#print(x+y)                         #addition
#print(x-y)                         #subtraction
#print(x * y)                       #multiblication 
#print(x / y)                       #division 
#print(x // y)                      #floor division 
#print(x % y)                       #modulus (reminder)
#print(x ** y)                      #exponentiaion 

#print(max(3, 8, 9))
#print(min(3, 8, 9))
#print(round(3.75))
#print(pow(2,4))
#print(abs(-7))

import math

#print(math.sqrt(25))                 #for square root
#print(math.floor(3.9))               # floor 
#print(math.ceil(9.1))                # ceil
#print(math.pi)

#val1 = int(input("Enter a number: "))
#val2 = int(input("Enter another number: "))
#bigger = max(val1 , val2)
#smaller = min(val1 , val2)
#sum = val1 + val2 
#sub = bigger - smaller 
#product = val1 * val2
#Quotient = bigger / smaller 
#print("the summition = " , sum)
#print("the subtraction = " , sub)
#print("the product = " , product)
#print("the Quotient = " , Quotient)

#________________________________________________

'''

name = input("Enter your name: ")
num_courses = int(input("How many courses do you have? "))

grades = []
for i in range(num_courses):
    grade = float(input(f"Enter grade for course {i+1}: "))
    grades.append(grade)
    Avrage = sum(grades) / num_courses

print("... report for" , name , "grades ..." )
print("Grades: " , grades)
print("Avrage = " , Avrage )
print("The hifger grade = " , max(grades))
print("the lowest grade = " , min(grades))

if Avrage >= 50: 
      print("Statue: Pass!")
else: 
   print("Statue: Fail!")    

'''   

#___________________________________________________

""""

items_num = int(input("How mant items you wanna buy? "))

items = []
prices = [] 

for i in range(items_num):
    item_name = input(f"enter the item {i+1} name: ")
    item_price = float(input(f"Enter the item {i+1} price: "))

    items.append(item_name)
    prices.append(item_price)

print("\n--- Shopping Summary ---")
print("Items:", items)
print("Prices:", prices)    
total = sum(prices)
Average = total / items_num
print(items)
print(prices)
print("Total: " , total)
print("The most expensive item: " , max(prices))
print("The cheapest item: " , min(prices))

"""

#_________________________________________________

"""
Essay = input("Enter your essay: ")
words = Essay.split()
count = len(words)

print("the number of words = " , count , "words.")

"""

#___________________________________________________



student = {"name": "Dann" , "Age": 22 , "Grade": "A+"}

#print(student["name"])
#print(student["Age"])
#print(student["Grade"])
#print(student.get("Grade"))
#print("Age" in student) 


#student["Grade"] = "A"
#student.update({"Age": 29})
#print(student)

""""
Grades = {"Michel": 88 , "Jonas": 99 , "Adam": 1} 
for name, score in Grades.items():
    print(name , "got" , score)

highest = max(Grades.values())
A_Student = max(Grades , key=Grades.get)
print("The a student is " , A_Student , "with excact " , highest , "marks")    

"""

#_______________________________________________________________________

'''

#cars = {"Benz" , "BMW" , "Audi" , "ford" , "Nissan"}
#cars.add("Fiat")
#cars.discard("Benz") 
#print(cars)  

x = {1, 2, 3, 4}
y = {3, 4, 5, 6}

#print(x.issubset(y))
#print(y.issuperset(x)) 
#print(x ^ y) 

print("Union: " , x | y)
print("Intersection: " , x & y)
print("Difference; " , x - y)
print(len(x))
print(3 in x)

'''

'''

countries = {
    "Egypt": 104_000_000,
    "France": 67_000_000,
    "Japan": 126_000_000
}
print("Number of items:", len(countries))
print("Countries:", countries.keys())
print("Populatios:", countries.values())
print("The greater populations:", max(countries.values()))

'''

grades = {"Ali": 80, "Ahmed": 98, "Rabee3": 42}
best_student = max(grades, key=grades.get)
print("the top student: ", best_student, "with", grades[best_student])

worest_student = min(grades, key=grades.get)
print("The lowest Student: ", worest_student , "with" , grades[worest_student]) 

average = sum(grades.values()) / len(grades)
print("The average is:" , average)

print("_______________________________________________________________________________")

me = {"English" , "Arabic" , "French"} 
Ghada = {"English" , "Arabic" , "Korean"}

print("Common languages: " , me & Ghada) 
print("my laanguages only: " , me - Ghada)
print("All Unique Languages: " , me | Ghada) 