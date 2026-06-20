# java_chunk5.py
# Phase 8: Statistical & Machine Learning Algorithms
# Phase 9: Systems Programming (Stack VM & Assembler)
# Phase 10: 15 Java Debug Challenges
# Phase 11: Academic Textbook Lectures & Big-O

chunk_content = r"""
        // ====================================================================
        // 8.1  Matrix Operations from Scratch
        // ====================================================================

        static class Matrix {
            private final double[][] data;
            private final int rows, cols;

            Matrix(int r, int c) {
                this.rows = r; this.cols = c;
                this.data = new double[r][c];
            }

            static Matrix multiply(Matrix A, Matrix B) {
                if (A.cols != B.rows) throw new IllegalArgumentException("Incompatible dimensions.");
                Matrix C = new Matrix(A.rows, B.cols);
                for (int i = 0; i < A.rows; i++) {
                    for (int j = 0; j < B.cols; j++) {
                        double sum = 0.0;
                        for (int k = 0; k < A.cols; k++) {
                            sum += A.data[i][k] * B.data[k][j];
                        }
                        C.data[i][j] = sum;
                    }
                }
                return C;
            }

            Matrix transpose() {
                Matrix T = new Matrix(cols, rows);
                for (int i = 0; i < rows; i++) {
                    for (int j = 0; j < cols; j++) {
                        T.data[j][i] = data[i][j];
                    }
                }
                return T;
            }

            static Matrix identity(int n) {
                Matrix I = new Matrix(n, n);
                for (int i = 0; i < n; i++) I.data[i][i] = 1.0;
                return I;
            }

            boolean invert3x3(Matrix inv) {
                if (rows != 3 || cols != 3 || inv.rows != 3 || inv.cols != 3) return false;
                double det = determinant3x3();
                if (Math.abs(det) < 1e-9) return false;

                double invDet = 1.0 / det;
                inv.data[0][0] = (data[1][1] * data[2][2] - data[1][2] * data[2][1]) * invDet;
                inv.data[0][1] = (data[0][2] * data[2][1] - data[0][1] * data[2][2]) * invDet;
                inv.data[0][2] = (data[0][1] * data[1][2] - data[0][2] * data[1][1]) * invDet;
                inv.data[1][0] = (data[1][2] * data[2][0] - data[1][0] * data[2][2]) * invDet;
                inv.data[1][1] = (data[0][0] * data[2][2] - data[0][2] * data[2][0]) * invDet;
                inv.data[1][2] = (data[0][2] * data[1][0] - data[0][0] * data[1][2]) * invDet;
                inv.data[2][0] = (data[1][0] * data[2][1] - data[1][1] * data[2][0]) * invDet;
                inv.data[2][1] = (data[0][1] * data[2][0] - data[0][0] * data[2][1]) * invDet;
                inv.data[2][2] = (data[0][0] * data[1][1] - data[0][1] * data[1][0]) * invDet;
                return true;
            }

            double determinant3x3() {
                if (rows != 3 || cols != 3) return 0.0;
                return data[0][0] * (data[1][1] * data[2][2] - data[1][2] * data[2][1]) -
                       data[0][1] * (data[1][0] * data[2][2] - data[1][2] * data[2][0]) +
                       data[0][2] * (data[1][0] * data[2][1] - data[1][1] * data[2][0]);
            }

            boolean solveGaussian(double[] b, double[] x) {
                if (rows != cols || b.length != rows || x.length != rows) return false;
                int n = rows;
                double[][] A = new double[n][n + 1];
                for (int i = 0; i < n; i++) {
                    System.arraycopy(data[i], 0, A[i], 0, n);
                    A[i][n] = b[i];
                }

                for (int i = 0; i < n; i++) {
                    int pivot = i;
                    for (int row = i + 1; row < n; row++) {
                        if (Math.abs(A[row][i]) > Math.abs(A[pivot][i])) pivot = row;
                    }
                    double[] temp = A[i]; A[i] = A[pivot]; A[pivot] = temp;

                    if (Math.abs(A[i][i]) < 1e-9) return false;

                    for (int row = i + 1; row < n; row++) {
                        double factor = A[row][i] / A[i][i];
                        for (int col = i; col <= n; col++) {
                            A[row][col] -= factor * A[i][col];
                        }
                    }
                }

                for (int i = n - 1; i >= 0; i--) {
                    double sum = 0.0;
                    for (int j = i + 1; j < n; j++) {
                        sum += A[i][j] * x[j];
                    }
                    x[i] = (A[i][n] - sum) / A[i][i];
                }
                return true;
            }

            void print() {
                for (int i = 0; i < rows; i++) {
                    for (int j = 0; j < cols; j++) {
                        System.out.printf("  %8.4f ", data[i][j]);
                    }
                    System.out.println();
                }
            }
        }

        static class VectorUtils {
            static double dotProduct(double[] a, double[] b) {
                if (a.length != b.length) throw new IllegalArgumentException("Vector length mismatch.");
                double dot = 0.0;
                for (int i = 0; i < a.length; i++) dot += a[i] * b[i];
                return dot;
            }

            static double l2Norm(double[] a) {
                double sum = 0.0;
                for (double val : a) sum += val * val;
                return Math.sqrt(sum);
            }

            static double cosineSimilarity(double[] a, double[] b) {
                double normA = l2Norm(a);
                double normB = l2Norm(b);
                if (normA == 0.0 || normB == 0.0) return 0.0;
                return dotProduct(a, b) / (normA * normB);
            }

            static double[] add(double[] a, double[] b) {
                if (a.length != b.length) throw new IllegalArgumentException("Vector length mismatch.");
                double[] res = new double[a.length];
                for (int i = 0; i < a.length; i++) res[i] = a[i] + b[i];
                return res;
            }

            static double[] subtract(double[] a, double[] b) {
                if (a.length != b.length) throw new IllegalArgumentException("Vector length mismatch.");
                double[] res = new double[a.length];
                for (int i = 0; i < a.length; i++) res[i] = a[i] - b[i];
                return res;
            }
        }

        // ====================================================================
        // 8.2  Machine Learning Algorithms
        // ====================================================================

        // --- 1. Linear & Logistic Regression ---
        static class RegressionModels {
            static void linearRegression(double[] x, double[] y, double[] params, double lr, int epochs) {
                double w = 0.0, b = 0.0;
                int n = x.length;
                for (int e = 0; e < epochs; e++) {
                    double dw = 0.0, db = 0.0;
                    for (int i = 0; i < n; i++) {
                        double error = (w * x[i] + b) - y[i];
                        dw += error * x[i];
                        db += error;
                    }
                    w -= lr * (dw / n);
                    b -= lr * (db / n);
                }
                params[0] = w; params[1] = b;
            }

            static void logisticRegression(double[] x, double[] y, double[] params, double lr, int epochs) {
                double w = 0.0, b = 0.0;
                int n = x.length;
                for (int e = 0; e < epochs; e++) {
                    double dw = 0.0, db = 0.0;
                    for (int i = 0; i < n; i++) {
                        double z = w * x[i] + b;
                        double prediction = 1.0 / (1.0 + Math.exp(-z));
                        double error = prediction - y[i];
                        dw += error * x[i];
                        db += error;
                    }
                    w -= lr * (dw / n);
                    b -= lr * (db / n);
                }
                params[0] = w; params[1] = b;
            }
        }

        // --- 2. Decision Tree Classifier ---
        static class DecisionTree {
            static class Node {
                int featureIndex = -1;
                double threshold;
                Node left, right;
                int value = -1;
                boolean isLeaf;
            }

            private Node root;

            void train(double[][] X, int[] y, int maxDepth) {
                root = buildTree(X, y, 0, maxDepth);
            }

            private Node buildTree(double[][] X, int[] y, int depth, int maxDepth) {
                Node node = new Node();
                int numSamples = X.length;
                if (numSamples == 0) return node;

                boolean sameLabel = true;
                for (int label : y) {
                    if (label != y[0]) { sameLabel = false; break; }
                }

                if (sameLabel || depth >= maxDepth || numSamples < 2) {
                    node.isLeaf = true;
                    node.value = majorityVote(y);
                    return node;
                }

                int numFeatures = X[0].length;
                int bestFeature = -1;
                double bestThreshold = 0.0;
                double bestGini = 1.0;

                for (int f = 0; f < numFeatures; f++) {
                    for (int i = 0; i < numSamples; i++) {
                        double threshold = X[i][f];
                        double gini = calculateSplitGini(X, y, f, threshold);
                        if (gini < bestGini) {
                            bestGini = gini;
                            bestFeature = f;
                            bestThreshold = threshold;
                        }
                    }
                }

                if (bestGini >= calculateGini(y)) {
                    node.isLeaf = true;
                    node.value = majorityVote(y);
                    return node;
                }

                node.featureIndex = bestFeature;
                node.threshold = bestThreshold;

                List<double[]> leftX = new ArrayList<>();
                List<Integer> leftY = new ArrayList<>();
                List<double[]> rightX = new ArrayList<>();
                List<Integer> rightY = new ArrayList<>();

                for (int i = 0; i < numSamples; i++) {
                    if (X[i][bestFeature] < bestThreshold) {
                        leftX.add(X[i]); leftY.add(y[i]);
                    } else {
                        rightX.add(X[i]); rightY.add(y[i]);
                    }
                }

                node.left = buildTree(leftX.toArray(new double[0][]), leftY.stream().mapToInt(Integer::intValue).toArray(), depth + 1, maxDepth);
                node.right = buildTree(rightX.toArray(new double[0][]), rightY.stream().mapToInt(Integer::intValue).toArray(), depth + 1, maxDepth);
                return node;
            }

            private double calculateGini(int[] y) {
                int n = y.length;
                if (n == 0) return 0.0;
                int c0 = 0, c1 = 0;
                for (int label : y) {
                    if (label == 0) c0++; else c1++;
                }
                double p0 = (double) c0 / n;
                double p1 = (double) c1 / n;
                return 1.0 - (p0 * p0 + p1 * p1);
            }

            private double calculateSplitGini(double[][] X, int[] y, int col, double threshold) {
                int leftCount = 0, rightCount = 0;
                List<Integer> leftY = new ArrayList<>();
                List<Integer> rightY = new ArrayList<>();
                for (int i = 0; i < X.length; i++) {
                    if (X[i][col] < threshold) {
                        leftCount++; leftY.add(y[i]);
                    } else {
                        rightCount++; rightY.add(y[i]);
                    }
                }
                int n = X.length;
                double gLeft = calculateGini(leftY.stream().mapToInt(Integer::intValue).toArray());
                double gRight = calculateGini(rightY.stream().mapToInt(Integer::intValue).toArray());
                return ((double) leftCount / n) * gLeft + ((double) rightCount / n) * gRight;
            }

            private int majorityVote(int[] y) {
                int c0 = 0, c1 = 0;
                for (int val : y) {
                    if (val == 0) c0++; else c1++;
                }
                return c1 > c0 ? 1 : 0;
            }

            int predict(double[] sample) {
                Node curr = root;
                while (!curr.isLeaf) {
                    if (sample[curr.featureIndex] < curr.threshold) {
                        curr = curr.left;
                    } else {
                        curr = curr.right;
                    }
                }
                return curr.value;
            }
        }

        // --- 3. Neural Network MLP (XOR Gate) ---
        static class MLP {
            private final double[][] w1 = new double[2][3]; // Hidden weights
            private final double[] b1 = new double[3];    // Hidden bias
            private final double[] w2 = new double[3];      // Output weights
            private double b2;                            // Output bias

            MLP() {
                w1[0][0] = 0.15; w1[0][1] = 0.20; w1[0][2] = 0.25;
                w1[1][0] = 0.25; w1[1][1] = 0.30; w1[1][2] = 0.35;
                b1[0] = 0.35; b1[1] = 0.35; b1[2] = 0.35;
                w2[0] = 0.40; w2[1] = 0.45; w2[2] = 0.50;
                b2 = 0.60;
            }

            private double sigmoid(double x) { return 1.0 / (1.0 + Math.exp(-x)); }

            void train(double[][] X, double[] y, double lr, int epochs) {
                for (int epoch = 0; epoch < epochs; epoch++) {
                    for (int i = 0; i < X.length; i++) {
                        // Forward
                        double[] h = new double[3];
                        for (int j = 0; j < 3; j++) {
                            double z = X[i][0] * w1[0][j] + X[i][1] * w1[1][j] + b1[j];
                            h[j] = sigmoid(z);
                        }
                        double z_out = h[0] * w2[0] + h[1] * w2[1] + h[2] * w2[2] + b2;
                        double out = sigmoid(z_out);

                        // Backprop
                        double delta_out = (out - y[i]) * out * (1.0 - out);
                        double[] delta_h = new double[3];
                        for (int j = 0; j < 3; j++) {
                            delta_h[j] = delta_out * w2[j] * h[j] * (1.0 - h[j]);
                        }

                        // Update weights
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

            double predict(double x0, double x1) {
                double[] h = new double[3];
                for (int j = 0; j < 3; j++) {
                    double z = x0 * w1[0][j] + x1 * w1[1][j] + b1[j];
                    h[j] = sigmoid(z);
                }
                double z_out = h[0] * w2[0] + h[1] * w2[1] + h[2] * w2[2] + b2;
                return sigmoid(z_out);
            }
        }

        // --- 4. KNN Classifier ---
        static class KNNPoint {
            double[] coords;
            int label;
            KNNPoint(double[] pt, int lbl) { coords = pt; label = lbl; }
        }
        static class KNN {
            static int classify(List<KNNPoint> dataset, double[] target, int k) {
                List<Map.Entry<Double, Integer>> distances = new ArrayList<>();
                for (var pt : dataset) {
                    double d = 0.0;
                    for (int i = 0; i < target.length; i++) {
                        d += (pt.coords[i] - target[i]) * (pt.coords[i] - target[i]);
                    }
                    distances.add(new AbstractMap.SimpleEntry<>(Math.sqrt(d), pt.label));
                }
                distances.sort(Comparator.comparingDouble(Map.Entry::getKey));
                int c0 = 0, c1 = 0;
                for (int i = 0; i < k; i++) {
                    if (distances.get(i).getValue() == 0) c0++; else c1++;
                }
                return c1 > c0 ? 1 : 0;
            }
        }

        // --- 5. Naive Bayes Classifier ---
        static class NaiveBayes {
            private double meanSpam, meanHam;
            private double varSpam, varHam;
            private double priorSpam, priorHam;

            void train(double[] features, int[] labels) {
                List<Double> spam = new ArrayList<>();
                List<Double> ham = new ArrayList<>();
                for (int i = 0; i < features.length; i++) {
                    if (labels[i] == 1) spam.add(features[i]);
                    else ham.add(features[i]);
                }
                priorSpam = (double) spam.size() / features.length;
                priorHam = (double) ham.size() / features.length;

                meanSpam = spam.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
                meanHam = ham.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);

                varSpam = spam.stream().mapToDouble(x -> (x - meanSpam) * (x - meanSpam)).average().orElse(0.1);
                varHam = ham.stream().mapToDouble(x -> (x - meanHam) * (x - meanHam)).average().orElse(0.1);
            }

            private double getGaussianProbability(double x, double mean, double var) {
                return (1.0 / Math.sqrt(2 * Math.PI * var)) * Math.exp(-((x - mean) * (x - mean)) / (2 * var));
            }

            int predict(double feature) {
                double pSpam = Math.log(priorSpam) + Math.log(getGaussianProbability(feature, meanSpam, varSpam));
                double pHam = Math.log(priorHam) + Math.log(getGaussianProbability(feature, meanHam, varHam));
                return pSpam > pHam ? 1 : 0;
            }
        }

        // --- 6. KMeans Clustering ---
        static class KMeans {
            static class Centroid { double x, y; Centroid(double x, double y) { this.x = x; this.y = y; } }
            static class Point { double x, y; int cluster; Point(double x, double y) { this.x = x; this.y = y; } }

            static void cluster(List<Point> points, List<Centroid> centroids, int maxIter) {
                int k = centroids.size();
                for (int iter = 0; iter < maxIter; iter++) {
                    // Assign
                    for (Point p : points) {
                        double minDist = Double.MAX_VALUE;
                        int bestCluster = 0;
                        for (int c = 0; c < k; c++) {
                            double d = Math.sqrt((p.x - centroids.get(c).x)*(p.x - centroids.get(c).x) +
                                                 (p.y - centroids.get(c).y)*(p.y - centroids.get(c).y));
                            if (d < minDist) { minDist = d; bestCluster = c; }
                        }
                        p.cluster = bestCluster;
                    }
                    // Update
                    for (int c = 0; c < k; c++) {
                        double sumX = 0, sumY = 0;
                        int count = 0;
                        for (Point p : points) {
                            if (p.cluster == c) { sumX += p.x; sumY += p.y; count++; }
                        }
                        if (count > 0) {
                            centroids.set(c, new Centroid(sumX / count, sumY / count));
                        }
                    }
                }
            }
        }

        static void mlDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("8.  MACHINE LEARNING ALGORITHMS DEMO");
            System.out.println("=".repeat(60));

            // Matrix Operations
            Matrix m1 = new Matrix(3, 3);
            m1.data[0][0] = 1; m1.data[0][1] = 2; m1.data[0][2] = 3;
            m1.data[1][0] = 0; m1.data[1][1] = 1; m1.data[1][2] = 4;
            m1.data[2][0] = 5; m1.data[2][1] = 6; m1.data[2][2] = 0;
            Matrix inv = new Matrix(3, 3);
            if (m1.invert3x3(inv)) {
                System.out.println("  Matrix Inverted successfully: ");
                inv.print();
            }

            double[] gauss_b = {5, 5, 0};
            double[] gauss_x = new double[3];
            if (m1.solveGaussian(gauss_b, gauss_x)) {
                System.out.println("  Gaussian Solver: x = " + Arrays.toString(gauss_x));
            }

            // Vector Algebra
            double[] vecA = {1.0, 2.0, 3.0};
            double[] vecB = {4.0, 5.0, 6.0};
            System.out.printf("  Vector dot product: %.4f%n", VectorUtils.dotProduct(vecA, vecB));
            System.out.printf("  Vector cosine similarity: %.4f%n", VectorUtils.cosineSimilarity(vecA, vecB));

            // Regressions
            double[] regX = {1, 2, 3, 4, 5};
            double[] regY = {2, 4, 5, 4, 5};
            double[] params = new double[2];
            RegressionModels.linearRegression(regX, regY, params, 0.01, 1000);
            System.out.printf("  Linear Reg: y = %.4f * x + %.4f%n", params[0], params[1]);

            // Decision Tree
            double[][] dt_X = {{1.0, 1.0}, {1.5, 2.0}, {5.0, 5.0}, {6.0, 6.0}, {1.2, 1.5}};
            int[] dt_y = {0, 0, 1, 1, 0};
            DecisionTree dt = new DecisionTree();
            dt.train(dt_X, dt_y, 3);
            System.out.println("  DecisionTree Predict (1.1, 1.2): " + dt.predict(new double[]{1.1, 1.2}));

            // XOR MLP
            double[][] xor_X = {{0.0, 0.0}, {0.0, 1.0}, {1.0, 0.0}, {1.0, 1.0}};
            double[] xor_y = {0.0, 1.0, 1.0, 0.0};
            MLP neuralNet = new MLP();
            neuralNet.train(xor_X, xor_y, 0.5, 5000);
            System.out.printf("  XOR MLP Predict (0,1): %.4f, Predict (1,1): %.4f%n",
                              neuralNet.predict(0.0, 1.0), neuralNet.predict(1.0, 1.0));

            // KNN
            List<KNNPoint> pts = List.of(
                new KNNPoint(new double[]{1.0, 1.0}, 0),
                new KNNPoint(new double[]{2.0, 2.0}, 0),
                new KNNPoint(new double[]{5.0, 5.0}, 1),
                new KNNPoint(new double[]{6.0, 6.0}, 1)
            );
            System.out.println("  KNN Classifier for (3,3): " + KNN.classify(pts, new double[]{3.0, 3.0}, 3));

            // Naive Bayes
            double[] nb_features = {1.0, 1.5, 2.0, 5.0, 5.5, 6.0};
            int[] nb_labels = {0, 0, 0, 1, 1, 1};
            NaiveBayes nb = new NaiveBayes();
            nb.train(nb_features, nb_labels);
            System.out.println("  NaiveBayes Predict 2.2 (Class): " + nb.predict(2.2));

            // KMeans
            List<KMeans.Point> kmPts = new ArrayList<>(List.of(
                new KMeans.Point(1.0, 1.0), new KMeans.Point(2.0, 2.0),
                new KMeans.Point(5.0, 5.0), new KMeans.Point(6.0, 6.0)
            ));
            List<KMeans.Centroid> centroids = new ArrayList<>(List.of(
                new KMeans.Centroid(1.5, 1.5), new KMeans.Centroid(5.5, 5.5)
            ));
            KMeans.cluster(kmPts, centroids, 10);
            System.out.printf("  KMeans Centroids: C0=(%.2f, %.2f), C1=(%.2f, %.2f)%n",
                              centroids.get(0).x, centroids.get(0).y, centroids.get(1).x, centroids.get(1).y);
        }

        // ====================================================================
        // 9.1  Systems Programming — Stack Virtual Machine & Assembler
        // ====================================================================

        static class VMInstruction {
            int opcode;
            int operand;
            VMInstruction(int op, int arg) { this.opcode = op; this.operand = arg; }
        }

        static class StackVM {
            static final int INST_PUSH = 0;
            static final int INST_ADD = 1;
            static final int INST_SUB = 2;
            static final int INST_MUL = 3;
            static final int INST_DIV = 4;
            static final int INST_JMP = 5;
            static final int INST_JZ = 6;
            static final int INST_JNZ = 7;
            static final int INST_PRINT = 8;
            static final int INST_HALT = 9;

            private final int[] stack = new int[256];
            private int ip = 0;
            private final List<VMInstruction> program;

            StackVM(List<VMInstruction> prog) { this.program = prog; }

            void run() {
                int sp = -1;
                ip = 0;
                while (ip < program.size()) {
                    VMInstruction instr = program.get(ip);
                    String opName = switch(instr.opcode) {
                        case INST_PUSH -> "PUSH";
                        case INST_ADD -> "ADD";
                        case INST_SUB -> "SUB";
                        case INST_MUL -> "MUL";
                        case INST_DIV -> "DIV";
                        case INST_JMP -> "JMP";
                        case INST_JZ -> "JZ";
                        case INST_JNZ -> "JNZ";
                        case INST_PRINT -> "PRINT";
                        case INST_HALT -> "HALT";
                        default -> "UNKNOWN";
                    };
                    System.out.printf("    [VM Trace] IP=%-2d | Op=%-5s | Arg=%-3d | SP=%-2d | StackTop=%s%n",
                                      ip, opName, instr.operand, sp, (sp >= 0 ? String.valueOf(stack[sp]) : "empty"));
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
                            System.out.println("    [VM PRINT] Stack Top: " + stack[sp]);
                            ip++;
                            break;
                        case INST_HALT:
                            return;
                    }
                }
            }

            static List<VMInstruction> assemble(List<String> source) {
                List<VMInstruction> instructions = new ArrayList<>();
                for (String line : source) {
                    String[] tokens = line.trim().split("\\s+");
                    if (tokens.length == 0 || tokens[0].isEmpty()) continue;
                    String op = tokens[0];
                    int operand = 0;
                    if (tokens.length > 1) {
                        operand = Integer.parseInt(tokens[1]);
                    }
                    switch (op) {
                        case "PUSH":  instructions.add(new VMInstruction(INST_PUSH, operand)); break;
                        case "ADD":   instructions.add(new VMInstruction(INST_ADD, 0)); break;
                        case "SUB":   instructions.add(new VMInstruction(INST_SUB, 0)); break;
                        case "MUL":   instructions.add(new VMInstruction(INST_MUL, 0)); break;
                        case "DIV":   instructions.add(new VMInstruction(INST_DIV, 0)); break;
                        case "JMP":   instructions.add(new VMInstruction(INST_JMP, operand)); break;
                        case "JZ":    instructions.add(new VMInstruction(INST_JZ, operand)); break;
                        case "JNZ":   instructions.add(new VMInstruction(INST_JNZ, operand)); break;
                        case "PRINT": instructions.add(new VMInstruction(INST_PRINT, 0)); break;
                        case "HALT":  instructions.add(new VMInstruction(INST_HALT, 0)); break;
                    }
                }
                return instructions;
            }
        }

        static void systemsVM_Demo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("9.  SYSTEMS VM & ASSEMBLER DEMO");
            System.out.println("=".repeat(60));

            // Assembly program: calculates factorial(5) i.e. 5*4*3*2*1
            // In assembly:
            // PUSH 5
            // PUSH 4
            // MUL
            // PUSH 3
            // MUL
            // PUSH 2
            // MUL
            // PRINT
            // HALT
            List<String> asmSource = List.of(
                "PUSH 5",
                "PUSH 4",
                "MUL",
                "PUSH 3",
                "MUL",
                "PUSH 2",
                "MUL",
                "PRINT",
                "HALT"
            );
            List<VMInstruction> bytecode = StackVM.assemble(asmSource);
            System.out.println("  Running bytecode on StackVM: ");
            StackVM vm = new StackVM(bytecode);
            vm.run();
        }

        // ====================================================================
        // 10.  15 Java Debug Challenges (Modern Java Gotchas)
        // ====================================================================

        static void bugChallenges() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("10.  15 JAVA DEBUG CHALLENGES");
            System.out.println("=".repeat(60));

            // Challenge 1: String Identity comparison
            String s1 = "hello"; 
            String s2 = new String("hello");
            System.out.println("  1. String == comparison (Identity): " + (s1 == s2) + " (incorrect comparison)");
            System.out.println("     Resolved: s1.equals(s2) = " + s1.equals(s2));

            // Challenge 2: Integer Pool boundary cache
            Integer i1 = 128; 
            Integer i2 = 128;
            System.out.println("  2. Integer cache comparison (128 == 128): " + (i1 == i2) + " (fails outside -128..127)");
            System.out.println("     Resolved: i1.equals(i2) = " + i1.equals(i2));

            // Challenge 3: ConcurrentModificationException on iteration removals
            try {
                List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4));
                System.out.print("  3. CME Trigger: ");
                for (int x : list) {
                    if (x == 3) list.remove(Integer.valueOf(x)); // throws CME
                }
            } catch (ConcurrentModificationException e) {
                System.out.println("Caught CME expectedly!");
                List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4));
                list.removeIf(val -> val == 3);
                System.out.println("     Resolved: list.removeIf -> list = " + list);
            }

            // Challenge 4: Autoboxing NullPointerException
            try {
                Integer maybeNull = null;
                System.out.print("  4. Autoboxing NPE Trigger: ");
                int val = maybeNull; // throws NPE
                System.out.println(val);
            } catch (NullPointerException e) {
                System.out.println("Caught NPE expectedly!");
                Integer maybeNull = null;
                int fallback = (maybeNull != null) ? maybeNull : 0;
                System.out.println("     Resolved: null check fallback = " + fallback);
            }

            // Challenge 5: Array equals() gotcha
            int[] arrA = {1, 2}; 
            int[] arrB = {1, 2};
            System.out.println("  5. Array equals() direct comparison: " + arrA.equals(arrB) + " (incorrectly checks reference)");
            System.out.println("     Resolved: Arrays.equals(arrA, arrB) = " + Arrays.equals(arrA, arrB));

            // Challenge 6: Double-Check Locking without Volatile
            System.out.println("  6. Singleton DCL visibility risk resolved: Handled by static nested Holder class (safe classloading).");

            // Challenge 7: Hash contract violation (equals without hashCode)
            @SuppressWarnings("overrides")
            class BadKey {
                final int id;
                BadKey(int id) { this.id = id; }
                @Override public boolean equals(Object o) {
                    if (this == o) return true;
                    if (!(o instanceof BadKey)) return false;
                    return id == ((BadKey) o).id;
                }
                // missing hashCode causes hash map to miss matching keys
            }
            Map<BadKey, String> badMap = new HashMap<>();
            badMap.put(new BadKey(1), "One");
            System.out.println("  7. Missing hashCode result (get search): " + badMap.get(new BadKey(1)) + " (returns null)");

            // Challenge 8: ArrayStoreException covariance
            try {
                Object[] objArr = new String[5];
                System.out.print("  8. ArrayStoreException Trigger: ");
                objArr[0] = Integer.valueOf(42); // throws ArrayStoreException
            } catch (ArrayStoreException e) {
                System.out.println("Caught ArrayStoreException expectedly!");
                System.out.println("     Resolved: Use generic collections like List<String> to enforce compile-time safety.");
            }

            // Challenge 9: Non-synchronized list thread safety
            try {
                List<Integer> unsafeList = new ArrayList<>();
                Thread t1 = new Thread(() -> { for (int i = 0; i < 100; i++) unsafeList.add(i); });
                Thread t2 = new Thread(() -> { for (int i = 0; i < 100; i++) unsafeList.add(i); });
                t1.start(); t2.start();
                t1.join(); t2.join();
                System.out.println("  9. Unsynchronized ArrayList size (expected 200): " + unsafeList.size() + " (data race risk)");
                
                List<Integer> safeList = Collections.synchronizedList(new ArrayList<>());
                Thread t3 = new Thread(() -> { for (int i = 0; i < 100; i++) safeList.add(i); });
                Thread t4 = new Thread(() -> { for (int i = 0; i < 100; i++) safeList.add(i); });
                t3.start(); t4.start();
                t3.join(); t4.join();
                System.out.println("     Resolved: Synchronized list size: " + safeList.size());
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }

            // Challenge 10: StackOverflow infinite recursion
            class Recurser {
                int run(int x) { if (x > 50) throw new RuntimeException("Stack Limit reached"); return run(x + 1); }
            }
            try {
                System.out.print(" 10. StackOverflow simulated boundary: ");
                new Recurser().run(0);
            } catch (Exception e) {
                System.out.println("Caught simulation depth exception!");
                System.out.println("     Resolved: Define a base case check to exit or rewrite using loops.");
            }

            // Challenge 11: Floating point arithmetic precision
            double doubleVal = 0.1 + 0.2;
            System.out.println(" 11. Floating-point error (0.1 + 0.2): " + doubleVal + " (imprecise)");
            java.math.BigDecimal d1 = new java.math.BigDecimal("0.1");
            java.math.BigDecimal d2 = new java.math.BigDecimal("0.2");
            System.out.println("     Resolved: BigDecimal sum = " + d1.add(d2));

            // Challenge 12: Resource leak / unclosed streams
            System.out.println(" 12. Unclosed files: Solved using Try-with-Resources construct which auto-closes AutoCloseable resources.");

            // Challenge 13: Array out-of-bounds error
            try {
                int[] listTest = {1, 2};
                System.out.print(" 13. IndexOutOfBounds Trigger: ");
                int val = listTest[2]; // throws Exception
                System.out.println(val);
            } catch (ArrayIndexOutOfBoundsException e) {
                System.out.println("Caught ArrayIndexOutOfBoundsException expectedly!");
                System.out.println("     Resolved: Bound check using array.length.");
            }

            // Challenge 14: Division by zero unchecked values
            try {
                System.out.print(" 14. ArithmeticException Trigger: ");
                int zeroVal = 0;
                int quotient = 10 / zeroVal; // throws Exception
                System.out.println(quotient);
            } catch (ArithmeticException e) {
                System.out.println("Caught ArithmeticException expectedly!");
                System.out.println("     Resolved: Assert denominator != 0 before division.");
            }

            // Challenge 15: Memory leak via static collection references
            System.out.println(" 15. Static reference leak resolved: Use WeakHashMap or clear collections after task completion to free GC memory.");
        }

        // ====================================================================
        // 11.  Academic Textbook Lectures & Big-O Reference
        // ====================================================================

        static void academicLectures() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("11.1 ACADEMIC LECTURES & SYSTEM METRICS");
            System.out.println("=".repeat(60));
            
            System.out.println("  [System Info] Operating System: " + System.getProperty("os.name"));
            System.out.println("  [System Info] Java Version:     " + System.getProperty("java.version"));
            System.out.println("  [System Info] Java Home:        " + System.getProperty("java.home"));
            
            Runtime runtime = Runtime.getRuntime();
            long totalMemory = runtime.totalMemory();
            long freeMemory = runtime.freeMemory();
            long maxMemory = runtime.maxMemory();
            System.out.printf("  [JVM Memory] Max Memory:   %,d bytes%n", maxMemory);
            System.out.printf("  [JVM Memory] Total Memory: %,d bytes%n", totalMemory);
            System.out.printf("  [JVM Memory] Free Memory:  %,d bytes%n", freeMemory);
            System.out.printf("  [JVM Memory] Used Memory:  %,d bytes%n", (totalMemory - freeMemory));
            System.out.println("  [CPU Info] Available Processors: " + runtime.availableProcessors());

            System.out.println("\n  --- Garbage Collection MXBeans ---");
            try {
                var gcBeans = java.lang.management.ManagementFactory.getGarbageCollectorMXBeans();
                for (var gcBean : gcBeans) {
                    System.out.printf("    GC Name: %-20s | Collections: %-5d | Time: %-5d ms%n",
                                      gcBean.getName(), gcBean.getCollectionCount(), gcBean.getCollectionTime());
                }
            } catch (Exception e) {
                System.out.println("    Could not retrieve GC MXBean metrics.");
            }

            System.out.println("\n  --- JIT Compiler MXBean ---");
            try {
                var compBean = java.lang.management.ManagementFactory.getCompilationMXBean();
                if (compBean != null) {
                    System.out.printf("    JIT Compiler Name: %s | Total Compilation Time: %d ms%n",
                                      compBean.getName(), compBean.getTotalCompilationTime());
                } else {
                    System.out.println("    No JIT compiler available.");
                }
            } catch (Exception e) {
                System.out.println("    Could not retrieve Compilation MXBean metrics.");
            }
            
            System.out.println("\n  --- Heap/Non-Heap Memory Pools ---");
            try {
                var memBean = java.lang.management.ManagementFactory.getMemoryMXBean();
                var heapUsage = memBean.getHeapMemoryUsage();
                var nonHeapUsage = memBean.getNonHeapMemoryUsage();
                System.out.printf("    Heap Memory:     Init=%,d, Used=%,d, Max=%,d%n",
                                  heapUsage.getInit(), heapUsage.getUsed(), heapUsage.getMax());
                System.out.printf("    Non-Heap Memory: Init=%,d, Used=%,d, Max=%,d%n",
                                  nonHeapUsage.getInit(), nonHeapUsage.getUsed(), nonHeapUsage.getMax());
            } catch (Exception e) {
                System.out.println("    Could not retrieve Memory MXBean metrics.");
            }
        }

        static void complexityCheatSheet() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("11.  ACADEMIC REFERENCE & PARADIGMS");
            System.out.println("=".repeat(60));
            System.out.println("  [Reference 1] Memory Schematics: JVM Stack vs Garbage-Collected Heap.");
            System.out.println("    - Stack: Stores local variables and execution frames. Fast, thread-local, LIFO.");
            System.out.println("    - Heap: Stores all objects. Shared across threads, managed by Garbage Collector (G1, Parallel, ZGC).");
            System.out.println("  [Reference 2] Tree Balance Theory:");
            System.out.println("    - AVL Trees: Maintain strict balance factor of <= 1. Faster lookup, slower insertion rotations.");
            System.out.println("    - Red-Black Trees: Colored nodes, height bounded by 2 * log(n + 1). Balanced via recolor and rotations.");
            System.out.println("    - Segment Trees: Represent interval ranges. Support range updates and queries in O(log n) time.");
            System.out.println("  [Reference 3] Machine Learning Mathematics:");
            System.out.println("    - Sigmoid: f(x) = 1 / (1 + exp(-x)). Maps linear inputs to [0,1] probability range.");
            System.out.println("    - Gini Impurity: 1 - sum(p_i^2). Measures split cleanliness in Decision Tree models.");
            System.out.println("  [Reference 4] Concurrency Primitive Models:");
            System.out.println("    - Locks: ReentrantLock supports fair/unfair locking. Conditions allow fine-grained wait/signal cues.");
            System.out.println("    - BlockingQueue: Bounded buffer synchronizing producers and consumers via lock-state condition monitors.");
            System.out.println("  [Reference 5] Big-O Complexity Comparison Chart:");
            System.out.println("    Structure            Insert       Search       Delete       Space");
            System.out.println("    -----------------------------------------------------------------");
            System.out.println("    ArrayList            O(1)*        O(n)         O(n)         O(n)");
            System.out.println("    LinkedList           O(1)         O(n)         O(1)*        O(n)");
            System.out.println("    BST                  O(log n)     O(log n)     O(log n)     O(n)");
            System.out.println("    AVL Tree             O(log n)     O(log n)     O(log n)     O(n)");
            System.out.println("    Red-Black Tree       O(log n)     O(log n)     O(log n)     O(n)");
            System.out.println("    HashMap              O(1)         O(1)         O(1)         O(n)");
            System.out.println("    Trie                 O(L)         O(L)         O(L)         O(Alphabet * L)");
            System.out.println("    Skip List            O(log n)     O(log n)     O(log n)     O(n)");
            System.out.println("    * Amortized or with direct pointer reference access.");
        }
"""
