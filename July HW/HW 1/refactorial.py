def refactorial(n):
	"""This function finds the factorial of a user-provided integer.
	"""
	
	#Recursively compute the factorial of n
	m = 1
	for i in range(n):
		m = m * (i + 1)
	return m

#Take input for n
n = input('Provide a natural number: ')

#Convert the provided string to an integer
n = int(n)
	
#Print the computed value
print(refactorial(n))

input()