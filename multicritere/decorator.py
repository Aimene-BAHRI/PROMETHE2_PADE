"""
Author Oussama FORTAS
"""
print("PROMETHEE 2 METHOD")
print("#######################################################")

print("We will be using AHP : Analytic Hierarchy Process.")

import csv
import numpy as np

Matrix = np.array(list(csv.reader(open("MP.csv", "r"), delimiter=",")))
print(Matrix)
#to print matrix in a good format 
#len(matix) gives us the number of rows


# Step1 Normalize the evaluation matrix (Decision Matrix)
print("STEP 1 : Normalize the Evaluation Matrix")
# make the matrix as array to facilitate the Loop function
array_Matrix  = np.array(Matrix)
# Delete first ligne and column and keep only the float variables
Alternative_matix = array_Matrix[1:,1:].astype(np.float)
print('Alternative_matix \n',Alternative_matix)
# Save the Labels of the Ligne we deleted (we will need it later)
labels = array_Matrix[0,1:]
print('labels \n',labels)
# Save the Names of the Column we deleted (we will need it later)
Alternatives = array_Matrix[1:,0]
print('Names \n',Alternatives)
# Get min and max for each criteria
min_criteria_array = Alternative_matix.min(axis=0)
max_criteria_array = Alternative_matix.max(axis=0)
print(min_criteria_array)
print(max_criteria_array)

# Calculate the new matrix with beneficial non beneficial criteria:
# Beneficial Criteria == 1(python nebdou mel 0)
# NON ben Criteria == 2,3,4(python == 1,2,3)
for i in range(len(Alternative_matix)):
    for j in range(len(Alternative_matix[i])):
        if j == 0:
            Alternative_matix[i][j] = (max_criteria_array[j]-Alternative_matix[i][j])/(max_criteria_array[j]-min_criteria_array[j])
        else:
            Alternative_matix[i][j] = (Alternative_matix[i][j]-min_criteria_array[j])/(max_criteria_array[j]-min_criteria_array[j])

print(Alternative_matix)

print("STEP 2 : Calculate Evaluative ieme per the othere {m1-m2 | m1-m3 | ....}")
# Create the Alternatives Possibilities array[m1-m2,........]
def all_alternatives(Alternatives):
    Alternative_possibilities = []
    for i in range(len(Alternatives)):
        for j in range(len(Alternatives)):
            if i != j:
                Alternative_possibilities.append(Alternatives[i]+'-'+Alternatives[j])
            else:
                pass
    return np.array(Alternative_possibilities).reshape(len(Alternative_possibilities),1)
Alternative_possibilities = all_alternatives(Alternatives)
print('Alternative_possibilities \n', Alternative_possibilities)

# create the matrix of all variables possibilities:
def all_variables(matrix):
    new_matrix = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i != j:
                new_matrix.append(matrix[i]-matrix[j])
            else:
                pass
    return np.array(new_matrix).reshape(len(matrix)*(len(matrix)-1),len(matrix))

variables_possibilities = all_variables(Alternative_matix)
print('variables_possibilities \n', variables_possibilities)

# concatenate the Names and variables related 
the_all_matrix = np.hstack([Alternative_possibilities, variables_possibilities])
print('The All Matrix \n', the_all_matrix)

print("STEP 3 : Calculate the PREFERENCE Function")
# Create an updated matrix that return 0 if value is negative or equal to 0 
# else keep value as it it
def changetozeros(matrix):
    for i in range(len(matrix)) :  
        for j in range(len(matrix[i])) :  
            if matrix[i][j] <= 0 :
                matrix[i][j] = 0
    return matrix

Preference_matrix = changetozeros(variables_possibilities)
print('PREFERENCE_matrix \n', Preference_matrix)

# concatenate the Names and preferences related 
the_Preference_matrix = np.hstack([Alternative_possibilities, Preference_matrix])
print('the_Preference_matrix \n', the_Preference_matrix)

# calculate the aggregated preferenbce function
# hna nedourbou f les poids(weights)
# lets call the weights from a csv file
print("STEP 4 : Multyplie the PREFERENCE Function by Weights")

weights =list(csv.reader(open("weights.csv", "r"), delimiter=","))
print('weights \n', weights)
array_weights = np.asarray(weights[0], dtype='float64')
print('array_weights \n', array_weights)

# lets create a fucntion to mult the weights with the matrix of preferences variables
def mult_matrix_vect(matrix, weight):
    data = np.dot(matrix, weight.transpose())
    return data
# TODO: Check this multyplie function
# def show_mult_matrix_vect(matrix, weight):
#     data = []
#     for i in range(len(matrix)) :  
#         for j in range(len(matrix[i])) : 
#             data.append('{}*{}'.format(weight[j],matrix[i][j]))
#     return np.array(data)

Agregate_preference_matrix = mult_matrix_vect(Preference_matrix,array_weights)

print('Agregate_preference_matrix \n', Agregate_preference_matrix)

# lets add a column to sum these aggregated preferences
def add_aggregated_preferences_line(matrix):
    average_line_weight = []
    
    for i in range(len(matrix)) :
        sum = 0  
        for j in range(len(matrix[i])) :
            sum = sum + matrix[i][j] 
        average_line_weight.append(sum)
        
    matrix = np.vstack([matrix.transpose(), average_line_weight]).transpose()
    return matrix

Agregate_preference_matrix_with_sum = add_aggregated_preferences_line(Agregate_preference_matrix)
print('Agregate_preference_matrix_with_sum \n', Agregate_preference_matrix_with_sum)

# take only the aggragated sum values(LAST column) and create aggregated preference Function
def create_aggregated_matrix(matrix):
    # retrieve only the aggregated column(list)
    aggregated_matrix = np.zeros((len(Alternatives), len(Alternatives)))
    aggregate_column = np.array(matrix[:, -1].transpose()).tolist()
    print('aggregate_column type', type(aggregate_column))
    print(aggregate_column)
    
    for i in range(len(aggregated_matrix)) :  
        for j in range(len(aggregated_matrix[i])) :             
            if i == j:
                aggregated_matrix[i][j] = 0
            else:  
                aggregated_matrix[i][j]= aggregate_column[0]
                aggregate_column.pop(0) 
                
    return aggregated_matrix


print("len alternatives length\n", len(Alternatives))

aggregated_matrix = create_aggregated_matrix(Agregate_preference_matrix_with_sum)
print("aggregated_matrix\n", aggregated_matrix)

print("STEP 5 : Determine leaving and entering outracking flows")

sumrows = np.sum(aggregated_matrix, axis = 1)
print('sum rows \n', sumrows/(len(Alternatives)-1))

aggregated_matrix_function = np.vstack([aggregated_matrix.transpose(), sumrows/(len(Alternatives)-1)]).transpose()
print('aggregated_matrix_function \n', aggregated_matrix_function)

sumcolumns = np.sum(aggregated_matrix_function, axis = 0)
print('sum columns \n', sumcolumns)

aggregated_matrix_function = np.vstack((aggregated_matrix_function, sumcolumns/(len(Alternatives)-1)))
print('aggregated_matrix_function \n', aggregated_matrix_function)

print("STEP 6 : Determine Net flow")
aggregated_matrix_last_data = np.subtract(aggregated_matrix_function[:,-1], aggregated_matrix_function[-1,:])
print('aggregated_matrix_last_data\n', aggregated_matrix_last_data)







# sorted_aggregated__data = -np.sort(- aggregated_matrix_last_data)
# print('sorted_aggregated__data\n', sorted_aggregated__data)

# final_sorted_result = np.vstack([Alternatives, aggregated_matrix.transpose() ])
# print('final_sorted_result\n', final_sorted_result)

