#Gianna Maniaci

#This project demonstrates the way linked lists work as well as adding a fun game to the mix!
#Josephus takes any number inputted by the user and makes a link list of 1 to that number
#it will then rotate the linked list so the first value becomes the last and removes the new first value
#it will continue to do this until there is only one number left, this is the survivor!
#I created this project in Computer Science 241, but added the help section




#from Linked_List import Linked_List   <----- This has been commented out because I added the 
                                              #linked list class into this document
import argparse

def Josephus(ll):
  #Prints the linked list after each time it rotates left and 
  #removes the first value
  while (len(ll) != 1):
    ll.rotate_left()
    ll.remove_element_at(0)
    print(ll)
  #prints the surviving value
  print ("The survivor is: " + str(ll.get_element_at(0)))



class Linked_List:
  
  class __Node:
    
    #defines a node
    def __init__(self, val):
      self.val = val
      self.next = None
      self.prev = None

  #defines a linked list
  def __init__(self):
    self.__size = 0
    self.__header = Linked_List.__Node(None)
    self.__trailer = Linked_List.__Node(None)
    self.__header.next = self.__trailer
    self.__trailer.prev = self.__header

  #returns length of list
  def __len__(self):
    return self.__size

  #add val to the end of the list
  def append_element(self, val):
    new_element = Linked_List.__Node(val)

    #if there are no values currently in the list implement this:
    if (self.__size == 0):
      self.__trailer.prev = new_element
      self.__header.next = new_element
      new_element.next = self.__trailer
      new_element.prev = self.__header

    #if there are values currently in the list implement this:
    else:
      new_element.prev = self.__trailer.prev
      new_element.next = self.__trailer
      self.__trailer.prev.next = new_element
      self.__trailer.prev = new_element

    #increases size by 1
    self.__size = self.__size + 1

  #inserts a value at a position given by the user
  def insert_element_at(self, val, index):   
    new_element = Linked_List.__Node(val)
    pointer = self.__header.next

    #makes sure the index is in bounds
    if (index < self.__size and index >= 0):
      #if the index is at 0 it will implement this
      if (index == 0):
        new_element.prev = self.__header
        new_element.next = self.__header.next
        self.__header.next.prev = new_element
        self.__header.next = new_element
        

      #otherwise inserts the value at the given index
      else:
        location = 0
        while (location != (index-1)):
          location = location + 1
          if (location != (index-1)):
            pointer = pointer.next
        new_element.prev = pointer
        new_element.next = pointer.next
        pointer.next.prev = new_element
        pointer.next = new_element


      #increases size by 1
      self.__size = self.__size + 1

  #if index is out of bounds it will raise an error
    else:
      raise IndexError

  #removes element at given value
  def remove_element_at(self, index):
    pointer = self.__header.next

    #makes sure index given is in bounds
    if(index < self.__size and index >= 0):
      #removes element at index 0 if index given is 0 
      if (index == 0):
        self.__header.next = self.__header.next.next
        self.__header.next.prev = self.__header

      #removes the last item in the list if user indicated this index
      elif (index == self.__size - 1):
        self.__trailer.prev = self.__trailer.prev.prev
        self.__trailer.prev.next = self.__trailer

      #otherwise removes the value at the given index
      else:
        location = 0
        while (location != (index-1)):
          location = location + 1
          pointer = pointer.next
        pointer.next = pointer.next.next
        pointer.next.prev = pointer

      #decreases size by 1
      self.__size = self.__size - 1

    #raises error if index is out of bounds
    else:
      raise IndexError
      

  #returns the value stored in a given index
  def get_element_at(self, index):

    #makes sure index given is in bounds
    if (index < self.__size and index >= 0):
      #if the user wants the last item in the list implement this:
      if (index == self.__size - 1):
        pointer = self.__trailer.prev
        return (pointer.val)

      #finds correct index location and returns the value
      pointer = self.__header.next
      location = 0
      while (location != index):
        location = location + 1
        pointer = pointer.next
      return (pointer.val)

    #raises an index error if index is out of bounds
    else:
      raise IndexError
    
  #removes first element in the list and appends it to the end
  def rotate_left(self):
    first_number = self.get_element_at(0)
    self.remove_element_at(0)
    self.append_element(first_number)
    
  def __str__(self):
    #returns an empty list if there is nothing in the linked list
    if (self.__size == 0):
      return '[]'
    #if the linked list is not empty it adds one value at a time
    #to a new string and returns it.
    else:
      current = self.__header.next
      print_this = ("[ " + str(current.val))
    while (current.next != self.__trailer):
      current = current.next
      print_this += ", " + str(current.val)
    return (print_this + " ]")


  def __iter__(self):
    #tells the iterator where to start
    self.__iter_index = 0
    return self

  def __next__(self):
    # fetch the next value and return it. If there are no more 
    # values to fetch, raise a StopIteration exception.
    if (self.__iter__ == self.__size):
      raise StopIteration
    to_return = self.get_element_at(self.__iter_index)
    self.__iter_index = self.__iter_index + 1
    return to_return




if __name__ == '__main__':

  p = argparse.ArgumentParser(description="Josephus Finds the Surviving Individual")
  args = p.parse_args()

  #asks user for n value
  n = int(input("Input the total number of people: "))
  #creates linked list
  ll = Linked_List()
  #adds n values to the linked list
  i = 1
  while (i < n + 1):
    ll.append_element(i) 
    i = i + 1
  #prints the initial list
  print("Initial order:", ll)
  #calls the function
  Josephus(ll)