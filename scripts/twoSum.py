'''
@Author: Tinh Son. Date: 2020-1-28
@Description: This code is written as a practice challenge from Leetcode.com, with linear run time.

@Problem
Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:

Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].

Execution format: python .\PEP8_TinhSon.py LIST TARGET
Where LIST is in string 
Where TARGET is a whole number

Example: python .\PEP8_TinhSon.py "2, 7, 11, 15" 9

'''
# import sys argv to receive input from console
import sys
# use regex to check input
import re 

def printHelp():
    print("Execution format: python .\PEP8_TinhSon.py LIST TARGET \n Where LIST is in string \n Where TARGET is a whole number \n Example: python .\\PEP8_TinhSon.py \"2, 7, 11, 15, 9\" 26")
          
# function takes in list and target, returns list
def twoSum(nums: list, target: int) -> list:
    # create hash-table
    dic = {}

    # loops through value and index
    for ind, val in enumerate(nums):
        # if complement value is not in hash-table
        if (target - val) not in dic:
            # add current value with corresponding index to hash-table
            dic[val] = ind
        else:
            # complement value found
             return [dic[target - val], ind]
            
    # none found
    return []

# where main function is called
def main(argv):
    # make sure argument length is 2
    assert len(argv[1:]) == 2, "Too many arguments"
    
    # parses string format into list
    preNums =  argv[1:][0]
    
    # use regex to check if each variable is valid input. Perform negative lookbehind/ahead for a decimal point. 
    formatCheck = re.findall(r'(?<!\.)\b[\d]+\b(?!\.)', preNums)
    
    # if everything is in proper format, number of values in filter will be the same as numher of values in preNums
    assert len(formatCheck) == len(preNums.split(',')), "Input must be all whole numbers and follows proper format"
    
    # convert preNums to nums after assert is True
    nums = map(int, preNums.strip('[]').split(','))
        
    # takes second target arugment
    target = argv[-1]
    
    # use regex to make sure the input is neither string nor a float
    assert len(re.findall(r'(?<!\.)\b[\d]+\b(?!\.)', target)) == 1, "Target only accepts one input, and input needs to be a whole number"
    
    target = int(target)
    
    # printa result
    print(twoSum(nums, target))

if __name__ == "__main__":
    if len(sys.argv) <= 1 or sys.argv[1] in ["--h", "--help"]:
        printHelp()
        exit(1)
    main(sys.argv)