# expand_builder.py
# Performs expansions on build_cs_ds_encyclopedia_c.py to increase line count and detail level

with open("build_cs_ds_encyclopedia_c.py", "r", encoding="utf-8") as f:
    content = f.read()

# ---------------------------------------------------------------------------
# 1. Segment Tree Lazy Propagation Expansion
# ---------------------------------------------------------------------------
old_seg_tree_c = """static int seg_tree_query(const int *tree, int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;
    if (l <= start && end <= r) return tree[node];
    int mid = (start + end) / 2;
    return seg_tree_query(tree, 2 * node, start, mid, l, r) +
           seg_tree_query(tree, 2 * node + 1, mid + 1, end, l, r);
}"""

new_seg_tree_c = """static int seg_tree_query(const int *tree, int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;
    if (l <= start && end <= r) return tree[node];
    int mid = (start + end) / 2;
    return seg_tree_query(tree, 2 * node, start, mid, l, r) +
           seg_tree_query(tree, 2 * node + 1, mid + 1, end, l, r);
}

static void seg_tree_update_range(int *tree, int *lazy, int node, int start, int end, int l, int r, int val) {
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
    int mid = (start + end) / 2;
    seg_tree_update_range(tree, lazy, 2 * node, start, mid, l, r, val);
    seg_tree_update_range(tree, lazy, 2 * node + 1, mid + 1, end, l, r, val);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
}

static int seg_tree_query_lazy(int *tree, int *lazy, int node, int start, int end, int l, int r) {
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
    int mid = (start + end) / 2;
    return seg_tree_query_lazy(tree, lazy, 2 * node, start, mid, l, r) +
           seg_tree_query_lazy(tree, lazy, 2 * node + 1, mid + 1, end, l, r);
}"""

# ---------------------------------------------------------------------------
# 2. Segment Tree Demo Expansion
# ---------------------------------------------------------------------------
old_seg_demo = """    /* Segment Tree Demo */
    int arr[] = {1, 3, 5, 7, 9, 11};
    int n = 6;
    int *tree = (int*)calloc(4 * n, sizeof(int));
    seg_tree_build(tree, arr, 1, 0, n - 1);
    printf("  Segment Tree: Sum of values in range [1, 3] = %d\\n", seg_tree_query(tree, 1, 0, n - 1, 1, 3));
    seg_tree_update(tree, 1, 0, n - 1, 1, 10);
    printf("  Segment Tree after update: Sum of values in range [1, 3] = %d\\n", seg_tree_query(tree, 1, 0, n - 1, 1, 3));
    free(tree);"""

new_seg_demo = """    /* Segment Tree Demo */
    int arr[] = {1, 3, 5, 7, 9, 11};
    int n = 6;
    int *tree = (int*)calloc(4 * n, sizeof(int));
    seg_tree_build(tree, arr, 1, 0, n - 1);
    printf("  Segment Tree: Sum of values in range [1, 3] = %d\\n", seg_tree_query(tree, 1, 0, n - 1, 1, 3));
    seg_tree_update(tree, 1, 0, n - 1, 1, 10);
    printf("  Segment Tree after update: Sum of values in range [1, 3] = %d\\n", seg_tree_query(tree, 1, 0, n - 1, 1, 3));
    
    /* Lazy Propagation Segment Tree Demo */
    int *lazy = (int*)calloc(4 * n, sizeof(int));
    seg_tree_update_range(tree, lazy, 1, 0, n - 1, 1, 5, 10);
    printf("  Segment Tree Lazy Query sum [1, 3] = %d\\n", seg_tree_query_lazy(tree, lazy, 1, 0, n - 1, 1, 3));
    free(lazy);
    free(tree);"""

# ---------------------------------------------------------------------------
# 3. Dijkstra Path Reconstruction
# ---------------------------------------------------------------------------
old_dijkstra_c = """static void run_dijkstra(const AdjListGraph *g, int src, int *dist) {
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
}"""

new_dijkstra_c = """static void run_dijkstra(const AdjListGraph *g, int src, int *dist) {
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

static void print_dijkstra_path_rec(const int parent[], int j) {
    if (parent[j] == -1) return;
    print_dijkstra_path_rec(parent, parent[j]);
    printf("-> %d ", j);
}

static void run_dijkstra_with_path(const AdjListGraph *g, int src, int *dist) {
    int parent[MAX_VERTICES];
    for (int i = 0; i < MAX_VERTICES; i++) {
        dist[i] = GRAPH_INF;
        parent[i] = -1;
    }
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
                parent[v] = u;
                dj_heap_push(h, v, dist[v]);
            }
            curr = curr->next;
        }
    }
    printf("    Shortest paths reconstructed from vertex %d:\\n", src);
    for (int i = 0; i < 5; i++) {
        if (dist[i] != GRAPH_INF && i != src) {
            printf("      Path to %d: %d ", i, src);
            print_dijkstra_path_rec(parent, i);
            printf("(dist: %d)\\n", dist[i]);
        }
    }
    free(h->data);
    free(h);
}"""

# ---------------------------------------------------------------------------
# 4. Dijkstra Demo Expansion
# ---------------------------------------------------------------------------
old_dijkstra_demo = """    /* Dijkstra */
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
    printf("  Dijkstra Shortest Paths from vertex 0:\\n");
    for (int i = 0; i < 5; i++) {
        printf("    Vertex %d: distance = %d\\n", i, dist[i]);
    }
    graph_list_free(dj_g);"""

new_dijkstra_demo = """    /* Dijkstra with Path Reconstruction */
    AdjListGraph *dj_g = graph_list_create();
    graph_list_add_edge(dj_g, 0, 1, 4);
    graph_list_add_edge(dj_g, 0, 2, 2);
    graph_list_add_edge(dj_g, 1, 2, 5);
    graph_list_add_edge(dj_g, 1, 3, 10);
    graph_list_add_edge(dj_g, 2, 3, 3);
    graph_list_add_edge(dj_g, 2, 4, 8);
    graph_list_add_edge(dj_g, 3, 4, 2);
    
    int dist[MAX_VERTICES];
    run_dijkstra_with_path(dj_g, 0, dist);
    graph_list_free(dj_g);"""

# ---------------------------------------------------------------------------
# 5. Gaussian Elimination Matrix Solver
# ---------------------------------------------------------------------------
old_matrix_det = """static double matrix_determinant_3x3(const double *M) {
    return M[0]*(M[4]*M[8] - M[5]*M[7]) - M[1]*(M[3]*M[8] - M[5]*M[6]) + M[2]*(M[3]*M[7] - M[4]*M[6]);
}"""

new_matrix_det = """static double matrix_determinant_3x3(const double *M) {
    return M[0]*(M[4]*M[8] - M[5]*M[7]) - M[1]*(M[3]*M[8] - M[5]*M[6]) + M[2]*(M[3]*M[7] - M[4]*M[6]);
}

static bool matrix_solve_gaussian(const double *A, const double *b, double *x, int n) {
    double *M = (double*)malloc(n * (n + 1) * sizeof(double));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            M[i * (n + 1) + j] = A[i * n + j];
        }
        M[i * (n + 1) + n] = b[i];
    }
    
    for (int i = 0; i < n; i++) {
        int pivot = i;
        for (int j = i + 1; j < n; j++) {
            if (fabs(M[j * (n + 1) + i]) > fabs(M[pivot * (n + 1) + i])) {
                pivot = j;
            }
        }
        if (pivot != i) {
            for (int k = 0; k <= n; k++) {
                double tmp = M[i * (n + 1) + k];
                M[i * (n + 1) + k] = M[pivot * (n + 1) + k];
                M[pivot * (n + 1) + k] = tmp;
            }
        }
        if (fabs(M[i * (n + 1) + i]) < 1e-9) {
            free(M);
            return false;
        }
        for (int j = i + 1; j < n; j++) {
            double factor = M[j * (n + 1) + i] / M[i * (n + 1) + i];
            for (int k = i; k <= n; k++) {
                M[j * (n + 1) + k] -= factor * M[i * (n + 1) + k];
            }
        }
    }
    for (int i = n - 1; i >= 0; i--) {
        double sum = 0.0;
        for (int j = i + 1; j < n; j++) {
            sum += M[i * (n + 1) + j] * x[j];
        }
        x[i] = (M[i * (n + 1) + n] - sum) / M[i * (n + 1) + i];
    }
    free(M);
    return true;
}"""

# ---------------------------------------------------------------------------
# 6. Real Decision Tree Classifier Implementation
# ---------------------------------------------------------------------------
old_dt_c = """static double dt_calculate_gini(const int classes[], int n) {
    if (n == 0) return 0.0;
    int c0 = 0, c1 = 0;
    for (int i = 0; i < n; i++) {
        if (classes[i] == 0) c0++;
        else c1++;
    }
    double p0 = (double)c0 / n;
    double p1 = (double)c1 / n;
    return 1.0 - (p0*p0 + p1*p1);
}

static DTNode *dt_build_tree_stub(double val) {
    DTNode *node = (DTNode*)malloc(sizeof(DTNode));
    node->is_leaf = true;
    node->leaf_val = val;
    node->left = node->right = NULL;
    return node;
}

static void dt_free(DTNode *root) {
    if (root) {
        dt_free(root->left);
        dt_free(root->right);
        free(root);
    }
}"""

new_dt_c = """static double dt_calculate_gini(const int classes[], int n) {
    if (n == 0) return 0.0;
    int c0 = 0, c1 = 0;
    for (int i = 0; i < n; i++) {
        if (classes[i] == 0) c0++;
        else c1++;
    }
    double p0 = (double)c0 / n;
    double p1 = (double)c1 / n;
    return 1.0 - (p0*p0 + p1*p1);
}

static void dt_split_dataset(const double X[], const int y[], int n, int feature_idx, double threshold,
                             double **X_left, int **y_left, int *n_left,
                             double **X_right, int **y_right, int *n_right) {
    *n_left = 0;
    *n_right = 0;
    for (int i = 0; i < n; i++) {
        if (X[i * 2 + feature_idx] < threshold) (*n_left)++;
        else (*n_right)++;
    }
    *X_left = (double*)malloc((*n_left) * 2 * sizeof(double));
    *y_left = (int*)malloc((*n_left) * sizeof(int));
    *X_right = (double*)malloc((*n_right) * 2 * sizeof(double));
    *y_right = (int*)malloc((*n_right) * sizeof(int));
    int il = 0, ir = 0;
    for (int i = 0; i < n; i++) {
        if (X[i * 2 + feature_idx] < threshold) {
            (*X_left)[il * 2] = X[i * 2];
            (*X_left)[il * 2 + 1] = X[i * 2 + 1];
            (*y_left)[il] = y[i];
            il++;
        } else {
            (*X_right)[ir * 2] = X[i * 2];
            (*X_right)[ir * 2 + 1] = X[i * 2 + 1];
            (*y_right)[ir] = y[i];
            ir++;
        }
    }
}

static DTNode *dt_train(const double X[], const int y[], int n, int depth, int max_depth) {
    bool pure = true;
    for (int i = 1; i < n; i++) {
        if (y[i] != y[0]) { pure = false; break; }
    }
    if (pure || depth >= max_depth || n <= 2) {
        DTNode *node = (DTNode*)malloc(sizeof(DTNode));
        node->is_leaf = true;
        int c0 = 0, c1 = 0;
        for (int i = 0; i < n; i++) {
            if (y[i] == 0) c0++; else c1++;
        }
        node->leaf_val = (c1 > c0) ? 1.0 : 0.0;
        node->left = node->right = NULL;
        return node;
    }

    double best_gini = 1.0;
    int best_f = -1;
    double best_t = 0.0;
    for (int f = 0; f < 2; f++) {
        for (int i = 0; i < n; i++) {
            double threshold = X[i * 2 + f];
            double *X_l; int *y_l, n_l;
            double *X_r; int *y_r, n_r;
            dt_split_dataset(X, y, n, f, threshold, &X_l, &y_l, &n_l, &X_r, &y_r, &n_r);
            double gini_l = dt_calculate_gini(y_l, n_l);
            double gini_r = dt_calculate_gini(y_r, n_r);
            double total_gini = ((double)n_l / n) * gini_l + ((double)n_r / n) * gini_r;
            if (total_gini < best_gini) {
                best_gini = total_gini;
                best_f = f;
                best_t = threshold;
            }
            free(X_l); free(y_l);
            free(X_r); free(y_r);
        }
    }

    if (best_f == -1) {
        DTNode *node = (DTNode*)malloc(sizeof(DTNode));
        node->is_leaf = true;
        int c0 = 0, c1 = 0;
        for (int i = 0; i < n; i++) {
            if (y[i] == 0) c0++; else c1++;
        }
        node->leaf_val = (c1 > c0) ? 1.0 : 0.0;
        node->left = node->right = NULL;
        return node;
    }

    DTNode *node = (DTNode*)malloc(sizeof(DTNode));
    node->is_leaf = false;
    node->feature_idx = best_f;
    node->threshold = best_t;
    double *X_l; int *y_l, n_l;
    double *X_r; int *y_r, n_r;
    dt_split_dataset(X, y, best_f, best_t, &X_l, &y_l, &n_l, &X_r, &y_r, &n_r);
    node->left = dt_train(X_l, y_l, n_l, depth + 1, max_depth);
    node->right = dt_train(X_r, y_r, n_r, depth + 1, max_depth);
    free(X_l); free(y_l);
    free(X_r); free(y_r);
    return node;
}

static double dt_predict(const DTNode *node, const double sample[2]) {
    if (node->is_leaf) return node->leaf_val;
    if (sample[node->feature_idx] < node->threshold) {
        return dt_predict(node->left, sample);
    } else {
        return dt_predict(node->right, sample);
    }
}

static void dt_free(DTNode *root) {
    if (root) {
        dt_free(root->left);
        dt_free(root->right);
        free(root);
    }
}"""

# ---------------------------------------------------------------------------
# 7. Decision Tree Demo Expansion
# ---------------------------------------------------------------------------
old_dt_demo = """    /* Decision Tree Impurity Split */
    int labels[] = {0, 0, 1, 1, 1, 0};
    printf("  Gini impurity split count (6 items): %.4f\\n", dt_calculate_gini(labels, 6));
    DTNode *root = dt_build_tree_stub(1.0);
    dt_free(root);"""

new_dt_demo = """    /* Decision Tree Impurity Split */
    int labels[] = {0, 0, 1, 1, 1, 0};
    printf("  Gini impurity split count (6 items): %.4f\\n", dt_calculate_gini(labels, 6));
    
    /* Decision Tree Classifier Training & Testing */
    double dt_X[] = {1.0, 1.0,  1.5, 2.0,  5.0, 5.0,  6.0, 6.0,  1.2, 1.5};
    int dt_y[] = {0, 0, 1, 1, 0};
    DTNode *dt_root = dt_train(dt_X, dt_y, 5, 0, 3);
    double test_sample[2] = {1.1, 1.2};
    printf("  Decision Tree trained. Classification of sample (1.1, 1.2): %.1f\\n", dt_predict(dt_root, test_sample));
    dt_free(dt_root);

    /* Gaussian Elimination solver */
    double gauss_A[4] = {2, 1, 1, 3};
    double gauss_b[2] = {5, 5};
    double gauss_x[2];
    if (matrix_solve_gaussian(gauss_A, gauss_b, gauss_x, 2)) {
        printf("  Gaussian Elimination (2x2): x0=%.2f, x1=%.2f (expected 2.00, 1.00)\\n", gauss_x[0], gauss_x[1]);
    }"""

# Perform replacements
content = content.replace(old_seg_tree_c, new_seg_tree_c)
content = content.replace(old_seg_demo, new_seg_demo)
content = content.replace(old_dijkstra_c, new_dijkstra_c)
content = content.replace(old_dijkstra_demo, new_dijkstra_demo)
content = content.replace(old_matrix_det, new_matrix_det)
content = content.replace(old_dt_c, new_dt_c)
content = content.replace(old_dt_demo, new_dt_demo)

with open("build_cs_ds_encyclopedia_c.py", "w", encoding="utf-8") as f:
    f.write(content)

print("build_cs_ds_encyclopedia_c.py expanded successfully with advanced algorithms!")
