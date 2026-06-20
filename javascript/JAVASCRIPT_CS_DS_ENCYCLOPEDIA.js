#!/usr/bin/env node
"use strict";
/**
 * ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                                                                        ║
 * ║          JAVASCRIPT CS & DATA SCIENCE ENCYCLOPEDIA                     ║
 * ║          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                    ║
 * ║                                                                        ║
 * ║  An exhaustive, fully-runnable reference spanning:                      ║
 * ║    Phase 1: JavaScript Core, Internals & OOP                           ║
 * ║    Phase 2: Data Structures (Pure CS)                                  ║
 * ║    Phase 3: Algorithmic Mastery & Dynamic Programming                  ║
 * ║    Phase 4: Software Architecture & Design Patterns (GoF)              ║
 * ║    Phase 5: Functional Programming & Advanced JS                       ║
 * ║    Phase 6: Async Patterns & Concurrency                               ║
 * ║    Phase 7: Node.js Essentials                                         ║
 * ║    Phase 8: Testing, Error Handling & Performance                      ║
 * ║    Bonus:   Debug Challenges (Intentional Bugs)                        ║
 * ║                                                                        ║
 * ║  Self-contained: runs with Node.js (v18+). No external dependencies.   ║
 * ║  Every section includes JSDoc comments, Big-O analysis, and            ║
 * ║  inline comments explaining "the why".                                 ║
 * ║                                                                        ║
 * ║  Run:  node JAVASCRIPT_CS_DS_ENCYCLOPEDIA.js                           ║
 * ╚══════════════════════════════════════════════════════════════════════════╝
 */


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 1: JAVASCRIPT CORE, INTERNALS & OOP                         ║
// ╚══════════════════════════════════════════════════════════════════════╝
// This phase covers the bedrock of JavaScript: types, coercion, closures,
// prototypal inheritance, ES6+ classes, iterators, generators, Promises,
// Proxies, and the module system.


// ========================================================================
// 1.1  Core Types, Typeof, Equality, Mutability
// ========================================================================

function coreTypesDemo() {
    /**
     * JavaScript has 7 primitive types and 1 structural type:
     *
     * Primitives (immutable, passed by value):
     *   number, string, boolean, undefined, null, symbol, bigint
     *
     * Structural (mutable, passed by reference):
     *   object (includes arrays, functions, Date, RegExp, Map, Set, etc.)
     *
     * Key Insight: typeof null === "object" — this is a historic bug in JS
     * that was never fixed for backward compatibility.
     *
     * Big-O Note: All demonstrations here are O(1).
     */

    // --- typeof checks ---
    console.log("--- typeof checks ---");
    const values = [
        42, 3.14, "hello", true, undefined, null,
        Symbol("id"), 10n, [1, 2], { a: 1 }, function () { }, new Date()
    ];
    for (const v of values) {
        console.log(`  typeof ${String(v).padEnd(25)} = ${typeof v}`);
    }
    // Note: typeof null === "object" (historic bug)
    // Note: typeof function === "function" (special case of object)

    // --- === vs == (strict vs loose equality) ---
    console.log("\n--- === vs == (strict vs loose equality) ---");
    console.log(`  0 == false:      ${0 == false}`);       // true (coercion)
    console.log(`  0 === false:     ${0 === false}`);      // false (no coercion)
    console.log(`  "" == false:     ${"" == false}`);      // true (coercion)
    console.log(`  "" === false:    ${"" === false}`);     // false
    console.log(`  null == undefined: ${null == undefined}`); // true (special case)
    console.log(`  null === undefined: ${null === undefined}`); // false
    console.log(`  NaN === NaN:     ${NaN === NaN}`);      // false! Use Number.isNaN()
    console.log(`  Number.isNaN(NaN): ${Number.isNaN(NaN)}`); // true
    // RULE: Always use === unless you specifically want coercion.
    // The ONLY valid use of == is `x == null` to check for both null and undefined.

    // --- Primitives vs Objects (immutability vs mutability) ---
    console.log("\n--- Primitives vs Objects ---");
    let a = "hello";
    let b = a;          // b gets a COPY of the value
    a = "world";
    console.log(`  After reassigning a: a="${a}", b="${b}"`);  // b is still "hello"

    const obj1 = { x: 1, y: 2 };
    const obj2 = obj1;   // obj2 points to the SAME object
    obj1.x = 99;
    console.log(`  After mutating obj1: obj1.x=${obj1.x}, obj2.x=${obj2.x}`);  // both 99

    // --- Object.freeze (shallow immutability) ---
    const frozen = Object.freeze({ a: 1, nested: { b: 2 } });
    // frozen.a = 99;    // Silently fails in non-strict mode, throws in strict mode
    frozen.nested.b = 99; // This WORKS — freeze is SHALLOW
    console.log(`  Frozen object nested mutation: frozen.nested.b = ${frozen.nested.b}`);

    // --- Number edge cases ---
    console.log("\n--- Number Edge Cases ---");
    console.log(`  0.1 + 0.2 === 0.3: ${0.1 + 0.2 === 0.3}`);  // false!
    console.log(`  0.1 + 0.2 = ${0.1 + 0.2}`);                   // 0.30000000000000004
    console.log(`  Safe comparison: ${Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON}`); // true
    console.log(`  Number.MAX_SAFE_INTEGER: ${Number.MAX_SAFE_INTEGER}`);  // 2^53 - 1
    console.log(`  BigInt example: ${10n ** 20n}`);                // 100000000000000000000n

    // --- Type coercion pitfalls ---
    console.log("\n--- Type Coercion ---");
    console.log(`  [] + []:         "${[] + []}"`);          // "" (empty string)
    console.log(`  [] + {}:         "${[] + {}}"`);          // "[object Object]"
    console.log(`  {} + []:         ${+[]}`);                // 0 (unary + on empty array)
    console.log(`  "5" - 3:         ${"5" - 3}`);           // 2 (string coerced to number)
    console.log(`  "5" + 3:         ${"5" + 3}`);           // "53" (number coerced to string)
    console.log(`  true + true:     ${true + true}`);       // 2
}

coreTypesDemo();


// ========================================================================
// 1.2  Control Flow, Destructuring, Spread/Rest, Modern Syntax
// ========================================================================

function controlFlowDemo() {
    /**
     * Modern JavaScript control flow and syntactic sugar.
     *
     * Covers:
     * - for...of (iterables), for...in (object keys)
     * - Destructuring (array & object)
     * - Spread (...) and Rest (...) operators
     * - Optional chaining (?.), nullish coalescing (??)
     * - Template literals, tagged templates
     * - Short-circuit evaluation patterns
     *
     * Big-O Notes:
     * - for...of: O(n) — one pass over the iterable.
     * - Destructuring: O(1) — just variable assignment.
     * - Spread on array: O(n) — creates a shallow copy.
     */

    // --- for...of vs for...in ---
    console.log("\n--- for...of vs for...in ---");
    const arr = [10, 20, 30];
    arr.customProp = "extra";   // Arrays are objects — you can add properties

    process.stdout.write("  for...of (values): ");
    for (const val of arr) process.stdout.write(`${val} `);
    console.log();
    // for...of iterates VALUES (via Symbol.iterator). Ignores non-index properties.

    process.stdout.write("  for...in (keys):   ");
    for (const key in arr) process.stdout.write(`${key} `);
    console.log();
    // for...in iterates KEYS (including "customProp"). DO NOT use on arrays!

    // --- Array Destructuring ---
    console.log("\n--- Destructuring ---");
    const [first, second, ...rest] = [1, 2, 3, 4, 5];
    console.log(`  Array: first=${first}, second=${second}, rest=${JSON.stringify(rest)}`);

    // Swap without temp variable
    let x = 10, y = 20;
    [x, y] = [y, x];
    console.log(`  Swap: x=${x}, y=${y}`);

    // Object destructuring with rename and default
    const { name: userName = "Anonymous", age = 0 } = { name: "Alice", score: 95 };
    console.log(`  Object: userName="${userName}", age=${age}`);

    // Nested destructuring
    const { address: { city, zip = "00000" } } = {
        address: { city: "NYC", state: "NY" }
    };
    console.log(`  Nested: city="${city}", zip="${zip}"`);

    // --- Spread & Rest ---
    console.log("\n--- Spread & Rest ---");
    const arr1 = [1, 2, 3];
    const arr2 = [4, 5, 6];
    const merged = [...arr1, ...arr2];   // Shallow copy + merge
    console.log(`  Spread merge: ${JSON.stringify(merged)}`);

    const obj = { a: 1, b: 2 };
    const extended = { ...obj, c: 3, b: 99 };  // Later keys override
    console.log(`  Object spread: ${JSON.stringify(extended)}`);

    // Rest in function parameters
    function sum(...nums) {
        return nums.reduce((acc, n) => acc + n, 0);
    }
    console.log(`  Rest params sum(1,2,3,4,5) = ${sum(1, 2, 3, 4, 5)}`);

    // --- Optional Chaining (?.) ---
    console.log("\n--- Optional Chaining & Nullish Coalescing ---");
    const user = { profile: { address: { city: "London" } } };
    console.log(`  user?.profile?.address?.city = "${user?.profile?.address?.city}"`);
    console.log(`  user?.profile?.phone?.number = ${user?.profile?.phone?.number}`); // undefined
    // Without ?. this would throw: "Cannot read property 'number' of undefined"

    // Optional chaining with method calls
    const map = new Map();
    console.log(`  map.get?.("key") = ${map.get?.("key")}`);   // undefined (method exists)

    // --- Nullish Coalescing (??) ---
    // ?? returns right side ONLY if left is null or undefined (NOT 0, "", false)
    const config = { timeout: 0, retries: null };
    console.log(`  config.timeout ?? 30 = ${config.timeout ?? 30}`);   // 0 (not null/undefined)
    console.log(`  config.retries ?? 3  = ${config.retries ?? 3}`);    // 3 (null → use default)
    console.log(`  config.timeout || 30 = ${config.timeout || 30}`);   // 30 (0 is falsy!)
    // KEY DIFFERENCE: || treats 0, "", false as falsy. ?? only treats null/undefined.

    // --- Template Literals ---
    console.log("\n--- Template Literals ---");
    const name2 = "World";
    console.log(`  Basic: Hello, ${name2}!`);
    console.log(`  Expression: 2 + 3 = ${2 + 3}`);
    console.log(`  Multi-line: Line 1\n              Line 2`);

    // Tagged template literal
    function highlight(strings, ...values) {
        return strings.reduce((result, str, i) =>
            result + str + (values[i] !== undefined ? `【${values[i]}】` : ""), "");
    }
    const item = "book";
    const price = 29.99;
    console.log(`  Tagged: ${highlight`I bought a ${item} for $${price}`}`);

    // --- Short-circuit patterns ---
    console.log("\n--- Short-circuit Patterns ---");
    const debug = false;
    debug && console.log("  This won't print (short-circuit AND)");
    const fallback = null ?? "default value";
    console.log(`  Nullish fallback: "${fallback}"`);
}

controlFlowDemo();


// ========================================================================
// 1.3  Functions: Closures, IIFE, Arrow Functions, this Binding
// ========================================================================

function functionsDemo() {
    /**
     * Deep-dive into JavaScript functions — the building block of the language.
     *
     * Covers:
     * - Function declarations vs expressions vs arrows
     * - Closures (lexical scoping)
     * - IIFE (Immediately Invoked Function Expression)
     * - Higher-order functions
     * - `this` binding: call, apply, bind
     * - Arrow functions and lexical `this`
     *
     * Key Insight: In JS, functions are first-class objects. They can be
     * assigned to variables, passed as arguments, and returned from functions.
     */

    // --- Function types ---
    console.log("\n--- Function Types ---");

    // Declaration (hoisted — can be called before definition)
    function greet(name) { return `Hello, ${name}!`; }

    // Expression (NOT hoisted)
    const greet2 = function (name) { return `Hi, ${name}!`; };

    // Arrow function (concise syntax, lexical `this`)
    const greet3 = (name) => `Hey, ${name}!`;

    console.log(`  Declaration: ${greet("Alice")}`);
    console.log(`  Expression:  ${greet2("Bob")}`);
    console.log(`  Arrow:       ${greet3("Charlie")}`);

    // --- Closures ---
    console.log("\n--- Closures ---");
    /**
     * A closure is a function that "remembers" the variables from its
     * lexical scope even after the outer function has returned.
     *
     * This is possible because JavaScript uses lexical scoping:
     * functions are linked to the scope where they are DEFINED, not
     * where they are CALLED.
     */
    function makeCounter(initial = 0) {
        let count = initial;   // This variable is "closed over"
        return {
            increment: () => ++count,
            decrement: () => --count,
            getCount: () => count,
        };
    }

    const counter = makeCounter(10);
    console.log(`  counter.increment() = ${counter.increment()}`);  // 11
    console.log(`  counter.increment() = ${counter.increment()}`);  // 12
    console.log(`  counter.decrement() = ${counter.decrement()}`);  // 11
    // `count` is private — inaccessible from outside. This is the MODULE PATTERN.

    // --- IIFE (Immediately Invoked Function Expression) ---
    console.log("\n--- IIFE ---");
    const result = (() => {
        const secret = 42;
        return secret * 2;
    })();
    console.log(`  IIFE result: ${result}`);  // 84
    // IIFEs create a new scope. Before `let`/`const` (ES6), this was the only
    // way to create block-scoped variables. Still useful for one-time initialization.

    // --- Higher-Order Functions ---
    console.log("\n--- Higher-Order Functions ---");
    const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

    // map: transform each element. O(n)
    const doubled = numbers.map(n => n * 2);
    console.log(`  map (×2):    ${JSON.stringify(doubled)}`);

    // filter: keep elements matching predicate. O(n)
    const evens = numbers.filter(n => n % 2 === 0);
    console.log(`  filter (even): ${JSON.stringify(evens)}`);

    // reduce: accumulate into a single value. O(n)
    const sum = numbers.reduce((acc, n) => acc + n, 0);
    console.log(`  reduce (sum): ${sum}`);

    // Chaining: filter → map → reduce
    const sumOfSquaredEvens = numbers
        .filter(n => n % 2 === 0)
        .map(n => n * n)
        .reduce((acc, n) => acc + n, 0);
    console.log(`  Chain (sum of squared evens): ${sumOfSquaredEvens}`);

    // --- `this` Binding ---
    console.log("\n--- this Binding ---");
    /**
     * In JavaScript, `this` is determined by HOW a function is called:
     *
     * 1. Regular function call:  this = globalThis (or undefined in strict mode)
     * 2. Method call (obj.fn()): this = obj
     * 3. Constructor (new Fn()): this = newly created object
     * 4. call/apply/bind:        this = explicitly specified
     * 5. Arrow function:         this = lexical (inherited from enclosing scope)
     */

    const person = {
        name: "Alice",
        greet() {
            return `Hello, I'm ${this.name}`;
        },
        greetArrow: () => {
            // Arrow functions don't have their own `this`
            // `this` here refers to the enclosing scope (module/global)
            return `Hello, I'm ${typeof this === "object" ? this?.name : "undefined"}`;
        }
    };

    console.log(`  Method call:     ${person.greet()}`);            // "Alice"
    const detached = person.greet;
    // console.log(detached());  // undefined — `this` is lost when detached

    // Fix with bind:
    const bound = person.greet.bind(person);
    console.log(`  bind():          ${bound()}`);                   // "Alice"

    // call and apply:
    const otherPerson = { name: "Bob" };
    console.log(`  call():          ${person.greet.call(otherPerson)}`);    // "Bob"
    console.log(`  apply():         ${person.greet.apply(otherPerson)}`);   // "Bob"
    // call takes arguments individually; apply takes an array. Remember: Apply = Array.
}

functionsDemo();


// ========================================================================
// 1.4  Prototypal Inheritance, ES6 Classes, Private Fields
// ========================================================================

function oopDemo() {
    /**
     * JavaScript uses PROTOTYPAL inheritance — objects inherit directly
     * from other objects via the prototype chain.
     *
     * ES6 classes are syntactic sugar over the prototype system.
     * They don't introduce a new OOP model — they just make the existing
     * prototype-based system easier to use.
     *
     * Covers:
     * - Prototype chain
     * - ES6 classes: constructor, methods, static, extends, super
     * - Private fields (#)
     * - Getters and setters
     * - Symbol.toPrimitive, Symbol.iterator
     */

    // --- Prototype Chain (the foundation) ---
    console.log("\n--- Prototype Chain ---");

    function Animal(name, legs) {
        this.name = name;
        this.legs = legs;
    }
    Animal.prototype.speak = function () {
        return `${this.name} makes a generic sound`;
    };

    function Dog(name) {
        Animal.call(this, name, 4);  // Call parent constructor
    }
    Dog.prototype = Object.create(Animal.prototype);  // Set up inheritance
    Dog.prototype.constructor = Dog;                    // Fix constructor reference
    Dog.prototype.speak = function () {
        return `${this.name} says Woof!`;
    };

    const rex = new Dog("Rex");
    console.log(`  ${rex.speak()}`);
    console.log(`  rex instanceof Dog: ${rex instanceof Dog}`);
    console.log(`  rex instanceof Animal: ${rex instanceof Animal}`);

    // Walking the prototype chain:
    let proto = rex;
    const chain = [];
    while (proto = Object.getPrototypeOf(proto)) {
        chain.push(proto.constructor?.name || "null");
    }
    console.log(`  Prototype chain: Rex → ${chain.join(" → ")}`);

    // --- ES6 Classes (syntactic sugar) ---
    console.log("\n--- ES6 Classes ---");

    class Shape {
        /** @type {string} */
        #color;   // Private field (ES2022) — inaccessible outside the class

        /**
         * @param {string} color - The shape's color
         */
        constructor(color = "red") {
            this.#color = color;
        }

        /** Getter for the private #color field. */
        get color() { return this.#color; }

        /** Setter with validation. */
        set color(value) {
            if (typeof value !== "string") throw new TypeError("Color must be a string");
            this.#color = value;
        }

        /**
         * Area calculation — must be overridden by subclasses.
         * @returns {number}
         */
        area() {
            throw new Error("area() must be implemented by subclass");
        }

        /** Static factory method. */
        static createRed() {
            return new this("red");
        }

        /**
         * Custom string conversion.
         * Symbol.toPrimitive is called when JS needs to coerce the object.
         * @param {string} hint - "number", "string", or "default"
         */
        [Symbol.toPrimitive](hint) {
            if (hint === "string") return `Shape(color=${this.#color})`;
            if (hint === "number") return this.area();
            return this.area();  // default
        }

        toString() {
            return `Shape(color=${this.#color})`;
        }
    }

    class Circle extends Shape {
        /** @type {number} */
        #radius;

        /**
         * @param {number} radius
         * @param {string} color
         */
        constructor(radius, color = "blue") {
            super(color);   // MUST call super() before using `this`
            this.#radius = radius;
        }

        get radius() { return this.#radius; }

        set radius(value) {
            if (value <= 0) throw new RangeError("Radius must be positive");
            this.#radius = value;
        }

        /** @returns {number} */
        area() {
            return Math.PI * this.#radius ** 2;
        }

        /** @returns {number} */
        circumference() {
            return 2 * Math.PI * this.#radius;
        }

        toString() {
            return `Circle(radius=${this.#radius}, color=${this.color})`;
        }
    }

    class Rectangle extends Shape {
        /** @type {number} */ #width;
        /** @type {number} */ #height;

        constructor(width, height, color = "green") {
            super(color);
            this.#width = width;
            this.#height = height;
        }

        area() { return this.#width * this.#height; }

        toString() {
            return `Rectangle(${this.#width}×${this.#height}, color=${this.color})`;
        }
    }

    const c = new Circle(5, "blue");
    const r = new Rectangle(4, 6, "green");
    console.log(`  ${c} → area=${c.area().toFixed(4)}, circumference=${c.circumference().toFixed(4)}`);
    console.log(`  ${r} → area=${r.area()}`);
    console.log(`  c instanceof Circle: ${c instanceof Circle}`);
    console.log(`  c instanceof Shape:  ${c instanceof Shape}`);

    // Private field access attempt:
    try {
        // c.#radius;  // SyntaxError at parse time — can't even write this
        console.log(`  Private fields: Cannot access #radius from outside (enforced by syntax)`);
    } catch (e) {
        console.log(`  Private field error: ${e.message}`);
    }

    // --- Mixins (composition over inheritance) ---
    console.log("\n--- Mixins ---");
    const Serializable = (Base) => class extends Base {
        toJSON() {
            return JSON.stringify({ type: this.constructor.name, ...this });
        }
    };

    const Printable = (Base) => class extends Base {
        print() {
            console.log(`  [Print] ${this.toString()}`);
        }
    };

    // Apply mixins using composition
    class FancyCircle extends Printable(Serializable(Circle)) {
        constructor(radius, color) {
            super(radius, color);
        }
    }

    const fc = new FancyCircle(3, "purple");
    fc.print();   // Uses Printable mixin
    console.log(`  Mixin chain works: fc instanceof Circle = ${fc instanceof Circle}`);
}

oopDemo();


// ========================================================================
// 1.5  Iterators & Generators
// ========================================================================

function iteratorsGeneratorsDemo() {
    /**
     * The Iterator Protocol:
     * An object is iterable if it has a [Symbol.iterator]() method that
     * returns an iterator. An iterator has a next() method that returns
     * { value, done }.
     *
     * Generators (function*):
     * A special function that can be paused (yield) and resumed.
     * They automatically implement the iterator protocol.
     *
     * Big-O Notes:
     * - Generators: O(1) memory per yielded item (lazy evaluation).
     * - Iterators enable processing large datasets without loading all into memory.
     */

    // --- Custom Iterable ---
    console.log("\n--- Custom Iterable (Range) ---");

    class Range {
        /**
         * Creates an iterable range [start, end) with optional step.
         * @param {number} start
         * @param {number} end
         * @param {number} step
         */
        constructor(start, end, step = 1) {
            this.start = start;
            this.end = end;
            this.step = step;
        }

        /** Makes Range work with for...of, spread, destructuring, etc. */
        [Symbol.iterator]() {
            let current = this.start;
            const end = this.end;
            const step = this.step;
            return {
                next() {
                    if (current < end) {
                        const value = current;
                        current += step;
                        return { value, done: false };
                    }
                    return { value: undefined, done: true };
                }
            };
        }
    }

    const range = new Range(0, 10, 2);
    console.log(`  Range(0, 10, 2): ${[...range]}`);           // [0, 2, 4, 6, 8]
    console.log(`  Destructure: ${(() => { const [a, b, c] = range; return `${a},${b},${c}`; })()}`);

    // --- Generator Functions ---
    console.log("\n--- Generator Functions ---");

    function* fibonacci(limit) {
        /**
         * Yield Fibonacci numbers up to `limit`.
         * Memory: O(1) — only two variables held at any time.
         * Time:   O(limit) — one iteration per number.
         */
        let a = 0, b = 1;
        while (a < limit) {
            yield a;        // Suspend here, resume on next()
            [a, b] = [b, a + b];
        }
    }

    console.log(`  Fibonacci < 100: ${[...fibonacci(100)]}`);

    // --- Generator with yield* (delegation) ---
    function* concat(...iterables) {
        /** Yield* delegates to another iterable/generator. */
        for (const iterable of iterables) {
            yield* iterable;    // Yields each element from the iterable
        }
    }

    console.log(`  concat([1,2], [3,4]): ${[...concat([1, 2], [3, 4], [5])]}`);

    // --- Infinite Generator ---
    function* naturals(start = 1) {
        /** Infinite sequence of natural numbers. O(1) memory. */
        let n = start;
        while (true) {
            yield n++;
        }
    }

    // Take first 5 from infinite generator
    function take(n, iterable) {
        const result = [];
        for (const val of iterable) {
            result.push(val);
            if (result.length >= n) break;
        }
        return result;
    }

    console.log(`  First 5 naturals: ${take(5, naturals())}`);
    console.log(`  Naturals from 10: ${take(5, naturals(10))}`);

    // --- Generator as data pipeline ---
    console.log("\n--- Generator Pipeline ---");

    function* map(iterable, fn) {
        for (const val of iterable) yield fn(val);
    }

    function* filter(iterable, pred) {
        for (const val of iterable) {
            if (pred(val)) yield val;
        }
    }

    // Pipeline: naturals → filter evens → square → take 5
    const pipeline = take(5,
        map(
            filter(naturals(), n => n % 2 === 0),
            n => n * n
        )
    );
    console.log(`  Pipeline (first 5 squared evens): ${pipeline}`);
    // [4, 16, 36, 64, 100] — all computed lazily!
}

iteratorsGeneratorsDemo();


// ========================================================================
// 1.6  Promises, async/await
// ========================================================================

async function asyncDemo() {
    /**
     * Promises represent eventual completion (or failure) of an async operation.
     *
     * States: pending → fulfilled (resolved) OR rejected
     *
     * async/await is syntactic sugar over Promises:
     *   - async function always returns a Promise
     *   - await pauses execution until the Promise settles
     *
     * Key Methods:
     *   Promise.all([...])        — resolves when ALL resolve, rejects on FIRST rejection
     *   Promise.allSettled([...]) — waits for ALL to settle (never rejects)
     *   Promise.race([...])       — resolves/rejects with the FIRST to settle
     *   Promise.any([...])        — resolves with FIRST fulfillment, rejects if ALL reject
     */

    console.log("\n--- Promises & async/await ---");

    // --- Creating Promises ---
    function delay(ms, value) {
        return new Promise((resolve) => setTimeout(() => resolve(value), ms));
    }

    function failAfter(ms, reason) {
        return new Promise((_, reject) => setTimeout(() => reject(new Error(reason)), ms));
    }

    // --- Basic async/await ---
    const result = await delay(10, "Hello from Promise!");
    console.log(`  await delay: "${result}"`);

    // --- Error handling with try/catch ---
    try {
        await failAfter(10, "Something went wrong");
    } catch (err) {
        console.log(`  Caught error: "${err.message}"`);
    }

    // --- Promise.all (parallel execution) ---
    const startAll = Date.now();
    const [r1, r2, r3] = await Promise.all([
        delay(20, "A"),
        delay(30, "B"),
        delay(10, "C"),
    ]);
    console.log(`  Promise.all: [${r1}, ${r2}, ${r3}] in ~${Date.now() - startAll}ms`);
    // All run concurrently — total time ≈ max(20, 30, 10) = ~30ms

    // --- Promise.allSettled ---
    const settled = await Promise.allSettled([
        delay(10, "success"),
        failAfter(10, "failure"),
        delay(10, "another success"),
    ]);
    console.log(`  Promise.allSettled:`);
    for (const s of settled) {
        if (s.status === "fulfilled") {
            console.log(`    ✅ ${s.value}`);
        } else {
            console.log(`    ❌ ${s.reason.message}`);
        }
    }

    // --- Promise.race ---
    const fastest = await Promise.race([
        delay(30, "slow"),
        delay(10, "fast"),
        delay(20, "medium"),
    ]);
    console.log(`  Promise.race winner: "${fastest}"`);  // "fast"

    // --- Promise chaining (alternative to await) ---
    const chainResult = await Promise.resolve(5)
        .then(x => x * 2)
        .then(x => x + 1)
        .then(x => `Result: ${x}`);
    console.log(`  Promise chain: "${chainResult}"`);  // "Result: 11"

    // --- Sequential vs Parallel ---
    console.log("\n--- Sequential vs Parallel Execution ---");

    // Sequential (bad for independent tasks):
    const seqStart = Date.now();
    await delay(20, "seq1");
    await delay(20, "seq2");
    console.log(`  Sequential: ~${Date.now() - seqStart}ms (waits for each)`);

    // Parallel (good for independent tasks):
    const parStart = Date.now();
    await Promise.all([delay(20, "par1"), delay(20, "par2")]);
    console.log(`  Parallel:   ~${Date.now() - parStart}ms (runs concurrently)`);
}

// Run async demo synchronously for the encyclopedia
asyncDemo().then(() => {


// ========================================================================
// 1.7  Proxies, Reflect, Symbols, Map/Set, WeakMap/WeakSet
// ========================================================================

function advancedFeaturesDemo() {
    /**
     * Advanced JavaScript features for metaprogramming and data management.
     *
     * Proxy: Intercept and customize operations on objects (get, set, delete,
     * has, apply, construct, etc.). The foundation of Vue.js reactivity.
     *
     * Reflect: Provides methods matching Proxy traps. Always returns a boolean
     * for success/failure instead of throwing.
     *
     * Symbol: Unique, immutable identifiers. Used for well-known protocols
     * (Symbol.iterator, Symbol.toPrimitive) and private-ish properties.
     *
     * Map/Set: Hash-based collections. Keys can be ANY type (not just strings).
     * WeakMap/WeakSet: Keys must be objects, and references are WEAK
     * (don't prevent garbage collection).
     */

    console.log("\n--- Proxy & Reflect ---");

    // Validation proxy — enforce type constraints on object properties
    const validator = {
        set(target, prop, value) {
            if (prop === "age") {
                if (typeof value !== "number" || value < 0 || value > 150) {
                    throw new RangeError(`Invalid age: ${value}`);
                }
            }
            return Reflect.set(target, prop, value);
        },
        get(target, prop) {
            if (!(prop in target)) {
                return `[Property "${String(prop)}" not found]`;
            }
            return Reflect.get(target, prop);
        }
    };

    const person = new Proxy({}, validator);
    person.name = "Alice";
    person.age = 30;
    console.log(`  person.name = "${person.name}"`);
    console.log(`  person.age = ${person.age}`);
    console.log(`  person.email = "${person.email}"`);  // Custom "not found" message

    try {
        person.age = -5;   // Throws RangeError
    } catch (e) {
        console.log(`  Validation error: ${e.message}`);
    }

    // Logging proxy — track all property accesses
    function createLogged(target) {
        const accessLog = [];
        const proxy = new Proxy(target, {
            get(t, prop) {
                accessLog.push({ op: "get", prop: String(prop) });
                return Reflect.get(t, prop);
            },
            set(t, prop, value) {
                accessLog.push({ op: "set", prop: String(prop), value });
                return Reflect.set(t, prop, value);
            }
        });
        return { proxy, accessLog };
    }

    const { proxy: logged, accessLog } = createLogged({ x: 1 });
    logged.x;
    logged.y = 2;
    logged.y;
    console.log(`  Access log: ${JSON.stringify(accessLog)}`);

    // --- Symbols ---
    console.log("\n--- Symbols ---");
    const id1 = Symbol("id");
    const id2 = Symbol("id");
    console.log(`  Symbol("id") === Symbol("id"): ${id1 === id2}`);  // false! Always unique

    // Global symbol registry
    const globalSym = Symbol.for("app.config");
    const sameSym = Symbol.for("app.config");
    console.log(`  Symbol.for: same ref? ${globalSym === sameSym}`);  // true

    // Using symbols as "hidden" properties
    const SECRET_KEY = Symbol("secretKey");
    const obj = { name: "public", [SECRET_KEY]: "classified" };
    console.log(`  Object.keys: ${JSON.stringify(Object.keys(obj))}`);       // ["name"]
    console.log(`  Symbol prop:  ${obj[SECRET_KEY]}`);                        // "classified"
    // Symbols don't appear in for...in, Object.keys, or JSON.stringify

    // --- Map & Set ---
    console.log("\n--- Map & Set ---");

    // Map: any type as key, maintains insertion order
    const map = new Map();
    const objKey = { role: "admin" };
    map.set(objKey, "Alice");
    map.set(42, "The Answer");
    map.set("string", "key");
    console.log(`  Map size: ${map.size}`);
    console.log(`  Map.get(objKey): "${map.get(objKey)}"`);
    console.log(`  Map.has(42): ${map.has(42)}`);

    // Iterating a Map
    process.stdout.write("  Map entries: ");
    for (const [key, val] of map) {
        process.stdout.write(`[${typeof key === "object" ? "obj" : key}→${val}] `);
    }
    console.log();

    // Set: unique values, maintains insertion order
    const set = new Set([1, 2, 3, 2, 1, 4, 3, 5]);
    console.log(`  Set from [1,2,3,2,1,4,3,5]: ${[...set]}`);  // [1,2,3,4,5]
    console.log(`  Set.has(3): ${set.has(3)}`);
    // Set operations
    const setA = new Set([1, 2, 3, 4]);
    const setB = new Set([3, 4, 5, 6]);
    const union = new Set([...setA, ...setB]);
    const intersection = new Set([...setA].filter(x => setB.has(x)));
    const difference = new Set([...setA].filter(x => !setB.has(x)));
    console.log(`  Union: ${[...union]}`);
    console.log(`  Intersection: ${[...intersection]}`);
    console.log(`  Difference (A-B): ${[...difference]}`);

    // --- WeakMap / WeakSet ---
    console.log("\n--- WeakMap & WeakSet ---");
    console.log("  WeakMap: Keys must be objects, refs are weak (GC-friendly)");
    console.log("  Use case: Caching data associated with DOM elements or objects");
    console.log("  Use case: Storing private data for class instances");

    const privateData = new WeakMap();
    class User {
        constructor(name, password) {
            this.name = name;
            privateData.set(this, { password }); // Private data linked to instance
        }
        checkPassword(pw) {
            return privateData.get(this).password === pw;
        }
    }
    const u = new User("Alice", "secret123");
    console.log(`  u.name: "${u.name}"`);
    console.log(`  u.checkPassword("secret123"): ${u.checkPassword("secret123")}`);
    console.log(`  u.checkPassword("wrong"):     ${u.checkPassword("wrong")}`);
    // When `u` is garbage collected, its WeakMap entry is automatically removed.
}

advancedFeaturesDemo();


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 2: DATA STRUCTURES (PURE COMPUTER SCIENCE)                   ║
// ╚══════════════════════════════════════════════════════════════════════╝
// Pure implementations of fundamental data structures.
// Every method includes Big-O time and space analysis.


// ========================================================================
// 2.1  Linked Lists — Singly & Doubly Linked Lists
// ========================================================================

class SinglyLinkedListNode {
    /**
     * A single node in a singly linked list.
     * Each node stores a value and a pointer to the next node.
     * Memory: O(1) per node.
     */
    constructor(value, next = null) {
        this.value = value;
        this.next = next;
    }
}

class SinglyLinkedList {
    /**
     * Singly Linked List — a chain of nodes where each node points forward.
     *
     * Real-world use case: Implementing stacks, undo buffers, and simple
     * task queues where insertion at the head is the primary operation.
     *
     * Complexity Summary:
     * | Operation         | Time   | Space |
     * |-------------------|--------|-------|
     * | Insert at head    | O(1)   | O(1)  |
     * | Insert at tail    | O(n)   | O(1)  |
     * | Delete by value   | O(n)   | O(1)  |
     * | Search            | O(n)   | O(1)  |
     * | Traversal         | O(n)   | O(1)  |
     */
    constructor() {
        this.head = null;
        this._size = 0;
    }

    get size() { return this._size; }

    toString() {
        const nodes = [];
        let current = this.head;
        while (current) {
            nodes.push(String(current.value));
            current = current.next;
        }
        return nodes.join(" → ") + " → null";
    }

    /** Insert a new node at the beginning.  O(1) time. */
    insertAtHead(value) {
        this.head = new SinglyLinkedListNode(value, this.head);
        this._size++;
    }

    /** Insert a new node at the end.  O(n) time — must traverse. */
    insertAtTail(value) {
        const newNode = new SinglyLinkedListNode(value);
        if (!this.head) {
            this.head = newNode;
        } else {
            let current = this.head;
            while (current.next) current = current.next;
            current.next = newNode;
        }
        this._size++;
    }

    /**
     * Delete the first node with the given value.
     * Returns true if found and deleted, false otherwise.
     * O(n) time — may need to scan the entire list.
     */
    delete(value) {
        if (!this.head) return false;

        if (this.head.value === value) {
            this.head = this.head.next;
            this._size--;
            return true;
        }

        let current = this.head;
        while (current.next) {
            if (current.next.value === value) {
                current.next = current.next.next;
                this._size--;
                return true;
            }
            current = current.next;
        }
        return false;
    }

    /** Check if a value exists in the list.  O(n) time. */
    search(value) {
        let current = this.head;
        while (current) {
            if (current.value === value) return true;
            current = current.next;
        }
        return false;
    }

    /**
     * Reverse the list in-place.  O(n) time, O(1) space.
     * Algorithm: Three-pointer technique (prev, current, nextNode).
     */
    reverse() {
        let prev = null;
        let current = this.head;
        while (current) {
            const nextNode = current.next;
            current.next = prev;
            prev = current;
            current = nextNode;
        }
        this.head = prev;
    }
}

// --- Demo ---
console.log("\n" + "=".repeat(60));
console.log("SINGLY LINKED LIST DEMO");
console.log("=".repeat(60));
const sll = new SinglyLinkedList();
for (const v of [10, 20, 30, 40]) sll.insertAtTail(v);
console.log(`Original:  ${sll}`);
sll.insertAtHead(5);
console.log(`After insertAtHead(5): ${sll}`);
sll.delete(30);
console.log(`After delete(30):      ${sll}`);
sll.reverse();
console.log(`After reverse():       ${sll}`);
console.log(`Search 20: ${sll.search(20)}, Search 99: ${sll.search(99)}`);


// --- Doubly Linked List ---

class DoublyLinkedListNode {
    /** Node for a doubly linked list — stores prev AND next pointers. */
    constructor(value, prev = null, next = null) {
        this.value = value;
        this.prev = prev;
        this.next = next;
    }
}

class DoublyLinkedList {
    /**
     * Doubly Linked List — nodes have both forward and backward pointers.
     *
     * Advantage over singly linked: O(1) deletion when you have a reference
     * to the node (no need to find the predecessor).
     *
     * Real-world use case: LRU caches, browser history (back/forward),
     * and text editor undo/redo.
     *
     * Complexity Summary:
     * | Operation             | Time | Space |
     * |-----------------------|------|-------|
     * | Insert at head/tail   | O(1) | O(1)  |
     * | Delete given node ref | O(1) | O(1)  |
     * | Delete by value       | O(n) | O(1)  |
     * | Traverse (fwd / bkwd) | O(n) | O(1)  |
     */
    constructor() {
        // Sentinel nodes simplify edge cases (no null checks needed)
        this._sentinelHead = new DoublyLinkedListNode(null);
        this._sentinelTail = new DoublyLinkedListNode(null);
        this._sentinelHead.next = this._sentinelTail;
        this._sentinelTail.prev = this._sentinelHead;
        this._size = 0;
    }

    get size() { return this._size; }

    toString() {
        const nodes = [];
        let current = this._sentinelHead.next;
        while (current !== this._sentinelTail) {
            nodes.push(String(current.value));
            current = current.next;
        }
        return nodes.join(" ⇄ ");
    }

    /** Internal helper: insert between two nodes. O(1). */
    _insertBetween(value, predecessor, successor) {
        const newNode = new DoublyLinkedListNode(value, predecessor, successor);
        predecessor.next = newNode;
        successor.prev = newNode;
        this._size++;
        return newNode;
    }

    /** O(1) insertion at the front. */
    insertAtHead(value) {
        return this._insertBetween(value, this._sentinelHead, this._sentinelHead.next);
    }

    /** O(1) insertion at the back. */
    insertAtTail(value) {
        return this._insertBetween(value, this._sentinelTail.prev, this._sentinelTail);
    }

    /** Remove a node given a direct reference. O(1) time. */
    deleteNode(node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
        this._size--;
    }

    /** Find and remove the first occurrence of value. O(n) time. */
    deleteByValue(value) {
        let current = this._sentinelHead.next;
        while (current !== this._sentinelTail) {
            if (current.value === value) {
                this.deleteNode(current);
                return true;
            }
            current = current.next;
        }
        return false;
    }
}

// --- Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("DOUBLY LINKED LIST DEMO");
console.log("=".repeat(60));
const dll = new DoublyLinkedList();
dll.insertAtTail(10);
dll.insertAtTail(20);
const node30 = dll.insertAtTail(30);
dll.insertAtTail(40);
console.log(`Original: ${dll}`);
dll.deleteNode(node30);
console.log(`After deleting node 30: ${dll}`);
dll.insertAtHead(5);
console.log(`After insertAtHead(5): ${dll}`);


// ========================================================================
// 2.2  Trees — BST, AVL Tree, Trie
// ========================================================================

// -------------------------------------------------------------------
// 2.2.1  Binary Search Tree (BST)
// -------------------------------------------------------------------

class BSTNode {
    constructor(key) {
        this.key = key;
        this.left = null;
        this.right = null;
    }
}

class BinarySearchTree {
    /**
     * Binary Search Tree (BST).
     *
     * Invariant: For every node, all keys in the left subtree are LESS than
     * the node's key, and all keys in the right subtree are GREATER.
     *
     * Complexity (average case — balanced tree):
     * | Operation | Time     | Space  |
     * |-----------|----------|--------|
     * | Insert    | O(log n) | O(1)   |
     * | Search    | O(log n) | O(1)   |
     * | Delete    | O(log n) | O(1)   |
     * | In-order  | O(n)     | O(h)*  |
     *
     * * h = height; O(log n) if balanced, O(n) if degenerate.
     * Worst case (degenerate): All operations degrade to O(n).
     */
    constructor() {
        this.root = null;
    }

    /** Insert a key into the BST.  O(log n) average. */
    insert(key) {
        if (!this.root) { this.root = new BSTNode(key); return; }
        let current = this.root;
        while (true) {
            if (key < current.key) {
                if (!current.left) { current.left = new BSTNode(key); return; }
                current = current.left;
            } else if (key > current.key) {
                if (!current.right) { current.right = new BSTNode(key); return; }
                current = current.right;
            } else {
                return;  // Duplicate keys are not inserted
            }
        }
    }

    /** Search for a key.  O(log n) average. */
    search(key) {
        let current = this.root;
        while (current) {
            if (key === current.key) return true;
            current = key < current.key ? current.left : current.right;
        }
        return false;
    }

    /** In-order traversal → sorted sequence.  O(n) time, O(h) stack. */
    inorder() {
        const result = [];
        const walk = (node) => {
            if (node) {
                walk(node.left);
                result.push(node.key);
                walk(node.right);
            }
        };
        walk(this.root);
        return result;
    }

    /** Find the minimum node in a subtree. */
    _findMin(node) {
        while (node.left) node = node.left;
        return node;
    }

    /**
     * Delete a key from the BST.  O(log n) average.
     * Three cases:
     * 1. Leaf → remove it.
     * 2. One child → replace with child.
     * 3. Two children → replace with in-order successor.
     */
    delete(key) {
        const _delete = (node, key) => {
            if (!node) return node;
            if (key < node.key) {
                node.left = _delete(node.left, key);
            } else if (key > node.key) {
                node.right = _delete(node.right, key);
            } else {
                if (!node.left) return node.right;
                if (!node.right) return node.left;
                const successor = this._findMin(node.right);
                node.key = successor.key;
                node.right = _delete(node.right, successor.key);
            }
            return node;
        };
        this.root = _delete(this.root, key);
    }
}

// --- BST Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("BINARY SEARCH TREE DEMO");
console.log("=".repeat(60));
const bst = new BinarySearchTree();
for (const val of [50, 30, 70, 20, 40, 60, 80]) bst.insert(val);
console.log(`In-order: ${JSON.stringify(bst.inorder())}`);
console.log(`Search 40: ${bst.search(40)}`);
console.log(`Search 99: ${bst.search(99)}`);
bst.delete(30);
console.log(`After deleting 30: ${JSON.stringify(bst.inorder())}`);


// -------------------------------------------------------------------
// 2.2.2  AVL Tree (Self-Balancing BST)
// -------------------------------------------------------------------

class AVLNode {
    constructor(key) {
        this.key = key;
        this.left = null;
        this.right = null;
        this.height = 1;
    }
}

class AVLTree {
    /**
     * AVL Tree — a self-balancing BST (Adelson-Velsky & Landis).
     *
     * The AVL invariant: |height(left) - height(right)| ≤ 1 for every node.
     *
     * Complexity (guaranteed):
     * | Operation | Time     | Space |
     * |-----------|----------|-------|
     * | Insert    | O(log n) | O(1)  |
     * | Search    | O(log n) | O(1)  |
     * | Delete    | O(log n) | O(1)  |
     *
     * Rotations:
     * - Left Rotation:  Fixes Right-Right (RR) imbalance
     * - Right Rotation: Fixes Left-Left (LL) imbalance
     * - Left-Right (LR): Left rotate child, then right rotate node
     * - Right-Left (RL): Right rotate child, then left rotate node
     */
    constructor() {
        this.root = null;
    }

    _height(node) { return node ? node.height : 0; }

    _balanceFactor(node) {
        return node ? this._height(node.left) - this._height(node.right) : 0;
    }

    _updateHeight(node) {
        node.height = 1 + Math.max(this._height(node.left), this._height(node.right));
    }

    /**
     * Right rotation around node z.  O(1) — pointer reassignment.
     *       z                y
     *      / \              / \
     *     y   T4    →     x   z
     *    / \                 / \
     *   x   T3             T3  T4
     */
    _rightRotate(z) {
        const y = z.left;
        const t3 = y.right;
        y.right = z;
        z.left = t3;
        this._updateHeight(z);
        this._updateHeight(y);
        return y;
    }

    /** Left rotation around node z (mirror of right rotation).  O(1). */
    _leftRotate(z) {
        const y = z.right;
        const t2 = y.left;
        y.left = z;
        z.right = t2;
        this._updateHeight(z);
        this._updateHeight(y);
        return y;
    }

    insert(key) { this.root = this._insert(this.root, key); }

    _insert(node, key) {
        if (!node) return new AVLNode(key);
        if (key < node.key) node.left = this._insert(node.left, key);
        else if (key > node.key) node.right = this._insert(node.right, key);
        else return node;

        this._updateHeight(node);
        const bf = this._balanceFactor(node);

        // Left-Left
        if (bf > 1 && key < node.left.key) return this._rightRotate(node);
        // Right-Right
        if (bf < -1 && key > node.right.key) return this._leftRotate(node);
        // Left-Right
        if (bf > 1 && key > node.left.key) {
            node.left = this._leftRotate(node.left);
            return this._rightRotate(node);
        }
        // Right-Left
        if (bf < -1 && key < node.right.key) {
            node.right = this._rightRotate(node.right);
            return this._leftRotate(node);
        }
        return node;
    }

    inorder() {
        const result = [];
        const walk = (node) => {
            if (node) { walk(node.left); result.push(node.key); walk(node.right); }
        };
        walk(this.root);
        return result;
    }
}

// --- AVL Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("AVL TREE DEMO");
console.log("=".repeat(60));
const avl = new AVLTree();
for (const val of [10, 20, 30, 40, 50, 25]) avl.insert(val);
console.log(`In-order (should be sorted): ${JSON.stringify(avl.inorder())}`);
console.log(`Root key: ${avl.root.key} (would be 30 after balancing, not 10)`);


// -------------------------------------------------------------------
// 2.2.3  Trie (Prefix Tree)
// -------------------------------------------------------------------

class TrieNode {
    constructor() {
        this.children = new Map();
        this.isEndOfWord = false;
    }
}

class Trie {
    /**
     * Trie (Prefix Tree) — optimized for prefix-based lookups.
     *
     * Real-world use cases: Autocomplete, spell checkers, IP routing tables.
     *
     * Complexity (for a word of length m):
     * | Operation     | Time | Space |
     * |---------------|------|-------|
     * | Insert        | O(m) | O(m)  |
     * | Search        | O(m) | O(1)  |
     * | Starts-with   | O(m) | O(1)  |
     * | Autocomplete  | O(m + k) where k = number of results |
     */
    constructor() {
        this.root = new TrieNode();
    }

    /** Insert a word into the trie.  O(m). */
    insert(word) {
        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) {
                node.children.set(char, new TrieNode());
            }
            node = node.children.get(char);
        }
        node.isEndOfWord = true;
    }

    /** Check if an exact word exists.  O(m). */
    search(word) {
        const node = this._findNode(word);
        return node !== null && node.isEndOfWord;
    }

    /** Check if any word starts with prefix.  O(m). */
    startsWith(prefix) {
        return this._findNode(prefix) !== null;
    }

    /** Return all words that start with prefix.  O(m + k). */
    autocomplete(prefix) {
        const node = this._findNode(prefix);
        if (!node) return [];
        const results = [];
        this._dfsCollect(node, [...prefix], results);
        return results;
    }

    _findNode(prefix) {
        let node = this.root;
        for (const char of prefix) {
            if (!node.children.has(char)) return null;
            node = node.children.get(char);
        }
        return node;
    }

    _dfsCollect(node, path, results) {
        if (node.isEndOfWord) results.push(path.join(""));
        const sorted = [...node.children.entries()].sort((a, b) => a[0].localeCompare(b[0]));
        for (const [char, child] of sorted) {
            path.push(char);
            this._dfsCollect(child, path, results);
            path.pop();
        }
    }
}

// --- Trie Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("TRIE (PREFIX TREE) DEMO");
console.log("=".repeat(60));
const trie = new Trie();
for (const w of ["apple", "app", "application", "apply", "banana", "band", "bandana"]) {
    trie.insert(w);
}
console.log(`Search 'app':         ${trie.search("app")}`);
console.log(`Search 'application': ${trie.search("application")}`);
console.log(`Search 'apt':         ${trie.search("apt")}`);
console.log(`Starts with 'app':    ${trie.startsWith("app")}`);
console.log(`Autocomplete 'app':   ${JSON.stringify(trie.autocomplete("app"))}`);
console.log(`Autocomplete 'ban':   ${JSON.stringify(trie.autocomplete("ban"))}`);


// ========================================================================
// 2.3  Graphs — Adjacency List & Adjacency Matrix
// ========================================================================

class GraphAdjList {
    /**
     * Graph with adjacency list (Map of Sets).
     *
     * Why adjacency list?
     * - Memory efficient for SPARSE graphs: O(V + E) space.
     * - Fast neighbor iteration: O(degree(v)).
     * - Adding an edge: O(1).
     */
    constructor(directed = false) {
        this._adj = new Map();
        this.directed = directed;
    }

    addVertex(v) {
        if (!this._adj.has(v)) this._adj.set(v, []);
    }

    addEdge(u, v, weight = 1.0) {
        this.addVertex(u);
        this.addVertex(v);
        this._adj.get(u).push([v, weight]);
        if (!this.directed) this._adj.get(v).push([u, weight]);
    }

    neighbors(v) { return this._adj.get(v) || []; }
    vertices() { return [...this._adj.keys()]; }

    toString() {
        const lines = [];
        for (const [v, edges] of [...this._adj.entries()].sort()) {
            lines.push(`  ${v} → ${JSON.stringify(edges)}`);
        }
        return "GraphAdjList:\n" + lines.join("\n");
    }
}

class GraphAdjMatrix {
    /**
     * Graph with adjacency matrix (2D array).
     *
     * Why adjacency matrix?
     * - O(1) edge existence check.
     * - Simpler for dense graphs and matrix-based algorithms.
     * - Memory: O(V²).
     */
    constructor(numVertices) {
        this.n = numVertices;
        this.matrix = Array.from({ length: numVertices }, () =>
            new Array(numVertices).fill(0)
        );
    }

    addEdge(u, v, weight = 1.0, directed = false) {
        this.matrix[u][v] = weight;
        if (!directed) this.matrix[v][u] = weight;
    }

    hasEdge(u, v) { return this.matrix[u][v] !== 0; }

    toString() {
        const rows = this.matrix.map((row, i) => `  ${i}: [${row.join(", ")}]`);
        return "GraphAdjMatrix:\n" + rows.join("\n");
    }
}

// --- Graph Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("GRAPH IMPLEMENTATIONS DEMO");
console.log("=".repeat(60));
const g = new GraphAdjList(false);
g.addEdge("A", "B", 4);
g.addEdge("A", "C", 2);
g.addEdge("B", "D", 3);
g.addEdge("C", "D", 1);
g.addEdge("D", "E", 5);
console.log(g.toString());
console.log(`Neighbors of A: ${JSON.stringify(g.neighbors("A"))}`);

const gm = new GraphAdjMatrix(4);
gm.addEdge(0, 1, 5);
gm.addEdge(1, 2, 3);
gm.addEdge(2, 3, 1);
console.log(`\n${gm}`);
console.log(`Edge 0→1 exists: ${gm.hasEdge(0, 1)}`);
console.log(`Edge 0→3 exists: ${gm.hasEdge(0, 3)}`);


// ========================================================================
// 2.4  Heaps — Min-Heap and Max-Heap from Scratch
// ========================================================================

class MinHeap {
    /**
     * Min-Heap — complete binary tree where each parent ≤ its children.
     *
     * Array-based: For node at index i:
     *   Parent:      Math.floor((i - 1) / 2)
     *   Left child:  2*i + 1
     *   Right child: 2*i + 2
     *
     * Complexity:
     * | Operation     | Time     | Space |
     * |---------------|----------|-------|
     * | Insert (push) | O(log n) | O(1)  |
     * | Extract min   | O(log n) | O(1)  |
     * | Peek min      | O(1)     | O(1)  |
     * | Heapify array | O(n)     | O(1)  |
     */
    constructor() {
        this._data = [];
    }

    get size() { return this._data.length; }

    toString() { return `MinHeap(${JSON.stringify(this._data)})`; }

    _parent(i) { return Math.floor((i - 1) / 2); }
    _left(i) { return 2 * i + 1; }
    _right(i) { return 2 * i + 2; }

    _swap(i, j) {
        [this._data[i], this._data[j]] = [this._data[j], this._data[i]];
    }

    _siftUp(i) {
        while (i > 0) {
            const parent = this._parent(i);
            if (this._data[i] < this._data[parent]) {
                this._swap(i, parent);
                i = parent;
            } else break;
        }
    }

    _siftDown(i) {
        const size = this._data.length;
        while (true) {
            let smallest = i;
            const left = this._left(i);
            const right = this._right(i);
            if (left < size && this._data[left] < this._data[smallest]) smallest = left;
            if (right < size && this._data[right] < this._data[smallest]) smallest = right;
            if (smallest !== i) {
                this._swap(i, smallest);
                i = smallest;
            } else break;
        }
    }

    /** Insert a value.  O(log n). */
    push(value) {
        this._data.push(value);
        this._siftUp(this._data.length - 1);
    }

    /** Remove and return the minimum.  O(log n). */
    pop() {
        if (!this._data.length) throw new Error("pop from empty heap");
        this._swap(0, this._data.length - 1);
        const minVal = this._data.pop();
        if (this._data.length) this._siftDown(0);
        return minVal;
    }

    /** Return the minimum without removing.  O(1). */
    peek() {
        if (!this._data.length) throw new Error("peek at empty heap");
        return this._data[0];
    }

    /** Build a heap from an array in O(n) time. */
    static heapify(arr) {
        const heap = new MinHeap();
        heap._data = [...arr];
        for (let i = Math.floor(heap._data.length / 2) - 1; i >= 0; i--) {
            heap._siftDown(i);
        }
        return heap;
    }
}

class MaxHeap {
    /** Max-Heap — wraps MinHeap by negating values. O(1) overhead per operation. */
    constructor() { this._heap = new MinHeap(); }
    get size() { return this._heap.size; }
    push(value) { this._heap.push(-value); }
    pop() { return -this._heap.pop(); }
    peek() { return -this._heap.peek(); }
}

// --- Heap Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("MIN-HEAP & MAX-HEAP DEMO");
console.log("=".repeat(60));
const mh = new MinHeap();
for (const v of [15, 10, 20, 8, 25, 5]) mh.push(v);
console.log(`MinHeap after insertions: ${mh}`);
console.log(`Peek min: ${mh.peek()}`);
process.stdout.write("Pop sequence: ");
while (mh.size) process.stdout.write(`${mh.pop()} `);
console.log();

const h2 = MinHeap.heapify([40, 10, 30, 20, 50]);
console.log(`Heapified: ${h2}`);

const maxh = new MaxHeap();
for (const v of [15, 10, 20, 8, 25, 5]) maxh.push(v);
process.stdout.write("MaxHeap pop sequence: ");
while (maxh.size) process.stdout.write(`${maxh.pop()} `);
console.log();


// ========================================================================
// 2.5  Hash Maps — Custom Hash Table with Collision Resolution
// ========================================================================

class HashTableChaining {
    /**
     * Hash Table using SEPARATE CHAINING for collision resolution.
     *
     * How: hash(key) % capacity → bucket index. Each bucket is an array
     * of [key, value] pairs. Resize when load factor > 0.75.
     *
     * Complexity (amortized, with good hash function):
     * | Operation | Average | Worst Case |
     * |-----------|---------|------------|
     * | Insert    | O(1)    | O(n)       |
     * | Lookup    | O(1)    | O(n)       |
     * | Delete    | O(1)    | O(n)       |
     */
    constructor(capacity = 8) {
        this._capacity = capacity;
        this._size = 0;
        this._buckets = Array.from({ length: capacity }, () => []);
    }

    get size() { return this._size; }

    _hash(key) {
        // Simple string hash (DJB2 algorithm)
        const str = String(key);
        let hash = 5381;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) + hash + str.charCodeAt(i)) & 0x7fffffff;
        }
        return hash % this._capacity;
    }

    _resize() {
        const oldBuckets = this._buckets;
        this._capacity *= 2;
        this._buckets = Array.from({ length: this._capacity }, () => []);
        this._size = 0;
        for (const bucket of oldBuckets) {
            for (const [key, value] of bucket) {
                this.put(key, value);
            }
        }
    }

    put(key, value) {
        const idx = this._hash(key);
        const bucket = this._buckets[idx];
        for (let i = 0; i < bucket.length; i++) {
            if (bucket[i][0] === key) {
                bucket[i][1] = value;
                return;
            }
        }
        bucket.push([key, value]);
        this._size++;
        if (this._size / this._capacity > 0.75) this._resize();
    }

    get(key, defaultVal = undefined) {
        const idx = this._hash(key);
        for (const [k, v] of this._buckets[idx]) {
            if (k === key) return v;
        }
        return defaultVal;
    }

    delete(key) {
        const idx = this._hash(key);
        const bucket = this._buckets[idx];
        for (let i = 0; i < bucket.length; i++) {
            if (bucket[i][0] === key) {
                bucket.splice(i, 1);
                this._size--;
                return true;
            }
        }
        return false;
    }

    toString() {
        const items = [];
        for (const bucket of this._buckets) {
            for (const [k, v] of bucket) items.push(`${JSON.stringify(k)}: ${JSON.stringify(v)}`);
        }
        return `HashTable({${items.join(", ")}})`;
    }
}

class HashTableOpenAddressing {
    /**
     * Hash Table using OPEN ADDRESSING (Linear Probing).
     *
     * Trade-offs vs Chaining:
     * + Better cache locality (contiguous array).
     * + No linked list overhead.
     * - Clustering can degrade performance.
     * - Deletion needs DELETED sentinels.
     */
    static EMPTY = Symbol("EMPTY");
    static DELETED = Symbol("DELETED");

    constructor(capacity = 8) {
        this._capacity = capacity;
        this._size = 0;
        this._keys = new Array(capacity).fill(HashTableOpenAddressing.EMPTY);
        this._values = new Array(capacity).fill(null);
    }

    get size() { return this._size; }

    _hash(key) {
        const str = String(key);
        let hash = 5381;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) + hash + str.charCodeAt(i)) & 0x7fffffff;
        }
        return hash % this._capacity;
    }

    *_probe(key) {
        let idx = this._hash(key);
        for (let i = 0; i < this._capacity; i++) {
            yield idx;
            idx = (idx + 1) % this._capacity;
        }
    }

    put(key, value) {
        if (this._size / this._capacity > 0.6) this._resize();
        let firstDeleted = null;
        for (const idx of this._probe(key)) {
            if (this._keys[idx] === HashTableOpenAddressing.EMPTY) {
                const target = firstDeleted !== null ? firstDeleted : idx;
                this._keys[target] = key;
                this._values[target] = value;
                this._size++;
                return;
            } else if (this._keys[idx] === HashTableOpenAddressing.DELETED) {
                if (firstDeleted === null) firstDeleted = idx;
            } else if (this._keys[idx] === key) {
                this._values[idx] = value;
                return;
            }
        }
    }

    get(key, defaultVal = undefined) {
        for (const idx of this._probe(key)) {
            if (this._keys[idx] === HashTableOpenAddressing.EMPTY) return defaultVal;
            if (this._keys[idx] !== HashTableOpenAddressing.DELETED && this._keys[idx] === key) {
                return this._values[idx];
            }
        }
        return defaultVal;
    }

    delete(key) {
        for (const idx of this._probe(key)) {
            if (this._keys[idx] === HashTableOpenAddressing.EMPTY) return false;
            if (this._keys[idx] !== HashTableOpenAddressing.DELETED && this._keys[idx] === key) {
                this._keys[idx] = HashTableOpenAddressing.DELETED;
                this._values[idx] = null;
                this._size--;
                return true;
            }
        }
        return false;
    }

    _resize() {
        const oldKeys = this._keys;
        const oldValues = this._values;
        this._capacity *= 2;
        this._keys = new Array(this._capacity).fill(HashTableOpenAddressing.EMPTY);
        this._values = new Array(this._capacity).fill(null);
        this._size = 0;
        for (let i = 0; i < oldKeys.length; i++) {
            if (oldKeys[i] !== HashTableOpenAddressing.EMPTY &&
                oldKeys[i] !== HashTableOpenAddressing.DELETED) {
                this.put(oldKeys[i], oldValues[i]);
            }
        }
    }
}

// --- Hash Table Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("HASH TABLE DEMO");
console.log("=".repeat(60));
const ht = new HashTableChaining();
ht.put("name", "Alice");
ht.put("age", 30);
ht.put("city", "NYC");
console.log(`Chaining: ${ht}`);
console.log(`get('name') = ${ht.get("name")}`);
ht.delete("age");
console.log(`After deleting 'age': ${ht}`);

const ht2 = new HashTableOpenAddressing();
ht2.put("x", 10);
ht2.put("y", 20);
ht2.put("z", 30);
console.log(`\nOpen Addressing: get('y') = ${ht2.get("y")}`);
ht2.delete("y");
console.log(`After deleting 'y': get('y') = ${ht2.get("y")}`);
console.log(`get('z') still works: ${ht2.get("z")}`);


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 3: ALGORITHMIC MASTERY & DYNAMIC PROGRAMMING                 ║
// ╚══════════════════════════════════════════════════════════════════════╝


// ========================================================================
// 3.1  Sorting Algorithms
// ========================================================================

/**
 * QuickSort — Divide and Conquer.
 * Best/Average: O(n log n), Worst: O(n²). Space: O(log n).
 * Not stable. Worst case: sorted input (pivot = min/max every time).
 * @param {number[]} arr
 * @returns {number[]}
 */
function quicksort(arr) {
    if (arr.length <= 1) return arr;
    const pivot = arr[arr.length - 1];
    const left = arr.slice(0, -1).filter(x => x <= pivot);
    const right = arr.slice(0, -1).filter(x => x > pivot);
    return [...quicksort(left), pivot, ...quicksort(right)];
}

/**
 * MergeSort — Stable, always O(n log n). Space: O(n).
 * @param {number[]} arr
 * @returns {number[]}
 */
function mergeSort(arr) {
    if (arr.length <= 1) return arr;
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));
    const merged = [];
    let i = 0, j = 0;
    while (i < left.length && j < right.length) {
        if (left[i] <= right[j]) merged.push(left[i++]);
        else merged.push(right[j++]);
    }
    return [...merged, ...left.slice(i), ...right.slice(j)];
}

/**
 * HeapSort — In-place, O(n log n), O(1) space. Not stable.
 * @param {number[]} arr
 * @returns {number[]}
 */
function heapsort(arr) {
    const result = [...arr];
    const n = result.length;

    function siftDown(heap, size, root) {
        let largest = root;
        const left = 2 * root + 1;
        const right = 2 * root + 2;
        if (left < size && heap[left] > heap[largest]) largest = left;
        if (right < size && heap[right] > heap[largest]) largest = right;
        if (largest !== root) {
            [heap[root], heap[largest]] = [heap[largest], heap[root]];
            siftDown(heap, size, largest);
        }
    }

    // Build max-heap
    for (let i = Math.floor(n / 2) - 1; i >= 0; i--) siftDown(result, n, i);
    // Extract elements
    for (let i = n - 1; i > 0; i--) {
        [result[0], result[i]] = [result[i], result[0]];
        siftDown(result, i, 0);
    }
    return result;
}

/**
 * RadixSort — Non-comparison sort for non-negative integers.
 * Time: O(d × n), Space: O(n). Where d = number of digits.
 * @param {number[]} arr
 * @returns {number[]}
 */
function radixSort(arr) {
    if (!arr.length) return arr;
    const maxVal = Math.max(...arr);
    let result = [...arr];
    let exp = 1;

    while (Math.floor(maxVal / exp) > 0) {
        const count = new Array(10).fill(0);
        const output = new Array(result.length).fill(0);

        for (const num of result) count[Math.floor(num / exp) % 10]++;
        for (let i = 1; i < 10; i++) count[i] += count[i - 1];
        for (let i = result.length - 1; i >= 0; i--) {
            const digit = Math.floor(result[i] / exp) % 10;
            count[digit]--;
            output[count[digit]] = result[i];
        }
        result = output;
        exp *= 10;
    }
    return result;
}

// --- Sorting Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("SORTING ALGORITHMS DEMO");
console.log("=".repeat(60));
const testArr = Array.from({ length: 15 }, () => Math.floor(Math.random() * 100) + 1);
console.log(`Original:   ${JSON.stringify(testArr)}`);
console.log(`QuickSort:  ${JSON.stringify(quicksort(testArr))}`);
console.log(`MergeSort:  ${JSON.stringify(mergeSort(testArr))}`);
console.log(`HeapSort:   ${JSON.stringify(heapsort(testArr))}`);
console.log(`RadixSort:  ${JSON.stringify(radixSort(testArr.map(Math.abs)))}`);


// ========================================================================
// 3.2  Searching — Binary Search, BFS, DFS
// ========================================================================

/**
 * Binary Search on a SORTED array.
 * Time: O(log n). Space: O(1).
 * @param {number[]} arr - Sorted array
 * @param {number} target
 * @returns {number} Index of target, or -1 if not found
 */
function binarySearch(arr, target) {
    let low = 0, high = arr.length - 1;
    while (low <= high) {
        const mid = Math.floor((low + high) / 2);
        if (arr[mid] === target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

/**
 * BFS — Breadth-First Search. O(V + E) time, O(V) space.
 * @param {Object} graph - Adjacency list as { vertex: [neighbors] }
 * @param {string} start
 * @returns {string[]}
 */
function bfs(graph, start) {
    const visited = new Set();
    const order = [];
    const queue = [start];
    visited.add(start);

    while (queue.length) {
        const vertex = queue.shift();
        order.push(vertex);
        for (const neighbor of (graph[vertex] || [])) {
            if (!visited.has(neighbor)) {
                visited.add(neighbor);
                queue.push(neighbor);
            }
        }
    }
    return order;
}

/**
 * DFS — Depth-First Search (iterative). O(V + E) time, O(V) space.
 * @param {Object} graph
 * @param {string} start
 * @returns {string[]}
 */
function dfs(graph, start) {
    const visited = new Set();
    const order = [];
    const stack = [start];

    while (stack.length) {
        const vertex = stack.pop();
        if (!visited.has(vertex)) {
            visited.add(vertex);
            order.push(vertex);
            for (const neighbor of (graph[vertex] || []).slice().reverse()) {
                if (!visited.has(neighbor)) stack.push(neighbor);
            }
        }
    }
    return order;
}

// --- Searching Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("SEARCHING ALGORITHMS DEMO");
console.log("=".repeat(60));
const sortedArr = Array.from({ length: 20 }, (_, i) => i * 5);
console.log(`Binary search for 35 in [${sortedArr}]: index = ${binarySearch(sortedArr, 35)}`);
console.log(`Binary search for 37: index = ${binarySearch(sortedArr, 37)}`);

const graphDict = {
    A: ["B", "C"], B: ["A", "D", "E"], C: ["A", "F"],
    D: ["B"], E: ["B", "F"], F: ["C", "E"],
};
console.log(`\nBFS from A: ${JSON.stringify(bfs(graphDict, "A"))}`);
console.log(`DFS from A: ${JSON.stringify(dfs(graphDict, "A"))}`);


// ========================================================================
// 3.3  Pathfinding — Dijkstra's & A*
// ========================================================================

/**
 * Dijkstra's Algorithm — shortest paths with NON-NEGATIVE weights.
 * Time: O((V + E) log V) with a binary heap. Space: O(V).
 */
function dijkstra(graph, start, end = null) {
    const distances = {};
    const predecessors = {};
    for (const v of Object.keys(graph)) {
        distances[v] = Infinity;
        predecessors[v] = null;
    }
    distances[start] = 0;

    // Simple priority queue using sorted insertions
    const pq = [[0, start]];

    while (pq.length) {
        pq.sort((a, b) => a[0] - b[0]);
        const [currentDist, u] = pq.shift();
        if (currentDist > distances[u]) continue;

        for (const [neighbor, weight] of graph[u]) {
            const newDist = currentDist + weight;
            if (newDist < distances[neighbor]) {
                distances[neighbor] = newDist;
                predecessors[neighbor] = u;
                pq.push([newDist, neighbor]);
            }
        }
    }

    let path = [];
    if (end !== null) {
        let node = end;
        while (node !== null) {
            path.push(node);
            node = predecessors[node];
        }
        path.reverse();
    }
    return { distances, path };
}

/**
 * A* Algorithm — informed search using heuristic.
 * Time: O(E log V) worst case. In practice, much faster with good heuristic.
 */
function aStar(graph, start, goal, heuristic) {
    const openSet = [[heuristic[start] || 0, 0, start]];
    const gScores = { [start]: 0 };
    const cameFrom = {};
    const closedSet = new Set();

    while (openSet.length) {
        openSet.sort((a, b) => a[0] - b[0]);
        const [, gScore, current] = openSet.shift();

        if (current === goal) {
            const path = [];
            let node = goal;
            while (node in cameFrom) { path.push(node); node = cameFrom[node]; }
            path.push(start);
            path.reverse();
            return { cost: gScore, path };
        }

        if (closedSet.has(current)) continue;
        closedSet.add(current);

        for (const [neighbor, weight] of (graph[current] || [])) {
            if (closedSet.has(neighbor)) continue;
            const tentativeG = gScore + weight;
            if (tentativeG < (gScores[neighbor] ?? Infinity)) {
                gScores[neighbor] = tentativeG;
                cameFrom[neighbor] = current;
                const f = tentativeG + (heuristic[neighbor] || 0);
                openSet.push([f, tentativeG, neighbor]);
            }
        }
    }
    return { cost: Infinity, path: [] };
}

// --- Pathfinding Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("PATHFINDING DEMO");
console.log("=".repeat(60));
const weightedGraph = {
    A: [["B", 4], ["C", 2]], B: [["A", 4], ["D", 3], ["E", 1]],
    C: [["A", 2], ["D", 5]], D: [["B", 3], ["C", 5], ["E", 2], ["F", 6]],
    E: [["B", 1], ["D", 2], ["F", 4]], F: [["D", 6], ["E", 4]],
};
const dResult = dijkstra(weightedGraph, "A", "F");
console.log(`Dijkstra A→F: distance = ${dResult.distances.F}, path = ${JSON.stringify(dResult.path)}`);
console.log(`All distances from A: ${JSON.stringify(dResult.distances)}`);

const heuristic = { A: 7, B: 4, C: 6, D: 3, E: 2, F: 0 };
const aResult = aStar(weightedGraph, "A", "F", heuristic);
console.log(`\nA* search A→F: cost = ${aResult.cost}, path = ${JSON.stringify(aResult.path)}`);


// ========================================================================
// 3.4  Dynamic Programming — Fibonacci, 0/1 Knapsack, LCS
// ========================================================================

function fibonacciDemo() {
    /**
     * DP applied to the Fibonacci sequence.
     * Three approaches with increasing sophistication.
     */

    // Approach 1: Naive Recursion — O(2^n) time, O(n) space
    function fibNaive(n) {
        if (n <= 1) return n;
        return fibNaive(n - 1) + fibNaive(n - 2);
    }

    // Approach 2: Memoization (Top-Down DP) — O(n) time, O(n) space
    function fibMemo(n, memo = {}) {
        if (n in memo) return memo[n];
        if (n <= 1) return n;
        memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
        return memo[n];
    }

    // Approach 3: Tabulation (Bottom-Up DP) — O(n) time, O(1) space
    function fibTab(n) {
        if (n <= 1) return n;
        let prev2 = 0, prev1 = 1;
        for (let i = 2; i <= n; i++) [prev2, prev1] = [prev1, prev2 + prev1];
        return prev1;
    }

    console.log("\nFibonacci Comparison:");
    for (const n of [5, 10, 20, 30]) {
        const memoResult = fibMemo(n);
        const tabResult = fibTab(n);
        console.log(`  F(${String(n).padStart(2)}) = ${String(tabResult).padStart(10)}  (memo == tab: ${memoResult === tabResult})`);
    }
}

fibonacciDemo();

/**
 * 0/1 Knapsack Problem — Classic DP.
 * Time: O(n × W). Space: O(n × W).
 */
function knapsack01(weights, values, capacity) {
    const n = weights.length;
    const dp = Array.from({ length: n + 1 }, () => new Array(capacity + 1).fill(0));

    for (let i = 1; i <= n; i++) {
        for (let w = 0; w <= capacity; w++) {
            dp[i][w] = dp[i - 1][w];
            if (weights[i - 1] <= w) {
                const take = dp[i - 1][w - weights[i - 1]] + values[i - 1];
                dp[i][w] = Math.max(dp[i][w], take);
            }
        }
    }

    // Backtrack
    const selected = [];
    let w = capacity;
    for (let i = n; i > 0; i--) {
        if (dp[i][w] !== dp[i - 1][w]) {
            selected.push(i - 1);
            w -= weights[i - 1];
        }
    }
    selected.reverse();
    return { maxValue: dp[n][capacity], selected };
}

console.log(`\n${"=".repeat(60)}`);
console.log("0/1 KNAPSACK PROBLEM");
console.log("=".repeat(60));
const kWeights = [2, 3, 4, 5];
const kValues = [3, 4, 5, 6];
const kCapacity = 8;
const kResult = knapsack01(kWeights, kValues, kCapacity);
console.log(`Items:    weights=${JSON.stringify(kWeights)}, values=${JSON.stringify(kValues)}`);
console.log(`Capacity: ${kCapacity}`);
console.log(`Max value: ${kResult.maxValue}, selected indices: ${JSON.stringify(kResult.selected)}`);
for (const idx of kResult.selected) {
    console.log(`  Item ${idx}: weight=${kWeights[idx]}, value=${kValues[idx]}`);
}

/**
 * Longest Common Subsequence (LCS).
 * Time: O(m × n). Space: O(m × n).
 */
function longestCommonSubsequence(s1, s2) {
    const m = s1.length, n = s2.length;
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (s1[i - 1] === s2[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
            else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
        }
    }

    // Backtrack
    const lcs = [];
    let i = m, j = n;
    while (i > 0 && j > 0) {
        if (s1[i - 1] === s2[j - 1]) { lcs.push(s1[i - 1]); i--; j--; }
        else if (dp[i - 1][j] > dp[i][j - 1]) i--;
        else j--;
    }
    lcs.reverse();
    return { length: dp[m][n], lcs: lcs.join("") };
}

console.log(`\n${"=".repeat(60)}`);
console.log("LONGEST COMMON SUBSEQUENCE");
console.log("=".repeat(60));
const lcsS1 = "ABCBDAB", lcsS2 = "BDCAB";
const lcsResult = longestCommonSubsequence(lcsS1, lcsS2);
console.log(`s1 = "${lcsS1}"`);
console.log(`s2 = "${lcsS2}"`);
console.log(`LCS length = ${lcsResult.length}, LCS = "${lcsResult.lcs}"`);


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 4: SOFTWARE ARCHITECTURE & DESIGN PATTERNS (Gang of Four)    ║
// ╚══════════════════════════════════════════════════════════════════════╝


// ========================================================================
// 4.1  Creational Patterns — Singleton, Factory Method, Builder
// ========================================================================

// -------------------------------------------------------------------
// 4.1.1  Singleton Pattern
// -------------------------------------------------------------------

class DatabaseConnection {
    /**
     * Singleton — ensures a class has only ONE instance.
     *
     * Uses a static instance field. The constructor checks if an instance
     * already exists and returns it if so.
     *
     * Real-world: DB connection pools, logging, config managers.
     */
    static _instance = null;

    constructor(host = "localhost", port = 5432) {
        if (DatabaseConnection._instance) {
            return DatabaseConnection._instance;
        }
        this.host = host;
        this.port = port;
        this._connected = true;
        console.log(`  [Singleton] Created connection to ${host}:${port}`);
        DatabaseConnection._instance = this;
    }

    query(sql) { return `  [DB] Executing: ${sql}`; }

    static resetInstance() { DatabaseConnection._instance = null; }
}

// --- Singleton Demo ---
console.log(`\n${"=".repeat(60)}`);
console.log("SINGLETON PATTERN DEMO");
console.log("=".repeat(60));
DatabaseConnection.resetInstance();
const db1 = new DatabaseConnection("prod-server", 5432);
const db2 = new DatabaseConnection("other-server", 3306);
console.log(`db1 === db2: ${db1 === db2}`);
console.log(`db1.host: ${db1.host}`);
console.log(db1.query("SELECT * FROM users"));

// -------------------------------------------------------------------
// 4.1.2  Factory Method Pattern
// -------------------------------------------------------------------

class Notification {
    send(message) { throw new Error("send() must be implemented"); }
}

class EmailNotification extends Notification {
    send(message) { return `  📧 Email: ${message}`; }
}

class SMSNotification extends Notification {
    send(message) { return `  📱 SMS: ${message}`; }
}

class PushNotification extends Notification {
    send(message) { return `  🔔 Push: ${message}`; }
}

class NotificationFactory {
    /**
     * Factory — creates the right notification type based on a string key.
     * Client code doesn't need to know about concrete classes.
     */
    static _creators = {
        email: EmailNotification,
        sms: SMSNotification,
        push: PushNotification,
    };

    static create(channel) {
        const Creator = this._creators[channel.toLowerCase()];
        if (!Creator) throw new Error(`Unknown channel: "${channel}"`);
        return new Creator();
    }

    static register(channel, creatorClass) {
        this._creators[channel.toLowerCase()] = creatorClass;
    }
}

console.log(`\n${"=".repeat(60)}`);
console.log("FACTORY METHOD PATTERN DEMO");
console.log("=".repeat(60));
for (const channel of ["email", "sms", "push"]) {
    const notif = NotificationFactory.create(channel);
    console.log(notif.send(`Hello from ${channel}!`));
}

// -------------------------------------------------------------------
// 4.1.3  Builder Pattern
// -------------------------------------------------------------------

class HTTPRequest {
    /**
     * Builder — separates construction of complex objects from representation.
     * Uses method chaining (fluent interface).
     */
    constructor() {
        this.method = "GET";
        this.url = "";
        this.headers = {};
        this.body = null;
        this.timeout = 30;
    }

    setMethod(method) { this.method = method.toUpperCase(); return this; }
    setUrl(url) { this.url = url; return this; }
    addHeader(key, value) { this.headers[key] = value; return this; }
    setBody(body) { this.body = body; return this; }
    setTimeout(seconds) { this.timeout = seconds; return this; }

    build() {
        if (!this.url) throw new Error("URL is required");
        return { ...this };  // Return a plain object snapshot
    }

    toString() {
        return `HTTPRequest(method=${this.method}, url=${this.url}, ` +
            `headers=${JSON.stringify(this.headers)}, body=${this.body}, timeout=${this.timeout})`;
    }
}

console.log(`\n${"=".repeat(60)}`);
console.log("BUILDER PATTERN DEMO");
console.log("=".repeat(60));
const request = new HTTPRequest()
    .setMethod("POST")
    .setUrl("https://api.example.com/data")
    .addHeader("Authorization", "Bearer token123")
    .addHeader("Content-Type", "application/json")
    .setBody('{"user": "alice", "action": "login"}')
    .setTimeout(10);
console.log(`Built request: ${request}`);


// ========================================================================
// 4.2  Structural Patterns — Adapter, Decorator, Facade
// ========================================================================

// -------------------------------------------------------------------
// 4.2.1  Adapter Pattern
// -------------------------------------------------------------------

class LegacyPrinter {
    printDocument(text) { return `  [Legacy Printer] ${text}`; }
}

class PrinterAdapter {
    /**
     * Adapter — wraps a legacy class to match a modern interface.
     * Lets incompatible interfaces work together.
     */
    constructor(legacyPrinter) { this._printer = legacyPrinter; }
    output(content) { return this._printer.printDocument(content); }
}

console.log(`\n${"=".repeat(60)}`);
console.log("ADAPTER PATTERN DEMO");
console.log("=".repeat(60));
const legacy = new LegacyPrinter();
const adapted = new PrinterAdapter(legacy);
console.log(adapted.output("Adapter converts interfaces seamlessly"));

// -------------------------------------------------------------------
// 4.2.2  Decorator Pattern
// -------------------------------------------------------------------

class FileDataSource {
    constructor() { this._data = ""; }
    write(data) { this._data = data; return `  [File] Wrote: "${data}"`; }
    read() { return this._data; }
}

class DataSourceDecorator {
    /**
     * Decorator — attach additional responsibilities dynamically.
     * Flexible alternative to subclassing.
     */
    constructor(source) { this._wrapped = source; }
    write(data) { return this._wrapped.write(data); }
    read() { return this._wrapped.read(); }
}

class EncryptionDecorator extends DataSourceDecorator {
    /** Simple ROT13 "encryption" for demonstration. */
    write(data) {
        const encrypted = data.replace(/[a-zA-Z]/g, c => {
            const base = c <= "Z" ? 65 : 97;
            return String.fromCharCode(((c.charCodeAt(0) - base + 13) % 26) + base);
        });
        console.log("  [Encryption] Encrypting data before write");
        return super.write(encrypted);
    }
    read() {
        const data = super.read();
        return data.replace(/[a-zA-Z]/g, c => {
            const base = c <= "Z" ? 65 : 97;
            return String.fromCharCode(((c.charCodeAt(0) - base + 13) % 26) + base);
        });
    }
}

class CompressionDecorator extends DataSourceDecorator {
    /** Simulated compression (removes spaces). */
    write(data) {
        console.log("  [Compression] Compressing data before write");
        return super.write(data.replace(/ /g, ""));
    }
    read() { return super.read(); }
}

console.log(`\n${"=".repeat(60)}`);
console.log("DECORATOR PATTERN DEMO");
console.log("=".repeat(60));
const source = new CompressionDecorator(new EncryptionDecorator(new FileDataSource()));
console.log(source.write("Hello World Secret Data"));
console.log(`  Reading back: "${source.read()}"`);

// -------------------------------------------------------------------
// 4.2.3  Facade Pattern
// -------------------------------------------------------------------

class CPU {
    freeze() { return "  [CPU] Freezing processor"; }
    jump(addr) { return `  [CPU] Jumping to 0x${addr.toString(16).padStart(8, "0").toUpperCase()}`; }
    execute() { return "  [CPU] Executing instructions"; }
}

class Memory {
    load(addr, data) { return `  [Memory] Loading "${data}" at 0x${addr.toString(16).padStart(8, "0").toUpperCase()}`; }
}

class HardDrive {
    read(sector, size) { return `  [HDD] Reading ${size} bytes from sector ${sector}`; }
}

class ComputerFacade {
    /**
     * Facade — simplified interface to a complex subsystem.
     */
    constructor() {
        this._cpu = new CPU();
        this._memory = new Memory();
        this._hdd = new HardDrive();
    }

    start() {
        console.log(this._cpu.freeze());
        console.log(this._hdd.read(0, 1024));
        console.log(this._memory.load(0, "boot sector"));
        console.log(this._cpu.jump(0));
        console.log(this._cpu.execute());
        console.log("  [Facade] Computer started successfully!");
    }
}

console.log(`\n${"=".repeat(60)}`);
console.log("FACADE PATTERN DEMO");
console.log("=".repeat(60));
const computer = new ComputerFacade();
computer.start();


// ========================================================================
// 4.3  Behavioral Patterns — Observer, Strategy, Command
// ========================================================================

// -------------------------------------------------------------------
// 4.3.1  Observer Pattern (Pub/Sub)
// -------------------------------------------------------------------

class EventManager {
    /**
     * Observer (Pub/Sub) — decouples event producers from consumers.
     * One-to-many dependency: when subject changes, all dependents are notified.
     */
    constructor() { this._listeners = new Map(); }

    subscribe(eventType, listener) {
        if (!this._listeners.has(eventType)) this._listeners.set(eventType, []);
        this._listeners.get(eventType).push(listener);
    }

    unsubscribe(eventType, listener) {
        const listeners = this._listeners.get(eventType);
        if (listeners) {
            const idx = listeners.indexOf(listener);
            if (idx !== -1) listeners.splice(idx, 1);
        }
    }

    notify(eventType, data = null) {
        for (const listener of (this._listeners.get(eventType) || [])) {
            listener(eventType, data);
        }
    }
}

class UserService {
    constructor(events) { this.events = events; }
    createUser(username) {
        console.log(`  [UserService] Created user: ${username}`);
        this.events.notify("user_created", { username });
    }
    deleteUser(username) {
        console.log(`  [UserService] Deleted user: ${username}`);
        this.events.notify("user_deleted", { username });
    }
}

console.log(`\n${"=".repeat(60)}`);
console.log("OBSERVER (PUB/SUB) PATTERN DEMO");
console.log("=".repeat(60));
const events = new EventManager();
const logListener = (event, data) => console.log(`  [Logger] Event: ${event}, Data: ${JSON.stringify(data)}`);
const emailListener = (event, data) => console.log(`  [Email] Sending welcome email to ${data.username}`);
events.subscribe("user_created", logListener);
events.subscribe("user_created", emailListener);
events.subscribe("user_deleted", logListener);
const userService = new UserService(events);
userService.createUser("alice");
userService.deleteUser("bob");

// -------------------------------------------------------------------
// 4.3.2  Strategy Pattern
// -------------------------------------------------------------------

class DataProcessor {
    /**
     * Strategy — select algorithm at runtime via a function.
     * In JS, functions are first-class, so strategies are just functions.
     */
    constructor(data, strategy) {
        this.data = data;
        this._strategy = strategy;
    }
    setStrategy(strategy) { this._strategy = strategy; }
    execute() { return this._strategy(this.data); }
}

const meanStrategy = (data) => data.reduce((a, b) => a + b, 0) / data.length;
const medianStrategy = (data) => {
    const sorted = [...data].sort((a, b) => a - b);
    const n = sorted.length;
    return n % 2 === 0 ? (sorted[n / 2 - 1] + sorted[n / 2]) / 2 : sorted[Math.floor(n / 2)];
};
const modeStrategy = (data) => {
    const counts = new Map();
    for (const v of data) counts.set(v, (counts.get(v) || 0) + 1);
    return [...counts.entries()].sort((a, b) => b[1] - a[1])[0][0];
};

console.log(`\n${"=".repeat(60)}`);
console.log("STRATEGY PATTERN DEMO");
console.log("=".repeat(60));
const processorData = [4.0, 1.0, 2.0, 2.0, 3.0, 5.0, 2.0];
const processor = new DataProcessor(processorData, meanStrategy);
console.log(`Data: ${JSON.stringify(processorData)}`);
console.log(`Mean strategy:   ${processor.execute().toFixed(2)}`);
processor.setStrategy(medianStrategy);
console.log(`Median strategy: ${processor.execute().toFixed(2)}`);
processor.setStrategy(modeStrategy);
console.log(`Mode strategy:   ${processor.execute().toFixed(2)}`);

// -------------------------------------------------------------------
// 4.3.3  Command Pattern
// -------------------------------------------------------------------

class TextEditor {
    constructor() { this.content = ""; }
    insert(text) { this.content += text; }
    deleteLast(count) {
        const deleted = this.content.slice(-count);
        this.content = this.content.slice(0, -count);
        return deleted;
    }
    toString() { return `TextEditor(content="${this.content}")`; }
}

class InsertCommand {
    constructor(editor, text) { this._editor = editor; this._text = text; }
    execute() { this._editor.insert(this._text); return `  [Insert] Added: "${this._text}"`; }
    undo() { this._editor.deleteLast(this._text.length); return `  [Undo Insert] Removed: "${this._text}"`; }
}

class CommandHistory {
    constructor() { this._history = []; }
    execute(command) {
        const result = command.execute();
        this._history.push(command);
        return result;
    }
    undo() {
        if (!this._history.length) return "  [History] Nothing to undo";
        return this._history.pop().undo();
    }
}

console.log(`\n${"=".repeat(60)}`);
console.log("COMMAND PATTERN DEMO");
console.log("=".repeat(60));
const editor = new TextEditor();
const history = new CommandHistory();
console.log(history.execute(new InsertCommand(editor, "Hello ")));
console.log(history.execute(new InsertCommand(editor, "World")));
console.log(history.execute(new InsertCommand(editor, "!")));
console.log(`  Editor state: ${editor}`);
console.log(history.undo());
console.log(`  After undo: ${editor}`);
console.log(history.undo());
console.log(`  After undo: ${editor}`);


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 5: FUNCTIONAL PROGRAMMING & ADVANCED JS                     ║
// ╚══════════════════════════════════════════════════════════════════════╝


// ========================================================================
// 5.1  Functional Core — Composition, Currying, Partial Application
// ========================================================================

function functionalCoreDemo() {
    /**
     * Functional programming in JavaScript.
     *
     * Core Principles:
     * - Pure functions: No side effects, same input → same output.
     * - Immutability: Don't mutate data, create new data.
     * - Function composition: Combine small functions into larger ones.
     * - Higher-order functions: Functions that take/return functions.
     */

    console.log("\n--- Function Composition ---");

    /** compose(f, g, h)(x) = f(g(h(x))) — right-to-left */
    const compose = (...fns) => (x) => fns.reduceRight((acc, fn) => fn(acc), x);

    /** pipe(f, g, h)(x) = h(g(f(x))) — left-to-right */
    const pipe = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);

    const double = (x) => x * 2;
    const increment = (x) => x + 1;
    const square = (x) => x * x;

    const composed = compose(square, increment, double);
    console.log(`  compose(square, inc, double)(3) = square(inc(double(3))) = ${composed(3)}`);
    // double(3)=6, increment(6)=7, square(7)=49

    const piped = pipe(double, increment, square);
    console.log(`  pipe(double, inc, square)(3) = square(inc(double(3))) = ${piped(3)}`);

    // --- Currying ---
    console.log("\n--- Currying ---");
    /**
     * Currying: Transform f(a, b, c) into f(a)(b)(c).
     * Each call returns a new function until all arguments are received.
     *
     * Why? Enables partial application and function composition.
     */
    function curry(fn) {
        return function curried(...args) {
            if (args.length >= fn.length) return fn(...args);
            return (...moreArgs) => curried(...args, ...moreArgs);
        };
    }

    const add = (a, b, c) => a + b + c;
    const curriedAdd = curry(add);
    console.log(`  curry(add)(1)(2)(3) = ${curriedAdd(1)(2)(3)}`);
    console.log(`  curry(add)(1, 2)(3) = ${curriedAdd(1, 2)(3)}`);
    console.log(`  curry(add)(1)(2, 3) = ${curriedAdd(1)(2, 3)}`);

    // Practical use: creating specialized functions
    const multiply = curry((a, b) => a * b);
    const double2 = multiply(2);
    const triple = multiply(3);
    console.log(`  double(5) = ${double2(5)}, triple(5) = ${triple(5)}`);

    // --- Partial Application ---
    console.log("\n--- Partial Application ---");
    function partial(fn, ...presetArgs) {
        return (...laterArgs) => fn(...presetArgs, ...laterArgs);
    }

    const log = (level, timestamp, message) =>
        `  [${level}] ${timestamp}: ${message}`;

    const debugLog = partial(log, "DEBUG", new Date().toISOString().slice(0, 10));
    const errorLog = partial(log, "ERROR", new Date().toISOString().slice(0, 10));
    console.log(debugLog("System initialized"));
    console.log(errorLog("Connection failed"));

    // --- Practical Pipeline ---
    console.log("\n--- Practical Data Pipeline ---");
    const users = [
        { name: "Alice", age: 25, active: true },
        { name: "Bob", age: 30, active: false },
        { name: "Charlie", age: 35, active: true },
        { name: "Diana", age: 28, active: true },
        { name: "Eve", age: 22, active: false },
    ];

    const result = users
        .filter(u => u.active)
        .map(u => ({ ...u, name: u.name.toUpperCase() }))
        .sort((a, b) => a.age - b.age)
        .map(u => `${u.name} (${u.age})`);

    console.log(`  Active users sorted by age: ${JSON.stringify(result)}`);
}

functionalCoreDemo();


// ========================================================================
// 5.2  Immutability Patterns
// ========================================================================

function immutabilityDemo() {
    /**
     * Immutability patterns in JavaScript.
     *
     * Why immutability?
     * - Prevents accidental mutations (bugs).
     * - Enables efficient change detection (React's reconciliation).
     * - Makes code easier to reason about (no hidden state changes).
     * - Enables undo/redo and time-travel debugging.
     */

    console.log("\n--- Immutable Updates ---");

    // Object spread for immutable updates
    const original = { name: "Alice", address: { city: "NYC", zip: "10001" } };
    const updated = {
        ...original,
        address: { ...original.address, city: "LA" },
    };
    console.log(`  Original: ${JSON.stringify(original)}`);
    console.log(`  Updated:  ${JSON.stringify(updated)}`);
    console.log(`  Original unchanged: ${original.address.city === "NYC"}`);

    // Array immutable operations
    const arr = [1, 2, 3, 4, 5];
    const withAdded = [...arr, 6];                           // Add
    const withRemoved = arr.filter(x => x !== 3);            // Remove
    const withUpdated = arr.map(x => x === 3 ? 30 : x);     // Update
    const withInserted = [...arr.slice(0, 2), 99, ...arr.slice(2)]; // Insert at index
    console.log(`  Original:    ${JSON.stringify(arr)}`);
    console.log(`  With added:  ${JSON.stringify(withAdded)}`);
    console.log(`  With removed: ${JSON.stringify(withRemoved)}`);
    console.log(`  With updated: ${JSON.stringify(withUpdated)}`);
    console.log(`  With inserted: ${JSON.stringify(withInserted)}`);

    // --- Deep Freeze (recursive Object.freeze) ---
    function deepFreeze(obj) {
        Object.freeze(obj);
        for (const val of Object.values(obj)) {
            if (typeof val === "object" && val !== null && !Object.isFrozen(val)) {
                deepFreeze(val);
            }
        }
        return obj;
    }

    const frozen = deepFreeze({ a: 1, nested: { b: 2, deep: { c: 3 } } });
    try {
        frozen.nested.b = 99;  // Silently fails in non-strict
    } catch (e) { /* strict mode would throw */ }
    console.log(`  Deep frozen nested.b: ${frozen.nested.b}`); // Still 2
}

immutabilityDemo();


// ========================================================================
// 5.3  Maybe/Option & Result/Either Patterns
// ========================================================================

function monadsLiteDemo() {
    /**
     * Monadic patterns for safe error handling without exceptions.
     *
     * Maybe/Option: Represents a value that may or may not exist.
     * Replaces null checks with chainable operations.
     *
     * Result/Either: Represents success or failure with a reason.
     * Replaces try/catch with explicit error handling.
     */

    console.log("\n--- Maybe/Option Pattern ---");

    class Maybe {
        constructor(value) { this._value = value; }

        static of(value) { return new Maybe(value); }
        static empty() { return new Maybe(null); }

        isNothing() { return this._value === null || this._value === undefined; }

        /** Apply fn only if value exists. */
        map(fn) {
            return this.isNothing() ? Maybe.empty() : Maybe.of(fn(this._value));
        }

        /** Like map but fn returns a Maybe — prevents nesting. */
        flatMap(fn) {
            return this.isNothing() ? Maybe.empty() : fn(this._value);
        }

        /** Extract value, using fallback if empty. */
        getOrElse(fallback) {
            return this.isNothing() ? fallback : this._value;
        }

        toString() {
            return this.isNothing() ? "Maybe(Nothing)" : `Maybe(${this._value})`;
        }
    }

    // Without Maybe (ugly null checks):
    // const city = user && user.address && user.address.city;

    // With Maybe (clean chaining):
    const getNestedProp = (obj, ...keys) =>
        keys.reduce((maybe, key) => maybe.flatMap(o => Maybe.of(o[key])), Maybe.of(obj));

    const userObj = { profile: { address: { city: "London" } } };
    console.log(`  ${getNestedProp(userObj, "profile", "address", "city")}`);
    console.log(`  ${getNestedProp(userObj, "profile", "phone", "number")}`);
    console.log(`  ${getNestedProp(userObj, "profile", "phone", "number").getOrElse("N/A")}`);

    // --- Result/Either Pattern ---
    console.log("\n--- Result/Either Pattern ---");

    class Result {
        constructor(ok, value, error) {
            this._ok = ok;
            this._value = value;
            this._error = error;
        }

        static ok(value) { return new Result(true, value, null); }
        static err(error) { return new Result(false, null, error); }

        isOk() { return this._ok; }
        isErr() { return !this._ok; }

        map(fn) { return this._ok ? Result.ok(fn(this._value)) : this; }

        flatMap(fn) { return this._ok ? fn(this._value) : this; }

        mapErr(fn) { return this._ok ? this : Result.err(fn(this._error)); }

        unwrap() {
            if (this._ok) return this._value;
            throw new Error(`Called unwrap on Err: ${this._error}`);
        }

        unwrapOr(fallback) { return this._ok ? this._value : fallback; }

        toString() {
            return this._ok ? `Ok(${this._value})` : `Err(${this._error})`;
        }
    }

    // Safe division
    const safeDivide = (a, b) =>
        b === 0 ? Result.err("Division by zero") : Result.ok(a / b);

    const safeParseInt = (str) => {
        const n = parseInt(str, 10);
        return Number.isNaN(n) ? Result.err(`Cannot parse "${str}" as integer`) : Result.ok(n);
    };

    // Chain operations safely
    const computation = safeParseInt("42")
        .flatMap(n => safeDivide(n, 7))
        .map(n => n * 10);
    console.log(`  Parse "42" → ÷7 → ×10 = ${computation}`);

    const failing = safeParseInt("abc")
        .flatMap(n => safeDivide(n, 7))
        .map(n => n * 10);
    console.log(`  Parse "abc" → ÷7 → ×10 = ${failing}`);
    console.log(`  Failing with fallback: ${failing.unwrapOr(0)}`);
}

monadsLiteDemo();


// ========================================================================
// 5.4  Lazy Evaluation with Generators
// ========================================================================

function lazyEvaluationDemo() {
    /**
     * Lazy evaluation: compute values only when needed.
     * Generators + iterator protocol enable efficient lazy pipelines.
     */

    console.log("\n--- Lazy Evaluation with Generators ---");

    function* lazyMap(iterable, fn) {
        for (const val of iterable) yield fn(val);
    }

    function* lazyFilter(iterable, pred) {
        for (const val of iterable) if (pred(val)) yield val;
    }

    function* lazyTake(iterable, n) {
        let count = 0;
        for (const val of iterable) {
            if (count >= n) return;
            yield val;
            count++;
        }
    }

    function* lazyFlatMap(iterable, fn) {
        for (const val of iterable) yield* fn(val);
    }

    // Infinite range
    function* range(start = 0, step = 1) {
        let n = start;
        while (true) yield (n += step) - step;
    }

    // Pipeline: take first 10 primes lazily
    function isPrime(n) {
        if (n < 2) return false;
        for (let i = 2; i <= Math.sqrt(n); i++) {
            if (n % i === 0) return false;
        }
        return true;
    }

    const first10Primes = [...lazyTake(lazyFilter(range(2), isPrime), 10)];
    console.log(`  First 10 primes (lazy): ${JSON.stringify(first10Primes)}`);

    // Lazy zip
    function* lazyZip(...iterables) {
        const iterators = iterables.map(it => it[Symbol.iterator]());
        while (true) {
            const results = iterators.map(it => it.next());
            if (results.some(r => r.done)) return;
            yield results.map(r => r.value);
        }
    }

    const zipped = [...lazyTake(lazyZip(range(1), range(100, 10)), 5)];
    console.log(`  Lazy zip: ${JSON.stringify(zipped)}`);

    // Demonstrate laziness: only compute what's needed
    let computeCount = 0;
    const expensiveSquare = (n) => { computeCount++; return n * n; };

    const lazySquares = lazyMap(range(1), expensiveSquare);
    const firstThree = [...lazyTake(lazySquares, 3)];
    console.log(`  First 3 squares: ${JSON.stringify(firstThree)}, computations: ${computeCount}`);
    // Only 3 computations, not infinite!
}

lazyEvaluationDemo();


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 6: ASYNC PATTERNS & CONCURRENCY                             ║
// ╚══════════════════════════════════════════════════════════════════════╝


// ========================================================================
// 6.1  Event Loop Deep-Dive: Microtasks vs Macrotasks
// ========================================================================

function eventLoopDemo() {
    /**
     * The JavaScript Event Loop — the heart of async execution.
     *
     * Execution Order:
     * 1. Execute all synchronous code in the current call stack.
     * 2. Drain the MICROTASK queue (Promises, queueMicrotask, MutationObserver).
     * 3. Execute ONE macrotask (setTimeout, setInterval, I/O, setImmediate).
     * 4. Drain microtask queue again.
     * 5. Repeat from step 3.
     *
     * Key Insight: Microtasks have PRIORITY over macrotasks.
     * A microtask scheduled during a macrotask runs BEFORE the next macrotask.
     */

    console.log("\n--- Event Loop Execution Order ---");
    console.log("  (Results shown after all sync code completes)");

    // This demonstrates the order but we'll show it inline for the encyclopedia
    const order = [];

    // These would execute in this order in a real event loop:
    // 1. Sync code runs first
    order.push("1. Synchronous");

    // 2. Microtasks (Promises) run next
    // Promise.resolve().then(() => order.push("2. Microtask (Promise)"));

    // 3. queueMicrotask runs in microtask queue
    // queueMicrotask(() => order.push("3. Microtask (queueMicrotask)"));

    // 4. Macrotasks (setTimeout) run last
    // setTimeout(() => order.push("4. Macrotask (setTimeout)"), 0);

    console.log("  Expected order: Sync → Promise → queueMicrotask → setTimeout");
    console.log("  Microtasks ALWAYS drain before the next macrotask");

    // --- Microtask starvation risk ---
    console.log("\n  ⚠️  WARNING: Microtasks can starve macrotasks!");
    console.log("  If a microtask schedules another microtask indefinitely,");
    console.log("  setTimeout/I/O callbacks will NEVER execute.");
}

eventLoopDemo();


// ========================================================================
// 6.2  Async Patterns: Retry, Timeout, Throttle, Debounce
// ========================================================================

function asyncPatternsDemo() {
    /**
     * Common async patterns for production JavaScript.
     */

    console.log("\n--- Async Utility Patterns ---");

    // --- Retry with exponential backoff ---
    async function retry(fn, maxRetries = 3, baseDelay = 100) {
        /**
         * Retry a failed async operation with exponential backoff.
         * Delay doubles each retry: 100ms → 200ms → 400ms → ...
         */
        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return await fn();
            } catch (err) {
                if (attempt === maxRetries) throw err;
                const delay = baseDelay * Math.pow(2, attempt);
                // await new Promise(r => setTimeout(r, delay));
                console.log(`    Retry ${attempt + 1}/${maxRetries} after ${delay}ms`);
            }
        }
    }

    console.log("  retry(fn, 3, 100): Retries with exponential backoff");
    console.log("    Delays: 100ms → 200ms → 400ms");

    // --- Timeout wrapper ---
    function withTimeout(promise, ms) {
        /** Race a promise against a timeout. */
        const timeout = new Promise((_, reject) =>
            setTimeout(() => reject(new Error(`Timeout after ${ms}ms`)), ms)
        );
        return Promise.race([promise, timeout]);
    }

    console.log("  withTimeout(promise, ms): Rejects if promise takes too long");

    // --- Debounce ---
    function debounce(fn, delay) {
        /**
         * Debounce: Only execute fn after `delay` ms of inactivity.
         * Use case: Search input — don't fire API call on every keystroke.
         *
         * Timeline: [call][call][call]---delay---[execute once]
         */
        let timer = null;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    console.log("  debounce(fn, delay): Executes after inactivity period");

    // --- Throttle ---
    function throttle(fn, interval) {
        /**
         * Throttle: Execute fn at most once per `interval` ms.
         * Use case: Scroll handler — limit to 60fps (16ms interval).
         *
         * Timeline: [execute]---interval---[execute]---interval---[execute]
         */
        let lastTime = 0;
        return function (...args) {
            const now = Date.now();
            if (now - lastTime >= interval) {
                lastTime = now;
                return fn.apply(this, args);
            }
        };
    }

    console.log("  throttle(fn, interval): At most once per interval");

    // --- Semaphore (concurrency limiter) ---
    class Semaphore {
        /**
         * Limits concurrent async operations.
         * Use case: API rate limiting — at most N requests in flight.
         */
        constructor(maxConcurrency) {
            this._max = maxConcurrency;
            this._running = 0;
            this._queue = [];
        }

        async acquire() {
            if (this._running < this._max) {
                this._running++;
                return;
            }
            await new Promise(resolve => this._queue.push(resolve));
        }

        release() {
            this._running--;
            if (this._queue.length > 0) {
                this._running++;
                this._queue.shift()();
            }
        }

        async run(fn) {
            await this.acquire();
            try { return await fn(); }
            finally { this.release(); }
        }
    }

    console.log("  Semaphore(n): Limits to n concurrent operations");
    const sem = new Semaphore(3);
    console.log(`  Created Semaphore(3): max concurrent = ${sem._max}`);
}

asyncPatternsDemo();


// ========================================================================
// 6.3  Async Iterators & for await...of
// ========================================================================

function asyncIteratorsDemo() {
    /**
     * Async Iterators: [Symbol.asyncIterator]() → { async next() }
     * Used with `for await...of` to consume async data streams.
     *
     * Use cases: Reading files line by line, consuming paginated APIs,
     * processing event streams, reading from databases.
     */

    console.log("\n--- Async Iterators ---");

    // Async generator function
    async function* asyncRange(start, end, delayMs = 0) {
        for (let i = start; i < end; i++) {
            if (delayMs > 0) await new Promise(r => setTimeout(r, delayMs));
            yield i;
        }
    }

    // Paginated API simulator
    async function* paginatedFetch(totalItems, pageSize) {
        /**
         * Simulates fetching paginated data from an API.
         * Each yield returns one page of results.
         */
        let page = 0;
        while (page * pageSize < totalItems) {
            // Simulate API delay
            // await new Promise(r => setTimeout(r, 10));
            const start = page * pageSize;
            const end = Math.min(start + pageSize, totalItems);
            const items = Array.from({ length: end - start }, (_, i) => ({
                id: start + i,
                name: `Item ${start + i}`,
            }));
            yield { page: page + 1, items };
            page++;
        }
    }

    console.log("  Async generator: async function* asyncRange(start, end)");
    console.log("  Usage: for await (const val of asyncRange(0, 5)) { ... }");
    console.log("  Paginated fetch: yields one page at a time");

    // Demonstrate synchronously
    const gen = paginatedFetch(12, 5);
    console.log("  Paginated results (simulated):");
    // We'll consume synchronously since generators work sync too for demo
    (async () => {
        for await (const page of paginatedFetch(12, 5)) {
            console.log(`    Page ${page.page}: ${page.items.map(i => i.name).join(", ")}`);
        }
    })();
}

asyncIteratorsDemo();


// ========================================================================
// 6.4  Worker Threads Concept & SharedArrayBuffer
// ========================================================================

function concurrencyConceptsDemo() {
    /**
     * JavaScript Concurrency Model.
     *
     * Single-threaded: JS runs on ONE thread. The event loop provides
     * concurrency (not parallelism) for I/O operations.
     *
     * Worker Threads (Node.js): True parallelism for CPU-intensive tasks.
     * - Each worker has its own V8 instance and event loop.
     * - Communication via message passing (structured clone) or
     *   SharedArrayBuffer (shared memory).
     *
     * SharedArrayBuffer + Atomics:
     * - Shared memory between threads.
     * - Atomics provides atomic operations (compare-and-swap, load, store).
     * - Required for lock-free data structures and synchronization.
     */

    console.log("\n--- Concurrency Concepts ---");
    console.log("  JS is single-threaded with an event loop for concurrency.");
    console.log("  Worker Threads provide true parallelism (separate V8 instances).");
    console.log("  SharedArrayBuffer enables shared memory between workers.");
    console.log("  Atomics provides thread-safe atomic operations.");

    // Demonstrate SharedArrayBuffer and Atomics concepts
    const sab = new SharedArrayBuffer(16); // 16 bytes = 4 Int32 slots
    const view = new Int32Array(sab);

    // Atomic operations (thread-safe)
    Atomics.store(view, 0, 42);
    console.log(`  Atomics.load: ${Atomics.load(view, 0)}`);

    const oldVal = Atomics.compareExchange(view, 0, 42, 100);
    console.log(`  Atomics.compareExchange(42 → 100): old=${oldVal}, new=${Atomics.load(view, 0)}`);

    Atomics.add(view, 0, 5);
    console.log(`  Atomics.add(5): ${Atomics.load(view, 0)}`);

    console.log("\n  Worker Thread usage (conceptual):");
    console.log("  const { Worker, isMainThread } = require('worker_threads');");
    console.log("  if (isMainThread) {");
    console.log("    const worker = new Worker('./worker.js');");
    console.log("    worker.on('message', msg => console.log(msg));");
    console.log("  } else {");
    console.log("    parentPort.postMessage('Hello from worker!');");
    console.log("  }");
}

concurrencyConceptsDemo();


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 7: NODE.JS ESSENTIALS                                        ║
// ╚══════════════════════════════════════════════════════════════════════╝


// ========================================================================
// 7.1  Module Systems: CommonJS vs ESM
// ========================================================================

function moduleSystemsDemo() {
    /**
     * JavaScript Module Systems.
     *
     * CommonJS (CJS) — Node.js original:
     *   const fs = require('fs');
     *   module.exports = { myFunc };
     *   - Synchronous loading
     *   - Dynamic (can require conditionally)
     *   - Each require() returns the SAME cached module instance
     *
     * ES Modules (ESM) — The standard:
     *   import fs from 'fs';
     *   export const myFunc = () => {};
     *   - Static imports (analyzed at compile time → tree-shaking)
     *   - import() for dynamic imports (returns a Promise)
     *   - Strict mode by default
     *   - Top-level await supported
     *
     * package.json "type" field:
     *   "type": "module"    → .js files are ESM
     *   "type": "commonjs"  → .js files are CJS (default)
     *   .mjs → always ESM
     *   .cjs → always CJS
     */

    console.log("\n--- Module Systems ---");
    console.log("  CommonJS: require() / module.exports — synchronous, dynamic");
    console.log("  ESM:      import / export — static, tree-shakeable, async");
    console.log("  This file uses CommonJS (no 'type: module' in package.json)");

    // Demonstrate dynamic require (CommonJS)
    const path = require("path");
    console.log(`  require('path').basename: ${path.basename("/foo/bar/baz.txt")}`);

    // Module caching
    const mod1 = require("path");
    const mod2 = require("path");
    console.log(`  Module caching: mod1 === mod2: ${mod1 === mod2}`);
}

moduleSystemsDemo();


// ========================================================================
// 7.2  File System Operations
// ========================================================================

function fileSystemDemo() {
    /**
     * Node.js File System API.
     *
     * Three variants:
     * - Callback-based: fs.readFile(path, cb)      — original, callback hell
     * - Synchronous:    fs.readFileSync(path)       — blocks the event loop!
     * - Promise-based:  fs.promises.readFile(path)  — modern, use this!
     *
     * Key Operations:
     *   readFile/writeFile — read/write entire files
     *   readdir — list directory contents
     *   stat — get file metadata (size, timestamps, isFile/isDirectory)
     *   mkdir — create directories
     *   unlink — delete files
     *   watch — watch for file changes
     */

    const fs = require("fs");
    const path = require("path");

    console.log("\n--- File System Operations ---");
    console.log("  Three APIs: callback, sync, promise-based");

    // Sync operations (for demo simplicity — avoid in production servers)
    const thisFile = __filename;
    const stats = fs.statSync(thisFile);
    console.log(`  This file: ${path.basename(thisFile)}`);
    console.log(`  Size: ${stats.size} bytes`);
    console.log(`  Is file: ${stats.isFile()}`);
    console.log(`  Modified: ${stats.mtime.toISOString()}`);

    // Directory listing
    const dir = __dirname;
    const files = fs.readdirSync(dir);
    console.log(`  Files in directory: ${files.filter(f => f.endsWith('.js')).join(', ')}`);

    // Path operations
    console.log(`\n  path.join('/foo', 'bar', 'baz.txt') = "${path.join('/foo', 'bar', 'baz.txt')}"`);
    console.log(`  path.resolve('./test.js') = "${path.resolve('./test.js')}"`);
    console.log(`  path.extname('file.tar.gz') = "${path.extname('file.tar.gz')}"`);
    console.log(`  path.parse('/home/user/file.txt'):`);
    console.log(`    ${JSON.stringify(path.parse('/home/user/file.txt'))}`);
}

fileSystemDemo();


// ========================================================================
// 7.3  HTTP Server & Middleware Pattern
// ========================================================================

function httpServerDemo() {
    /**
     * Building an HTTP server with the raw `http` module.
     * Demonstrates the middleware pattern used by Express.js.
     *
     * Middleware: Functions that process requests in a pipeline.
     * Each middleware can:
     * 1. Modify the request/response objects
     * 2. End the request-response cycle
     * 3. Call next() to pass control to the next middleware
     */

    console.log("\n--- HTTP Server & Middleware Pattern ---");

    // Simple middleware engine (Express-like)
    class MiddlewareEngine {
        constructor() { this._middlewares = []; }

        use(fn) {
            this._middlewares.push(fn);
            return this;
        }

        async handle(req, res) {
            let idx = 0;
            const next = async () => {
                if (idx < this._middlewares.length) {
                    const middleware = this._middlewares[idx++];
                    await middleware(req, res, next);
                }
            };
            await next();
        }
    }

    // Simulate middleware stack
    const app = new MiddlewareEngine();

    // Logger middleware
    app.use(async (req, res, next) => {
        req.startTime = Date.now();
        console.log(`  [Logger] ${req.method} ${req.url}`);
        await next();
        console.log(`  [Logger] Completed in ${Date.now() - req.startTime}ms`);
    });

    // Auth middleware
    app.use(async (req, res, next) => {
        if (req.headers?.authorization) {
            req.user = "authenticated_user";
            console.log("  [Auth] User authenticated");
        } else {
            console.log("  [Auth] No auth header (anonymous)");
        }
        await next();
    });

    // Route handler
    app.use(async (req, res, next) => {
        res.body = { message: `Hello from ${req.url}!`, user: req.user || "anonymous" };
        console.log(`  [Handler] Response: ${JSON.stringify(res.body)}`);
    });

    // Simulate a request
    const mockReq = { method: "GET", url: "/api/users", headers: { authorization: "Bearer token" } };
    const mockRes = {};
    app.handle(mockReq, mockRes);

    console.log("\n  Real HTTP server (conceptual):");
    console.log("  const http = require('http');");
    console.log("  const server = http.createServer((req, res) => {");
    console.log("    res.writeHead(200, { 'Content-Type': 'application/json' });");
    console.log("    res.end(JSON.stringify({ hello: 'world' }));");
    console.log("  });");
    console.log("  server.listen(3000);");
}

httpServerDemo();


// ========================================================================
// 7.4  EventEmitter & Buffer
// ========================================================================

function eventEmitterDemo() {
    /**
     * Node.js EventEmitter — the foundation of Node's event-driven architecture.
     *
     * Core Methods:
     *   emitter.on(event, listener)     — Subscribe
     *   emitter.once(event, listener)   — Subscribe (fires once)
     *   emitter.emit(event, ...args)    — Emit event
     *   emitter.off(event, listener)    — Unsubscribe
     *   emitter.removeAllListeners()    — Remove all
     *
     * Many Node.js core modules extend EventEmitter:
     *   http.Server, net.Socket, fs.ReadStream, process, etc.
     */

    const EventEmitter = require("events");

    console.log("\n--- EventEmitter ---");

    class MyServer extends EventEmitter {
        start() {
            console.log("  [Server] Starting...");
            this.emit("start", { timestamp: Date.now() });
        }

        handleRequest(path) {
            this.emit("request", { path, timestamp: Date.now() });
        }

        stop() {
            this.emit("stop");
            console.log("  [Server] Stopped.");
        }
    }

    const server = new MyServer();

    server.on("start", (data) => console.log(`  [Listener] Server started`));
    server.on("request", (data) => console.log(`  [Listener] Request: ${data.path}`));
    server.once("stop", () => console.log("  [Listener] Server stopped (once)"));

    server.start();
    server.handleRequest("/api/users");
    server.handleRequest("/api/posts");
    server.stop();

    // --- Buffer ---
    console.log("\n--- Buffer (Binary Data) ---");
    /**
     * Buffer: Fixed-size chunk of memory for binary data.
     * Used for file I/O, network protocols, cryptography, and
     * any operation involving raw bytes.
     */

    // Creating buffers
    const buf1 = Buffer.from("Hello, World!", "utf-8");
    const buf2 = Buffer.alloc(10);  // 10 zero-filled bytes
    const buf3 = Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]); // From byte array

    console.log(`  Buffer from string: ${buf1.toString("hex")}`);
    console.log(`  Buffer to string:   "${buf1.toString("utf-8")}"`);
    console.log(`  Buffer from bytes:  "${buf3.toString("utf-8")}"`);
    console.log(`  Buffer length:      ${buf1.length} bytes`);
    console.log(`  Buffer.isBuffer:    ${Buffer.isBuffer(buf1)}`);

    // Encoding conversions
    console.log(`  Base64 encode: "${buf1.toString("base64")}"`);
    console.log(`  Hex encode:    "${buf1.toString("hex")}"`);

    // Buffer operations
    const combined = Buffer.concat([buf1, Buffer.from(" 🌍")]);
    console.log(`  Concatenated: "${combined.toString("utf-8")}"`);
}

eventEmitterDemo();


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  PHASE 8: TESTING, ERROR HANDLING & PERFORMANCE                     ║
// ╚══════════════════════════════════════════════════════════════════════╝


// ========================================================================
// 8.1  Error Handling Patterns
// ========================================================================

function errorHandlingDemo() {
    /**
     * Comprehensive error handling patterns for production JavaScript.
     *
     * Types of Errors:
     * - SyntaxError:    Invalid code (parsing fails)
     * - ReferenceError: Accessing undeclared variable
     * - TypeError:      Wrong type (e.g., null.property)
     * - RangeError:     Number out of range
     * - Custom errors:  Application-specific errors
     */

    console.log("\n--- Custom Error Hierarchy ---");

    class AppError extends Error {
        constructor(message, statusCode = 500, code = "INTERNAL_ERROR") {
            super(message);
            this.name = this.constructor.name;
            this.statusCode = statusCode;
            this.code = code;
            this.timestamp = new Date().toISOString();
            Error.captureStackTrace?.(this, this.constructor);
        }

        toJSON() {
            return {
                error: this.name,
                code: this.code,
                message: this.message,
                statusCode: this.statusCode,
            };
        }
    }

    class NotFoundError extends AppError {
        constructor(resource, id) {
            super(`${resource} with ID ${id} not found`, 404, "NOT_FOUND");
            this.resource = resource;
            this.resourceId = id;
        }
    }

    class ValidationError extends AppError {
        constructor(field, reason) {
            super(`Validation failed for '${field}': ${reason}`, 400, "VALIDATION_ERROR");
            this.field = field;
        }
    }

    // Usage
    try {
        throw new NotFoundError("User", 42);
    } catch (err) {
        if (err instanceof NotFoundError) {
            console.log(`  Caught NotFoundError: ${JSON.stringify(err.toJSON())}`);
        }
    }

    try {
        throw new ValidationError("email", "must be a valid email address");
    } catch (err) {
        console.log(`  Caught ValidationError: ${JSON.stringify(err.toJSON())}`);
    }

    // --- Error Boundary Pattern ---
    console.log("\n--- Error Boundary Pattern ---");

    function errorBoundary(fn, fallback) {
        /** Wraps a function to catch errors and return a fallback. */
        try {
            return fn();
        } catch (err) {
            console.log(`  [ErrorBoundary] Caught: ${err.message}`);
            return typeof fallback === "function" ? fallback(err) : fallback;
        }
    }

    const riskyResult = errorBoundary(
        () => JSON.parse("{invalid json}"),
        "default value"
    );
    console.log(`  Error boundary result: "${riskyResult}"`);

    // --- Retry with backoff ---
    console.log("\n--- Retry Logic ---");
    let attempts = 0;
    function unreliableOperation() {
        attempts++;
        if (attempts < 3) throw new Error(`Attempt ${attempts} failed`);
        return "Success on attempt " + attempts;
    }

    function retrySync(fn, maxRetries = 3) {
        for (let i = 0; i <= maxRetries; i++) {
            try { return fn(); }
            catch (err) {
                if (i === maxRetries) throw err;
                console.log(`  Retry ${i + 1}/${maxRetries}: ${err.message}`);
            }
        }
    }

    attempts = 0;
    const retryResult = retrySync(unreliableOperation, 5);
    console.log(`  Retry result: "${retryResult}"`);
}

errorHandlingDemo();


// ========================================================================
// 8.2  Performance: Memoization, Debounce/Throttle, Profiling
// ========================================================================

function performanceDemo() {
    /**
     * Performance patterns for JavaScript.
     */

    console.log("\n--- Memoization ---");

    /**
     * Memoize: Cache function results based on arguments.
     * Time: O(1) for cached calls. Space: O(n) for cache.
     */
    function memoize(fn) {
        const cache = new Map();
        return function (...args) {
            const key = JSON.stringify(args);
            if (cache.has(key)) return cache.get(key);
            const result = fn.apply(this, args);
            cache.set(key, result);
            return result;
        };
    }

    // Expensive Fibonacci without memoization
    function fibSlow(n) {
        if (n <= 1) return n;
        return fibSlow(n - 1) + fibSlow(n - 2);
    }

    const fibFast = memoize(function fib(n) {
        if (n <= 1) return n;
        return fibFast(n - 1) + fibFast(n - 2);
    });

    console.time("  fib(35) without memo");
    fibSlow(35);
    console.timeEnd("  fib(35) without memo");

    console.time("  fib(35) with memo");
    fibFast(35);
    console.timeEnd("  fib(35) with memo");

    console.log(`  fib(35) = ${fibFast(35)}`);
    console.log(`  fib(100) = ${fibFast(100)}`);  // Instant with memo!

    // --- Performance measurement ---
    console.log("\n--- Performance Profiling ---");

    function benchmark(name, fn, iterations = 10000) {
        const start = process.hrtime.bigint();
        for (let i = 0; i < iterations; i++) fn();
        const elapsed = Number(process.hrtime.bigint() - start) / 1e6;
        console.log(`  ${name}: ${elapsed.toFixed(2)}ms for ${iterations} iterations`);
        return elapsed;
    }

    const arr = Array.from({ length: 1000 }, (_, i) => i);

    benchmark("for loop", () => {
        let sum = 0;
        for (let i = 0; i < arr.length; i++) sum += arr[i];
    });

    benchmark("for...of", () => {
        let sum = 0;
        for (const v of arr) sum += v;
    });

    benchmark("reduce", () => {
        arr.reduce((a, b) => a + b, 0);
    });

    // --- Object pool pattern ---
    console.log("\n--- Object Pool Pattern ---");
    class ObjectPool {
        /**
         * Reuse objects to avoid garbage collection pressure.
         * Use case: Game engines (particles, bullets), database connections.
         */
        constructor(factory, initialSize = 10) {
            this._factory = factory;
            this._pool = Array.from({ length: initialSize }, () => factory());
        }

        acquire() {
            return this._pool.length > 0 ? this._pool.pop() : this._factory();
        }

        release(obj) {
            this._pool.push(obj);
        }

        get size() { return this._pool.length; }
    }

    const pool = new ObjectPool(() => ({ x: 0, y: 0, active: false }), 5);
    console.log(`  Pool created with ${pool.size} objects`);
    const obj1 = pool.acquire();
    const obj2 = pool.acquire();
    console.log(`  After 2 acquires: ${pool.size} remaining`);
    pool.release(obj1);
    console.log(`  After 1 release: ${pool.size} remaining`);
}

performanceDemo();


// ========================================================================
// 8.3  Regular Expressions Deep-Dive
// ========================================================================

function regexDemo() {
    /**
     * JavaScript Regular Expressions — a powerful text processing tool.
     *
     * Syntax: /pattern/flags
     * Flags: g (global), i (case-insensitive), m (multiline),
     *        s (dotAll), u (unicode), d (indices)
     *
     * Special Characters:
     *   .     Any character (except \n without s flag)
     *   \d    Digit [0-9]
     *   \w    Word char [a-zA-Z0-9_]
     *   \s    Whitespace
     *   \b    Word boundary
     *   ^/$   Start/end of string (or line with m flag)
     *   *+?   Quantifiers (0+, 1+, 0 or 1)
     *   {n,m} Between n and m occurrences
     */

    console.log("\n--- Regular Expressions ---");

    // --- Basic patterns ---
    console.log("  Basic patterns:");
    console.log(`    /hello/i.test("Hello World") = ${/hello/i.test("Hello World")}`);
    console.log(`    "abc123".match(/\\d+/) = ${JSON.stringify("abc123".match(/\d+/))}`);

    // --- Named capture groups ---
    const dateRegex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
    const dateMatch = "2024-03-15".match(dateRegex);
    console.log(`\n  Named groups: ${JSON.stringify(dateMatch?.groups)}`);

    // --- Lookahead and Lookbehind ---
    console.log("\n  Lookahead/Lookbehind:");
    const lookahead = /\d+(?= dollars)/g;      // Number followed by " dollars"
    console.log(`    "100 dollars 200 euros".match(/\\d+(?= dollars)/) = ${JSON.stringify("100 dollars 200 euros".match(lookahead))}`);

    const lookbehind = /(?<=\$)\d+/g;          // Number preceded by "$"
    console.log(`    "$100 and $200".match(/(?<=\\$)\\d+/) = ${JSON.stringify("$100 and $200".match(lookbehind))}`);

    // --- Practical patterns ---
    console.log("\n  Practical patterns:");

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    console.log(`    Email valid "test@example.com": ${emailRegex.test("test@example.com")}`);
    console.log(`    Email valid "not-email":        ${emailRegex.test("not-email")}`);

    // URL parsing
    const urlRegex = /^(?<protocol>https?):\/\/(?<host>[^/:]+)(?::(?<port>\d+))?(?<path>\/[^?]*)?(?:\?(?<query>.*))?$/;
    const urlMatch = "https://example.com:8080/api/users?active=true".match(urlRegex);
    console.log(`    URL parse: ${JSON.stringify(urlMatch?.groups)}`);

    // --- Replace with function ---
    const camelToKebab = (str) =>
        str.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
    console.log(`\n  camelToKebab("backgroundColor") = "${camelToKebab("backgroundColor")}"`);

    // Template literal replacement
    const template = "Hello {{name}}, welcome to {{city}}!";
    const data = { name: "Alice", city: "NYC" };
    const rendered = template.replace(/\{\{(\w+)\}\}/g, (_, key) => data[key] || "");
    console.log(`  Template render: "${rendered}"`);
}

regexDemo();


// ========================================================================
// 8.4  Data Validation Patterns
// ========================================================================

function validationDemo() {
    /**
     * Schema-based validation patterns for JavaScript.
     * Demonstrates building a type-safe validation system.
     */

    console.log("\n--- Schema Validation ---");

    class Schema {
        constructor() { this._checks = []; }

        _addCheck(fn, message) {
            this._checks.push({ fn, message });
            return this;
        }

        validate(value) {
            const errors = [];
            for (const { fn, message } of this._checks) {
                if (!fn(value)) errors.push(message);
            }
            return { valid: errors.length === 0, errors };
        }
    }

    class StringSchema extends Schema {
        constructor() {
            super();
            this._addCheck(v => typeof v === "string", "Must be a string");
        }
        minLength(n) { return this._addCheck(v => v.length >= n, `Min length: ${n}`); }
        maxLength(n) { return this._addCheck(v => v.length <= n, `Max length: ${n}`); }
        matches(regex) { return this._addCheck(v => regex.test(v), `Must match ${regex}`); }
        email() { return this.matches(/^[^\s@]+@[^\s@]+\.[^\s@]+$/); }
    }

    class NumberSchema extends Schema {
        constructor() {
            super();
            this._addCheck(v => typeof v === "number" && !isNaN(v), "Must be a number");
        }
        min(n) { return this._addCheck(v => v >= n, `Min value: ${n}`); }
        max(n) { return this._addCheck(v => v <= n, `Max value: ${n}`); }
        integer() { return this._addCheck(v => Number.isInteger(v), "Must be an integer"); }
        positive() { return this._addCheck(v => v > 0, "Must be positive"); }
    }

    class ObjectSchema {
        constructor(shape) { this._shape = shape; }

        validate(obj) {
            if (typeof obj !== "object" || obj === null) {
                return { valid: false, errors: { _root: ["Must be an object"] } };
            }
            const errors = {};
            for (const [key, schema] of Object.entries(this._shape)) {
                const result = schema.validate(obj[key]);
                if (!result.valid) errors[key] = result.errors;
            }
            return { valid: Object.keys(errors).length === 0, errors };
        }
    }

    // Define schema
    const userSchema = new ObjectSchema({
        name: new StringSchema().minLength(2).maxLength(50),
        email: new StringSchema().email(),
        age: new NumberSchema().integer().min(0).max(150),
    });

    // Validate good data
    const goodResult = userSchema.validate({
        name: "Alice", email: "alice@example.com", age: 30,
    });
    console.log(`  Valid user: ${JSON.stringify(goodResult)}`);

    // Validate bad data
    const badResult = userSchema.validate({
        name: "A", email: "not-an-email", age: -5,
    });
    console.log(`  Invalid user: ${JSON.stringify(badResult)}`);
}

validationDemo();


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  DEBUG CHALLENGES — INTENTIONAL BUGS FOR STUDENTS TO FIX            ║
// ╚══════════════════════════════════════════════════════════════════════╝


// ========================================================================
// BUG CHALLENGE 1: var Hoisting vs let/const Block Scoping
// ========================================================================

function bugChallenge1() {
    /**
     * 🐛 BUG CHALLENGE: var hoisting vs let/const block scoping.
     *
     * `var` is function-scoped and HOISTED (declaration moves to top).
     * `let` and `const` are block-scoped and NOT hoisted (temporal dead zone).
     */
    console.log("\nBUG CHALLENGE 1: var Hoisting");

    // --- BUGGY CODE ---
    const buggyResults = [];
    for (var i = 0; i < 5; i++) {
        setTimeout(() => buggyResults.push(i), 0);
    }
    // After the loop, `i` is 5. ALL callbacks see i=5.
    // Expected: [0, 1, 2, 3, 4]. Got: [5, 5, 5, 5, 5]
    console.log(`  Buggy (var): All callbacks will see i=${i} (var is function-scoped)`);

    // --- FIXED CODE ---
    const fixedResults = [];
    for (let j = 0; j < 5; j++) {
        // `let` creates a NEW binding for each iteration
        fixedResults.push(j);
    }
    console.log(`  Fixed (let): ${JSON.stringify(fixedResults)}`);
}

bugChallenge1();


// ========================================================================
// BUG CHALLENGE 2: `this` Context Loss in Callbacks
// ========================================================================

function bugChallenge2() {
    /**
     * 🐛 BUG CHALLENGE: `this` context loss.
     *
     * When you pass a method as a callback, it loses its `this` binding.
     */
    console.log("\nBUG CHALLENGE 2: this Context Loss");

    // --- BUGGY CODE ---
    class TimerBuggy {
        constructor() { this.seconds = 0; }
        start() {
            // BUG: Regular function in setInterval loses `this`
            // setInterval(function() { this.seconds++; }, 1000);
            // `this` inside the callback is undefined (strict mode) or globalThis
            console.log("  Buggy: regular function callback loses `this` context");
        }
    }

    // --- FIXED CODE ---
    class TimerFixed {
        constructor() { this.seconds = 0; }
        start() {
            // FIX 1: Arrow function (captures `this` from enclosing scope)
            // setInterval(() => { this.seconds++; }, 1000);
            console.log("  Fix 1: Use arrow function (lexical `this`)");
        }
        startAlt() {
            // FIX 2: bind
            // setInterval(this.tick.bind(this), 1000);
            console.log("  Fix 2: Use .bind(this)");
        }
    }

    const timer = new TimerFixed();
    timer.start();
    timer.startAlt();
}

bugChallenge2();


// ========================================================================
// BUG CHALLENGE 3: Floating Point Comparison
// ========================================================================

function bugChallenge3() {
    /**
     * 🐛 BUG CHALLENGE: Floating point precision.
     *
     * IEEE 754 doubles can't represent all decimal fractions exactly.
     * 0.1 + 0.2 = 0.30000000000000004, NOT 0.3.
     */
    console.log("\nBUG CHALLENGE 3: Floating Point");

    // --- BUGGY CODE ---
    const buggy = (0.1 + 0.2 === 0.3);
    console.log(`  Buggy: 0.1 + 0.2 === 0.3 → ${buggy}`);
    console.log(`  Actual: 0.1 + 0.2 = ${0.1 + 0.2}`);

    // --- FIXED CODE ---
    function nearlyEqual(a, b, epsilon = Number.EPSILON) {
        return Math.abs(a - b) < epsilon;
    }
    const fixed = nearlyEqual(0.1 + 0.2, 0.3);
    console.log(`  Fixed: nearlyEqual(0.1 + 0.2, 0.3) → ${fixed}`);

    // For money, use integers (cents):
    const priceInCents = 199;  // $1.99
    const taxInCents = 15;      // $0.15
    console.log(`  Money: $${(priceInCents + taxInCents) / 100} (using integer cents)`);
}

bugChallenge3();


// ========================================================================
// BUG CHALLENGE 4: Async forEach Pitfall
// ========================================================================

function bugChallenge4() {
    /**
     * 🐛 BUG CHALLENGE: forEach doesn't await async callbacks.
     *
     * Array.prototype.forEach ignores the return value of callbacks,
     * including Promises. Async operations fire but aren't awaited.
     */
    console.log("\nBUG CHALLENGE 4: Async forEach");

    // --- BUGGY CODE ---
    console.log("  Buggy: [1,2,3].forEach(async (n) => { await fetch(n); })");
    console.log("  forEach IGNORES the returned Promise — all requests fire at once,");
    console.log("  and the code after forEach runs BEFORE they complete.");

    // --- FIXED CODE ---
    console.log("\n  Fix 1 (sequential): for...of with await");
    console.log("    for (const item of items) { await process(item); }");

    console.log("  Fix 2 (parallel):  Promise.all with map");
    console.log("    await Promise.all(items.map(item => process(item)));");

    console.log("  Fix 3 (limited parallel): Use a semaphore/pool");
}

bugChallenge4();


// ========================================================================
// BUG CHALLENGE 5: Equality Gotchas (== Coercion)
// ========================================================================

function bugChallenge5() {
    /**
     * 🐛 BUG CHALLENGE: JavaScript's == operator coercion.
     *
     * == performs type coercion before comparison, leading to
     * counterintuitive results.
     */
    console.log("\nBUG CHALLENGE 5: Equality Gotchas");

    const gotchas = [
        ['[] == false', [] == false],             // true ([] → "" → 0 → false)
        ['[] == ![]', [] == ![]],                   // true! (both coerce to 0)
        ['"" == false', "" == false],               // true
        ['"0" == false', "0" == false],             // true
        ['"" == 0', "" == 0],                       // true
        ['null == undefined', null == undefined],   // true (special case)
        ['null == 0', null == 0],                   // false (null only == undefined)
        ['NaN == NaN', NaN == NaN],                 // false! NaN is not equal to anything
    ];

    for (const [expr, result] of gotchas) {
        console.log(`  ${expr.padEnd(25)} → ${result}`);
    }

    console.log("\n  FIX: ALWAYS use === (strict equality)");
    console.log("  EXCEPTION: x == null to check for both null and undefined");
}

bugChallenge5();


// ╔══════════════════════════════════════════════════════════════════════╗
// ║  END OF ENCYCLOPEDIA                                                ║
// ╚══════════════════════════════════════════════════════════════════════╝

console.log("\n" + "=".repeat(60));
console.log("  JAVASCRIPT CS & DATA SCIENCE ENCYCLOPEDIA — COMPLETE");
console.log("=".repeat(60));
console.log("  All phases executed successfully.");
console.log("  Run: node JAVASCRIPT_CS_DS_ENCYCLOPEDIA.js");
console.log("=".repeat(60));


}); // End of asyncDemo().then() wrapper
