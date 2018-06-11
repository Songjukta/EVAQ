import csv
import matplotlib.pyplot as plt
import seaborn as sns

M = 20

environment_summary = [[0 for i in xrange(M)] for j in xrange(M)]

data_file = open('Environment_States.csv')
csv_data = csv.reader(data_file)

for i, row in enumerate(csv_data):
    for j, val in enumerate(row):
        #print i, j, i%20
        if int(val) >= 5:
            environment_summary[(i%20)][j] += 1

print environment_summary
sns.heatmap(environment_summary, annot = True)
#plt.imshow(environment_summary, cmap='plasma', interpolation='nearest')
plt.savefig('Heatmap.png')
            
        
        
