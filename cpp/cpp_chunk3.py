# cpp_chunk3.py
# Phase 3: Algorithms (Sorting, Search, Graphs, DP, String Matching, Custom STL Allocators) - Updated with all calls

chunk_content = r"""
    /* ==================================================================
     *  PHASE 3: STL CONTAINERS, ALGORITHMS & GRAPH/DP MASTERY
     * ================================================================== */

    /* 3.1 Custom STL Allocator */
    template <typename T>
    class CustomAllocator {
    public:
        using value_type = T;

        CustomAllocator() noexcept = default;
        template <typename U> CustomAllocator(const CustomAllocator<U>&) noexcept {}

        T* allocate(size_t n) {
            cout << "    [Custom Allocator] Allocating " << n << " elements of size " << sizeof(T) << "\n";
            if (auto p = static_cast<T*>(malloc(n * sizeof(T)))) return p;
            throw bad_alloc();
        }

        void deallocate(T* p, size_t n) noexcept {
            (void)n;
            cout << "    [Custom Allocator] Deallocating elements\n";
            free(p);
        }
    };

    template <typename T, typename U>
    bool operator==(const CustomAllocator<T>&, const CustomAllocator<U>&) { return true; }
    template <typename T, typename U>
    bool operator!=(const CustomAllocator<T>&, const CustomAllocator<U>&) { return false; }

    static void stl_demo() {
        print_sep("3.1  CUSTOM STL ALLOCATOR & STANDARD TEMPLATES");
        vector<int, CustomAllocator<int>> custom_vec;
        custom_vec.push_back(42);
        custom_vec.push_back(100);

        map<string, int> age_map;
        age_map["KeyA"] = 1;

        unordered_set<int> uset = {3, 9, 1, 5};

        vector<int> src = {1, 2, 3, 4, 5};
        vector<int> dst(5);
        transform(src.begin(), src.end(), dst.begin(), [](int x) { return x * x; });
        cout << "    transform output: ";
        for (int x : dst) cout << x << " ";
        cout << "\n";
    }

    /* 3.2 Advanced Sorting Algorithms */
    static int partition_lomuto(vector<int>& arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                swap(arr[i], arr[j]);
            }
        }
        swap(arr[i + 1], arr[high]);
        return i + 1;
    }

    static void quicksort_lomuto(vector<int>& arr, int low, int high) {
        if (low < high) {
            int pi = partition_lomuto(arr, low, high);
            quicksort_lomuto(arr, low, pi - 1);
            quicksort_lomuto(arr, pi + 1, high);
        }
    }

    static int partition_hoare(vector<int>& arr, int low, int high) {
        int pivot = arr[low];
        int i = low - 1, j = high + 1;
        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);
            if (i >= j) return j;
            swap(arr[i], arr[j]);
        }
    }

    static void quicksort_hoare(vector<int>& arr, int low, int high) {
        if (low < high) {
            int pi = partition_hoare(arr, low, high);
            quicksort_hoare(arr, low, pi);
            quicksort_hoare(arr, pi + 1, high);
        }
    }

    static void merge_combine(vector<int>& arr, int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;
        vector<int> L(n1), R(n2);
        for (int i = 0; i < n1; i++) L[i] = arr[l + i];
        for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {
                arr[k] = L[i];
                i++;
            } else {
                arr[k] = R[j];
                j++;
            }
            k++;
        }
        while (i < n1) {
            arr[k] = L[i];
            i++;
            k++;
        }
        while (j < n2) {
            arr[k] = R[j];
            j++;
            k++;
        }
    }

    static void merge_sort(vector<int>& arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            merge_sort(arr, l, m);
            merge_sort(arr, m + 1, r);
            merge_combine(arr, l, m, r);
        }
    }

    static void counting_sort(vector<int>& arr) {
        if (arr.empty()) return;
        int max_val = *max_element(arr.begin(), arr.end());
        int min_val = *min_element(arr.begin(), arr.end());
        int range = max_val - min_val + 1;
        vector<int> count(range, 0);
        vector<int> output(arr.size());
        for (int x : arr) count[x - min_val]++;
        for (int i = 1; i < range; i++) count[i] += count[i - 1];
        for (int i = arr.size() - 1; i >= 0; i--) {
            output[count[arr[i] - min_val] - 1] = arr[i];
            count[arr[i] - min_val]--;
        }
        arr = move(output);
    }

    static void radix_sort(vector<int>& arr) {
        if (arr.empty()) return;
        int max_val = *max_element(arr.begin(), arr.end());
        auto counting_sort_digit = [](vector<int>& a, int exp) {
            int n = a.size();
            vector<int> output(n);
            int count[10] = {0};
            for (int i = 0; i < n; i++) count[(a[i] / exp) % 10]++;
            for (int i = 1; i < 10; i++) count[i] += count[i - 1];
            for (int i = n - 1; i >= 0; i--) {
                output[count[(a[i] / exp) % 10] - 1] = a[i];
                count[(a[i] / exp) % 10]--;
            }
            a = move(output);
        };
        for (int exp = 1; max_val / exp > 0; exp *= 10) {
            counting_sort_digit(arr, exp);
        }
    }

    static void shell_sort(vector<int>& arr) {
        int n = arr.size();
        for (int gap = n / 2; gap > 0; gap /= 2) {
            for (int i = gap; i < n; i++) {
                int temp = arr[i];
                int j;
                for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                    arr[j] = arr[j - gap];
                }
                arr[j] = temp;
            }
        }
    }

    /* 3.3 Search Algorithms: Binary Search limits */
    static int binary_search_lower_bound(const vector<int>& arr, int target) {
        int low = 0, high = arr.size();
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] >= target) high = mid;
            else low = mid + 1;
        }
        return low;
    }

    static int binary_search_upper_bound(const vector<int>& arr, int target) {
        int low = 0, high = arr.size();
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] > target) high = mid;
            else low = mid + 1;
        }
        return low;
    }

    /* 3.4 Graph Algorithms: Pathfinding & MST (Dijkstra, Kruskal, Prim, Bellman-Ford, Floyd-Warshall) */
    struct GEdge {
        int src, dest, weight;
    };

    struct GraphAdjList {
        int V;
        vector<vector<pair<int, int>>> adj; // pairs of {dest, weight}
        GraphAdjList(int v) : V(v), adj(v) {}
        void add_edge(int u, int v, int w) {
            adj[u].push_back({v, w});
        }
    };

    static void run_dijkstra(const GraphAdjList& g, int src, vector<int>& dist, vector<int>& parent) {
        dist.assign(g.V, GRAPH_INF);
        parent.assign(g.V, -1);
        dist[src] = 0;
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, src});
        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            if (d > dist[u]) continue;
            for (const auto& [v, w] : g.adj[u]) {
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    parent[v] = u;
                    pq.push({dist[v], v});
                }
            }
        }
    }

    static void reconstruct_path_helper(const vector<int>& parent, int j) {
        if (parent[j] == -1) return;
        reconstruct_path_helper(parent, parent[j]);
        cout << "-> " << j << " ";
    }

    class DSU {
        vector<int> parent;
        vector<int> rank;
    public:
        DSU(int n) {
            parent.resize(n);
            rank.assign(n, 0);
            iota(parent.begin(), parent.end(), 0);
        }
        int find(int i) {
            if (parent[i] == i) return i;
            return parent[i] = find(parent[i]); // Path compression
        }
        void unite(int i, int j) {
            int root_i = find(i);
            int root_j = find(j);
            if (root_i != root_j) {
                if (rank[root_i] < rank[root_j]) swap(root_i, root_j);
                parent[root_j] = root_i;
                if (rank[root_i] == rank[root_j]) rank[root_i]++;
            }
        }
    };

    static int run_kruskal(int V, vector<GEdge>& edges, vector<GEdge>& mst) {
        sort(edges.begin(), edges.end(), [](const GEdge& a, const GEdge& b) {
            return a.weight < b.weight;
        });
        DSU dsu(V);
        int mst_weight = 0;
        for (const auto& edge : edges) {
            if (dsu.find(edge.src) != dsu.find(edge.dest)) {
                dsu.unite(edge.src, edge.dest);
                mst.push_back(edge);
                mst_weight += edge.weight;
            }
        }
        return mst_weight;
    }

    static int run_prims(int V, const GraphAdjList& g, vector<pair<int, int>>& mst_edges) {
        vector<int> key(V, GRAPH_INF);
        vector<int> parent(V, -1);
        vector<bool> in_mst(V, false);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        key[0] = 0;
        pq.push({0, 0});
        int total_weight = 0;
        while (!pq.empty()) {
            int u = pq.top().second;
            pq.pop();
            if (in_mst[u]) continue;
            in_mst[u] = true;
            total_weight += key[u];
            if (parent[u] != -1) {
                mst_edges.push_back({parent[u], u});
            }
            for (const auto& [v, w] : g.adj[u]) {
                if (!in_mst[v] && w < key[v]) {
                    key[v] = w;
                    parent[v] = u;
                    pq.push({key[v], v});
                }
            }
        }
        return total_weight;
    }

    static bool run_bellman_ford(int V, int src, const vector<GEdge>& edges, vector<int>& dist) {
        dist.assign(V, GRAPH_INF);
        dist[src] = 0;
        for (int i = 1; i <= V - 1; i++) {
            for (const auto& edge : edges) {
                if (dist[edge.src] != GRAPH_INF && dist[edge.src] + edge.weight < dist[edge.dest]) {
                    dist[edge.dest] = dist[edge.src] + edge.weight;
                }
            }
        }
        for (const auto& edge : edges) {
            if (dist[edge.src] != GRAPH_INF && dist[edge.src] + edge.weight < dist[edge.dest]) {
                return false; // Negative cycle detected
            }
        }
        return true;
    }

    static void run_floyd_warshall(int V, vector<vector<int>>& dist) {
        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {
                    if (dist[i][k] != GRAPH_INF && dist[k][j] != GRAPH_INF && dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }
    }

    /* 3.5 Dynamic Programming: Knapsack, LCS, Edit Distance, Matrix Chain Multiplication, LIS */
    static int dp_knapsack_01(int W, const vector<int>& wt, const vector<int>& val, vector<int>& selected) {
        int n = val.size();
        vector<vector<int>> K(n + 1, vector<int>(W + 1, 0));
        for (int i = 0; i <= n; i++) {
            for (int w = 0; w <= W; w++) {
                if (i == 0 || w == 0) K[i][w] = 0;
                else if (wt[i - 1] <= w) {
                    K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);
                } else {
                    K[i][w] = K[i - 1][w];
                }
            }
        }
        int res = K[n][W];
        int w = W;
        for (int i = n; i > 0 && res > 0; i--) {
            if (res == K[i - 1][w]) continue;
            selected.push_back(i - 1);
            res -= val[i - 1];
            w -= wt[i - 1];
        }
        return K[n][W];
    }

    static string dp_lcs(const string& X, const string& Y) {
        int m = X.size(), n = Y.size();
        vector<vector<int>> L(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0 || j == 0) L[i][j] = 0;
                else if (X[i - 1] == Y[j - 1]) L[i][j] = L[i - 1][j - 1] + 1;
                else L[i][j] = max(L[i - 1][j], L[i][j - 1]);
            }
        }
        int index = L[m][n];
        string lcs_str(index, ' ');
        int i = m, j = n;
        while (i > 0 && j > 0) {
            if (X[i - 1] == Y[j - 1]) {
                lcs_str[index - 1] = X[i - 1];
                i--; j--; index--;
            } else if (L[i - 1][j] > L[i][j - 1]) i--;
            else j--;
        }
        return lcs_str;
    }

    static int dp_edit_distance(const string& str1, const string& str2) {
        int m = str1.size(), n = str2.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                if (i == 0) dp[i][j] = j;
                else if (j == 0) dp[i][j] = i;
                else if (str1[i - 1] == str2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
                else {
                    dp[i][j] = 1 + min({dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]});
                }
            }
        }
        return dp[m][n];
    }

    static int dp_mcm(const vector<int>& p, vector<vector<int>>& s) {
        int n = p.size() - 1;
        vector<vector<int>> m(n + 1, vector<int>(n + 1, 0));
        s.assign(n + 1, vector<int>(n + 1, 0));
        for (int l = 2; l <= n; l++) {
            for (int i = 1; i <= n - l + 1; i++) {
                int j = i + l - 1;
                m[i][j] = GRAPH_INF;
                for (int k = i; k <= j - 1; k++) {
                    int q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                    if (q < m[i][j]) {
                        m[i][j] = q;
                        s[i][j] = k;
                    }
                }
            }
        }
        return m[1][n];
    }

    static void print_mcm_parenthesis(const vector<vector<int>>& s, int i, int j) {
        if (i == j) {
            cout << "A" << i;
            return;
        }
        cout << "(";
        print_mcm_parenthesis(s, i, s[i][j]);
        print_mcm_parenthesis(s, s[i][j] + 1, j);
        cout << ")";
    }

    static int dp_lis(const vector<int>& arr) {
        int n = arr.size();
        if (n == 0) return 0;
        vector<int> lis(n, 1);
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (arr[i] > arr[j] && lis[i] < lis[j] + 1) {
                    lis[i] = lis[j] + 1;
                }
            }
        }
        return *max_element(lis.begin(), lis.end());
    }

    /* 3.6 String Matching Algorithms: KMP, Rabin-Karp */
    static vector<int> kmp_search(const string& pat, const string& txt) {
        vector<int> matches;
        int M = pat.length();
        int N = txt.length();
        vector<int> lps(M, 0);
        int len = 0;
        int i = 1;
        while (i < M) {
            if (pat[i] == pat[len]) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        int txt_idx = 0;
        int pat_idx = 0;
        while (txt_idx < N) {
            if (pat[pat_idx] == txt[txt_idx]) {
                pat_idx++;
                txt_idx++;
            }
            if (pat_idx == M) {
                matches.push_back(txt_idx - pat_idx);
                pat_idx = lps[pat_idx - 1];
            } else if (txt_idx < N && pat[pat_idx] != txt[txt_idx]) {
                if (pat_idx != 0) pat_idx = lps[pat_idx - 1];
                else txt_idx++;
            }
        }
        return matches;
    }

    static vector<int> rabin_karp_search(const string& pat, const string& txt, int q = 101) {
        vector<int> matches;
        int d = 256;
        int M = pat.length();
        int N = txt.length();
        int p = 0; // Hash pattern
        int t = 0; // Hash text
        int h = 1;
        for (int i = 0; i < M - 1; i++) {
            h = (h * d) % q;
        }
        for (int i = 0; i < M; i++) {
            p = (d * p + pat[i]) % q;
            t = (d * t + txt[i]) % q;
        }
        for (int i = 0; i <= N - M; i++) {
            if (p == t) {
                bool match_found = true;
                for (int j = 0; j < M; j++) {
                    if (txt[i + j] != pat[j]) {
                        match_found = false;
                        break;
                    }
                }
                if (match_found) matches.push_back(i);
            }
            if (i < N - M) {
                t = (d * (t - txt[i] * h) + txt[i + M]) % q;
                if (t < 0) t = (t + q);
            }
        }
        return matches;
    }

    static void sorting_mst_demo() {
        print_sep("3.2 to 3.4 SORTING, SEARCH LIMITS, DSU & PATHS");
        vector<int> arr = {38, 27, 43, 3, 9, 82, 10};
        
        vector<int> temp = arr;
        quicksort_lomuto(temp, 0, temp.size() - 1);
        cout << "    Lomuto Quick Sorted: ";
        for (int x : temp) cout << x << " ";
        cout << "\n";

        temp = arr;
        quicksort_hoare(temp, 0, temp.size() - 1);
        cout << "    Hoare Quick Sorted: ";
        for (int x : temp) cout << x << " ";
        cout << "\n";

        temp = arr;
        merge_sort(temp, 0, temp.size() - 1);
        cout << "    Merge Sorted: ";
        for (int x : temp) cout << x << " ";
        cout << "\n";

        temp = arr;
        counting_sort(temp);
        cout << "    Counting Sorted: ";
        for (int x : temp) cout << x << " ";
        cout << "\n";

        temp = arr;
        radix_sort(temp);
        cout << "    Radix Sorted: ";
        for (int x : temp) cout << x << " ";
        cout << "\n";

        temp = arr;
        shell_sort(temp);
        cout << "    Shell Sorted: ";
        for (int x : temp) cout << x << " ";
        cout << "\n";

        vector<int> s_arr = {1, 2, 4, 4, 4, 5, 7, 9};
        cout << "    Lower bound of 4: index " << binary_search_lower_bound(s_arr, 4)
             << ", Upper bound of 4: index " << binary_search_upper_bound(s_arr, 4) << "\n";

        GraphAdjList g(5);
        g.add_edge(0, 1, 4);
        g.add_edge(0, 2, 2);
        g.add_edge(1, 2, 5);
        g.add_edge(1, 3, 10);
        g.add_edge(2, 3, 3);
        g.add_edge(2, 4, 8);
        g.add_edge(3, 4, 2);

        vector<int> dijkstra_dist;
        vector<int> dijkstra_parent;
        run_dijkstra(g, 0, dijkstra_dist, dijkstra_parent);
        cout << "    Dijkstra shortest paths from 0 (reconstructed):\n";
        for (int i = 0; i < 5; i++) {
            if (dijkstra_dist[i] != GRAPH_INF && i != 0) {
                cout << "      Path to " << i << ": 0 ";
                reconstruct_path_helper(dijkstra_parent, i);
                cout << "(dist: " << dijkstra_dist[i] << ")\n";
            }
        }

        vector<GEdge> edges = {
            {0, 1, 10}, {0, 2, 6}, {0, 3, 5},
            {1, 3, 15}, {2, 3, 4}
        };
        vector<GEdge> mst;
        int mst_w = run_kruskal(4, edges, mst);
        cout << "    Kruskal MST total weight: " << mst_w << "\n";

        vector<pair<int, int>> prim_mst;
        int prim_w = run_prims(5, g, prim_mst);
        cout << "    Prim MST total weight: " << prim_w << "\n";

        // Call Bellman-Ford
        vector<int> bf_dist;
        bool bf_success = run_bellman_ford(5, 0, edges, bf_dist);
        cout << "    Bellman-Ford execution success? " << (bf_success ? "Yes" : "No") << "\n";
        if (bf_success) {
            cout << "      Dist to vertex 3: " << bf_dist[3] << "\n";
        }

        // Call Floyd-Warshall
        vector<vector<int>> fw_dist(5, vector<int>(5, GRAPH_INF));
        for (int i = 0; i < 5; i++) fw_dist[i][i] = 0;
        for (const auto& e : edges) {
            fw_dist[e.src][e.dest] = e.weight;
        }
        run_floyd_warshall(5, fw_dist);
        cout << "    Floyd-Warshall distance matrix index (0 to 4): " << fw_dist[0][4] << "\n";
    }

    static void dp_demo() {
        print_sep("3.5 & 3.6 DYNAMIC PROGRAMMING & STRING MATCHING");
        vector<int> wt = {10, 20, 30};
        vector<int> val = {60, 100, 120};
        vector<int> selected;
        int max_val = dp_knapsack_01(50, wt, val, selected);
        cout << "    Knapsack 01 (W=50) Max value: " << max_val << ", Selected items indices: ";
        for (int idx : selected) cout << idx << " ";
        cout << "\n";

        cout << "    LCS of 'ABCDGH' and 'AEDFHR': " << dp_lcs("ABCDGH", "AEDFHR") << "\n";
        cout << "    Edit distance between 'kitten' and 'sitting': " << dp_edit_distance("kitten", "sitting") << "\n";

        vector<int> p = {10, 20, 30, 40, 30};
        vector<vector<int>> s;
        int mcm_cost = dp_mcm(p, s);
        cout << "    MCM Min calculations cost: " << mcm_cost << ", Parenthesization: ";
        print_mcm_parenthesis(s, 1, p.size() - 1);
        cout << "\n";

        vector<int> lis_arr = {10, 22, 9, 33, 21, 50, 41, 60};
        cout << "    LIS length: " << dp_lis(lis_arr) << "\n";

        string txt = "ABABDABACDABABCABAB";
        string pat = "ABABCABAB";
        vector<int> kmp_m = kmp_search(pat, txt);
        cout << "    KMP Matches indices: ";
        for (int idx : kmp_m) cout << idx << " ";
        cout << "\n";

        vector<int> rk_m = rabin_karp_search(pat, txt);
        cout << "    Rabin-Karp Matches indices: ";
        for (int idx : rk_m) cout << idx << " ";
        cout << "\n";
    }
"""
