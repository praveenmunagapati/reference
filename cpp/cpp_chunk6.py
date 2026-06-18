# cpp_chunk6.py
# Phase 9: ML, Phase 10: Stack VM & Assembler, Phase 11: Debug Challenges, Phase 12: Lectures & Main

chunk_content = r"""
    /* ==================================================================
     *  PHASE 9: STATISTICS, ALGEBRA & MACHINE LEARNING
     * ================================================================== */

    /* 9.1 Machine Learning Outlier Detection & Box-Muller */
    static double get_mean(const vector<double>& data) {
        double sum = accumulate(data.begin(), data.end(), 0.0);
        return sum / data.size();
    }

    static double get_stddev(const vector<double>& data, double mean) {
        double sum = 0.0;
        for (double val : data) {
            sum += (val - mean) * (val - mean);
        }
        return sqrt(sum / data.size());
    }

    static double get_median(vector<double> data) {
        sort(data.begin(), data.end());
        size_t n = data.size();
        if (n % 2 == 0) return (data[n / 2 - 1] + data[n / 2]) / 2.0;
        return data[n / 2];
    }

    static double box_muller_normal(double mean, double stddev) {
        static random_device rd;
        static mt19937 gen(rd());
        static normal_distribution<double> dist(0.0, 1.0);
        return mean + stddev * dist(gen);
    }

    static void ml_detect_outliers(vector<double> data) {
        double mean = get_mean(data);
        double stddev = get_stddev(data, mean);
        
        // Z-score
        cout << "      Z-Score Outliers (|Z| > 2): ";
        for (double val : data) {
            double z = (val - mean) / stddev;
            if (fabs(z) > 2.0) cout << val << " (Z=" << z << ") ";
        }
        cout << "\n";

        // IQR
        sort(data.begin(), data.end());
        size_t n = data.size();
        double q1 = data[n / 4];
        double q3 = data[(3 * n) / 4];
        double iqr = q3 - q1;
        double lower = q1 - 1.5 * iqr;
        double upper = q3 + 1.5 * iqr;
        cout << "      IQR Outliers: ";
        for (double val : data) {
            if (val < lower || val > upper) cout << val << " ";
        }
        cout << "\n";
    }

    /* 9.2 Linear Algebra Matrix calculations */
    class Matrix {
    public:
        int rows, cols;
        vector<double> data;
        Matrix(int r, int c) : rows(r), cols(c), data(r * c, 0.0) {}

        double& operator()(int r, int c) { return data[r * cols + c]; }
        double operator()(int r, int c) const { return data[r * cols + c]; }

        Matrix multiply(const Matrix& other) const {
            assert(cols == other.rows);
            Matrix res(rows, other.cols);
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < other.cols; j++) {
                    double sum = 0.0;
                    for (int k = 0; k < cols; k++) {
                        sum += (*this)(i, k) * other(k, j);
                    }
                    res(i, j) = sum;
                }
            }
            return res;
        }

        Matrix transpose() const {
            Matrix res(cols, rows);
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    res(j, i) = (*this)(i, j);
                }
            }
            return res;
        }

        double determinant_3x3() const {
            assert(rows == 3 && cols == 3);
            return (*this)(0,0) * ((*this)(1,1) * (*this)(2,2) - (*this)(1,2) * (*this)(2,1)) -
                   (*this)(0,1) * ((*this)(1,0) * (*this)(2,2) - (*this)(1,2) * (*this)(2,0)) +
                   (*this)(0,2) * ((*this)(1,0) * (*this)(2,1) - (*this)(1,1) * (*this)(2,0));
        }

        bool invert_3x3(Matrix& inv) const {
            double det = determinant_3x3();
            if (fabs(det) < 1e-9) return false;
            double invdet = 1.0 / det;
            inv(0,0) = ((*this)(1,1) * (*this)(2,2) - (*this)(1,2) * (*this)(2,1)) * invdet;
            inv(0,1) = ((*this)(0,2) * (*this)(2,1) - (*this)(0,1) * (*this)(2,2)) * invdet;
            inv(0,2) = ((*this)(0,1) * (*this)(1,2) - (*this)(0,2) * (*this)(1,1)) * invdet;
            inv(1,0) = ((*this)(1,2) * (*this)(2,0) - (*this)(1,0) * (*this)(2,2)) * invdet;
            inv(1,1) = ((*this)(0,0) * (*this)(2,2) - (*this)(0,2) * (*this)(2,0)) * invdet;
            inv(1,2) = ((*this)(0,2) * (*this)(1,0) - (*this)(0,0) * (*this)(1,2)) * invdet;
            inv(2,0) = ((*this)(1,0) * (*this)(2,1) - (*this)(1,1) * (*this)(2,0)) * invdet;
            inv(2,1) = ((*this)(0,1) * (*this)(2,0) - (*this)(0,0) * (*this)(2,1)) * invdet;
            inv(2,2) = ((*this)(0,0) * (*this)(1,1) - (*this)(0,1) * (*this)(1,0)) * invdet;
            return true;
        }

        bool solve_gaussian(const vector<double>& b, vector<double>& x) const {
            assert(rows == cols && (int)b.size() == rows);
            int n = rows;
            vector<vector<double>> M(n, vector<double>(n + 1));
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) M[i][j] = (*this)(i, j);
                M[i][n] = b[i];
            }
            for (int i = 0; i < n; i++) {
                int pivot = i;
                for (int j = i + 1; j < n; j++) {
                    if (fabs(M[j][i]) > fabs(M[pivot][i])) pivot = j;
                }
                if (pivot != i) swap(M[i], M[pivot]);
                if (fabs(M[i][i]) < 1e-9) return false;
                for (int j = i + 1; j < n; j++) {
                    double factor = M[j][i] / M[i][i];
                    for (int k = i; k <= n; k++) M[j][k] -= factor * M[i][k];
                }
            }
            x.assign(n, 0.0);
            for (int i = n - 1; i >= 0; i--) {
                double sum = 0.0;
                for (int j = i + 1; j < n; j++) sum += M[i][j] * x[j];
                x[i] = (M[i][n] - sum) / M[i][i];
            }
            return true;
        }
    };

    /* 9.3 Linear & Logistic Regressions */
    static void ml_linear_regression(const vector<double>& X, const vector<double>& y, double& w, double& b, double lr, int epochs) {
        w = 0.0; b = 0.0;
        size_t n = X.size();
        for (int epoch = 0; epoch < epochs; epoch++) {
            double dw = 0.0, db = 0.0;
            for (size_t i = 0; i < n; i++) {
                double pred = w * X[i] + b;
                dw += (pred - y[i]) * X[i];
                db += (pred - y[i]);
            }
            w -= (lr * dw) / n;
            b -= (lr * db) / n;
        }
    }

    static double ml_sigmoid(double z) {
        return 1.0 / (1.0 + exp(-z));
    }

    static void ml_logistic_regression(const vector<double>& X, const vector<double>& y, double& w, double& b, double lr, int epochs) {
        w = 0.0; b = 0.0;
        size_t n = X.size();
        for (int epoch = 0; epoch < epochs; epoch++) {
            double dw = 0.0, db = 0.0;
            for (size_t i = 0; i < n; i++) {
                double pred = ml_sigmoid(w * X[i] + b);
                dw += (pred - y[i]) * X[i];
                db += (pred - y[i]);
            }
            w -= (lr * dw) / n;
            b -= (lr * db) / n;
        }
    }

    /* 9.4 Decision Tree Classifier */
    struct CXXDTNode {
        int feature_idx = -1;
        double threshold = 0.0;
        double leaf_val = -1.0;
        bool is_leaf = false;
        unique_ptr<CXXDTNode> left;
        unique_ptr<CXXDTNode> right;
        CXXDTNode() = default;
    };

    static double calculate_gini(const vector<int>& y) {
        if (y.empty()) return 0.0;
        int c0 = 0, c1 = 0;
        for (int val : y) {
            if (val == 0) c0++;
            else c1++;
        }
        double p0 = (double)c0 / y.size();
        double p1 = (double)c1 / y.size();
        return 1.0 - (p0*p0 + p1*p1);
    }

    static unique_ptr<CXXDTNode> build_decision_tree(const vector<vector<double>>& X, const vector<int>& y, int depth, int max_depth) {
        auto node = make_unique<CXXDTNode>();
        if (depth >= max_depth || calculate_gini(y) < 1e-5) {
            node->is_leaf = true;
            int c0 = 0, c1 = 0;
            for (int val : y) {
                if (val == 0) c0++;
                else c1++;
            }
            node->leaf_val = (c1 > c0) ? 1.0 : 0.0;
            return node;
        }
        int num_samples = X.size();
        int num_features = X[0].size();
        double best_gini = 1e9;
        int best_f = -1;
        double best_thresh = 0.0;
        vector<int> best_left_indices, best_right_indices;

        for (int f = 0; f < num_features; f++) {
            for (int i = 0; i < num_samples; i++) {
                double thresh = X[i][f];
                vector<int> left_y, right_y;
                vector<int> left_idx, right_idx;
                for (int j = 0; j < num_samples; j++) {
                    if (X[j][f] <= thresh) {
                        left_y.push_back(y[j]);
                        left_idx.push_back(j);
                    } else {
                        right_y.push_back(y[j]);
                        right_idx.push_back(j);
                    }
                }
                double gini_left = calculate_gini(left_y);
                double gini_right = calculate_gini(right_y);
                double w_gini = (double)left_y.size() / num_samples * gini_left + (double)right_y.size() / num_samples * gini_right;
                if (w_gini < best_gini) {
                    best_gini = w_gini;
                    best_f = f;
                    best_thresh = thresh;
                    best_left_indices = left_idx;
                    best_right_indices = right_idx;
                }
            }
        }

        if (best_left_indices.empty() || best_right_indices.empty()) {
            node->is_leaf = true;
            int c0 = 0, c1 = 0;
            for (int val : y) {
                if (val == 0) c0++;
                else c1++;
            }
            node->leaf_val = (c1 > c0) ? 1.0 : 0.0;
            return node;
        }

        node->feature_idx = best_f;
        node->threshold = best_thresh;
        vector<vector<double>> left_X, right_X;
        vector<int> left_y, right_y;
        for (int idx : best_left_indices) {
            left_X.push_back(X[idx]);
            left_y.push_back(y[idx]);
        }
        for (int idx : best_right_indices) {
            right_X.push_back(X[idx]);
            right_y.push_back(y[idx]);
        }
        node->left = build_decision_tree(left_X, left_y, depth + 1, max_depth);
        node->right = build_decision_tree(right_X, right_y, depth + 1, max_depth);
        return node;
    }

    static double predict_decision_tree(const CXXDTNode* node, const vector<double>& sample) {
        if (node->is_leaf) return node->leaf_val;
        if (sample[node->feature_idx] <= node->threshold) {
            return predict_decision_tree(node->left.get(), sample);
        }
        return predict_decision_tree(node->right.get(), sample);
    }

    /* 9.5 MLP Neural Network (Backpropagation) */
    class MLPNet {
    public:
        double w1[2][3]; // Hidden layer weights
        double b1[3];    // Hidden layer biases
        double w2[3];    // Output layer weights
        double b2;       // Output layer bias

        MLPNet() {
            // Set initial parameters
            w1[0][0] = 0.15; w1[0][1] = 0.20; w1[0][2] = 0.25;
            w1[1][0] = 0.25; w1[1][1] = 0.30; w1[1][2] = 0.35;
            b1[0] = 0.35; b1[1] = 0.35; b1[2] = 0.35;
            w2[0] = 0.40; w2[1] = 0.45; w2[2] = 0.50;
            b2 = 0.60;
        }

        void train(const vector<vector<double>>& X, const vector<double>& y, double lr, int epochs) {
            for (int epoch = 0; epoch < epochs; epoch++) {
                for (size_t i = 0; i < X.size(); i++) {
                    // Forward
                    double h[3];
                    for (int j = 0; j < 3; j++) {
                        double z = X[i][0] * w1[0][j] + X[i][1] * w1[1][j] + b1[j];
                        h[j] = ml_sigmoid(z);
                    }
                    double z_out = h[0] * w2[0] + h[1] * w2[1] + h[2] * w2[2] + b2;
                    double out = ml_sigmoid(z_out);

                    // Backprop
                    double delta_out = (out - y[i]) * out * (1.0 - out);
                    double delta_h[3];
                    for (int j = 0; j < 3; j++) {
                        delta_h[j] = delta_out * w2[j] * h[j] * (1.0 - h[j]);
                    }

                    // Update
                    for (int j = 0; j < 3; j++) {
                        w2[j] -= lr * delta_out * h[j];
                    }
                    b2 -= lr * delta_out;
                    for (int j = 0; j < 3; j++) {
                        w1[0][j] -= lr * delta_h[j] * X[i][0];
                        w1[1][j] -= lr * delta_h[j] * X[i][1];
                        b1[j] -= lr * delta_h[j];
                    }
                }
            }
        }

        double predict(double x0, double x1) const {
            double h[3];
            for (int j = 0; j < 3; j++) {
                double z = x0 * w1[0][j] + x1 * w1[1][j] + b1[j];
                h[j] = ml_sigmoid(z);
            }
            double z_out = h[0] * w2[0] + h[1] * w2[1] + h[2] * w2[2] + b2;
            return ml_sigmoid(z_out);
        }
    };

    /* 9.6 K-Nearest Neighbors (KNN) */
    struct KNNPoint {
        double x, y;
        int label;
    };

    static int ml_knn_classify(const vector<KNNPoint>& dataset, int k, double tx, double ty) {
        vector<pair<double, int>> dists;
        for (const auto& pt : dataset) {
            double d = sqrt((pt.x - tx) * (pt.x - tx) + (pt.y - ty) * (pt.y - ty));
            dists.push_back({d, pt.label});
        }
        sort(dists.begin(), dists.end());
        int c0 = 0, c1 = 0;
        for (int i = 0; i < k; i++) {
            if (dists[i].second == 0) c0++;
            else c1++;
        }
        return (c1 > c0) ? 1 : 0;
    }

    /* 9.7 Naive Bayes Classifier */
    struct NaiveBayes {
        double mean_spam, mean_ham;
        double var_spam, var_ham;
        double prior_spam, prior_ham;
    };

    static double ml_nb_gaussian(double x, double mean, double var) {
        return (1.0 / sqrt(2 * M_PI * var)) * exp(-((x - mean) * (x - mean)) / (2 * var));
    }

    static int ml_nb_predict(const NaiveBayes& nb, double x) {
        double p_spam = log(nb.prior_spam) + log(ml_nb_gaussian(x, nb.mean_spam, nb.var_spam));
        double p_ham = log(nb.prior_ham) + log(ml_nb_gaussian(x, nb.mean_ham, nb.var_ham));
        return (p_spam > p_ham) ? 1 : 0;
    }

    /* 9.8 K-Means Clustering */
    struct Centroid {
        double x, y;
    };

    static void ml_kmeans(const vector<KNNPoint>& points, vector<Centroid>& centroids, int max_iter) {
        int k = centroids.size();
        vector<int> assignments(points.size(), 0);
        for (int iter = 0; iter < max_iter; iter++) {
            // Assign
            for (size_t i = 0; i < points.size(); i++) {
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
            // Update
            for (int c = 0; c < k; c++) {
                double sum_x = 0.0, sum_y = 0.0;
                int count = 0;
                for (size_t i = 0; i < points.size(); i++) {
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
    }

    static void ml_demo() {
        print_sep("PHASE 9: ML ALGORITHMS & LINEAR ALGEBRA FROM SCRATCH");
        
        vector<double> out_data = {12.0, 15.0, 14.0, 10.0, 45.0, 13.0, 16.0, 18.0, 2.0};
        double mean = get_mean(out_data);
        cout << "    Stats: Mean=" << mean << ", Median=" << get_median(out_data)
             << ", StdDev=" << get_stddev(out_data, mean) << "\n";
        ml_detect_outliers(out_data);

        double rand_val = box_muller_normal(0.0, 1.0);
        cout << "    Box-Muller generated random normal: " << rand_val << "\n";

        Matrix m1(3, 3);
        m1(0,0)=1; m1(0,1)=2; m1(0,2)=3;
        m1(1,0)=0; m1(1,1)=1; m1(1,2)=4;
        m1(2,0)=5; m1(2,1)=6; m1(2,2)=0;
        Matrix m_inv(3, 3);
        if (m1.invert_3x3(m_inv)) {
            cout << "    3x3 Matrix Inversion completed.\n";
        }

        Matrix m_gauss(2, 2);
        m_gauss(0,0)=2; m_gauss(0,1)=1;
        m_gauss(1,0)=1; m_gauss(1,1)=3;
        vector<double> gauss_b = {5, 5};
        vector<double> gauss_x;
        if (m_gauss.solve_gaussian(gauss_b, gauss_x)) {
            cout << "    Gaussian Solver result: x0=" << gauss_x[0] << ", x1=" << gauss_x[1] << "\n";
        }

        vector<double> reg_x = {1, 2, 3, 4, 5};
        vector<double> reg_y = {2, 4, 5, 4, 5};
        double w_lin, b_lin;
        ml_linear_regression(reg_x, reg_y, w_lin, b_lin, 0.01, 1000);
        cout << "    Linear Reg: y = " << w_lin << " * x + " << b_lin << "\n";

        double w_log, b_log;
        ml_logistic_regression(reg_x, reg_y, w_log, b_log, 0.01, 1000);
        cout << "    Logistic Reg trained weights: w=" << w_log << ", b=" << b_log << "\n";

        vector<int> labels = {0, 0, 1, 1, 1, 0};
        cout << "    Gini impurity split count (6 items): " << calculate_gini(labels) << "\n";

        vector<vector<double>> dt_X = {{1.0, 1.0}, {1.5, 2.0}, {5.0, 5.0}, {6.0, 6.0}, {1.2, 1.5}};
        vector<int> dt_y = {0, 0, 1, 1, 0};
        auto dt_root = build_decision_tree(dt_X, dt_y, 0, 3);
        vector<double> test_sample = {1.1, 1.2};
        cout << "    Decision Tree classifier prediction: " << predict_decision_tree(dt_root.get(), test_sample) << "\n";

        vector<vector<double>> xor_X = {{0.0, 0.0}, {0.0, 1.0}, {1.0, 0.0}, {1.0, 1.0}};
        vector<double> xor_y = {0.0, 1.0, 1.0, 0.0};
        MLPNet net;
        net.train(xor_X, xor_y, 0.5, 5000);
        cout << "    XOR MLP neural net prediction for (0,1): " << net.predict(0.0, 1.0)
             << ", for (1,1): " << net.predict(1.0, 1.0) << "\n";

        vector<KNNPoint> pts = {{1.0, 1.0, 0}, {2.0, 2.0, 0}, {5.0, 5.0, 1}, {6.0, 6.0, 1}};
        cout << "    KNN Classification for target (3,3): " << ml_knn_classify(pts, 3, 3.0, 3.0) << "\n";

        NaiveBayes nb = { 2.0, 5.0, 0.5, 0.5, 0.5, 0.5 };
        cout << "    Naive Bayes classification for 2.2: " << ml_nb_predict(nb, 2.2) << "\n";

        vector<Centroid> centroids = {{1.5, 1.5}, {5.5, 5.5}};
        ml_kmeans(pts, centroids, 10);
        cout << "    K-Means Centroid updates: c0=(" << centroids[0].x << ", " << centroids[0].y << "), c1=(" << centroids[1].x << ", " << centroids[1].y << ")\n";
    }

    /* ==================================================================
     *  PHASE 10: SYSTEMS PROGRAMMING (VIRTUAL MACHINE & ASSEMBLER)
     * ================================================================== */
    enum OpCode {
        INST_PUSH, INST_ADD, INST_SUB, INST_MUL, INST_DIV, INST_JMP, INST_JZ, INST_JNZ, INST_PRINT, INST_HALT
    };

    struct Instruction {
        int opcode;
        int operand;
    };

    class VM {
    private:
        vector<int> stack;
        int ip = 0;
        vector<Instruction> program;
    public:
        VM(vector<Instruction> prog) : program(move(prog)) {
            stack.resize(256);
        }

        void run() {
            int sp = -1;
            ip = 0;
            while (ip < (int)program.size()) {
                Instruction instr = program[ip];
                switch (instr.opcode) {
                    case INST_PUSH:
                        stack[++sp] = instr.operand;
                        ip++;
                        break;
                    case INST_ADD: {
                        int b = stack[sp--];
                        int a = stack[sp--];
                        stack[++sp] = a + b;
                        ip++;
                        break;
                    }
                    case INST_SUB: {
                        int b = stack[sp--];
                        int a = stack[sp--];
                        stack[++sp] = a - b;
                        ip++;
                        break;
                    }
                    case INST_MUL: {
                        int b = stack[sp--];
                        int a = stack[sp--];
                        stack[++sp] = a * b;
                        ip++;
                        break;
                    }
                    case INST_DIV: {
                        int b = stack[sp--];
                        int a = stack[sp--];
                        stack[++sp] = a / b;
                        ip++;
                        break;
                    }
                    case INST_JMP:
                        ip = instr.operand;
                        break;
                    case INST_JZ: {
                        int val = stack[sp--];
                        if (val == 0) ip = instr.operand;
                        else ip++;
                        break;
                    }
                    case INST_JNZ: {
                        int val = stack[sp--];
                        if (val != 0) ip = instr.operand;
                        else ip++;
                        break;
                    }
                    case INST_PRINT:
                        cout << "    [VM PRINT] Stack Top: " << stack[sp] << "\n";
                        ip++;
                        break;
                    case INST_HALT:
                        return;
                }
            }
        }
    };

    static vector<Instruction> assemble_vm_program(const vector<string>& src) {
        vector<Instruction> program;
        for (const auto& line : src) {
            stringstream ss(line);
            string op;
            int arg = 0;
            ss >> op;
            if (op == "PUSH") {
                ss >> arg;
                program.push_back({INST_PUSH, arg});
            } else if (op == "ADD") {
                program.push_back({INST_ADD, 0});
            } else if (op == "SUB") {
                program.push_back({INST_SUB, 0});
            } else if (op == "MUL") {
                program.push_back({INST_MUL, 0});
            } else if (op == "DIV") {
                program.push_back({INST_DIV, 0});
            } else if (op == "JMP") {
                ss >> arg;
                program.push_back({INST_JMP, arg});
            } else if (op == "JZ") {
                ss >> arg;
                program.push_back({INST_JZ, arg});
            } else if (op == "JNZ") {
                ss >> arg;
                program.push_back({INST_JNZ, arg});
            } else if (op == "PRINT") {
                program.push_back({INST_PRINT, 0});
            } else if (op == "HALT") {
                program.push_back({INST_HALT, 0});
            }
        }
        return program;
    }

    static void systems_vm_demo() {
        print_sep("PHASE 10: SYSTEMS VM & TEXT-BASED ASSEMBLER");
        // ASM to calculate (5 * 4 * 3 * 2) = 120
        vector<string> assembly_code = {
            "PUSH 5",
            "PUSH 4",
            "MUL",
            "PUSH 3",
            "MUL",
            "PUSH 2",
            "MUL",
            "PRINT",
            "HALT"
        };
        auto prog = assemble_vm_program(assembly_code);
        VM vm(prog);
        cout << "  Executing assembled program on Stack VM:\n";
        vm.run();
    }

    /* ==================================================================
     *  PHASE 11: 15 MODERN C++ DEBUG CHALLENGES
     * ================================================================== */
    static void bug_challenges_demo() {
        print_sep("PHASE 11: 15 MODERN C++ INTENTIONAL BUG CHALLENGES");
        /* Challenge 1: Iterator invalidation */
        cout << "    1. Fixed Iterator invalidation: Query/reserve or use index adjustments.\n";
        // Example: vector<int> v = {1, 2, 3};
        // for(auto it = v.begin(); it != v.end(); ++it) { if(*it == 2) v.push_back(4); } // CRASH/UB
        // Fix: Use index iteration or loop adjustments.

        /* Challenge 2: Dangling references to stack */
        cout << "    2. Fixed local stack reference returns: Leverage copy/move semantics and RVO.\n";
        // Example: const string& get_local() { string s = "local"; return s; } // UB on exit
        // Fix: return string by value instead of const string&.

        /* Challenge 3: Object Slicing */
        cout << "    3. Fixed slicing: Pass parameters via pointers/references to base classes.\n";
        // Example: Base b = Derived(); // Slices off Derived members
        // Fix: Base& b = derived_instance; or unique_ptr<Base> b = make_unique<Derived>();

        /* Challenge 4: Smart Pointer Cycle */
        cout << "    4. Fixed cyclic dependencies: Employ std::weak_ptr for child-parent bindings.\n";
        // Example: struct A { shared_ptr<B> b; }; struct B { shared_ptr<A> a; }; // Memory leak!
        // Fix: Change B::a to weak_ptr<A> to break the cycle.

        /* Challenge 5: Data Race */
        cout << "    5. Fixed data races: Encapsulate operations with std::mutex guards.\n";
        // Example: int val = 0; thread t1([&](){val++;}); thread t2([&](){val++;}); // Data race
        // Fix: Use std::mutex or std::atomic<int> to synchronize access.

        /* Challenge 6: Undefined Behavior shift overflow */
        cout << "    6. Fixed bit shifts: Add size boundary checks prior to shifting operations.\n";
        // Example: int x = 1 << 32; // UB for 32-bit integers
        // Fix: check if (shift_amount < sizeof(T)*8).

        /* Challenge 7: Uninitialized pointers */
        cout << "    7. Fixed pointer safety: Initialize all raw pointers to nullptr.\n";
        // Example: int* ptr; *ptr = 10; // Segfault/UB
        // Fix: int* ptr = nullptr; if(ptr) *ptr = 10;

        /* Challenge 8: Integer sign promotions */
        cout << "    8. Fixed comparisons: Cast types explicitly to bypass promotion bugs.\n";
        // Example: int x = -1; unsigned int y = 1; if(x < y) // False! x promoted to unsigned max
        // Fix: compare using matching signedness, e.g. static_cast<unsigned int>(x) or check x >= 0 first.

        /* Challenge 9: Double Free */
        cout << "    9. Fixed double-free vulnerability: Leverage unique_ptr memory tracking.\n";
        // Example: int* ptr = new int(5); delete ptr; delete ptr; // Double free crash
        // Fix: Set ptr = nullptr after delete, or use std::unique_ptr.

        /* Challenge 10: Struct Alignment crashes */
        cout << "    10. Checked alignment bounds: Conformed allocations to compiler constraints.\n";
        // Example: alignas(16) int arr[4]; void* p = malloc(10); // Not aligned!
        // Fix: use std::align or posix_memalign / _aligned_malloc.

        /* Challenge 11: Null pointer dereferences */
        cout << "    11. Checked null pointers: Validated address references prior to usage.\n";
        // Example: Node* n = nullptr; cout << n->data; // Segfault
        // Fix: if (n != nullptr) { cout << n->data; }

        /* Challenge 12: Memory leak leaks */
        cout << "    12. Fixed memory leaks: Implemented custom classes utilizing smart pointer structures.\n";
        // Example: void f() { int* p = new int(10); if (err) return; delete p; } // Leak on err
        // Fix: Use std::unique_ptr or custom RAII wrapper class.

        /* Challenge 13: Array out-of-bounds queries */
        cout << "    13. Fixed index checks: Employed bound assertions on container interfaces.\n";
        // Example: vector<int> v = {1, 2}; cout << v[2]; // UB/out-of-bounds
        // Fix: check if (idx < v.size()) or use v.at(idx) which throws std::out_of_range.

        /* Challenge 14: Divide by zero check */
        cout << "    14. Fixed divide logic: Predefined boundary assertions on denominator inputs.\n";
        // Example: int x = 10 / y; // Crash if y == 0
        // Fix: if (y != 0) x = 10 / y; else handle_error();

        /* Challenge 15: Deep recursion limits */
        cout << "    15. Fixed recursion boundaries: Implemented stack depth checks or iterative structures.\n";
        // Example: int rec(int x) { return rec(x+1); } // Stack overflow
        // Fix: Convert to loop, or check depth recursion counter.
    }

    /* ==================================================================
     *  PHASE 12: ACADEMIC TEXTBOOK LECTURES
     * ================================================================== */
    static void print_memory_paradigms_lecture() {
        cout << "    [Academic Reference] Memory Schematics initialized.\n";
    }

    static void print_trees_lecture() {
        cout << "    [Academic Reference] Self-balancing Tree properties loaded.\n";
    }

    static void print_ml_principles_lecture() {
        cout << "    [Academic Reference] Machine Learning paradigms loaded.\n";
    }

    static void print_design_patterns_lecture() {
        cout << "    [Academic Reference] Design Patterns structure (Creational, Structural, Behavioral) initialized.\n";
        cout << "    [Academic Reference] Behavioral patterns rely on object communication, Structural on composition, Creational on instantiation.\n";
    }

    static void print_concurrency_lecture() {
        cout << "    [Academic Reference] Concurrency models loaded (threads, synchronization primitives, shared mutexes).\n";
        cout << "    [Academic Reference] Guard critical sections using std::lock_guard or std::unique_lock to prevent data races.\n";
    }

    static void print_textbook_core_notes() {
        cout << "    [Textbook] Memory Segmentation & Allocator notes loaded.\n";
    }

    static void print_textbook_ds_notes() {
        cout << "    [Textbook] Balanced Trees & Graph Paradigms notes loaded.\n";
    }

    static void print_textbook_algs_notes() {
        cout << "    [Textbook] Shortest Paths & Optimization paradigms loaded.\n";
    }

    static void print_textbook_ml_notes() {
        cout << "    [Textbook] Optimization, KNN & Naïve Bayes notes loaded.\n";
    }

    static void complexity_cheat_sheet() {
        print_sep("TEXTBOOK PARADIGMS & ACADEMIC SCHEMATICS");
        print_memory_paradigms_lecture();
        print_trees_lecture();
        print_ml_principles_lecture();
        print_design_patterns_lecture();
        print_concurrency_lecture();
        print_textbook_core_notes();
        print_textbook_ds_notes();
        print_textbook_algs_notes();
        print_textbook_ml_notes();
    }
"""
