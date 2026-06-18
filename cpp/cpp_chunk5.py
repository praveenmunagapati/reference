# cpp_chunk5.py
# Phase 5: Bit Tricks & Memory, Phase 6: Custom String, Variadic Logger & Serializer, Phase 7: Advanced Template Metaprogramming, Phase 8: Concurrency

chunk_content = r"""
    /* ==================================================================
     *  PHASE 5: BITWISE MANIPULATION & MEMORY LAYOUTS
     * ================================================================== */

    /* 5.1 Bitwise Tricks Masterclass (20 Tricks) */
    static void bit_manipulation_demo() {
        print_sep("5.1  BITWISE MANIPULATION TRICKS");
        int n = 40;
        
        // 1. Power of 2 check
        cout << "    Is " << n << " a power of 2? " << ((n > 0 && (n & (n - 1)) == 0) ? "Yes" : "No") << "\n";
        // 2. Multiply by 2
        cout << "    " << n << " * 2 = " << (n << 1) << "\n";
        // 3. Divide by 2
        cout << "    " << n << " / 2 = " << (n >> 1) << "\n";
        // 4. Toggle bit 3 (0-indexed)
        cout << "    Toggling bit 3 of " << n << ": " << (n ^ (1 << 3)) << "\n";
        // 5. Clear bit 5
        cout << "    Clearing bit 5 of " << n << ": " << (n & ~(1 << 5)) << "\n";
        // 6. Set bit 1
        cout << "    Setting bit 1 of " << n << ": " << (n | (1 << 1)) << "\n";
        // 7. Check if odd
        cout << "    Is " << n << " odd? " << ((n & 1) ? "Yes" : "No") << "\n";
        // 8. Swap two ints with XOR
        int a = 11, b = 22;
        a ^= b; b ^= a; a ^= b;
        cout << "    XOR Swap result: a=" << a << ", b=" << b << "\n";
        // 9. Absolute value
        int v = -123;
        int mask = v >> 31;
        cout << "    Absolute value of -123: " << ((v + mask) ^ mask) << "\n";
        // 10. Counting set bits (Brian Kernighan's)
        int count = 0, temp = n;
        while (temp) { temp &= (temp - 1); count++; }
        cout << "    Set bits count in " << n << ": " << count << "\n";
        // 11. Lowest set bit mask
        cout << "    Lowest set bit of " << n << ": " << (n & -n) << "\n";
        // 12. Opposite signs check
        int s1 = 100, s2 = -200;
        cout << "    Do 100 and -200 have opposite signs? " << (((s1 ^ s2) < 0) ? "Yes" : "No") << "\n";
        // 13. Modulo by power of 2 (e.g. n % 8)
        cout << "    " << n << " % 8 = " << (n & (8 - 1)) << "\n";
        // 14. Turn off rightmost set bit
        cout << "    Turning off rightmost set bit of " << n << ": " << (n & (n - 1)) << "\n";
        // 15. Check bit at position 5
        cout << "    Bit at position 5 of " << n << ": " << ((n >> 5) & 1) << "\n";
        // 16. Power of 4 check
        bool is_pow4 = (n > 0) && ((n & (n - 1)) == 0) && ((n & 0x55555555) != 0);
        cout << "    Is " << n << " a power of 4? " << (is_pow4 ? "Yes" : "No") << "\n";
        // 17. Min of two elements
        int x = 12, y = 18;
        cout << "    Min of 12 and 18: " << (y ^ ((x ^ y) & -(x < y))) << "\n";
        // 18. Max of two elements
        cout << "    Max of 12 and 18: " << (x ^ ((x ^ y) & -(x < y))) << "\n";
        // 19. Parity check
        temp = n; bool parity = false;
        while (temp) { parity = !parity; temp &= (temp - 1); }
        cout << "    Parity of " << n << ": " << (parity ? "Odd" : "Even") << "\n";
        // 20. Count trailing zeros
        int tz = 0;
        if (n > 0) {
            int tz_temp = (n & -n);
            while (tz_temp > 1) { tz_temp >>= 1; tz++; }
        }
        cout << "    Trailing zeros in " << n << ": " << tz << "\n";
    }

    /* 5.2 Struct Alignment and Hex Memory Dumper */
    struct PaddingDemo {
        char c1;
        int i;
        char c2;
        double d;
    };

    static void raw_hexdumper(const void* addr, int len) {
        const auto* pc = static_cast<const unsigned char*>(addr);
        cout << "    Address: " << addr << " (Length: " << len << " bytes)\n";
        cout << "      ";
        for (int i = 0; i < len; i++) {
            cout << setfill('0') << setw(2) << hex << (int)pc[i] << " ";
            if ((i + 1) % 8 == 0) cout << " ";
        }
        cout << dec << "\n";
    }

    static void memory_layout_demo() {
        print_sep("5.2  STRUCT PADDING & RAW MEMORY HEXDUMP");
        cout << "    Sizeof PaddingDemo: " << sizeof(PaddingDemo) << " bytes (packed would be 14)\n";
        cout << "    Offset of c1: " << offsetof(PaddingDemo, c1) << "\n";
        cout << "    Offset of i:  " << offsetof(PaddingDemo, i) << "\n";
        cout << "    Offset of c2: " << offsetof(PaddingDemo, c2) << "\n";
        cout << "    Offset of d:  " << offsetof(PaddingDemo, d) << "\n";

        PaddingDemo demo = {'A', 9999, 'B', 3.14159};
        cout << "    Hex representation of struct PaddingDemo:\n";
        raw_hexdumper(&demo, sizeof(demo));
    }

    /* ==================================================================
     *  PHASE 6: FILE I/O, SERIALIZATION & CUSTOM STRINGS
     * ================================================================== */

    /* 6.1 Custom String operations */
    static size_t custom_strlen(const char* str) {
        const char* s = str;
        while (*s) s++;
        return s - str;
    }

    static char* custom_strcpy(char* dest, const char* src) {
        char* d = dest;
        while ((*d++ = *src++));
        return dest;
    }

    static vector<string> custom_string_split(const string& str, char delim) {
        vector<string> tokens;
        string token;
        istringstream tokenStream(str);
        while (getline(tokenStream, token, delim)) {
            tokens.push_back(token);
        }
        return tokens;
    }

    static void custom_string_trim(string& str) {
        str.erase(str.begin(), find_if(str.begin(), str.end(), [](unsigned char ch) {
            return !isspace(ch);
        }));
        str.erase(find_if(str.rbegin(), str.rend(), [](unsigned char ch) {
            return !isspace(ch);
        }).base(), str.end());
    }

    /* 6.2 Variadic Logging (C++ style parameter pack logging) */
    template <typename... Args>
    static void variadic_logger(const string& level, Args&&... args) {
        cout << "[" << level << "] ";
        (..., (cout << args << " "));
        cout << "\n";
    }

    /* 6.3 BST Serialization & Deserialization */
    static void serialize_bst_helper(const BSTNode<int>* node, ofstream& ofs) {
        if (!node) {
            int marker = -1;
            ofs.write(reinterpret_cast<const char*>(&marker), sizeof(marker));
            return;
        }
        ofs.write(reinterpret_cast<const char*>(&node->data), sizeof(node->data));
        serialize_bst_helper(node->left.get(), ofs);
        serialize_bst_helper(node->right.get(), ofs);
    }

    static unique_ptr<BSTNode<int>> deserialize_bst_helper(ifstream& ifs) {
        int val;
        if (!ifs.read(reinterpret_cast<char*>(&val), sizeof(val))) return nullptr;
        if (val == -1) return nullptr;
        auto node = make_unique<BSTNode<int>>(val);
        node->left = deserialize_bst_helper(ifs);
        node->right = deserialize_bst_helper(ifs);
        return node;
    }

    static void strings_io_demo() {
        print_sep("PHASE 6: CUSTOM STRINGS, VARIADIC LOGGING & SERIALIZATION");
        
        char test_buf[20];
        custom_strcpy(test_buf, "CopySuccess");
        cout << "    custom_strcpy: " << test_buf << " (length=" << custom_strlen(test_buf) << ")\n";

        string csv = "Data,Science,C++,Algorithms,Structures";
        cout << "    Split CSV: ";
        for (const auto& tok : custom_string_split(csv, ',')) cout << "[" << tok << "] ";
        cout << "\n";

        string pad = "   Trimmed String   ";
        custom_string_trim(pad);
        cout << "    Trimmed: '" << pad << "'\n";

        variadic_logger("INFO", "Starting up services, tick count:", clock());
        variadic_logger("WARN", "Memory load high, usage:", 85, "%");

        BST<int> tree;
        tree.insert(100);
        tree.insert(50);
        tree.insert(150);
        
        string filename = "cxx_tree.bin";
        ofstream ofs(filename, ios::binary);
        if (ofs) {
            serialize_bst_helper(tree.root.get(), ofs);
            ofs.close();
        }

        BST<int> deserialized_tree;
        ifstream ifs(filename, ios::binary);
        if (ifs) {
            deserialized_tree.root = deserialize_bst_helper(ifs);
            ifs.close();
        }
        cout << "    Deserialized BST Inorder: ";
        deserialized_tree.inorder();
        filesystem::remove(filename);
    }

    /* ==================================================================
     *  PHASE 7: ADVANCED TEMPLATE METAPROGRAMMING
     * ================================================================== */

    // Fold expressions (C++17)
    template <typename... Args>
    static void fold_expression_printer(Args&&... args) {
        cout << "    Fold expressions printing arguments: ";
        (..., (cout << args << " "));
        cout << "\n";
    }

    // SFINAE checks
    template <typename T>
    typename enable_if<is_integral<T>::value, bool>::type
    cxx_is_integer(T) { return true; }

    template <typename T>
    typename enable_if<!is_integral<T>::value, bool>::type
    cxx_is_integer(T) { return false; }

    // Constexpr calculations
    constexpr int constexpr_factorial(int n) {
        return (n <= 1) ? 1 : n * constexpr_factorial(n - 1);
    }

    static void preprocessor_demo() {
        print_sep("PHASE 7: ADVANCED C++ METAPROGRAMMING");
        fold_expression_printer(123, "C++17", 3.14f, 'X', true);
        cout << "    Is 42 integer? " << (cxx_is_integer(42) ? "Yes" : "No") << "\n";
        cout << "    Is 3.14 integer? " << (cxx_is_integer(3.14) ? "Yes" : "No") << "\n";
        constexpr int val_5 = constexpr_factorial(5);
        cout << "    constexpr factorial(5) = " << val_5 << " (calculated at compile-time)\n";
    }

    /* ==================================================================
     *  PHASE 8: CONCURRENCY & MULTITHREADING
     * ================================================================== */

    // Thread-safe Bounded queue (Producer-Consumer)
    class BoundedQueue {
    private:
        queue<int> q;
        size_t max_size;
        mutex mtx;
        condition_variable cv_prod;
        condition_variable cv_cons;
    public:
        BoundedQueue(size_t s) : max_size(s) {}

        void push(int val) {
            unique_lock<mutex> lock(mtx);
            cv_prod.wait(lock, [this]() { return q.size() < max_size; });
            q.push(val);
            cv_cons.notify_one();
        }

        int pop() {
            unique_lock<mutex> lock(mtx);
            cv_cons.wait(lock, [this]() { return !q.empty(); });
            int val = q.front();
            q.pop();
            cv_prod.notify_one();
            return val;
        }
    };

    // Shared reader-writer database
    class SharedDatabase {
    private:
        shared_mutex rw_mtx;
        int value = 0;
    public:
        void write(int new_val) {
            unique_lock<shared_mutex> lock(rw_mtx);
            value = new_val;
        }
        int read() {
            shared_lock<shared_mutex> lock(rw_mtx);
            return value;
        }
    };

    static void concurrency_demo() {
        print_sep("PHASE 8: CONCURRENCY & MULTITHREADING");
        BoundedQueue bq(2);
        
        thread producer([&bq]() {
            for (int i = 0; i < 3; i++) {
                bq.push((i + 1) * 100);
            }
        });

        thread consumer([&bq]() {
            for (int i = 0; i < 3; i++) {
                cout << "    Consumer popped: " << bq.pop() << "\n";
            }
        });

        producer.join();
        consumer.join();

        SharedDatabase db;
        db.write(42);
        
        future<int> fut = async(launch::async, [&db]() {
            return db.read();
        });
        cout << "    Async read task result: " << fut.get() << "\n";
    }
"""
