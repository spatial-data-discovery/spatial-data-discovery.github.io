import os 
import sys

for root, dirs, file in os.walk("."):
    for filename in file:
        num_col = 0
        num_row = 0
        dataset = list()
        discard = [0,1,2,3,4,5]
        if filename.endswith(".txt") or filename.endswith(".asc"):
            retrieveFile = os.path.join(root, filename)
            ouvrir = open(retrieveFile, "r")
            for line in ouvrir:
                if line != 0 and line != "\n":
                    line_data = line.split()
                    #print("line data:",line_data)
                    for char in line_data:
                        if char == " ":
                            line_data.remove(" ")
                    #print("cleaned line data:", line_data)
                    for i in range(len(line_data)):
                        if(line_data[i].isalpha()):
                            if(line_data[i].lower() == "ncols"):
                                num_col = int(line_data[i+1])
                                #print("Col ->",num_col)
                            if(line_data[i].lower()== "nrows"):
                                num_row = int(line_data[i+1])
                                #print("Row ->",num_row) 
                    dataset.append(line_data)
            dataset = dataset[6:len(dataset)+1]
            if(len(dataset) == num_row and len(dataset[0])== num_col):
                print(filename, "Has no problems, the number of stated rows and columns match that of the data values.")
            else:
                print(filename, "Has problems, the number of stated rows and columns don't match that of the data values. Kindly fix it.")

                    
