# cpp_chunk2.py
# Phase 2 (Part 2): Spatial KD-Tree, Segment Tree with Lazy Propagation, Skip List, Trie, Min/Max Heap, Resizing Hash Table, Graph Algorithms

chunk_content = r"""
    /* 2.3 Spatial Data Structures: KD-Tree (Nearest Neighbor Search) */
    struct KDNode {
        vector<double> point;
        unique_ptr<KDNode> left;
        unique_ptr<KDNode> right;
        KDNode(vector<double> pt) : point(move(pt)), left(nullptr), right(nullptr) {}
    };

    class KDTree {
    private:
        int k;

        unique_ptr<KDNode> build_helper(vector<vector<double>>& points, size_t start, size_t end, int depth) {
            if (start >= end) return nullptr;
            int axis = depth % k;
            size_t mid = start + (end - start) / 2;
            nth_element(points.begin() + start, points.begin() + mid, points.begin() + end,
                        [axis](const vector<double>& a, const vector<double>& b) {
                            return a[axis] < b[axis];
                        });
            auto node = make_unique<KDNode>(points[mid]);
            node->left = build_helper(points, start, mid, depth + 1);
            node->right = build_helper(points, mid + 1, end, depth + 1);
            return node;
        }

        double distance_sq(const vector<double>& a, const vector<double>& b) const {
            double sum = 0;
            for (size_t i = 0; i < a.size(); ++i) {
                double diff = a[i] - b[i];
                sum += diff * diff;
            }
            return sum;
        }

        void nearest_helper(const KDNode* node, const vector<double>& target, int depth,
                            const KDNode*& best, double& best_dist_sq) const {
            if (!node) return;
            double dist_sq = distance_sq(node->point, target);
            if (dist_sq < best_dist_sq) {
                best_dist_sq = dist_sq;
                best = node;
            }
            int axis = depth % k;
            const KDNode* next_branch = nullptr;
            const KDNode* other_branch = nullptr;
            if (target[axis] < node->point[axis]) {
                next_branch = node->left.get();
                other_branch = node->right.get();
            } else {
                next_branch = node->right.get();
                other_branch = node->left.get();
            }
            nearest_helper(next_branch, target, depth + 1, best, best_dist_sq);
            double axis_diff = target[axis] - node->point[axis];
            if (axis_diff * axis_diff < best_dist_sq) {
                nearest_helper(other_branch, target, depth + 1, best, best_dist_sq);
            }
        }

    public:
        unique_ptr<KDNode> root;

        KDTree(vector<vector<double>>& points, int dimensions) : k(dimensions) {
            root = build_helper(points, 0, points.size(), 0);
        }

        vector<double> nearest_neighbor(const vector<double>& target) const {
            const KDNode* best = nullptr;
            double best_dist_sq = numeric_limits<double>::max();
            nearest_helper(root.get(), target, 0, best, best_dist_sq);
            return best ? best->point : vector<double>{};
        }
    };

    /* 2.4 Range Query Structures: Segment Tree with Lazy Propagation */
    class SegmentTreeLazy {
    private:
        int n;
        vector<int> tree;
        vector<int> lazy;

        void build(const vector<int>& arr, int node, int start, int end) {
            if (start == end) {
                tree[node] = arr[start];
                return;
            }
            int mid = start + (end - start) / 2;
            build(arr, 2 * node, start, mid);
            build(arr, 2 * node + 1, mid + 1, end);
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }

        void update_range_helper(int node, int start, int end, int l, int r, int val) {
            if (lazy[node] != 0) {
                tree[node] += (end - start + 1) * lazy[node];
                if (start != end) {
                    lazy[2 * node] += lazy[node];
                    lazy[2 * node + 1] += lazy[node];
                }
                lazy[node] = 0;
            }
            if (start > end || start > r || end < l) return;
            if (start >= l && end <= r) {
                tree[node] += (end - start + 1) * val;
                if (start != end) {
                    lazy[2 * node] += val;
                    lazy[2 * node + 1] += val;
                }
                return;
            }
            int mid = start + (end - start) / 2;
            update_range_helper(2 * node, start, mid, l, r, val);
            update_range_helper(2 * node + 1, mid + 1, end, l, r, val);
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }

        int query_range_helper(int node, int start, int end, int l, int r) {
            if (start > end || start > r || end < l) return 0;
            if (lazy[node] != 0) {
                tree[node] += (end - start + 1) * lazy[node];
                if (start != end) {
                    lazy[2 * node] += lazy[node];
                    lazy[2 * node + 1] += lazy[node];
                }
                lazy[node] = 0;
            }
            if (start >= l && end <= r) return tree[node];
            int mid = start + (end - start) / 2;
            return query_range_helper(2 * node, start, mid, l, r) +
                   query_range_helper(2 * node + 1, mid + 1, end, l, r);
        }

    public:
        SegmentTreeLazy(const vector<int>& arr) {
            n = arr.size();
            tree.assign(4 * n, 0);
            lazy.assign(4 * n, 0);
            build(arr, 1, 0, n - 1);
        }

        void update_range(int l, int r, int val) {
            update_range_helper(1, 0, n - 1, l, r, val);
        }

        int query_range(int l, int r) {
            return query_range_helper(1, 0, n - 1, l, r);
        }
    };

    /* 2.5 Multi-Level Lists: Skip List */
    template <typename T>
    struct SkipNode {
        T key;
        vector<SkipNode*> forward;
        SkipNode(T k, int level) : key(k), forward(level, nullptr) {}
    };

    template <typename T>
    class SkipList {
    private:
        int max_level;
        float p;
        int level;
        SkipNode<T>* header;

        int random_level() {
            int lvl = 1;
            while (((float)rand() / RAND_MAX) < p && lvl < max_level) {
                lvl++;
            }
            return lvl;
        }

    public:
        SkipList(int max_lvl, float prob) : max_level(max_lvl), p(prob), level(1) {
            header = new SkipNode<T>(T{}, max_level);
        }

        ~SkipList() {
            SkipNode<T>* curr = header;
            while (curr) {
                SkipNode<T>* next_node = curr->forward[0];
                delete curr;
                curr = next_node;
            }
        }

        void insert(T key) {
            vector<SkipNode<T>*> update(max_level, nullptr);
            SkipNode<T>* curr = header;
            for (int i = level - 1; i >= 0; i--) {
                while (curr->forward[i] && curr->forward[i]->key < key) {
                    curr = curr->forward[i];
                }
                update[i] = curr;
            }
            curr = curr->forward[0];
            if (!curr || curr->key != key) {
                int r_level = random_level();
                if (r_level > level) {
                    for (int i = level; i < r_level; i++) {
                        update[i] = header;
                    }
                    level = r_level;
                }
                auto new_node = new SkipNode<T>(key, r_level);
                for (int i = 0; i < r_level; i++) {
                    new_node->forward[i] = update[i]->forward[i];
                    update[i]->forward[i] = new_node;
                }
            }
        }

        bool search(T key) const {
            SkipNode<T>* curr = header;
            for (int i = level - 1; i >= 0; i--) {
                while (curr->forward[i] && curr->forward[i]->key < key) {
                    curr = curr->forward[i];
                }
            }
            curr = curr->forward[0];
            return curr && curr->key == key;
        }

        void print() const {
            cout << "    SkipList structure:\n";
            for (int i = 0; i < level; i++) {
                SkipNode<T>* node = header->forward[i];
                cout << "      Level " << i << ": ";
                while (node) {
                    cout << node->key << " ";
                    node = node->forward[i];
                }
                cout << "\n";
            }
        }
    };

    /* 2.6 String Trie & Autocomplete Prefix System */
    struct TrieNode {
        unordered_map<char, unique_ptr<TrieNode>> children;
        bool is_word = false;
    };

    class Trie {
    private:
        unique_ptr<TrieNode> root;

        void collect_suggestions(const TrieNode* curr, const string& prefix, vector<string>& results) const {
            if (curr->is_word) {
                results.push_back(prefix);
            }
            for (const auto& [ch, child] : curr->children) {
                collect_suggestions(child.get(), prefix + ch, results);
            }
        }

    public:
        Trie() : root(make_unique<TrieNode>()) {}

        void insert(const string& word) {
            TrieNode* curr = root.get();
            for (char ch : word) {
                if (curr->children.find(ch) == curr->children.end()) {
                    curr->children[ch] = make_unique<TrieNode>();
                }
                curr = curr->children[ch].get();
            }
            curr->is_word = true;
        }

        bool search(const string& word) const {
            const TrieNode* curr = root.get();
            for (char ch : word) {
                auto it = curr->children.find(ch);
                if (it == curr->children.end()) return false;
                curr = it->second.get();
            }
            return curr->is_word;
        }

        vector<string> suggest(const string& prefix) const {
            vector<string> results;
            const TrieNode* curr = root.get();
            for (char ch : prefix) {
                auto it = curr->children.find(ch);
                if (it == curr->children.end()) return results;
                curr = it->second.get();
            }
            collect_suggestions(curr, prefix, results);
            return results;
        }
    };

    /* 2.7 Priority Queues: Templated Heaps */
    template <typename T, typename Compare = less<T>>
    class Heap {
    private:
        vector<T> data;
        Compare comp;

        void sift_up(size_t idx) {
            while (idx > 0) {
                size_t p_idx = (idx - 1) / 2;
                if (comp(data[idx], data[p_idx])) {
                    swap(data[idx], data[p_idx]);
                    idx = p_idx;
                } else {
                    break;
                }
            }
        }

        void sift_down(size_t idx) {
            size_t size = data.size();
            while (2 * idx + 1 < size) {
                size_t left = 2 * idx + 1;
                size_t right = 2 * idx + 2;
                size_t best = left;
                if (right < size && comp(data[right], data[left])) {
                    best = right;
                }
                if (comp(data[best], data[idx])) {
                    swap(data[best], data[idx]);
                    idx = best;
                } else {
                    break;
                }
            }
        }

    public:
        void push(T val) {
            data.push_back(val);
            sift_up(data.size() - 1);
        }

        T pop() {
            assert(!data.empty());
            T top_val = data.front();
            data.front() = data.back();
            data.pop_back();
            if (!data.empty()) {
                sift_down(0);
            }
            return top_val;
        }

        T peek() const {
            assert(!data.empty());
            return data.front();
        }

        bool empty() const { return data.empty(); }
        size_t size() const { return data.size(); }
    };

    /* 2.8 Custom Hash Tables: Chaining & Dynamic Load-Factor Rehashing */
    template <typename K, typename V>
    class HashTableChaining {
    private:
        struct HashEntry {
            K key;
            V val;
            HashEntry(K k, V v) : key(move(k)), val(move(v)) {}
        };

        vector<vector<HashEntry>> table;
        size_t num_elements = 0;
        size_t capacity;

        size_t get_hash(const K& key) const {
            hash<K> hasher;
            return hasher(key) % capacity;
        }

        void rehash() {
            size_t old_cap = capacity;
            capacity *= 2;
            vector<vector<HashEntry>> new_table(capacity);
            for (size_t i = 0; i < old_cap; i++) {
                for (auto& entry : table[i]) {
                    hash<K> hasher;
                    size_t new_idx = hasher(entry.key) % capacity;
                    new_table[new_idx].push_back(move(entry));
                }
            }
            table = move(new_table);
        }

    public:
        HashTableChaining(size_t initial_cap = 8) : capacity(initial_cap) {
            table.resize(capacity);
        }

        void put(K key, V val) {
            if ((double)num_elements / capacity > 0.75) {
                rehash();
            }
            size_t idx = get_hash(key);
            for (auto& entry : table[idx]) {
                if (entry.key == key) {
                    entry.val = val;
                    return;
                }
            }
            table[idx].emplace_back(move(key), move(val));
            num_elements++;
        }

        optional<V> get(const K& key) const {
            size_t idx = get_hash(key);
            for (const auto& entry : table[idx]) {
                if (entry.key == key) return entry.val;
            }
            return nullopt;
        }
    };

    /* 2.9 Graph Representation & Core Algorithms (BFS, DFS, Cycle Detection, Topological Sort) */
    class Graph {
    private:
        int num_vertices;
        vector<vector<int>> adj_list;

        bool dfs_cycle_helper(int u, vector<int>& visited) const {
            visited[u] = 1; // 1 means visiting (in recursion stack)
            for (int v : adj_list[u]) {
                if (visited[v] == 1) return true;
                if (visited[v] == 0) {
                    if (dfs_cycle_helper(v, visited)) return true;
                }
            }
            visited[u] = 2; // 2 means fully visited
            return false;
        }

        void topo_sort_helper(int u, vector<bool>& visited, stack<int>& st) const {
            visited[u] = true;
            for (int v : adj_list[u]) {
                if (!visited[v]) {
                    topo_sort_helper(v, visited, st);
                }
            }
            st.push(u);
        }

    public:
        Graph(int vertices) : num_vertices(vertices), adj_list(vertices) {}

        void add_edge(int u, int v) {
            adj_list[u].push_back(v); // Directed graph
        }

        vector<int> bfs(int start) const {
            vector<int> path;
            vector<bool> visited(num_vertices, false);
            queue<int> q;
            visited[start] = true;
            q.push(start);
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                path.push_back(u);
                for (int v : adj_list[u]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        q.push(v);
                    }
                }
            }
            return path;
        }

        vector<int> dfs(int start) const {
            vector<int> path;
            vector<bool> visited(num_vertices, false);
            stack<int> s;
            s.push(start);
            while (!s.empty()) {
                int u = s.top();
                s.pop();
                if (!visited[u]) {
                    visited[u] = true;
                    path.push_back(u);
                    for (auto it = adj_list[u].rbegin(); it != adj_list[u].rend(); ++it) {
                        if (!visited[*it]) {
                            s.push(*it);
                        }
                    }
                }
            }
            return path;
        }

        bool has_cycle() const {
            vector<int> visited(num_vertices, 0); // 0 = unvisited
            for (int i = 0; i < num_vertices; i++) {
                if (visited[i] == 0) {
                    if (dfs_cycle_helper(i, visited)) return true;
                }
            }
            return false;
        }

        vector<int> topological_sort() const {
            vector<bool> visited(num_vertices, false);
            stack<int> st;
            for (int i = 0; i < num_vertices; i++) {
                if (!visited[i]) {
                    topo_sort_helper(i, visited, st);
                }
            }
            vector<int> res;
            while (!st.empty()) {
                res.push_back(st.top());
                st.pop();
            }
            return res;
        }
    };

    static void spatial_structures_demo() {
        print_sep("2.3 & 2.4 SPATIAL STRUCTURES & SEGMENT TREES");
        vector<vector<double>> pts = {{2.0, 3.0}, {5.0, 4.0}, {9.0, 6.0}, {4.0, 7.0}, {8.0, 1.0}, {7.0, 2.0}};
        KDTree kdt(pts, 2);
        vector<double> target = {9.2, 5.8};
        vector<double> nearest = kdt.nearest_neighbor(target);
        cout << "    KD-Tree Nearest to (9.2, 5.8): (" << nearest[0] << ", " << nearest[1] << ")\n";

        vector<int> arr = {1, 3, 5, 7, 9, 11};
        SegmentTreeLazy seg(arr);
        cout << "    Segment Tree: Sum in range [1, 3] = " << seg.query_range(1, 3) << "\n";
        seg.update_range(1, 5, 10);
        cout << "    Segment Tree after range update (+10 in [1, 5]): Sum in range [1, 3] = " << seg.query_range(1, 3) << "\n";
    }

    static void structures_trie_heap_hash_demo() {
        print_sep("2.5 - 2.8 TRIE, SKIPLIST, HEAPS & RESIZING HASH TABLE");
        
        Trie trie;
        trie.insert("cpp");
        trie.insert("cplusplus");
        trie.insert("csharp");
        cout << "    Trie Autocomplete for 'cp': ";
        for (const auto& w : trie.suggest("cp")) cout << w << " ";
        cout << "\n";

        SkipList<int> sl(4, 0.5f);
        sl.insert(3);
        sl.insert(6);
        sl.insert(7);
        sl.insert(9);
        sl.print();

        Heap<int, less<int>> min_h;
        min_h.push(10);
        min_h.push(5);
        min_h.push(30);
        cout << "    Min-Heap Top popped: " << min_h.pop() << ", remaining top: " << min_h.peek() << "\n";

        HashTableChaining<string, int> htable;
        htable.put("Alice", 28);
        htable.put("Bob", 35);
        htable.put("Charlie", 42);
        cout << "    Hash table retrieval for 'Bob': " << (htable.get("Bob") ? to_string(*htable.get("Bob")) : "Not Found") << "\n";
    }

    static void graphs_demo() {
        print_sep("2.9 GRAPH CORE ALGORITHMS");
        Graph g(6);
        g.add_edge(5, 2);
        g.add_edge(5, 0);
        g.add_edge(4, 0);
        g.add_edge(4, 1);
        g.add_edge(2, 3);
        g.add_edge(3, 1);

        cout << "    BFS path from 5: ";
        for (int node : g.bfs(5)) cout << node << " ";
        cout << "\n";

        cout << "    DFS path from 5: ";
        for (int node : g.dfs(5)) cout << node << " ";
        cout << "\n";

        cout << "    Graph has cycle? " << (g.has_cycle() ? "Yes" : "No") << "\n";

        cout << "    Topological sort order: ";
        for (int node : g.topological_sort()) cout << node << " ";
        cout << "\n";
    }
"""
