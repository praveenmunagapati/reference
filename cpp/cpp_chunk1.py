# cpp_chunk1.py
# Phase 2 (Part 1): Custom Allocators (Arena, Pool), OOP Shapes, Lists, BST, AVL Tree, Red-Black Tree

chunk_content = r"""
    /* ==================================================================
     *  PHASE 2: CUSTOM MEMORY ALLOCATORS & TEMPLATED DATA STRUCTURES
     * ================================================================== */

    /* 2.1 Custom Systems Allocators */
    class ArenaAllocator {
    private:
        size_t capacity;
        uint8_t* buffer;
        size_t offset;
    public:
        ArenaAllocator(size_t cap) : capacity(cap), offset(0) {
            buffer = new uint8_t[capacity];
        }
        ~ArenaAllocator() {
            delete[] buffer;
        }
        void* allocate(size_t size, size_t alignment = 8) {
            size_t current_address = reinterpret_cast<size_t>(buffer + offset);
            size_t padding = (alignment - (current_address % alignment)) % alignment;
            if (offset + padding + size > capacity) {
                throw bad_alloc();
            }
            offset += padding;
            void* ptr = buffer + offset;
            offset += size;
            return ptr;
        }
        void reset() {
            offset = 0;
        }
        size_t get_used() const { return offset; }
        size_t get_capacity() const { return capacity; }
    };

    class PoolAllocator {
    private:
        struct Node {
            Node* next;
        };
        size_t block_size;
        size_t num_blocks;
        uint8_t* buffer;
        Node* free_list;
    public:
        PoolAllocator(size_t b_size, size_t n_blocks)
            : block_size(b_size), num_blocks(n_blocks), free_list(nullptr) {
            if (block_size < sizeof(Node)) block_size = sizeof(Node);
            buffer = new uint8_t[block_size * num_blocks];
            reset();
        }
        ~PoolAllocator() {
            delete[] buffer;
        }
        void reset() {
            free_list = nullptr;
            for (size_t i = 0; i < num_blocks; i++) {
                auto* node = reinterpret_cast<Node*>(buffer + i * block_size);
                node->next = free_list;
                free_list = node;
            }
        }
        void* allocate() {
            if (!free_list) throw bad_alloc();
            Node* node = free_list;
            free_list = free_list->next;
            return reinterpret_cast<void*>(node);
        }
        void deallocate(void* ptr) {
            if (!ptr) return;
            auto* node = reinterpret_cast<Node*>(ptr);
            node->next = free_list;
            free_list = node;
        }
    };

    static void allocators_demo() {
        print_sep("2.1  CUSTOM SYSTEMS ALLOCATORS (ARENA & POOL)");
        
        ArenaAllocator arena(1024);
        int* val1 = static_cast<int*>(arena.allocate(sizeof(int)));
        double* val2 = static_cast<double*>(arena.allocate(sizeof(double)));
        *val1 = 12345;
        *val2 = 98765.4321;
        cout << "    Arena Allocator: Allocated int=" << *val1 << ", double=" << *val2 << "\n";
        cout << "    Arena metrics: used=" << arena.get_used() << " bytes, capacity=" << arena.get_capacity() << " bytes\n";

        PoolAllocator pool(16, 4); // 4 blocks of size 16
        void* b1 = pool.allocate();
        void* b2 = pool.allocate();
        cout << "    Pool Allocator: Allocated block 1 at " << b1 << ", block 2 at " << b2 << "\n";
        pool.deallocate(b1);
        void* b3 = pool.allocate();
        cout << "    Pool Allocator: Allocated block 3 (reusing block 1) at " << b3 << "\n";
    }

    /* 2.2 OOP Shapes Extension */
    class Rectangle : public BaseShape {
        double w, h;
    public:
        Rectangle(double width, double height) : w(width), h(height) {}
        double area() const override { return w * h; }
        void describe() const override {
            cout << "  Rectangle: Width = " << w << ", Height = " << h << ", Area = " << area() << "\n";
        }
    };

    class Triangle : public BaseShape {
        double b, h;
    public:
        Triangle(double base, double height) : b(base), h(height) {}
        double area() const override { return 0.5 * b * h; }
        void describe() const override {
            cout << "  Triangle: Base = " << b << ", Height = " << h << ", Area = " << area() << "\n";
        }
    };

    class Square : public BaseShape {
        double s;
    public:
        Square(double side) : s(side) {}
        double area() const override { return s * s; }
        void describe() const override {
            cout << "  Square: Side = " << s << ", Area = " << area() << "\n";
        }
    };

    static void oop_extension_demo() {
        print_sep("2.2  OOP INHERITANCE POLYMORPHISM EXTENSION");
        vector<unique_ptr<BaseShape>> shapes;
        shapes.push_back(make_unique<Rectangle>(4.0, 5.0));
        shapes.push_back(make_unique<Triangle>(4.0, 3.0));
        shapes.push_back(make_unique<Square>(6.0));
        for (const auto& s : shapes) {
            s->describe();
        }
    }

    /* 2.3 Linked Lists: Singly, Doubly & Circular Linked Lists */
    template <typename T>
    struct SinglyNode {
        T data;
        unique_ptr<SinglyNode> next;
        SinglyNode(T val) : data(val), next(nullptr) {}
    };

    template <typename T>
    class SinglyLinkedList {
    public:
        unique_ptr<SinglyNode<T>> head;

        void insert(T val) {
            auto new_node = make_unique<SinglyNode<T>>(val);
            if (!head) {
                head = move(new_node);
            } else {
                SinglyNode<T>* temp = head.get();
                while (temp->next) {
                    temp = temp->next.get();
                }
                temp->next = move(new_node);
            }
        }

        void delete_val(T val) {
            if (!head) return;
            if (head->data == val) {
                head = move(head->next);
                return;
            }
            SinglyNode<T>* temp = head.get();
            while (temp->next && temp->next->data != val) {
                temp = temp->next.get();
            }
            if (temp->next) {
                temp->next = move(temp->next->next);
            }
        }

        void reverse() {
            unique_ptr<SinglyNode<T>> prev = nullptr;
            unique_ptr<SinglyNode<T>> curr = move(head);
            while (curr) {
                unique_ptr<SinglyNode<T>> next_node = move(curr->next);
                curr->next = move(prev);
                prev = move(curr);
                curr = move(next_node);
            }
            head = move(prev);
        }

        bool has_cycle() const {
            if (!head) return false;
            SinglyNode<T>* slow = head.get();
            SinglyNode<T>* fast = head.get();
            while (fast && fast->next) {
                slow = slow->next.get();
                fast = fast->next->next.get();
                if (slow == fast) return true;
            }
            return false;
        }

        void print() const {
            SinglyNode<T>* temp = head.get();
            while (temp) {
                cout << temp->data << " -> ";
                temp = temp->next.get();
            }
            cout << "nullptr\n";
        }
    };

    template <typename T>
    struct DoublyNode {
        T data;
        shared_ptr<DoublyNode<T>> next;
        weak_ptr<DoublyNode<T>> prev;
        DoublyNode(T val) : data(val), next(nullptr) {}
    };

    template <typename T>
    class DoublyLinkedList {
    public:
        shared_ptr<DoublyNode<T>> head;
        shared_ptr<DoublyNode<T>> tail;

        void insert(T val) {
            auto new_node = make_shared<DoublyNode<T>>(val);
            if (!head) {
                head = tail = new_node;
            } else {
                tail->next = new_node;
                new_node->prev = tail;
                tail = new_node;
            }
        }

        void reverse() {
            shared_ptr<DoublyNode<T>> temp = nullptr;
            shared_ptr<DoublyNode<T>> curr = head;
            tail = head;
            while (curr) {
                temp = curr->prev.lock();
                curr->prev = curr->next;
                curr->next = temp;
                curr = curr->prev.lock();
            }
            if (temp) {
                head = temp->prev.lock();
            }
        }

        void print() const {
            shared_ptr<DoublyNode<T>> temp = head;
            while (temp) {
                cout << temp->data << " <-> ";
                temp = temp->next;
            }
            cout << "nullptr\n";
        }
    };

    template <typename T>
    struct CircularNode {
        T data;
        CircularNode* next = nullptr;
        CircularNode(T val) : data(val) {}
    };

    template <typename T>
    class CircularLinkedList {
    public:
        CircularNode<T>* head = nullptr;

        ~CircularLinkedList() {
            if (!head) return;
            CircularNode<T>* curr = head;
            CircularNode<T>* next_node = nullptr;
            do {
                next_node = curr->next;
                delete curr;
                curr = next_node;
            } while (curr != head);
        }

        void insert(T val) {
            auto new_node = new CircularNode<T>(val);
            if (!head) {
                head = new_node;
                head->next = head;
            } else {
                CircularNode<T>* temp = head;
                while (temp->next != head) {
                    temp = temp->next;
                }
                temp->next = new_node;
                new_node->next = head;
            }
        }

        void print() const {
            if (!head) return;
            CircularNode<T>* temp = head;
            do {
                cout << temp->data << " -> ";
                temp = temp->next;
            } while (temp != head);
            cout << "(head)\n";
        }
    };

    static void lists_demo() {
        print_sep("2.3  TEMPLATED LINKED LISTS DEMO");
        SinglyLinkedList<int> s_list;
        s_list.insert(1);
        s_list.insert(2);
        s_list.insert(3);
        cout << "    SinglyList: ";
        s_list.print();
        s_list.reverse();
        cout << "    SinglyList Reversed: ";
        s_list.print();

        DoublyLinkedList<string> d_list;
        d_list.insert("C++");
        d_list.insert("STL");
        d_list.insert("Templates");
        cout << "    DoublyList: ";
        d_list.print();
        d_list.reverse();
        cout << "    DoublyList Reversed: ";
        d_list.print();

        CircularLinkedList<int> c_list;
        c_list.insert(10);
        c_list.insert(20);
        c_list.insert(30);
        cout << "    CircularList: ";
        c_list.print();
    }

    /* 2.4 Trees: Binary Search Tree (BST), AVL Tree, Red-Black Tree (RBT) */
    template <typename T>
    struct BSTNode {
        T data;
        unique_ptr<BSTNode<T>> left;
        unique_ptr<BSTNode<T>> right;
        BSTNode(T val) : data(val), left(nullptr), right(nullptr) {}
    };

    template <typename T>
    class BST {
    private:
        unique_ptr<BSTNode<T>> insert_helper(unique_ptr<BSTNode<T>> node, T val) {
            if (!node) return make_unique<BSTNode<T>>(val);
            if (val < node->data) {
                node->left = insert_helper(move(node->left), val);
            } else if (val > node->data) {
                node->right = insert_helper(move(node->right), val);
            }
            return node;
        }

        bool search_helper(const BSTNode<T>* node, T val) const {
            if (!node) return false;
            if (node->data == val) return true;
            if (val < node->data) return search_helper(node->left.get(), val);
            return search_helper(node->right.get(), val);
        }

        unique_ptr<BSTNode<T>> remove_helper(unique_ptr<BSTNode<T>> node, T val) {
            if (!node) return nullptr;
            if (val < node->data) {
                node->left = remove_helper(move(node->left), val);
            } else if (val > node->data) {
                node->right = remove_helper(move(node->right), val);
            } else {
                if (!node->left) return move(node->right);
                if (!node->right) return move(node->left);
                BSTNode<T>* min_node = node->right.get();
                while (min_node->left) min_node = min_node->left.get();
                node->data = min_node->data;
                node->right = remove_helper(move(node->right), min_node->data);
            }
            return node;
        }

        void inorder_helper(const BSTNode<T>* node) const {
            if (node) {
                inorder_helper(node->left.get());
                cout << node->data << " ";
                inorder_helper(node->right.get());
            }
        }

    public:
        unique_ptr<BSTNode<T>> root;

        void insert(T val) { root = insert_helper(move(root), val); }
        bool search(T val) const { return search_helper(root.get(), val); }
        void remove(T val) { root = remove_helper(move(root), val); }
        void inorder() const { inorder_helper(root.get()); cout << "\n"; }
    };

    template <typename T>
    struct AVLNode {
        T data;
        int height;
        unique_ptr<AVLNode<T>> left;
        unique_ptr<AVLNode<T>> right;
        AVLNode(T val) : data(val), height(1), left(nullptr), right(nullptr) {}
    };

    template <typename T>
    class AVLTree {
    private:
        int height(const AVLNode<T>* n) const { return n ? n->height : 0; }
        int balance_factor(const AVLNode<T>* n) const { return n ? height(n->left.get()) - height(n->right.get()) : 0; }

        unique_ptr<AVLNode<T>> rotate_right(unique_ptr<AVLNode<T>> y) {
            auto x = move(y->left);
            y->left = move(x->right);
            y->height = max(height(y->left.get()), height(y->right.get())) + 1;
            x->height = max(height(x->left.get()), height(x->right.get())) + 1;
            x->right = move(y);
            return x;
        }

        unique_ptr<AVLNode<T>> rotate_left(unique_ptr<AVLNode<T>> x) {
            auto y = move(x->right);
            x->right = move(y->left);
            x->height = max(height(x->left.get()), height(x->right.get())) + 1;
            y->height = max(height(y->left.get()), height(y->right.get())) + 1;
            y->left = move(x);
            return y;
        }

        unique_ptr<AVLNode<T>> insert_helper(unique_ptr<AVLNode<T>> node, T val) {
            if (!node) return make_unique<AVLNode<T>>(val);
            if (val < node->data) {
                node->left = insert_helper(move(node->left), val);
            } else if (val > node->data) {
                node->right = insert_helper(move(node->right), val);
            } else {
                return node;
            }

            node->height = max(height(node->left.get()), height(node->right.get())) + 1;
            int bf = balance_factor(node.get());

            if (bf > 1 && val < node->left->data) return rotate_right(move(node));
            if (bf < -1 && val > node->right->data) return rotate_left(move(node));
            if (bf > 1 && val > node->left->data) {
                node->left = rotate_left(move(node->left));
                return rotate_right(move(node));
            }
            if (bf < -1 && val < node->right->data) {
                node->right = rotate_right(move(node->right));
                return rotate_left(move(node));
            }
            return node;
        }

        void inorder_helper(const AVLNode<T>* node) const {
            if (node) {
                inorder_helper(node->left.get());
                cout << node->data << " ";
                inorder_helper(node->right.get());
            }
        }

    public:
        unique_ptr<AVLNode<T>> root;

        void insert(T val) { root = insert_helper(move(root), val); }
        void inorder() const { inorder_helper(root.get()); cout << "\n"; }
    };

    enum RBTColor { RED, BLACK };

    template <typename T>
    struct RBTNode {
        T data;
        RBTColor color;
        RBTNode* left = nullptr;
        RBTNode* right = nullptr;
        RBTNode* parent = nullptr;
        RBTNode(T val) : data(val), color(RED) {}
    };

    template <typename T>
    class RedBlackTree {
    private:
        RBTNode<T>* root = nullptr;

        void rotate_left(RBTNode<T>*& x) {
            RBTNode<T>* y = x->right;
            x->right = y->left;
            if (y->left != nullptr) y->left->parent = x;
            y->parent = x->parent;
            if (x->parent == nullptr) root = y;
            else if (x == x->parent->left) x->parent->left = y;
            else x->parent->right = y;
            y->left = x;
            x->parent = y;
        }

        void rotate_right(RBTNode<T>*& x) {
            RBTNode<T>* y = x->left;
            x->left = y->right;
            if (y->right != nullptr) y->right->parent = x;
            y->parent = x->parent;
            if (x->parent == nullptr) root = y;
            else if (x == x->parent->right) x->parent->right = y;
            else x->parent->left = y;
            y->right = x;
            x->parent = y;
        }

        void fix_insert(RBTNode<T>*& k) {
            RBTNode<T>* u;
            while (k->parent && k->parent->color == RED) {
                if (k->parent == k->parent->parent->right) {
                    u = k->parent->parent->left;
                    if (u && u->color == RED) {
                        u->color = BLACK;
                        k->parent->color = BLACK;
                        k->parent->parent->color = RED;
                        k = k->parent->parent;
                    } else {
                        if (k == k->parent->left) {
                            k = k->parent;
                            rotate_right(k);
                        }
                        k->parent->color = BLACK;
                        k->parent->parent->color = RED;
                        rotate_left(k->parent->parent);
                    }
                } else {
                    u = k->parent->parent->right;
                    if (u && u->color == RED) {
                        u->color = BLACK;
                        k->parent->color = BLACK;
                        k->parent->parent->color = RED;
                        k = k->parent->parent;
                    } else {
                        if (k == k->parent->right) {
                            k = k->parent;
                            rotate_left(k);
                        }
                        k->parent->color = BLACK;
                        k->parent->parent->color = RED;
                        rotate_right(k->parent->parent);
                    }
                }
                if (k == root) break;
            }
            root->color = BLACK;
        }

        void inorder_helper(RBTNode<T>* node) const {
            if (node) {
                inorder_helper(node->left);
                cout << node->data << (node->color == RED ? "(R) " : "(B) ");
                inorder_helper(node->right);
            }
        }

        void free_tree(RBTNode<T>* node) {
            if (node) {
                free_tree(node->left);
                free_tree(node->right);
                delete node;
            }
        }

    public:
        ~RedBlackTree() { free_tree(root); }

        void insert(T val) {
            RBTNode<T>* node = new RBTNode<T>(val);
            RBTNode<T>* y = nullptr;
            RBTNode<T>* x = root;
            while (x != nullptr) {
                y = x;
                if (node->data < x->data) x = x->left;
                else x = x->right;
            }
            node->parent = y;
            if (y == nullptr) root = node;
            else if (node->data < y->data) y->left = node;
            else y->right = node;

            if (node->parent == nullptr) {
                node->color = BLACK;
                return;
            }
            if (node->parent->parent == nullptr) return;
            fix_insert(node);
        }

        void inorder() const { inorder_helper(root); cout << "\n"; }
    };

    static void trees_demo() {
        print_sep("2.4  TEMPLATED TREE STRUCTURES (BST, AVL, RED-BLACK)");
        
        BST<int> bst;
        bst.insert(50);
        bst.insert(30);
        bst.insert(70);
        bst.insert(20);
        bst.insert(40);
        cout << "    BST Inorder: ";
        bst.inorder();
        bst.remove(30);
        cout << "    BST after removing 30: ";
        bst.inorder();

        AVLTree<int> avl;
        avl.insert(10);
        avl.insert(20);
        avl.insert(30);
        avl.insert(40);
        avl.insert(50);
        avl.insert(25);
        cout << "    AVL balanced inorder traversal: ";
        avl.inorder();

        RedBlackTree<int> rbt;
        rbt.insert(7);
        rbt.insert(3);
        rbt.insert(18);
        rbt.insert(10);
        rbt.insert(22);
        rbt.insert(8);
        rbt.insert(11);
        cout << "    RBT inorder traversal (color annotated): ";
        rbt.inorder();
    }
"""
