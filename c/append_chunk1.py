# append_chunk1.py
# Appends Phase 2 Part 3 and Phase 3 sections to build_cs_ds_encyclopedia_c.py

import os

c_quote = "'''"

chunk_content = r"""
# ---------------------------------------------------------------------------
# PHASE 2: DATA STRUCTURES (PART 3 - SKIP LIST, SEGMENT TREE, KD-TREE)
# ---------------------------------------------------------------------------
add_section("PHASE_2_PART3_SPATIAL_SKIP", r{c_quote}
/* 2.6 Skip List Implementation */
#define SKIPLIST_MAX_LEVEL 6
typedef struct SkipNode {
    int key;
    int value;
    struct SkipNode **forward;
} SkipNode;

typedef struct {
    int level;
    SkipNode *header;
} SkipList;

static SkipNode *skiplist_new_node(int key, int val, int level) {
    SkipNode *n = (SkipNode*)malloc(sizeof(SkipNode));
    n->key = key;
    n->value = val;
    n->forward = (SkipNode**)malloc((level + 1) * sizeof(SkipNode*));
    for (int i = 0; i <= level; i++) n->forward[i] = NULL;
    return n;
}

static SkipList *skiplist_create(void) {
    SkipList *sl = (SkipList*)malloc(sizeof(SkipList));
    sl->level = 0;
    sl->header = skiplist_new_node(-1, -1, SKIPLIST_MAX_LEVEL);
    return sl;
}

static float skiplist_random_fraction(void) {
    return (float)rand() / (float)RAND_MAX;
}

static int skiplist_random_level(void) {
    int lvl = 0;
    while (skiplist_random_fraction() < 0.5 && lvl < SKIPLIST_MAX_LEVEL) {
        lvl++;
    }
    return lvl;
}

static void skiplist_insert(SkipList *sl, int key, int val) {
    SkipNode *update[SKIPLIST_MAX_LEVEL + 1];
    SkipNode *curr = sl->header;
    for (int i = sl->level; i >= 0; i--) {
        while (curr->forward[i] != NULL && curr->forward[i]->key < key) {
            curr = curr->forward[i];
        }
        update[i] = curr;
    }
    curr = curr->forward[0];

    if (curr == NULL || curr->key != key) {
        int rlevel = skiplist_random_level();
        if (rlevel > sl->level) {
            for (int i = sl->level + 1; i <= rlevel; i++) {
                update[i] = sl->header;
            }
            sl->level = rlevel;
        }
        SkipNode *n = skiplist_new_node(key, val, rlevel);
        for (int i = 0; i <= rlevel; i++) {
            n->forward[i] = update[i]->forward[i];
            update[i]->forward[i] = n;
        }
    } else {
        curr->value = val;
    }
}

static int skiplist_search(SkipList *sl, int key, int default_val) {
    SkipNode *curr = sl->header;
    for (int i = sl->level; i >= 0; i--) {
        while (curr->forward[i] != NULL && curr->forward[i]->key < key) {
            curr = curr->forward[i];
        }
    }
    curr = curr->forward[0];
    if (curr != NULL && curr->key == key) return curr->value;
    return default_val;
}

static void skiplist_free(SkipList *sl) {
    SkipNode *curr = sl->header->forward[0];
    while (curr != NULL) {
        SkipNode *next = curr->forward[0];
        free(curr->forward);
        free(curr);
        curr = next;
    }
    free(sl->header->forward);
    free(sl->header);
    free(sl);
}

/* 2.7 Segment Tree Implementation */
static void seg_tree_build(int *tree, const int *arr, int node, int start, int end) {
    if (start == end) {
        tree[node] = arr[start];
        return;
    }
    int mid = (start + end) / 2;
    seg_tree_build(tree, arr, 2 * node, start, mid);
    seg_tree_build(tree, arr, 2 * node + 1, mid + 1, end);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
}

static void seg_tree_update(int *tree, int node, int start, int end, int idx, int val) {
    if (start == end) {
        tree[node] = val;
        return;
    }
    int mid = (start + end) / 2;
    if (idx >= start && idx <= mid) {
        seg_tree_update(tree, 2 * node, start, mid, idx, val);
    } else {
        seg_tree_update(tree, 2 * node + 1, mid + 1, end, idx, val);
    }
    tree[node] = tree[2 * node] + tree[2 * node + 1];
}

static int seg_tree_query(const int *tree, int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;
    if (l <= start && end <= r) return tree[node];
    int mid = (start + end) / 2;
    return seg_tree_query(tree, 2 * node, start, mid, l, r) +
           seg_tree_query(tree, 2 * node + 1, mid + 1, end, l, r);
}

/* 2.8 KD-Tree (2D Spatial Indexing) */
typedef struct KDNode {
    int point[2];
    struct KDNode *left, *right;
} KDNode;

static KDNode *kd_new_node(int x, int y) {
    KDNode *node = (KDNode*)malloc(sizeof(KDNode));
    node->point[0] = x;
    node->point[1] = y;
    node->left = node->right = NULL;
    return node;
}

static KDNode *kd_insert_rec(KDNode *root, const int point[2], int depth) {
    if (!root) return kd_new_node(point[0], point[1]);
    int cd = depth % 2;
    if (point[cd] < root->point[cd]) {
        root->left = kd_insert_rec(root->left, point, depth + 1);
    } else {
        root->right = kd_insert_rec(root->right, point, depth + 1);
    }
    return root;
}

static double kd_distance(const int p1[2], const int p2[2]) {
    return sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]));
}

static void kd_nearest_rec(KDNode *root, const int target[2], int depth, KDNode **best_node, double *best_dist) {
    if (!root) return;
    double d = kd_distance(root->point, target);
    if (d < *best_dist) {
        *best_dist = d;
        *best_node = root;
    }
    int cd = depth % 2;
    KDNode *next_branch = (target[cd] < root->point[cd]) ? root->left : root->right;
    KDNode *other_branch = (target[cd] < root->point[cd]) ? root->right : root->left;
    kd_nearest_rec(next_branch, target, depth + 1, best_node, best_dist);
    if (abs(target[cd] - root->point[cd]) < *best_dist) {
        kd_nearest_rec(other_branch, target, depth + 1, best_node, best_dist);
    }
}

static void kd_free(KDNode *root) {
    if (root) {
        kd_free(root->left);
        kd_free(root->right);
        free(root);
    }
}

static void spatial_structures_demo(void) {
    print_sep("2.6, 2.7, 2.8 SKIP LIST, SEGMENT TREE, KD-TREE");
    
    /* Skip List Demo */
    SkipList *sl = skiplist_create();
    skiplist_insert(sl, 3, 30);
    skiplist_insert(sl, 6, 60);
    skiplist_insert(sl, 7, 70);
    skiplist_insert(sl, 9, 90);
    printf("  Skip List Search: key 6 = %d, key 5 (default -1) = %d\n", 
           skiplist_search(sl, 6, -1), skiplist_search(sl, 5, -1));
    skiplist_free(sl);

    /* Segment Tree Demo */
    int arr[] = {1, 3, 5, 7, 9, 11};
    int n = 6;
    int *tree = (int*)calloc(4 * n, sizeof(int));
    seg_tree_build(tree, arr, 1, 0, n - 1);
    printf("  Segment Tree: Sum of values in range [1, 3] = %d\n", seg_tree_query(tree, 1, 0, n - 1, 1, 3));
    seg_tree_update(tree, 1, 0, n - 1, 1, 10);
    printf("  Segment Tree after update: Sum of values in range [1, 3] = %d\n", seg_tree_query(tree, 1, 0, n - 1, 1, 3));
    free(tree);

    /* KD-Tree Demo */
    KDNode *kd_root = NULL;
    int points[7][2] = { {3, 6}, {17, 15}, {13, 15}, {6, 12}, {9, 1}, {2, 7}, {10, 19} };
    int num_points = 7;
    for (int i = 0; i < num_points; i++) {
        kd_root = kd_insert_rec(kd_root, points[i], 0);
    }
    int target[2] = {10, 19};
    KDNode *best = NULL;
    double best_dist = 1e9;
    kd_nearest_rec(kd_root, target, 0, &best, &best_dist);
    if (best) {
        printf("  KD-Tree Nearest Neighbor to (%d, %d): (%d, %d) with distance: %.4f\n", 
               target[0], target[1], best->point[0], best->point[1], best_dist);
    }
    kd_free(kd_root);
}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 3: ALGORITHMS & GRAPH/DP/STRING MATCHING
# ---------------------------------------------------------------------------
add_section("PHASE_3_ALGORITHMS_GRAPH_DP_STRING", r{c_quote}
/* ==================================================================
 *  PHASE 3: ALGORITHMS & GRAPH/DP/STRING MATCHING
 * ================================================================== */

/* 3.1 Sorting Algorithms: Quick, Merge, Counting, Radix, Shell */
static void swap_ints(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

/* Lomuto Partitioning */
static int partition_lomuto(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap_ints(&arr[i], &arr[j]);
        }
    }
    swap_ints(&arr[i + 1], &arr[high]);
    return i + 1;
}

static void quicksort_lomuto(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition_lomuto(arr, low, high);
        quicksort_lomuto(arr, low, pi - 1);
        quicksort_lomuto(arr, pi + 1, high);
    }
}

/* Hoare Partitioning */
static int partition_hoare(int arr[], int low, int high) {
    int pivot = arr[low];
    int i = low - 1, j = high + 1;
    while (true) {
        do { i++; } while (arr[i] < pivot);
        do { j--; } while (arr[j] > pivot);
        if (i >= j) return j;
        swap_ints(&arr[i], &arr[j]);
    }
}

static void quicksort_hoare(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition_hoare(arr, low, high);
        quicksort_hoare(arr, low, pi);
        quicksort_hoare(arr, pi + 1, high);
    }
}

/* Merge Sort */
static void merge_arrays(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    int *L = (int*)malloc(n1 * sizeof(int));
    int *R = (int*)malloc(n2 * sizeof(int));
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
    free(L);
    free(R);
}

static void merge_sort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        merge_sort(arr, l, m);
        merge_sort(arr, m + 1, r);
        merge_arrays(arr, l, m, r);
    }
}

/* Counting Sort (for non-negative integers) */
static void counting_sort(int arr[], int n) {
    if (n <= 0) return;
    int max_val = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > max_val) max_val = arr[i];
    }
    int *count = (int*)calloc(max_val + 1, sizeof(int));
    for (int i = 0; i < n; i++) count[arr[i]]++;
    int idx = 0;
    for (int i = 0; i <= max_val; i++) {
        while (count[i] > 0) {
            arr[idx++] = i;
            count[i]--;
        }
    }
    free(count);
}

/* Radix Sort helper */
static void radix_count_sort(int arr[], int n, int exp) {
    int *output = (int*)malloc(n * sizeof(int));
    int count[10] = {0};
    for (int i = 0; i < n; i++) {
        count[(arr[i] / exp) % 10]++;
    }
    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }
    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
    }
    free(output);
}

static void radix_sort(int arr[], int n) {
    if (n <= 0) return;
    int max_val = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > max_val) max_val = arr[i];
    }
    for (int exp = 1; max_val / exp > 0; exp *= 10) {
        radix_count_sort(arr, n, exp);
    }
}

/* Shell Sort */
static void shell_sort(int arr[], int n) {
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

/* 3.2 Binary Search Lower and Upper Bounds */
static int lower_bound(const int arr[], int n, int target) {
    int low = 0, high = n;
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] >= target) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

static int upper_bound(const int arr[], int n, int target) {
    int low = 0, high = n;
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] > target) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

/* 3.3 Disjoint Set Union (DSU / Union-Find) with Rank and Path Compression */
typedef struct {
    int *parent;
    int *rank;
    int n;
} DSU;

static DSU *dsu_create(int n) {
    DSU *d = (DSU*)malloc(sizeof(DSU));
    d->n = n;
    d->parent = (int*)malloc(n * sizeof(int));
    d->rank = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        d->parent[i] = i;
        d->rank[i] = 0;
    }
    return d;
}

static int dsu_find(DSU *d, int i) {
    if (d->parent[i] == i) return i;
    return d->parent[i] = dsu_find(d, d->parent[i]); // Path compression
}

static void dsu_union(DSU *d, int i, int j) {
    int root_i = dsu_find(d, i);
    int root_j = dsu_find(d, j);
    if (root_i != root_j) {
        if (d->rank[root_i] < d->rank[root_j]) {
            d->parent[root_i] = root_j;
        } else if (d->rank[root_i] > d->rank[root_j]) {
            d->parent[root_j] = root_i;
        } else {
            d->parent[root_j] = root_i;
            d->rank[root_i]++;
        }
    }
}

static void dsu_free(DSU *d) {
    free(d->parent);
    free(d->rank);
    free(d);
}

/* 3.4 Dijkstra's Shortest Path Algorithm (using Min-Heap) */
typedef struct {
    int vertex;
    int dist;
} DijkstraHeapNode;

typedef struct {
    DijkstraHeapNode *data;
    int size;
    int capacity;
} DijkstraHeap;

static DijkstraHeap *dj_heap_create(int cap) {
    DijkstraHeap *h = (DijkstraHeap*)malloc(sizeof(DijkstraHeap));
    h->data = (DijkstraHeapNode*)malloc(cap * sizeof(DijkstraHeapNode));
    h->size = 0;
    h->capacity = cap;
    return h;
}

static void dj_heap_push(DijkstraHeap *h, int u, int dist) {
    if (h->size >= h->capacity) {
        h->capacity *= 2;
        h->data = (DijkstraHeapNode*)realloc(h->data, h->capacity * sizeof(DijkstraHeapNode));
    }
    h->data[h->size].vertex = u;
    h->data[h->size].dist = dist;
    int idx = h->size;
    h->size++;
    while (idx > 0) {
        int parent = (idx - 1) / 2;
        if (h->data[idx].dist < h->data[parent].dist) {
            DijkstraHeapNode tmp = h->data[idx];
            h->data[idx] = h->data[parent];
            h->data[parent] = tmp;
            idx = parent;
        } else {
            break;
        }
    }
}

static DijkstraHeapNode dj_heap_pop(DijkstraHeap *h) {
    DijkstraHeapNode res = h->data[0];
    h->data[0] = h->data[h->size - 1];
    h->size--;
    int idx = 0;
    while (2 * idx + 1 < h->size) {
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;
        int smallest = left;
        if (right < h->size && h->data[right].dist < h->data[left].dist) smallest = right;
        if (h->data[smallest].dist < h->data[idx].dist) {
            DijkstraHeapNode tmp = h->data[idx];
            h->data[idx] = h->data[smallest];
            h->data[smallest] = tmp;
            idx = smallest;
        } else {
            break;
        }
    }
    return res;
}

static void run_dijkstra(const AdjListGraph *g, int src, int *dist) {
    for (int i = 0; i < MAX_VERTICES; i++) dist[i] = GRAPH_INF;
    dist[src] = 0;
    DijkstraHeap *h = dj_heap_create(100);
    dj_heap_push(h, src, 0);
    while (h->size > 0) {
        DijkstraHeapNode node = dj_heap_pop(h);
        int u = node.vertex;
        if (node.dist > dist[u]) continue;
        GNode *curr = g->head[u];
        while (curr) {
            int v = curr->dest;
            int w = curr->weight;
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                dj_heap_push(h, v, dist[v]);
            }
            curr = curr->next;
        }
    }
    free(h->data);
    free(h);
}

/* 3.5 Bellman-Ford Pathfinding */
typedef struct {
    int src, dest, weight;
} Edge;

static bool run_bellman_ford(int vertices, int num_edges, const Edge edges[], int src) {
    int *dist = (int*)malloc(vertices * sizeof(int));
    for (int i = 0; i < vertices; i++) dist[i] = GRAPH_INF;
    dist[src] = 0;
    for (int i = 1; i <= vertices - 1; i++) {
        for (int j = 0; j < num_edges; j++) {
            int u = edges[j].src;
            int v = edges[j].dest;
            int w = edges[j].weight;
            if (dist[u] != GRAPH_INF && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    bool has_neg_cycle = false;
    for (int j = 0; j < num_edges; j++) {
        int u = edges[j].src;
        int v = edges[j].dest;
        int w = edges[j].weight;
        if (dist[u] != GRAPH_INF && dist[u] + w < dist[v]) {
            has_neg_cycle = true;
            break;
        }
    }
    free(dist);
    return !has_neg_cycle;
}

/* 3.6 Floyd-Warshall All-Pairs Shortest Paths */
static void run_floyd_warshall(int vertices, int graph[MAX_NODES][MAX_NODES]) {
    int dist[MAX_NODES][MAX_NODES];
    for (int i = 0; i < vertices; i++) {
        for (int j = 0; j < vertices; j++) {
            if (i == j) dist[i][j] = 0;
            else if (graph[i][j] == 0) dist[i][j] = GRAPH_INF;
            else dist[i][j] = graph[i][j];
        }
    }
    for (int k = 0; k < vertices; k++) {
        for (int i = 0; i < vertices; i++) {
            for (int j = 0; j < vertices; j++) {
                if (dist[i][k] != GRAPH_INF && dist[k][j] != GRAPH_INF && dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }
}

/* 3.7 Kruskal's Minimum Spanning Tree */
static int compare_edges(const void *a, const void *b) {
    return ((const Edge*)a)->weight - ((const Edge*)b)->weight;
}

static void run_kruskal(int vertices, int num_edges, Edge edges[]) {
    qsort(edges, num_edges, sizeof(Edge), compare_edges);
    DSU *d = dsu_create(vertices);
    int mst_weight = 0;
    int edges_in_mst = 0;
    for (int i = 0; i < num_edges && edges_in_mst < vertices - 1; i++) {
        int u = edges[i].src;
        int v = edges[i].dest;
        if (dsu_find(d, u) != dsu_find(d, v)) {
            dsu_union(d, u, v);
            mst_weight += edges[i].weight;
            edges_in_mst++;
        }
    }
    dsu_free(d);
}

/* 3.8 Prim's Minimum Spanning Tree */
static int prim_min_key(const int key[], const bool mst_set[], int vertices) {
    int min_val = GRAPH_INF, min_idx = -1;
    for (int v = 0; v < vertices; v++) {
        if (!mst_set[v] && key[v] < min_val) {
            min_val = key[v];
            min_idx = v;
        }
    }
    return min_idx;
}

static void run_prims_mst(int vertices, const int graph[MAX_NODES][MAX_NODES]) {
    int *parent = (int*)malloc(vertices * sizeof(int));
    int *key = (int*)malloc(vertices * sizeof(int));
    bool *mst_set = (bool*)malloc(vertices * sizeof(bool));
    for (int i = 0; i < vertices; i++) {
        key[i] = GRAPH_INF;
        mst_set[i] = false;
    }
    key[0] = 0;
    parent[0] = -1;
    for (int count = 0; count < vertices - 1; count++) {
        int u = prim_min_key(key, mst_set, vertices);
        mst_set[u] = true;
        for (int v = 0; v < vertices; v++) {
            if (graph[u][v] && !mst_set[v] && graph[u][v] < key[v]) {
                parent[v] = u;
                key[v] = graph[u][v];
            }
        }
    }
    free(parent);
    free(key);
    free(mst_set);
}

/* 3.9 Dynamic Programming: Knapsack, LCS, Edit Distance, Matrix Chain, LIS */
static int dp_max(int a, int b) { return (a > b) ? a : b; }
static int dp_min(int a, int b) { return (a < b) ? a : b; }

/* 0/1 Knapsack with Traceback */
static void run_knapsack_01(int W, const int wt[], const int val[], int n) {
    int **dp = (int**)malloc((n + 1) * sizeof(int*));
    for (int i = 0; i <= n; i++) dp[i] = (int*)calloc(W + 1, sizeof(int));
    
    for (int i = 1; i <= n; i++) {
        for (int w = 1; w <= W; w++) {
            if (wt[i - 1] <= w) {
                dp[i][w] = dp_max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }
    
    int w = W;
    printf("    Knapsack Traceback (Items included): ");
    for (int i = n; i > 0 && w > 0; i--) {
        if (dp[i][w] != dp[i - 1][w]) {
            printf("Item %d (val=%d, wt=%d) ", i - 1, val[i - 1], wt[i - 1]);
            w -= wt[i - 1];
        }
    }
    printf("\n");
    for (int i = 0; i <= n; i++) free(dp[i]);
    free(dp);
}

/* Longest Common Subsequence with Traceback */
static void run_lcs(const char *X, const char *Y) {
    int m = strlen(X);
    int n = strlen(Y);
    int **L = (int**)malloc((m + 1) * sizeof(int*));
    for (int i = 0; i <= m; i++) L[i] = (int*)calloc(n + 1, sizeof(int));
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (X[i - 1] == Y[j - 1]) {
                L[i][j] = L[i - 1][j - 1] + 1;
            } else {
                L[i][j] = dp_max(L[i - 1][j], L[i][j - 1]);
            }
        }
    }
    
    int index = L[m][n];
    char *lcs_str = (char*)malloc((index + 1) * sizeof(char));
    lcs_str[index] = '\0';
    int i = m, j = n;
    while (i > 0 && j > 0) {
        if (X[i - 1] == Y[j - 1]) {
            lcs_str[index - 1] = X[i - 1];
            i--; j--; index--;
        } else if (L[i - 1][j] > L[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }
    printf("    LCS Traceback: '%s'\n", lcs_str);
    free(lcs_str);
    for (int r = 0; r <= m; r++) free(L[r]);
    free(L);
}

/* Edit Distance with Operations Traceback */
static void run_edit_distance(const char *str1, const char *str2) {
    int m = strlen(str1);
    int n = strlen(str2);
    int **dp = (int**)malloc((m + 1) * sizeof(int*));
    for (int i = 0; i <= m; i++) dp[i] = (int*)malloc((n + 1) * sizeof(int));
    
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (str1[i - 1] == str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + dp_min(dp[i - 1][j - 1], dp_min(dp[i - 1][j], dp[i][j - 1]));
            }
        }
    }
    printf("    Edit Distance (Min ops count): %d\n", dp[m][n]);
    for (int i = 0; i <= m; i++) free(dp[i]);
    free(dp);
}

/* Matrix Chain Multiplication */
static int matrix_chain_order(const int p[], int n) {
    int **m = (int**)malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++) m[i] = (int*)calloc(n, sizeof(int));
    for (int l = 2; l < n; l++) {
        for (int i = 1; i < n - l + 1; i++) {
            int j = i + l - 1;
            m[i][j] = 100000000;
            for (int k = i; k <= j - 1; k++) {
                int q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                if (q < m[i][j]) m[i][j] = q;
            }
        }
    }
    int ans = m[1][n - 1];
    for (int i = 0; i < n; i++) free(m[i]);
    free(m);
    return ans;
}

/* Longest Increasing Subsequence */
static int longest_increasing_subsequence(const int arr[], int n) {
    if (n <= 0) return 0;
    int *lis = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) lis[i] = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (arr[i] > arr[j] && lis[i] < lis[j] + 1) {
                lis[i] = lis[j] + 1;
            }
        }
    }
    int max_val = lis[0];
    for (int i = 1; i < n; i++) {
        if (lis[i] > max_val) max_val = lis[i];
    }
    free(lis);
    return max_val;
}

/* 3.10 String Matching: KMP and Rabin-Karp */
/* KMP LPS construction */
static void kmp_compute_lps(const char *pat, int M, int *lps) {
    int len = 0;
    lps[0] = 0;
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
}

static void run_kmp(const char *txt, const char *pat) {
    int N = strlen(txt);
    int M = strlen(pat);
    int *lps = (int*)malloc(M * sizeof(int));
    kmp_compute_lps(pat, M, lps);
    int i = 0, j = 0;
    printf("    KMP Pattern Matching (Matches): ");
    while (i < N) {
        if (pat[j] == txt[i]) {
            i++; j++;
        }
        if (j == M) {
            printf("Index %d ", i - j);
            j = lps[j - 1];
        } else if (i < N && pat[j] != txt[i]) {
            if (j != 0) j = lps[j - 1];
            else i++;
        }
    }
    printf("\n");
    free(lps);
}

/* Rabin-Karp Rolling Hash */
#define RK_D 256
#define RK_Q 101
static void run_rabin_karp(const char *txt, const char *pat) {
    int N = strlen(txt);
    int M = strlen(pat);
    int p = 0; // hash for pattern
    int t = 0; // hash for text
    int h = 1;
    for (int i = 0; i < M - 1; i++) {
        h = (h * RK_D) % RK_Q;
    }
    for (int i = 0; i < M; i++) {
        p = (RK_D * p + pat[i]) % RK_Q;
        t = (RK_D * t + txt[i]) % RK_Q;
    }
    printf("    Rabin-Karp Pattern Matching (Matches): ");
    for (int i = 0; i <= N - M; i++) {
        if (p == t) {
            int j;
            for (j = 0; j < M; j++) {
                if (txt[i + j] != pat[j]) break;
            }
            if (j == M) printf("Index %d ", i);
        }
        if (i < N - M) {
            t = (RK_D * (t - txt[i] * h) + txt[i + M]) % RK_Q;
            if (t < 0) t = (t + RK_Q);
        }
    }
    printf("\n");
}

static void sorting_mst_demo(void) {
    print_sep("3.1 to 3.8 SORTING, SEARCH BOUNDS, DSU & GRAPH PATHS");
    
    /* Sorts */
    int arr[] = {38, 27, 43, 3, 9, 82, 10};
    int n = sizeof(arr)/sizeof(arr[0]);
    int *temp = (int*)malloc(n * sizeof(int));
    
    memcpy(temp, arr, n * sizeof(int));
    quicksort_lomuto(temp, 0, n - 1);
    printf("  Lomuto Quick Sorted: ");
    for(int i=0; i<n; i++) printf("%d ", temp[i]);
    printf("\n");

    memcpy(temp, arr, n * sizeof(int));
    merge_sort(temp, 0, n - 1);
    printf("  Merge Sorted: ");
    for(int i=0; i<n; i++) printf("%d ", temp[i]);
    printf("\n");

    memcpy(temp, arr, n * sizeof(int));
    counting_sort(temp, n);
    printf("  Counting Sorted: ");
    for(int i=0; i<n; i++) printf("%d ", temp[i]);
    printf("\n");
    free(temp);

    /* Lower/Upper Bounds */
    int s_arr[] = {1, 2, 4, 4, 4, 5, 7, 9};
    int sn = 8;
    printf("  Sorted Array: ");
    for(int i=0; i<sn; i++) printf("%d ", s_arr[i]);
    printf("\n");
    printf("  lower_bound of 4: index %d, upper_bound of 4: index %d\n", 
           lower_bound(s_arr, sn, 4), upper_bound(s_arr, sn, 4));

    /* DSU & Kruskal */
    Edge kr_edges[] = {
        {0, 1, 10}, {0, 2, 6}, {0, 3, 5},
        {1, 3, 15}, {2, 3, 4}
    };
    int num_k_edges = sizeof(kr_edges)/sizeof(kr_edges[0]);
    run_kruskal(4, num_k_edges, kr_edges);
    printf("  Kruskal's MST computed successfully (4 vertices, 5 edges)\n");

    /* Dijkstra */
    AdjListGraph *dj_g = graph_list_create();
    graph_list_add_edge(dj_g, 0, 1, 4);
    graph_list_add_edge(dj_g, 0, 2, 2);
    graph_list_add_edge(dj_g, 1, 2, 5);
    graph_list_add_edge(dj_g, 1, 3, 10);
    graph_list_add_edge(dj_g, 2, 3, 3);
    graph_list_add_edge(dj_g, 2, 4, 8);
    graph_list_add_edge(dj_g, 3, 4, 2);
    
    int dist[MAX_VERTICES];
    run_dijkstra(dj_g, 0, dist);
    printf("  Dijkstra Shortest Paths from vertex 0:\n");
    for (int i = 0; i < 5; i++) {
        printf("    Vertex %d: distance = %d\n", i, dist[i]);
    }
    graph_list_free(dj_g);
}

static void dp_demo(void) {
    print_sep("3.9, 3.10 DYNAMIC PROGRAMMING & STRING MATCHING");
    
    /* 0/1 Knapsack */
    int val[] = {60, 100, 120};
    int wt[] = {10, 20, 30};
    int W = 50;
    printf("  0/1 Knapsack (W=50):\n");
    run_knapsack_01(W, wt, val, 3);

    /* LCS */
    printf("  Longest Common Subsequence:\n");
    run_lcs("ABCDGH", "AEDFHR");

    /* Edit Distance */
    printf("  Edit Distance:\n");
    run_edit_distance("sunday", "saturday");

    /* Matrix Chain Multiplication */
    int p_arr[] = {10, 20, 30, 40, 30};
    printf("  Matrix Chain Multiplication Min Operations: %d\n", matrix_chain_order(p_arr, 5));

    /* String Pattern Matching */
    run_kmp("ABABDABACDABABCABAB", "ABABCABAB");
    run_rabin_karp("ABABDABACDABABCABAB", "ABABCABAB");
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
    print("Chunk 1 appended successfully!")
