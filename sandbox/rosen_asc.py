import os

extensions = [".txt", ".asc", ""]

# https://www.101computing.net/python-reading-a-text-file/
def check_file(input_path, fname):
    col_num = 0
    row_num = 0
    col_count = 0
    row_count = 0
    checking = open(os.path.join(input_path, fname),"r")
    row_count = 0
    st_line = ""
    for lines in checking:
        #st_line = checking.readline()
        st_line = lines.split()
        #print("first line entry:", st_line[0])
        if (st_line)[0].upper() == "NCOLS":
            col_num = st_line[1]
            #print("col num", col_num)
        elif (st_line)[0].upper() == "NROWS":
            row_num = st_line[1]
            #print("row num", row_num)
        elif str(st_line[0]).isdigit():
            col_count = len(st_line)
            #print("col count", col_count)
            if int(col_count) != int(col_num):
                print("Wrong number of columns in '%s'" % fname)
            '''elif (int(col_count) == int(col_num)):
                print("Correct number of columns")'''
            row_count += 1
    if int(row_count) != int(row_num):
        #print("row count", row_count)
        print("Wrong number of rows in '%s'" % fname)
    '''elif (int(row_count) == int(row_num)):
        print("Correct number of rows")'''
    checking.close()

# Main section
input_path = str(input("Type path to directory: "))
#input_path = str("/Users/Liz/Documents/DATA440/Repositories/spatial-data-discovery.github.io/sandbox")
listOfFile = os.listdir(input_path)
# https://stackoverflow.com/questions/7304117/split-filenames-with-python
for entry in listOfFile:
    print(entry)
    if entry == ".DS_Store":
        continue
    file_name = os.path.basename(entry)
    extension = os.path.splitext(file_name)[1]
    if extension in extensions:
        print("Checking " + str(entry))
        check_file(input_path, entry)
print("Done checking directory")
