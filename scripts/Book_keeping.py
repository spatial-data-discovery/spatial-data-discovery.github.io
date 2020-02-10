import pandas as pd
inventory = []
booksales = []

def Book_keeping(Inventory, Daily_sales):

    #reads in the two excel files

    Inventory = pd.read_excel(Inventory)
    Today_total = pd.read_excel(Daily_sales)

    #converts the idCode columns in each sheet into integers

    for num in Inventory["idCode"]:
        int(num)
    for digit in Today_total["idCode"]:
        int(digit)

    #iterates over the idCode column and creates a list for both sheets

    for copies in Inventory["idCode"]:
        inventory.append(copies)
    for book in Today_total["idCode"]:
        booksales.append(book)

    #Calculates where the new day's inventory will appear in the excel sheet

    tail = (len(inventory)-len(booksales))

    #removes purchased books from the inventory

    for book in booksales:
        inventory.remove(book)

    #adds the new inventory to the excel sheet

    for a in inventory:
        for part in Inventory["idCode"]:

            if a == part:
                Inventory = Inventory.append(Inventory.loc[Inventory["idCode"]== a])

    #removes the earlier entries

    Inventory = Inventory.tail(tail)

    #returns the final inventory list to be used the next day

    return Inventory.to_excel("NewInventory.xlsx",sheet_name = "Inventory",engine='xlsxwriter')

Book_keeping("Inventory.xlsx","Today.xlsx")
