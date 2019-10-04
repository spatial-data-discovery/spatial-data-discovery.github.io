import os

def check_asc_format(f):
    #store the content in the file in a list
    f = open(f,'r')
    line_counter = 0
    content = [];
    for line in f:
        #skip empty lines
        if line != '':
            line_content = line.split(' ')
            #clean up the line
            line_content[-1] = line_content[-1].rstrip("\n")
            for i in line_content:
                if i == '' or i == ' ':
                    line_content.remove(i)
            #add the line to a list of lines
            content.append(line_content)
            line_counter += 1

    #record the number of rows and the number of column header values
    col_total = int(content[0][1])
    row_total = int(content[1][1])

    #track if there is any issue with the formating.
    #set to False if any problems occurs.
    no_error = True
    #check if the number of entries in each row matches the number of column header value
    for i in range(6,len(content)):
        if len(content[i]) != col_total:
           print('The number of entries in line '+ str(i+1) + ' in the dataset is ' \
           + str(len(content[i])) + '. It does not match the header value.')
           no_error = False
        #check if the entries are numeric
        for num in content[i]:
            if not num.isnumeric():
                print("Found value '" + num + "' not numeric in line " + str(i+1))
                no_error = False

    #check if the number of rows is correct
    if len(content)-6 != row_total:
        print('The number of rows in the dataset does not match the header value.'\
        'The number of rows in the dataset is ' + str(len(content)-6) + '.')
        no_error = False

    #if no problem detected, tell the user the format is correct
    if no_error == True:
        print('The format of the dataset matches the header values.')

if __name__ == '__main__':
    #open the file
    folder_path = input('Enter the path of your directory:')
    for f in os.listdir(folder_path):
        if f.endswith('.txt'):
            print(f)
            check_asc_format(f)