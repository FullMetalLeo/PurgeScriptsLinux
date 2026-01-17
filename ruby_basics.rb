# ruby_basics.rb
# ==============================================================================
# This script demonstrates the fundamental building blocks of the Ruby language.
# Ruby is an object-oriented, dynamic language known for its readability.
# ==============================================================================

# 1. Variables and Data Types
# ------------------------------------------------------------------------------
# Variables in Ruby are dynamically typed (you don't need to specify the type).
name = "Ruby User"       # String: Text data
age = 25                 # Integer: Whole numbers
pi = 3.14                # Float: Decimal numbers
is_active = true         # Boolean: True or False
colors = ["red", "blue"] # Array: Ordered list of items
user_info = {            # Hash: Key-value pairs (like a Dictionary)
  "username" => "admin",
  "role" => "standard"
}

puts "--- 1. Variables ---"
puts "Hello #{name}, you are #{age} years old." # String Interpolation


# 2. Conditional Statements (if-else)
# ------------------------------------------------------------------------------
# Used to execute code based on whether a condition is true or false.
puts "\n--- 2. Conditionals ---"

if age >= 18
  puts "Feature: if-else -> Result: You are an adult."
elsif age > 12
  puts "Feature: if-else -> Result: You are a teenager."
else
  puts "Feature: if-else -> Result: You are a child."
end

# "unless" is the opposite of "if" (runs code if condition is FALSE)
is_authenticated = false
unless is_authenticated
  puts "Feature: unless -> Result: Access Denied! Please log in."
end


# 3. Loops (Iteration)
# ------------------------------------------------------------------------------
# Used to repeat code multiple times.
puts "\n--- 3. Loops ---"

# 'times' loop: Repeats code a specific number of times
print "times loop: "
3.times { |i| print "#{i} " }
puts ""

# 'while' loop: Repeats while a condition is true
counter = 0
print "while loop: "
while counter < 3
  print "#{counter} "
  counter += 1
end
puts ""

# 'each' loop: The Ruby way to iterate over collections (Arrays/Hashes)
print "each loop (Array): "
["Apple", "Banana", "Cherry"].each do |fruit|
  print "#{fruit} "
end
puts ""


# 4. Case Statements (Switch-Case equivalent)
# ------------------------------------------------------------------------------
# Used when you have many conditions for a single variable.
puts "\n--- 4. Case Statement ---"

day = "Friday"

case day
when "Monday"
  puts "Feature: case -> Start of the week."
when "Friday"
  puts "Feature: case -> End of the work week!"
when "Saturday", "Sunday"
  puts "Feature: case -> It's the weekend!"
else
  puts "Feature: case -> Just a normal day."
end


# 5. Methods (Functions)
# ------------------------------------------------------------------------------
# Block of reusable code. Methods in Ruby automatically return the last expression.
puts "\n--- 5. Methods ---"

# Feature: Method with parameters and a default value
def greet_user(username = "Guest")
  return "Hello, #{username}! Welcome to Ruby."
end

# Feature: Calling the method
message = greet_user("Antigravity")
puts "Feature: method -> #{message}"


# 6. Classes and Objects (Object-Oriented Programming)
# ------------------------------------------------------------------------------
# Ruby is pure OOP; everything is an object. Classes are blueprints for objects.
puts "\n--- 6. Classes & Objects ---"

class Calculator
  # Feature: Initialize method (Constructor) runs when .new is called
  def initialize(owner)
    @owner = owner # '@' denotes an instance variable (stored per object)
  end

  # Feature: Instance method
  def add(a, b)
    puts "Feature: Calculator.add -> #{@owner} is calculating #{a} + #{b}"
    a + b
  end
end

# Create an object (instance) of the class
my_calc = Calculator.new("Ruby Developer")
result = my_calc.add(10, 5)
puts "Result: #{result}"


# 7. Error Handling (Exception Handling)
# ------------------------------------------------------------------------------
# Prevents the program from crashing when an error occurs.
puts "\n--- 7. Error Handling ---"

begin
  # Code that might fail (dividing by zero)
  calculation = 10 / 0
rescue ZeroDivisionError => e
  # Code that runs if an error occurs
  puts "Feature: rescue -> Caught error: #{e.message}"
ensure
  # Code that runs no matter what (e.g., closing a file)
  puts "Feature: ensure -> This block always runs."
end

puts "\n============================================="
puts "Ruby Basics Tutorial Complete!"
puts "============================================="
