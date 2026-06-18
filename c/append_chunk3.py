# append_chunk3.py
# Appends Phase 5, Phase 6, and Phase 7 sections to build_cs_ds_encyclopedia_c.py

import os

c_quote = "'''"

chunk_content = r"""
# ---------------------------------------------------------------------------
# PHASE 5: MEMORY LAYOUT & BIT MANIPULATION
# ---------------------------------------------------------------------------
add_section("PHASE_5_MEMORY_LAYOUT_BIT", r{c_quote}
/* ==================================================================
 *  PHASE 5: MEMORY LAYOUT & BIT MANIPULATION
 * ================================================================== */

/* 5.1 Bitwise Tricks */
static void bit_manipulation_demo(void) {
    print_sep("5.1  BITWISE MANIPULATION TRICKS");
    
    int x = 40; // 00101000 in binary
    
    // 1. Check if power of 2
    bool is_pow2 = (x > 0) && ((x & (x - 1)) == 0);
    printf("    Is %d a power of 2? %s\n", x, is_pow2 ? "Yes" : "No");
    
    // 2. Multiply by 2 via shift
    printf("    %d * 2 = %d (via shift)\n", x, x << 1);
    
    // 3. Divide by 2 via shift
    printf("    %d / 2 = %d (via shift)\n", x, x >> 1);
    
    // 4. Toggle a bit (e.g., bit 3)
    int toggled = x ^ (1 << 3);
    printf("    Toggling bit 3 of %d: result = %d\n", x, toggled);
    
    // 5. Clear a bit (e.g., bit 5)
    int cleared = x & ~(1 << 5);
    printf("    Clearing bit 5 of %d: result = %d\n", x, cleared);
    
    // 6. Set a bit (e.g., bit 1)
    int setted = x | (1 << 1);
    printf("    Setting bit 1 of %d: result = %d\n", x, setted);
    
    // 7. Check if even/odd
    printf("    Is %d odd? %s\n", x, (x & 1) ? "Yes" : "No");
    
    // 8. Swap two numbers without temporary variable
    int a = 11, b = 22;
    printf("    Before swap: a = %d, b = %d\n", a, b);
    a = a ^ b;
    b = a ^ b;
    a = a ^ b;
    printf("    After swap: a = %d, b = %d\n", a, b);

    // 9. Absolute value without branching
    int n_val = -123;
    int temp_mask = n_val >> (sizeof(int) * 8 - 1);
    int abs_val = (n_val ^ temp_mask) - temp_mask;
    printf("    Absolute value of %d: %d\n", n_val, abs_val);

    // 10. Counting set bits (popcount)
    int count = 0;
    int pop_temp = x;
    while (pop_temp) {
        pop_temp &= (pop_temp - 1);
        count++;
    }
    printf("    Set bits count in %d: %d\n", x, count);

    // 11. Extract lowest set bit
    printf("    Lowest set bit of %d: %d\n", x, x & (-x));

    // 12. Check if opposite signs
    int sign1 = 100, sign2 = -200;
    bool opposite = ((sign1 ^ sign2) < 0);
    printf("    Do %d and %d have opposite signs? %s\n", sign1, sign2, opposite ? "Yes" : "No");

    // 13. Modulo with power of 2
    int pow2_mod = 8;
    printf("    %d %% %d = %d (via bitwise)\n", x, pow2_mod, x & (pow2_mod - 1));

    // 14. Turn off the rightmost set bit
    printf("    Turning off rightmost set bit of %d: %d\n", x, x & (x - 1));

    // 15. Check bit at position 5
    printf("    Bit at position 5 of %d: %d\n", x, (x >> 5) & 1);

    // 16. Power of 4 check
    bool is_pow4 = (x > 0) && ((x & (x - 1)) == 0) && ((x & 0x55555555) != 0);
    printf("    Is %d a power of 4? %s\n", x, is_pow4 ? "Yes" : "No");

    // 17. Minimum of two values without branching
    int val1 = 12, val2 = 18;
    int min_val = val2 ^ ((val1 ^ val2) & -(val1 < val2));
    printf("    Min of %d and %d: %d\n", val1, val2, min_val);

    // 18. Maximum of two values without branching
    int max_val = val1 ^ ((val1 ^ val2) & -(val1 < val2));
    printf("    Max of %d and %d: %d\n", val1, val2, max_val);

    // 19. Check parity
    bool parity = false;
    int par_temp = x;
    while (par_temp) {
        parity = !parity;
        par_temp &= (par_temp - 1);
    }
    printf("    Parity of %d (true=odd, false=even): %s\n", x, parity ? "Odd" : "Even");

    // 20. Count trailing zeros
    int tz_count = 0;
    if (x > 0) {
        int temp_tz = (x ^ (x - 1)) >> 1;
        while (temp_tz) {
            tz_count++;
            temp_tz >>= 1;
        }
    }
    printf("    Trailing zeros in %d: %d\n", x, tz_count);
}

/* 5.2 Hex Memory Dumper */
static void memory_hexdump(const void *addr, size_t len) {
    const unsigned char *pc = (const unsigned char*)addr;
    char buff[17];
    size_t i;
    for (i = 0; i < len; i++) {
        if ((i % 16) == 0) {
            if (i != 0) printf("  | %s\n", buff);
            printf("    %08x ", (unsigned int)(uintptr_t)(pc + i));
        }
        printf(" %02x", pc[i]);
        if ((pc[i] >= 0x20) && (pc[i] <= 0x7e)) buff[i % 16] = pc[i];
        else buff[i % 16] = '.';
        buff[(i % 16) + 1] = '\0';
    }
    while ((i % 16) != 0) {
        printf("   ");
        buff[i % 16] = ' ';
        buff[(i % 16) + 1] = '\0';
        i++;
    }
    printf("  | %s\n", buff);
}

/* 5.3 Struct Alignment & Padding */
struct PaddingDemo {
    char c1;      // 1 byte
                  // 3 bytes padding
    int i;        // 4 bytes
    char c2;      // 1 byte
                  // 7 bytes padding
    double d;     // 8 bytes
};

static void memory_layout_demo(void) {
    print_sep("5.2, 5.3  STRUCT PADDING & RAW MEMORY HEXDUMP");
    printf("  Sizeof PaddingDemo: %zu bytes (packed would be 14)\n", sizeof(struct PaddingDemo));
    printf("  Offset of elements:\n");
    printf("    c1: offset = %zu\n", offsetof(struct PaddingDemo, c1));
    printf("    i:  offset = %zu\n", offsetof(struct PaddingDemo, i));
    printf("    c2: offset = %zu\n", offsetof(struct PaddingDemo, c2));
    printf("    d:  offset = %zu\n", offsetof(struct PaddingDemo, d));

    struct PaddingDemo demo = {'A', 9999, 'B', 3.141592};
    printf("\n  Raw Hex Dump of PaddingDemo struct memory:\n");
    memory_hexdump(&demo, sizeof(demo));
}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 6: FILE I/O, SERIALIZATION & CUSTOM STRINGS
# ---------------------------------------------------------------------------
add_section("PHASE_6_CUSTOM_STR_SER", r{c_quote}
/* ==================================================================
 *  PHASE 6: FILE I/O, SERIALIZATION & CUSTOM STRINGS
 * ================================================================== */

/* 6.1 Custom String Implementations */
static size_t custom_strlen(const char *str) {
    const char *s = str;
    while (*s) s++;
    return s - str;
}

static char *custom_strcpy(char *dest, const char *src) {
    char *d = dest;
    while ((*d++ = *src++));
    return dest;
}

static char *custom_strtok_r(char *str, const char *delim, char **saveptr) {
    char *token;
    if (str == NULL) str = *saveptr;
    if (str == NULL || *str == '\0') {
        *saveptr = NULL;
        return NULL;
    }
    str += strspn(str, delim);
    if (*str == '\0') {
        *saveptr = NULL;
        return NULL;
    }
    token = str;
    str = strpbrk(token, delim);
    if (str == NULL) {
        *saveptr = NULL;
    } else {
        *str = '\0';
        *saveptr = str + 1;
    }
    return token;
}

static void string_trim_spaces(char *str) {
    int start = 0;
    while (str[start] != '\0' && isspace((unsigned char)str[start])) {
        start++;
    }
    int len = custom_strlen(str);
    int end = len - 1;
    while (end >= start && isspace((unsigned char)str[end])) {
        end--;
    }
    int idx = 0;
    for (int i = start; i <= end; i++) {
        str[idx++] = str[i];
    }
    str[idx] = '\0';
}

static void string_reverse(char *str) {
    int i = 0;
    int j = custom_strlen(str) - 1;
    while (i < j) {
        char tmp = str[i];
        str[i] = str[j];
        str[j] = tmp;
        i++; j--;
    }
}

/* 6.2 Variadic Loggers */
typedef enum { LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR } LogLevel;

static void variadic_logger(LogLevel level, const char *fmt, ...) {
    const char *labels[] = { "DEBUG", "INFO", "WARN", "ERROR" };
    printf("[%s] ", labels[level]);
    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
    printf("\n");
}

/* 6.3 Binary Tree Serialization and Deserialization */
static void bst_serialize_rec(const BSTNode *root, FILE *fp) {
    if (!root) {
        int marker = -1;
        fwrite(&marker, sizeof(int), 1, fp);
        return;
    }
    fwrite(&root->data, sizeof(int), 1, fp);
    bst_serialize_rec(root->left, fp);
    bst_serialize_rec(root->right, fp);
}

static bool bst_serialize(const BSTNode *root, const char *filename) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) return false;
    bst_serialize_rec(root, fp);
    fclose(fp);
    return true;
}

static BSTNode *bst_deserialize_rec(FILE *fp) {
    int val;
    if (fread(&val, sizeof(int), 1, fp) != 1) return NULL;
    if (val == -1) return NULL;
    
    BSTNode *node = bst_new_node(val);
    node->left = bst_deserialize_rec(fp);
    node->right = bst_deserialize_rec(fp);
    return node;
}

static BSTNode *bst_deserialize(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) return NULL;
    BSTNode *root = bst_deserialize_rec(fp);
    fclose(fp);
    return root;
}

static void strings_io_demo(void) {
    print_sep("PHASE 6: CUSTOM STRINGS, VARIADIC LOGGING & BST FILE SERIALIZATION");
    
    /* Tokenizer */
    char test_str[] = "Data,Science,Computer,Science,Algorithms";
    char *save_ptr = NULL;
    char *token = custom_strtok_r(test_str, ",", &save_ptr);
    printf("  Custom strtok_r splits: ");
    while (token) {
        printf("[%s] ", token);
        token = custom_strtok_r(NULL, ",", &save_ptr);
    }
    printf("\n");

    /* Variadic Logger */
    variadic_logger(LOG_INFO, "System started up at %ld ticks", (long)clock());
    variadic_logger(LOG_WARN, "Memory pool approaching capacity threshold: %d%% used", 85);

    /* BST Serialization */
    BSTNode *root = bst_new_node(50);
    bst_insert(root, 30);
    bst_insert(root, 70);
    bst_insert(root, 20);
    bst_insert(root, 40);
    
    const char *db_file = "binary_tree_db.bin";
    if (bst_serialize(root, db_file)) {
        printf("  Re-serialized BST successfully to '%s'.\n", db_file);
        BSTNode *deser_root = bst_deserialize(db_file);
        if (deser_root) {
            printf("  Deserialized BST root data matches: %d (inorder: ", deser_root->data);
            bst_inorder(deser_root);
            printf(")\n");
            bst_free(deser_root);
        }
        remove(db_file);
    }
    bst_free(root);
}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 7: PREPROCESSOR & MACROS
# ---------------------------------------------------------------------------
add_section("PHASE_7_PREPROCESSOR_MACROS", r{c_quote}
/* ==================================================================
 *  PHASE 7: PREPROCESSOR & MACROS
 * ================================================================== */

/* Safe do-while wrapping macro */
#define SAFE_PRINT(str) \
    do { \
        printf("    [SAFE_PRINT] Log: %s\n", str); \
    } while (0)

/* Compile-time static assertions */
#define STATIC_ASSERT(expr, msg) \
    typedef char static_assertion_##msg[(expr) ? 1 : -1]

STATIC_ASSERT(sizeof(int) >= 4, int_is_at_least_32_bits);

/* Generic mathematical functions using C11 _Generic selection */
static double add_doubles(double a, double b) { return a + b; }
static float add_floats(float a, float b) { return a + b; }
static int add_ints(int a, int b) { return a + b; }

#define generic_add(x, y) _Generic((x), \
    double: add_doubles, \
    float: add_floats, \
    default: add_ints \
)(x, y)

static void preprocessor_demo(void) {
    print_sep("PHASE 7: PREPROCESSOR, STATIC ASSERTIONS & _Generic SELECTION");
    SAFE_PRINT("Testing macro safety execution boundaries.");
    
    int val_i = generic_add(10, 20);
    float val_f = generic_add(1.5f, 2.5f);
    double val_d = generic_add(3.14, 2.71);
    
    printf("  _Generic selection additions:\n");
    printf("    generic_add(int):    %d\n", val_i);
    printf("    generic_add(float):  %.4f\n", val_f);
    printf("    generic_add(double): %.4f\n", val_d);
}
{c_quote})
""".replace("{c_quote}", c_quote)

# Read current build_cs_ds_encyclopedia_c.py
with open("build_cs_ds_encyclopedia_c.py", "r", encoding="utf-8") as f:
    builder_content = f.read()

# Locate the line "''')" of the last section
last_quote_index = builder_content.rfind("''')")
if last_quote_index == -1:
    print("Could not find the last ''') in build_cs_ds_encyclopedia_c.py")
else:
    # Append the chunk_content right after the last quote
    builder_content = builder_content[:last_quote_index + 4] + "\n" + chunk_content
    with open("build_cs_ds_encyclopedia_c.py", "w", encoding="utf-8") as f:
        f.write(builder_content)
    print("Chunk 3 appended successfully!")
