/*
 * GroovyDemo.groovy
 * ==============================================================================
 * A comprehensive guide to the Groovy programming language.
 * Groovy is an optional-typed, dynamic language for the Java platform,
 * designed to be concise, expressive, and easy to learn for Java developers.
 *
 * Usage:
 *   1. Install Groovy (https://groovy-lang.org/install.html)
 *   2. Run: groovy GroovyDemo.groovy
 * ==============================================================================
 */

println "=== 🚀 Welcome to the Groovy Demo! ===\n"

// ------------------------------------------------------------------------------
// 1. BASICS: VARIABLES & STRINGS
// ------------------------------------------------------------------------------
println "--- 1. Variables & Strings ---"

// 'def' is used for type inference (optional typing)
def language = "Groovy"
def version = 4.0

// GStrings (Groovy Strings) support interpolation with ${}
println "We are learning ${language} version ${version}."

// Multiline strings (Triple quotes)
def definition = """
    Groovy makes writing code
    on the JVM fun again!
"""
println definition.trim()


// ------------------------------------------------------------------------------
// 2. COLLECTIONS (LISTS & MAPS)
// ------------------------------------------------------------------------------
println "\n--- 2. Collections ---"

// Lists are first-class citizens (ArrayList by default)
def languages = ["Java", "Kotlin", "Groovy"]
languages << "Scala" // Left shift operator adds an element
println "Languages: ${languages}"
println "Second language: ${languages[1]}" // Index access

// Maps (LinkedHashMap by default)
def frameworks = [
    web: "Grails",
    build: "Gradle",
    test: "Spock"
]
println "Build tool: ${frameworks.build}" // Dot notation property access
println "Web framework: ${frameworks['web']}"


// ------------------------------------------------------------------------------
// 3. CLOSURES (The Heart of Groovy)
// ------------------------------------------------------------------------------
println "\n--- 3. Closures ---"
// A Closure is an open, anonymous block of code that takes arguments, returns a value,
// and can be assigned to a variable.

def greeter = { name -> "Hello, ${name}!" }
println greeter("Developer")

// Closures with Collections
println "Upper case languages:"
languages.each { lang ->
    print "${lang.toUpperCase()} "
}
println()

// 'it' is the implicit parameter if none is defined
def shortNames = languages.findAll { it.length() <= 5 }
println "Short names: ${shortNames}"


// ------------------------------------------------------------------------------
// 4. OOP Features (POGOs)
// ------------------------------------------------------------------------------
println "\n--- 4. OOP & POGOs ---"

// POGO: Plain Old Groovy Object
// - Public by default
// - Auto-generated getters and setters
// - Named argument constructor
class Person {
    String name
    int age
    
    def speak() {
        println "$name says: I love Groovy!"
    }
}

// Named argument constructor usage (Very readable!)
def dev = new Person(name: "Alice", age: 30)
println "Developer: ${dev.name}, Age: ${dev.age}" // Calls getName() and getAge()
dev.speak()


// ------------------------------------------------------------------------------
// 5. ADVANCED FEATURES
// ------------------------------------------------------------------------------
println "\n--- 5. Advanced Features ---"

// Null-Safe Navigation (?.)
// Avoids NullPointerExceptions gracefully
def nullPerson = null
def nameLength = nullPerson?.name?.length() // Returns null, doesn't crash
println "Null safe length: ${nameLength}"

// Elvis Operator (?:)
// Short for 'x != null ? x : default'
def displayName = nullPerson?.name ?: "Anonymous"
println "User is: ${displayName}"

// The Spread Operator (*.)
// Invokes an action on all elements of a collection
def languageLengths = languages*.length()
println "Lengths of names: ${languageLengths}"

// Traits (Interfaces with default implementation and state)
trait Flying {
    void fly() { println "I believe I can fly!" }
}

class SuperDeveloper implements Flying {}
def hero = new SuperDeveloper()
hero.fly()

// Dynamic Features (Expando)
// Create objects dynamically at runtime
def dynamicObj = new Expando()
dynamicObj.name = "Dynamic"
dynamicObj.sayHello = { -> println "Hello from ${name} object!" }
dynamicObj.sayHello()


// ------------------------------------------------------------------------------
// 6. POPULAR USE CASES
// ------------------------------------------------------------------------------
println """
\n==============================================================================
 WHERE IS GROOVY USED?
==============================================================================
Groovy is widely used in the Java ecosystem for:

 1. 🐘 Gradle Build Scripts:
    The standard language for writing Gradle build logic (build.gradle) is Groovy.
    Its DSL capabilities make it perfect for configuration.

 2. 👷 Jenkins Pipelines:
    Jenkinsfiles are written in Groovy. It allows you to script complex
    CI/CD pipelines with conditional logic, loops, and parallel execution.

 3. 🧪 Spock Testing Framework:
    A powerful testing framework for Java and Groovy applications.
    It uses Groovy's expressive syntax to write highly readable, BDD-style tests.

 4. 🌐 Grails Framework:
    A high-productivity web application framework (inspired by Ruby on Rails)
    built on top of Spring Boot.

 5. 📜 Scripting & Gluing:
    Because it runs on the JVM and interacts seamlessly with Java code,
    it's excellent for writing glue code, automation scripts, and
    extending existing Java applications.
==============================================================================
"""
