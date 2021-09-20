#This script allows you to input your calorie needs and how much food you have already eaten, and outputs a food that would get you to your calorie needs for the day

def calories_to_food(cal_needed):
    food = ''
    if cal_needed <= 0:
    	food = 'You have already met your calorie needs for the day'
    else if cal_needed <= 4:
    	food = 'You should eat an M&M'
    else if cal_needed <= 20:
    	food = 'Try half of a cucumber'
    else if cal_needed <= 50:
    	food = 'You could have 10 olives'
    else if cal_needed <= 100:
    	food = 'Have an apple'
    else if cal_needed <= 200:
    	food = 'You should drink half of a liter of Coke'
    else if cal_needed <= 350:
    	food = 'Maybe try a baked potatoe with some sour cream'
    else if cal_needed <= 500:
    	food = 'You could have some fried chicken to get to your goal'
    else if cal_needed <= 1000:
    	food = 'Try two-three hot dogs (depending on the toppings!)'
    else if cal_needed <= 2000:
    	food = 'A big mac, large fries, and McFlurry from Mcdonalds would fill you up!'
    else:
    	food = 'You still need a lot of calories to meet your goal. Try a couple meals!'
    return food

if __name__ == "__main__":
    total_cals = int(input('Input your daily calorie needs'))
    eaten_cals = int(input('Input how many calries you have already eaten today'))
    print(calories_to_food(total_cals-eaten_cals))
