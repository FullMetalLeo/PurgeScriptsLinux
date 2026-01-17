# ==============================================================================
#  COFFEESCRIPT: THE "IT'S JUST JAVASCRIPT" DEMO
# ==============================================================================
#  To run this file:
#  1. Install: npm install -g coffee-script
#  2. Run:     coffee CoffeeScriptDemo.coffee
# ==============================================================================

console.log "☕ Brewing some code...\n"

# ------------------------------------------------------------------------------
# 1. BASICS: VARIABLES & STRINGS
# ------------------------------------------------------------------------------
# No 'var', 'let', or 'const'. Scope is handled automatically.
name = "CoffeeScript"
year = 2009

# String Interpolation using #{ }
console.log "--> 1. BASICS: Hello, #{name}! Born in #{year}."

# Multi-line Strings (Heredocs)
description = """
  CoffeeScript is a little language
  that compiles into JavaScript.
"""
console.log description

# ------------------------------------------------------------------------------
# 2. FUNCTIONS
# ------------------------------------------------------------------------------
# Defined with '->'. The last expression is always implicitly returned.
square = (x) -> x * x

# With default arguments
greet = (msg = "Hello", person = "Stranger") ->
  "#{msg}, #{person}!"

console.log "\n--> 2. FUNCTIONS:"
console.log "    Square of 5: #{square(5)}"
console.log "    Greeting:    #{greet "Hi", "Developer"}"
console.log "    Default:     #{greet()}"

# ------------------------------------------------------------------------------
# 3. ARRAYS, OBJECTS & RANGES
# ------------------------------------------------------------------------------
# Arrays do not need braces if comma-separated
fruits = [
  "apple"
  "banana"
  "cherry"
]

# Objects can use YAML-style indentation (no braces/commas needed)
config =
  environment: "production"
  server:
    host: "localhost"
    port: 8080
  active: yes  # 'yes'/'on' compiles to true, 'no'/'off' to false

# Ranges
numbers = [1..10]      # Inclusive: 1 to 10
threeToSix = numbers[2..5] # Slicing (indexes)

console.log "\n--> 3. DATA STRUCTURES:"
console.log "    Config Port: #{config.server.port}"
console.log "    Sliced Array: #{threeToSix}"

# ------------------------------------------------------------------------------
# 4. CONTROL FLOW
# ------------------------------------------------------------------------------
console.log "\n--> 4. CONTROL FLOW:"

mood = "great"

# Post-fix conditionals (very readable!)
console.log "    I am happy!" if mood is "great"

# 'unless' is the opposite of 'if'
console.log "    This won't print" unless mood is "great"

# Switch statements (compile to efficient if/else chains)
activity = switch mood
  when "tired" then "sleep"
  when "hungry" then "eat"
  when "great" then "code"
  else "relax"

console.log "    Activity based on mood: #{activity}"

# ------------------------------------------------------------------------------
# 5. LOOPS & COMPREHENSIONS
# ------------------------------------------------------------------------------
console.log "\n--> 5. LOOPS:"

# Array Comprehension (One-liners are idiomatic)
# "Eat food for food in foods"
doubles = (num * 2 for num in [1..5])
console.log "    Doubles: #{doubles}"

# Filtering with 'when'
evens = (num for num in [1..10] when num % 2 is 0)
console.log "    Evens:   #{evens}"

# Object Iteration
console.log "    Iterating Config:"
for key, value of config
  # Note: value might be an object, so we json stringify for display
  displayVal = if typeof value is 'object' then JSON.stringify(value) else value
  console.log "      - #{key}: #{displayVal}"

# ------------------------------------------------------------------------------
# 6. CLASSES (OOP)
# ------------------------------------------------------------------------------
console.log "\n--> 6. CLASSES & INHERITANCE:"

class Animal
  # Constructor handles assignment of @name (this.name) automatically
  constructor: (@name) ->

  move: (meters) ->
    console.log "    #{@name} moved #{meters}m."

class Snake extends Animal
  move: ->
    console.log "    #{@name} implies slithering..."
    super 5 # Calls Animal.move(5)

sam = new Snake "Sammy the Python"
sam.move()

# ------------------------------------------------------------------------------
# 7. ADVANCED FEATURES
# ------------------------------------------------------------------------------
console.log "\n--> 7. ADVANCED:"

# Destructuring
[first, second] = ["Gold", "Silver"]
{ server } = config
console.log "    Destructured: #{first}, Server Host: #{server.host}"

# Splats (...) for variable arguments
showAwards = (competition, winners...) ->
  console.log "    #{competition} winners: #{winners.join(', ')}"

showAwards "Coding", "Alice", "Bob", "Charlie"

# The Existential Operator (?)
# Checks for null or undefined.
# 'zip = lottery.draw?.winner?.address?.zipcode' (The "Soak")

zombieland_rule_1 = "Cardio"
rule_2 = null

# 'or=' operator (ruby style ||=)
rule_2 ?= "Double Tap"

console.log "    Rule 1: #{zombieland_rule_1}"
console.log "    Rule 2: #{rule_2}"

# Chained Comparisons
temperature = 75
comfortable = 70 < temperature < 80
console.log "    Is it comfortable? #{comfortable}"

console.log "\n☕ Finished."
