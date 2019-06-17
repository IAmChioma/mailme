class ShoppingCart(object):
    def __init__(self):
        self.total = 0
        self.items = {}

    def add_item(self, item_name, quantity, price):
        self.total += quantity * price
        if type(item_name) == str and quantity > 0:
            self.items.update({item_name: quantity})

    def remove_item(self, item_name, quantity, price):
        if quantity >= self.items[item_name] and quantity > 1:
            items_cost = price * self.items[item_name]
            self.total -= items_cost
            del self.items[item_name]
        else:
            self.total -= quantity * price
            self.items[item_name] -= quantity

    def checkout(self, cash_paid):
        balance = 0
        if cash_paid < self.total:
            return "Cash paid not enough"
        balance = cash_paid - self.total
        return balance


class Shop(ShoppingCart):
    def __init__(self):
        self.quantity = 100

    def remove_item(self):
        self.quantity = self.quantity - 1


"""
Create a class called ShoppingCart.

Create a constructor that has no arguments and sets the total attribute to zero, and initializes an empty dict attribute named items.

Create a method add_item that requires item_name, quantity and price arguments. This method should add the cost of the added items to the current value of total. It should also add an entry to the items dict such that the key is the item_name and the value is the quantity of the item.

Create a method remove_item that requires similar arguments as add_item. It should remove items that have been added to the shopping cart and are not required. This method should deduct the cost of these items from the current total and also update the items dict accordingly. If the quantity of items to be removed exceeds current quantity in cart, assume that all entries of that item are to be removed.

Create a method checkout that takes in cash_paid and returns the value of balance from the payment. If cash_paid is not enough to cover the total, return Cash paid not enough.

Create a class called Shop that has a constructor which initializes an attribute called quantity at 100.

Make sure Shop inherits from ShoppingCart.

In the Shop class, override the remove_item method, such that calling Shop's remove_item with no arguments decrements quantity by one.

JavaScript
use camel case for your class method names, such that

    add_item 
becomes

    addItem 
You have completed this challenge! Make sure your code looks “production ready” before moving on to review & submi
"""



"""
We need the ability to divide an unknown integer into a given number of even parts — or at least as even as they can be. The sum of the parts should be the original value, but each part should be an integer, and they should be as close as possible.

Complete the function so that it returns an array of integer representing the parts. Ignoring the order of the parts, there is only one valid solution for each input to your function!

Also, there is no reason to test for edge cases: the input to your function will always be valid for this challenge.

Specification
split_integer(num, parts)
Divides an integer into an "even as can be" number of parts.

Parameters
num: Integer - The number that should be split into equal parts

parts: Integer - The number of parts that the number should be split into

Return Value
Array (of Integers) - An array of parts, with each index representing the part and the number contained within it representing the size of the part. The parts will be ordered from smallest to largest.

Examples
num	parts	Return Value
Completely even parts example	10	5	[2,2,2,2,2]
Even as can be parts example	20	6	[3,3,3,3,4,4]
You have completed this challenge! Make sure your code 
"""

def splitInteger(num,parts):
    #your code here
    quot, rem = divmod(num, parts)
    print(quot, rem)
    elem_one = [quot for i in range(parts - rem)]
    elem_two = [quot + 1 for j in range(rem)]
    print(elem_one, elem_two)
    print(elem_one +elem_two)
    return elem_one +elem_two

splitInteger(8,3)