/*
 * KotlinBasics.kt
 * ==============================================================================
 * This file demonstrates the fundamental building blocks of the Kotlin language.
 * Kotlin is a modern, statically typed language that runs on the JVM, known for
 * its conciseness and safety features (like Null Safety).
 * ==============================================================================
 */

// The 'main' function is the entry point of every Kotlin application.
fun main() {
    println("=== Kotlin Basics Tutorial ===\n")

    // 1. Variables and Data Types
    // ------------------------------------------------------------------------------
    // 'val' is for read-only variables (immutable - like 'final' in Java).
    // 'var' is for mutable variables (can be changed).
    // Kotlin usually infers the type automatically.
    
    val languageName = "Kotlin"        // String: Text
    val version = 1.9                  // Double: Decimal number
    var usersCount: Int = 0            // Int: Explicitly typed integer
    val isActive = true                // Boolean: True/False
    
    println("--- 1. Variables ---")
    println("Language: $languageName (Version $version)") // String Templates using $

    
    // 2. Conditional Logic (Control Flow)
    // ------------------------------------------------------------------------------
    // 'if' in Kotlin is an expression, meaning it returns a value.
    println("\n--- 2. Conditionals (If/Else) ---")
    
    val time = 15
    val greeting = if (time < 12) {
        "Good morning"
    } else {
        "Good afternoon" // The last line in the block is the return value
    }
    println("Feature: if-expression -> Result: $greeting")

    
    // 3. 'When' Expression (Switch Case replacement)
    // ------------------------------------------------------------------------------
    // 'when' is a powerful replacement for the switch statement.
    // It can check values, types, or ranges.
    println("\n--- 3. When Expression ---")
    
    val dayOfWeek = 3
    when (dayOfWeek) {
        1 -> println("Feature: when -> It's Monday")
        2, 3, 4 -> println("Feature: when -> It's a midweek day")
        5 -> println("Feature: when -> It's Friday!")
        in 6..7 -> println("Feature: when -> Weekend")
        else -> println("Feature: when -> Invalid day")
    }

    
    // 4. Loops (Iteration)
    // ------------------------------------------------------------------------------
    println("\n--- 4. Loops ---")
    
    // For Loop: Iterates over ranges, arrays, or collections
    print("For loop (Range): ")
    for (i in 1..3) { // Inclusive range [1, 3]
        print("$i ")
    }
    println()

    // While Loop: Repeats while condition is true
    print("While loop: ")
    var x = 3
    while (x > 0) {
        print("$x ")
        x--
    }
    println()

    // Iterating over a list
    val fruits = listOf("Apple", "Banana", "Cherry") // Immutable list
    print("Collection iteration: ")
    for (fruit in fruits) {
        print("$fruit ")
    }
    println()

    
    // 5. Functions
    // ------------------------------------------------------------------------------
    println("\n--- 5. Functions ---")
    
    val sum = addNumbers(5, 10)
    println("Feature: Function call -> 5 + 10 = $sum")
    
    // Named arguments allow specifying parameters by name
    greetUser(message = "Welcome to Kotlin", name = "Developer")

    
    // 6. Null Safety (Key Feature)
    // ------------------------------------------------------------------------------
    // Kotlin distinguishes between nullable and non-nullable types to prevent NullPointerExceptions.
    println("\n--- 6. Null Safety ---")
    
    var nullableText: String? = "I can be null" // '?' means it can hold null
    nullableText = null
    
    // Safe call operator (?.)
    // If nullableText is null, .length is not called and the expression returns null
    val length = nullableText?.length 
    println("Feature: Safe Call -> Length of null string is: $length")
    
    // Elvis Operator (?:)
    // Returns the value on the left if not null, otherwise returns the value on the right
    val safeLength = nullableText?.length ?: 0
    println("Feature: Elvis Operator -> Length is (defaulted): $safeLength")

    
    // 7. Classes and Data Classes
    // ------------------------------------------------------------------------------
    println("\n--- 7. Classes ---")
    
    val car = Car("Toyota", "Corolla")
    car.drive()
    
    // 'data class' automatically generates toString(), equals(), hashCode(), and copy()
    val user = User("Alice", 30)
    println("Feature: Data Class -> $user") // Prints formatted string automatically

    
    // 8. Exception Handling
    // ------------------------------------------------------------------------------
    println("\n--- 8. Exception Handling ---")
    try {
        val result = 100 / 0
    } catch (e: ArithmeticException) {
        println("Feature: try-catch -> Caught error: ${e.message}")
    } finally {
        println("Feature: finally -> cleanup code")
    }
}

// Function Definitions
// --------------------

// Basic function with return type
fun addNumbers(a: Int, b: Int): Int {
    return a + b
}

// Function with default argument values
fun greetUser(name: String, message: String = "Hello") {
    println("Feature: Function with defaults -> $message, $name!")
}

// Class Definition
class Car(val brand: String, val model: String) {
    fun drive() {
        println("Feature: Class method -> Driving a $brand $model")
    }
}

// Data Class Definition (optimized for holding data)
data class User(val name: String, val age: Int)
