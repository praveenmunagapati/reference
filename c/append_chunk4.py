# append_chunk4.py
# Appends Phase 8 (Statistics, Algebra & Machine Learning) section to build_cs_ds_encyclopedia_c.py

import os

c_quote = "'''"

chunk_content = r"""
# ---------------------------------------------------------------------------
# PHASE 8: STATISTICS, ALGEBRA & MACHINE LEARNING
# ---------------------------------------------------------------------------
add_section("PHASE_8_STATISTICS_ALGEBRA_ML", r{c_quote}
/* ==================================================================
 *  PHASE 8: STATISTICS, ALGEBRA & MACHINE LEARNING
 * ================================================================== */

/* 8.1 Basic Statistics & Probability */
static double stats_mean(const double data[], int n) {
    double sum = 0.0;
    for (int i = 0; i < n; i++) sum += data[i];
    return sum / n;
}

static int stats_compare_doubles(const void *a, const void *b) {
    double diff = *(const double*)a - *(const double*)b;
    return (diff > 0) - (diff < 0);
}

static double stats_median(double data[], int n) {
    qsort(data, n, sizeof(double), stats_compare_doubles);
    if (n % 2 == 0) return (data[n/2 - 1] + data[n/2]) / 2.0;
    return data[n/2];
}

static double stats_stddev(const double data[], int n, double mean) {
    double var_sum = 0.0;
    for (int i = 0; i < n; i++) {
        var_sum += (data[i] - mean) * (data[i] - mean);
    }
    return sqrt(var_sum / n);
}

/* Box-Muller Transform for Normal random generation */
static double box_muller_normal(double mean, double stddev) {
    static bool has_spare = false;
    static double spare;
    if (has_spare) {
        has_spare = false;
        return mean + stddev * spare;
    }
    has_spare = true;
    double u, v, s;
    do {
        u = 2.0 * ((double)rand() / RAND_MAX) - 1.0;
        v = 2.0 * ((double)rand() / RAND_MAX) - 1.0;
        s = u * u + v * v;
    } while (s >= 1.0 || s == 0.0);
    s = sqrt(-2.0 * log(s) / s);
    spare = v * s;
    return mean + stddev * (u * s);
}

/* Outlier detection using IQR and Z-Score */
static void stats_detect_outliers(double data[], int n) {
    double mean = stats_mean(data, n);
    double stddev = stats_stddev(data, n, mean);
    
    // Z-Score outlier check
    printf("    Z-Score Outliers (|Z| > 2): ");
    for (int i = 0; i < n; i++) {
        double z = (data[i] - mean) / stddev;
        if (fabs(z) > 2.0) printf("%.1f (Z=%.2f) ", data[i], z);
    }
    printf("\n");
    
    // IQR outlier check
    qsort(data, n, sizeof(double), stats_compare_doubles);
    double q1 = data[n / 4];
    double q3 = data[(3 * n) / 4];
    double iqr = q3 - q1;
    double lower_bound_iqr = q1 - 1.5 * iqr;
    double upper_bound_iqr = q3 + 1.5 * iqr;
    printf("    IQR Outliers: ");
    for (int i = 0; i < n; i++) {
        if (data[i] < lower_bound_iqr || data[i] > upper_bound_iqr) {
            printf("%.1f ", data[i]);
        }
    }
    printf("\n");
}

/* 8.2 Matrix Algebra Library */
static void matrix_multiply(const double *A, const double *B, double *C, int r1, int c1, int c2) {
    for (int i = 0; i < r1; i++) {
        for (int j = 0; j < c2; j++) {
            C[i * c2 + j] = 0.0;
            for (int k = 0; k < c1; k++) {
                C[i * c2 + j] += A[i * c1 + k] * B[k * c2 + j];
            }
        }
    }
}

static void matrix_transpose_3x3(const double *A, double *B) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            B[j * 3 + i] = A[i * 3 + j];
        }
    }
}

static double matrix_determinant_3x3(const double *M) {
    return M[0]*(M[4]*M[8] - M[5]*M[7]) - M[1]*(M[3]*M[8] - M[5]*M[6]) + M[2]*(M[3]*M[7] - M[4]*M[6]);
}

static bool matrix_invert_3x3(const double *M, double *I) {
    double det = matrix_determinant_3x3(M);
    if (fabs(det) < 1e-9) return false;
    double invdet = 1.0 / det;
    I[0] = (M[4] * M[8] - M[5] * M[7]) * invdet;
    I[1] = (M[2] * M[7] - M[1] * M[8]) * invdet;
    I[2] = (M[1] * M[5] - M[2] * M[4]) * invdet;
    I[3] = (M[5] * M[6] - M[3] * M[8]) * invdet;
    I[4] = (M[0] * M[8] - M[2] * M[6]) * invdet;
    I[5] = (M[2] * M[3] - M[0] * M[5]) * invdet;
    I[6] = (M[3] * M[7] - M[4] * M[6]) * invdet;
    I[7] = (M[1] * M[6] - M[0] * M[7]) * invdet;
    I[8] = (M[0] * M[4] - M[1] * M[3]) * invdet;
    return true;
}

/* Sparse Matrix Triplet */
typedef struct {
    int row;
    int col;
    double val;
} Triplet;

static void sparse_matrix_print(const Triplet triplets[], int count) {
    printf("    Sparse Matrix Triplets:\n");
    for (int i = 0; i < count; i++) {
        printf("      Row %d, Col %d: val = %.2f\n", triplets[i].row, triplets[i].col, triplets[i].val);
    }
}

/* 8.3 Machine Learning Models from Scratch */

/* Linear Regression with Gradient Descent */
static void ml_linear_regression(const double X[], const double y[], int n, double *w, double *b, double lr, int epochs) {
    *w = 0.0;
    *b = 0.0;
    for (int epoch = 0; epoch < epochs; epoch++) {
        double dw = 0.0;
        double db = 0.0;
        for (int i = 0; i < n; i++) {
            double pred = (*w) * X[i] + (*b);
            dw += (pred - y[i]) * X[i];
            db += (pred - y[i]);
        }
        *w -= (lr * dw) / n;
        *b -= (lr * db) / n;
    }
}

/* Logistic Regression with Sigmoid & Cross Entropy */
static double ml_sigmoid(double z) {
    return 1.0 / (1.0 + exp(-z));
}

static void ml_logistic_regression(const double X[], const double y[], int n, double *w, double *b, double lr, int epochs) {
    *w = 0.0;
    *b = 0.0;
    for (int epoch = 0; epoch < epochs; epoch++) {
        double dw = 0.0;
        double db = 0.0;
        for (int i = 0; i < n; i++) {
            double z = (*w) * X[i] + (*b);
            double pred = ml_sigmoid(z);
            dw += (pred - y[i]) * X[i];
            db += (pred - y[i]);
        }
        *w -= (lr * dw) / n;
        *b -= (lr * db) / n;
    }
}

/* Decision Tree Classifier (ID3 / Gini Impurity) */
typedef struct DTNode {
    int feature_idx;
    double threshold;
    double leaf_val;
    struct DTNode *left, *right;
    bool is_leaf;
} DTNode;

static double dt_calculate_gini(const int classes[], int n) {
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
}

/* XOR MLP Neural Network with Backpropagation */
typedef struct {
    double w1[2][3]; // Weights input to hidden (2x3)
    double b1[3];    // Bias hidden
    double w2[3];    // Weights hidden to output (3)
    double b2;       // Bias output
} MLPNet;

static double mlp_sigmoid_deriv(double a) {
    return a * (1.0 - a);
}

static void mlp_train(MLPNet *net, const double X[4][2], const double y[4], int epochs, double lr) {
    for (int epoch = 0; epoch < epochs; epoch++) {
        for (int i = 0; i < 4; i++) {
            // Forward pass
            double h[3];
            for (int j = 0; j < 3; j++) {
                double z = X[i][0] * net->w1[0][j] + X[i][1] * net->w1[1][j] + net->b1[j];
                h[j] = ml_sigmoid(z);
            }
            double z_out = h[0] * net->w2[0] + h[1] * net->w2[1] + h[2] * net->w2[2] + net->b2;
            double out = ml_sigmoid(z_out);

            // Backprop
            double error_out = out - y[i];
            double delta_out = error_out * mlp_sigmoid_deriv(out);

            double delta_h[3];
            for (int j = 0; j < 3; j++) {
                delta_h[j] = delta_out * net->w2[j] * mlp_sigmoid_deriv(h[j]);
            }

            // Update output layer weights
            for (int j = 0; j < 3; j++) {
                net->w2[j] -= lr * delta_out * h[j];
            }
            net->b2 -= lr * delta_out;

            // Update hidden layer weights
            for (int j = 0; j < 3; j++) {
                net->w1[0][j] -= lr * delta_h[j] * X[i][0];
                net->w1[1][j] -= lr * delta_h[j] * X[i][1];
                net->b1[j] -= lr * delta_h[j];
            }
        }
    }
}

static double mlp_predict(const MLPNet *net, double x0, double x1) {
    double h[3];
    for (int j = 0; j < 3; j++) {
        double z = x0 * net->w1[0][j] + x1 * net->w1[1][j] + net->b1[j];
        h[j] = ml_sigmoid(z);
    }
    double z_out = h[0] * net->w2[0] + h[1] * net->w2[1] + h[2] * net->w2[2] + net->b2;
    return ml_sigmoid(z_out);
}

/* K-Nearest Neighbors (KNN) */
typedef struct {
    double x, y;
    int label;
} KNNPoint;

static int ml_knn_classify(const KNNPoint dataset[], int size, int k, double tx, double ty) {
    typedef struct {
        double dist;
        int label;
    } KNNDist;
    
    KNNDist *dists = (KNNDist*)malloc(size * sizeof(KNNDist));
    for (int i = 0; i < size; i++) {
        dists[i].dist = sqrt((dataset[i].x - tx) * (dataset[i].x - tx) + (dataset[i].y - ty) * (dataset[i].y - ty));
        dists[i].label = dataset[i].label;
    }
    
    // Sort ascending
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (dists[j].dist > dists[j+1].dist) {
                KNNDist tmp = dists[j];
                dists[j] = dists[j+1];
                dists[j+1] = tmp;
            }
        }
    }
    
    int c0 = 0, c1 = 0;
    for (int i = 0; i < k; i++) {
        if (dists[i].label == 0) c0++;
        else c1++;
    }
    free(dists);
    return (c1 > c0) ? 1 : 0;
}

/* Naive Bayes Classifier */
typedef struct {
    double mean_spam, mean_ham;
    double var_spam, var_ham;
    double prior_spam, prior_ham;
} NaiveBayes;

static double ml_nb_gaussian_prob(double x, double mean, double var) {
    return (1.0 / sqrt(2 * M_PI * var)) * exp(-((x - mean) * (x - mean)) / (2 * var));
}

static int ml_nb_predict(const NaiveBayes *nb, double x) {
    double p_spam = log(nb->prior_spam) + log(ml_nb_gaussian_prob(x, nb->mean_spam, nb->var_spam));
    double p_ham = log(nb->prior_ham) + log(ml_nb_gaussian_prob(x, nb->mean_ham, nb->var_ham));
    return (p_spam > p_ham) ? 1 : 0;
}

/* K-Means Clustering */
typedef struct {
    double x, y;
} Centroid;

static void ml_kmeans(const KNNPoint points[], int num_pts, Centroid centroids[], int k, int max_iter) {
    int *assignments = (int*)malloc(num_pts * sizeof(int));
    for (int iter = 0; iter < max_iter; iter++) {
        // Step 1: Assign clusters
        for (int i = 0; i < num_pts; i++) {
            double min_d = 1e9;
            int best_c = 0;
            for (int c = 0; c < k; c++) {
                double d = sqrt((points[i].x - centroids[c].x) * (points[i].x - centroids[c].x) +
                                (points[i].y - centroids[c].y) * (points[i].y - centroids[c].y));
                if (d < min_d) {
                    min_d = d;
                    best_c = c;
                }
            }
            assignments[i] = best_c;
        }
        
        // Step 2: Update centroids
        for (int c = 0; c < k; c++) {
            double sum_x = 0.0, sum_y = 0.0;
            int count = 0;
            for (int i = 0; i < num_pts; i++) {
                if (assignments[i] == c) {
                    sum_x += points[i].x;
                    sum_y += points[i].y;
                    count++;
                }
            }
            if (count > 0) {
                centroids[c].x = sum_x / count;
                centroids[c].y = sum_y / count;
            }
        }
    }
    free(assignments);
}

static void ml_scratch_demo(void) {
    print_sep("PHASE 8: STATS, ALGEBRA & MACHINE LEARNING MODELS FROM SCRATCH");

    /* Statistics */
    double data[] = {12.0, 15.0, 14.0, 10.0, 45.0, 13.0, 16.0, 18.0, 2.0};
    int n = 9;
    double mean = stats_mean(data, n);
    printf("  Stats: Mean=%.2f, Median=%.2f, StdDev=%.2f\n", mean, stats_median(data, n), stats_stddev(data, n, mean));
    stats_detect_outliers(data, n);

    /* Matrix Inversion */
    double M[9] = {1.0, 2.0, 3.0, 0.0, 1.0, 4.0, 5.0, 6.0, 0.0};
    double I[9];
    if (matrix_invert_3x3(M, I)) {
        printf("  3x3 Matrix Inverted Successfully.\n");
    }

    /* Linear Regression */
    double reg_x[] = {1, 2, 3, 4, 5};
    double reg_y[] = {2, 4, 5, 4, 5};
    double w, b;
    ml_linear_regression(reg_x, reg_y, 5, &w, &b, 0.01, 1000);
    printf("  Linear Regression: y = %.4f * x + %.4f\n", w, b);

    /* Decision Tree Impurity Split */
    int labels[] = {0, 0, 1, 1, 1, 0};
    printf("  Gini impurity split count (6 items): %.4f\n", dt_calculate_gini(labels, 6));
    DTNode *root = dt_build_tree_stub(1.0);
    dt_free(root);

    /* XOR MLP Training */
    double tx[4][2] = {{0,0}, {0,1}, {1,0}, {1,1}};
    double ty[4] = {0, 1, 1, 0};
    MLPNet net = {
        .w1 = {{0.15, 0.20, 0.25}, {0.25, 0.30, 0.35}},
        .b1 = {0.35, 0.35, 0.35},
        .w2 = {0.40, 0.45, 0.50},
        .b2 = 0.60
    };
    mlp_train(&net, tx, ty, 5000, 0.5);
    printf("  XOR MLP Neural Net output for (0,1): %.4f, for (1,1): %.4f\n", 
           mlp_predict(&net, 0.0, 1.0), mlp_predict(&net, 1.0, 1.0));

    /* KNN classifier */
    KNNPoint points[] = {{1.0, 1.0, 0}, {2.0, 2.0, 0}, {5.0, 5.0, 1}, {6.0, 6.0, 1}};
    int knn_class = ml_knn_classify(points, 4, 3, 3.0, 3.0);
    printf("  KNN Classify target (3,3): class = %d\n", knn_class);

    /* Naive Bayes prediction */
    NaiveBayes nb = { 2.0, 5.0, 0.5, 0.5, 0.5, 0.5 };
    printf("  Naive Bayes predict for 2.2: class = %d\n", ml_nb_predict(&nb, 2.2));

    /* KMeans Centroids */
    Centroid centroids[2] = {{1.5, 1.5}, {5.5, 5.5}};
    ml_kmeans(points, 4, centroids, 2, 10);
    printf("  KMeans update centroids: c0=(%.2f, %.2f), c1=(%.2f, %.2f)\n", 
           centroids[0].x, centroids[0].y, centroids[1].x, centroids[1].y);
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
    print("Chunk 4 appended successfully!")
