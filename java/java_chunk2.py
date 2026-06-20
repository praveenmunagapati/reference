# java_chunk2.py
# Phase 2 (Part 2): Graphs, Heaps, Hash Tables
# Phase 3: Sorting, Search, Pathfinding, Spanning Trees, Dynamic Programming, and String Matching

chunk_content = r"""
        // ====================================================================
        // 2.4  Graphs — Adjacency List & Adjacency Matrix representations
        // ====================================================================

        static class GraphAdjList {
            private final Map<Integer, List<Integer>> adjList = new HashMap<>();

            void addVertex(int v) { adjList.putIfAbsent(v, new ArrayList<>()); }
            void addEdge(int u, int v) {
                addVertex(u); addVertex(v);
                adjList.get(u).add(v);
            }

            List<Integer> dfs(int start) {
                List<Integer> visitedOrder = new ArrayList<>();
                Set<Integer> visited = new HashSet<>();
                dfsRec(start, visited, visitedOrder);
                return visitedOrder;
            }

            private void dfsRec(int u, Set<Integer> visited, List<Integer> order) {
                visited.add(u);
                order.add(u);
                for (int v : adjList.getOrDefault(u, List.of())) {
                    if (!visited.contains(v)) dfsRec(v, visited, order);
                }
            }

            List<Integer> bfs(int start) {
                List<Integer> order = new ArrayList<>();
                Set<Integer> visited = new HashSet<>();
                Queue<Integer> q = new LinkedList<>();
                q.add(start);
                visited.add(start);
                while (!q.isEmpty()) {
                    int u = q.poll();
                    order.add(u);
                    for (int v : adjList.getOrDefault(u, List.of())) {
                        if (!visited.contains(v)) {
                            visited.add(v);
                            q.add(v);
                        }
                    }
                }
                return order;
            }

            List<Integer> topologicalSort() {
                List<Integer> order = new ArrayList<>();
                Set<Integer> visited = new HashSet<>();
                Stack<Integer> stack = new Stack<>();
                for (int v : adjList.keySet()) {
                    if (!visited.contains(v)) topoRec(v, visited, stack);
                }
                while (!stack.isEmpty()) order.add(stack.pop());
                return order;
            }

            private void topoRec(int u, Set<Integer> visited, Stack<Integer> stack) {
                visited.add(u);
                for (int v : adjList.getOrDefault(u, List.of())) {
                    if (!visited.contains(v)) topoRec(v, visited, stack);
                }
                stack.push(u);
            }
        }

        static class GraphAdjMatrix {
            private final int[][] adjMatrix;
            private final int numVertices;

            GraphAdjMatrix(int numVertices) {
                this.numVertices = numVertices;
                adjMatrix = new int[numVertices][numVertices];
            }

            void addEdge(int u, int v, int weight) {
                adjMatrix[u][v] = weight;
            }

            int getWeight(int u, int v) { return adjMatrix[u][v]; }
        }

        // ====================================================================
        // 2.5  Heaps — Min-Heap & Max-Heap
        // ====================================================================

        static class MinHeap {
            private final List<Integer> heap = new ArrayList<>();

            void insert(int val) {
                heap.add(val);
                siftUp(heap.size() - 1);
            }

            int poll() {
                if (heap.isEmpty()) throw new NoSuchElementException();
                int min = heap.get(0);
                int last = heap.remove(heap.size() - 1);
                if (!heap.isEmpty()) {
                    heap.set(0, last);
                    siftDown(0);
                }
                return min;
            }

            boolean isEmpty() { return heap.isEmpty(); }

            private void siftUp(int idx) {
                while (idx > 0) {
                    int p = (idx - 1) / 2;
                    if (heap.get(idx) >= heap.get(p)) break;
                    swap(idx, p);
                    idx = p;
                }
            }

            private void siftDown(int idx) {
                int size = heap.size();
                while (2 * idx + 1 < size) {
                    int left = 2 * idx + 1;
                    int right = 2 * idx + 2;
                    int smallest = left;
                    if (right < size && heap.get(right) < heap.get(left)) smallest = right;
                    if (heap.get(idx) <= heap.get(smallest)) break;
                    swap(idx, smallest);
                    idx = smallest;
                }
            }

            private void swap(int i, int j) {
                int temp = heap.get(i);
                heap.set(i, heap.get(j));
                heap.set(j, temp);
            }
        }

        static class MaxHeap {
            private final List<Integer> heap = new ArrayList<>();

            void insert(int val) {
                heap.add(val);
                siftUp(heap.size() - 1);
            }

            int poll() {
                if (heap.isEmpty()) throw new NoSuchElementException();
                int max = heap.get(0);
                int last = heap.remove(heap.size() - 1);
                if (!heap.isEmpty()) {
                    heap.set(0, last);
                    siftDown(0);
                }
                return max;
            }

            private void siftUp(int idx) {
                while (idx > 0) {
                    int p = (idx - 1) / 2;
                    if (heap.get(idx) <= heap.get(p)) break;
                    swap(idx, p);
                    idx = p;
                }
            }

            private void siftDown(int idx) {
                int size = heap.size();
                while (2 * idx + 1 < size) {
                    int left = 2 * idx + 1;
                    int right = 2 * idx + 2;
                    int largest = left;
                    if (right < size && heap.get(right) > heap.get(left)) largest = right;
                    if (heap.get(idx) >= heap.get(largest)) break;
                    swap(idx, largest);
                    idx = largest;
                }
            }

            private void swap(int i, int j) {
                int temp = heap.get(i);
                heap.set(i, heap.get(j));
                heap.set(j, temp);
            }

            boolean isEmpty() { return heap.isEmpty(); }
        }

        // ====================================================================
        // 2.6  Hash Tables — Chaining & Open Addressing (Linear Probing)
        // ====================================================================

        static class HashTableChaining<K, V> {
            private static class Entry<K, V> {
                K key; V val; Entry<K, V> next;
                Entry(K k, V v, Entry<K, V> n) { key = k; val = v; next = n; }
            }
            private Entry<K, V>[] buckets;
            private int size;
            private static final double LOAD_FACTOR = 0.75;

            @SuppressWarnings({"unchecked", "rawtypes"})
            HashTableChaining() {
                buckets = (Entry<K, V>[]) new Entry[16];
            }

            void put(K key, V val) {
                int idx = Math.abs(key.hashCode()) % buckets.length;
                Entry<K, V> curr = buckets[idx];
                while (curr != null) {
                    if (Objects.equals(curr.key, key)) {
                        curr.val = val;
                        return;
                    }
                    curr = curr.next;
                }
                buckets[idx] = new Entry<>(key, val, buckets[idx]);
                size++;
                if ((double) size / buckets.length > LOAD_FACTOR) resize();
            }

            V get(K key) {
                int idx = Math.abs(key.hashCode()) % buckets.length;
                Entry<K, V> curr = buckets[idx];
                while (curr != null) {
                    if (Objects.equals(curr.key, key)) return curr.val;
                    curr = curr.next;
                }
                return null;
            }

            @SuppressWarnings({"unchecked", "rawtypes"})
            private void resize() {
                Entry<K, V>[] old = buckets;
                buckets = (Entry<K, V>[]) new Entry[old.length * 2];
                size = 0;
                for (var b : old) {
                    Entry<K, V> curr = b;
                    while (curr != null) {
                        put(curr.key, curr.val);
                        curr = curr.next;
                    }
                }
            }
        }

        static class HashTableOpenAddressing<K, V> {
            private K[] keys;
            private V[] vals;
            private int size;

            @SuppressWarnings("unchecked")
            HashTableOpenAddressing() {
                keys = (K[]) new Object[16];
                vals = (V[]) new Object[16];
            }

            void put(K key, V val) {
                if (size >= keys.length / 2) resize();
                int i;
                for (i = Math.abs(key.hashCode()) % keys.length; keys[i] != null; i = (i + 1) % keys.length) {
                    if (keys[i].equals(key)) {
                        vals[i] = val;
                        return;
                    }
                }
                keys[i] = key;
                vals[i] = val;
                size++;
            }

            V get(K key) {
                for (int i = Math.abs(key.hashCode()) % keys.length; keys[i] != null; i = (i + 1) % keys.length) {
                    if (keys[i].equals(key)) return vals[i];
                }
                return null;
            }

            @SuppressWarnings("unchecked")
            private void resize() {
                K[] oldKeys = keys;
                V[] oldVals = vals;
                keys = (K[]) new Object[oldKeys.length * 2];
                vals = (V[]) new Object[oldVals.length * 2];
                size = 0;
                for (int i = 0; i < oldKeys.length; i++) {
                    if (oldKeys[i] != null) put(oldKeys[i], oldVals[i]);
                }
            }
        }

        static void graphDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("2.3  GRAPHS & HEAPS & HASH TABLES DEMO");
            System.out.println("=".repeat(60));
            var g = new GraphAdjList();
            g.addEdge(0, 1);
            g.addEdge(0, 2);
            g.addEdge(1, 3);
            g.addEdge(2, 3);
            System.out.println("  DFS start=0: " + g.dfs(0));
            System.out.println("  BFS start=0: " + g.bfs(0));

            var topo = new GraphAdjList();
            topo.addEdge(5, 2);
            topo.addEdge(5, 0);
            topo.addEdge(4, 0);
            topo.addEdge(4, 1);
            topo.addEdge(2, 3);
            topo.addEdge(3, 1);
            System.out.println("  Topological Sort: " + topo.topologicalSort());

            var minHeap = new MinHeap();
            minHeap.insert(50);
            minHeap.insert(20);
            minHeap.insert(30);
            System.out.print("  MinHeap Poll order: ");
            while (!minHeap.isEmpty()) {
                System.out.print(minHeap.poll() + " ");
            }
            System.out.println();

            var maxHeap = new MaxHeap();
            maxHeap.insert(50);
            maxHeap.insert(20);
            maxHeap.insert(30);
            System.out.print("  MaxHeap Poll order: ");
            while (!maxHeap.isEmpty()) {
                System.out.print(maxHeap.poll() + " ");
            }
            System.out.println();

            var hChaining = new HashTableChaining<String, Integer>();
            hChaining.put("Alice", 90);
            hChaining.put("Bob", 85);
            System.out.println("  HashChaining Alice: " + hChaining.get("Alice"));

            var hProbing = new HashTableOpenAddressing<String, Integer>();
            hProbing.put("Alice", 95);
            hProbing.put("Bob", 80);
            System.out.println("  HashProbing Bob:   " + hProbing.get("Bob"));
        }

        // ====================================================================
        // 3.1  Sorting & Search Algorithms
        // ====================================================================

        static void bubbleSort(int[] arr) {
            int n = arr.length;
            for (int i = 0; i < n - 1; i++) {
                for (int j = 0; j < n - i - 1; j++) {
                    if (arr[j] > arr[j + 1]) {
                        int temp = arr[j];
                        arr[j] = arr[j+1];
                        arr[j+1] = temp;
                    }
                }
            }
        }

        static void quickSort(int[] arr, int low, int high) {
            if (low < high) {
                int pi = partition(arr, low, high);
                quickSort(arr, low, pi - 1);
                quickSort(arr, pi + 1, high);
            }
        }

        private static int partition(int[] arr, int low, int high) {
            int pivot = arr[high];
            int i = (low - 1);
            for (int j = low; j < high; j++) {
                if (arr[j] < pivot) {
                    i++;
                    int temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }
            }
            int temp = arr[i + 1];
            arr[i + 1] = arr[high];
            arr[high] = temp;
            return i + 1;
        }

        static void mergeSort(int[] arr, int l, int r) {
            if (l < r) {
                int m = l + (r - l) / 2;
                mergeSort(arr, l, m);
                mergeSort(arr, m + 1, r);
                merge(arr, l, m, r);
            }
        }

        private static void merge(int[] arr, int l, int m, int r) {
            int n1 = m - l + 1;
            int n2 = r - m;
            int[] L = new int[n1];
            int[] R = new int[n2];
            System.arraycopy(arr, l, L, 0, n1);
            System.arraycopy(arr, m + 1, R, 0, n2);
            int i = 0, j = 0;
            int k = l;
            while (i < n1 && j < n2) {
                if (L[i] <= R[j]) { arr[k] = L[i]; i++; }
                else { arr[k] = R[j]; j++; }
                k++;
            }
            while (i < n1) { arr[k] = L[i]; i++; k++; }
            while (j < n2) { arr[k] = R[j]; j++; k++; }
        }

        static void shellSort(int[] arr) {
            int n = arr.length;
            for (int gap = n / 2; gap > 0; gap /= 2) {
                for (int i = gap; i < n; i += 1) {
                    int temp = arr[i];
                    int j;
                    for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                        arr[j] = arr[j - gap];
                    }
                    arr[j] = temp;
                }
            }
        }

        static void countingSort(int[] arr) {
            int n = arr.length;
            if (n == 0) return;
            int max = arr[0];
            for (int i = 1; i < n; i++) {
                if (arr[i] > max) max = arr[i];
            }
            int[] count = new int[max + 1];
            for (int i = 0; i < n; i++) count[arr[i]]++;
            int index = 0;
            for (int i = 0; i <= max; i++) {
                while (count[i] > 0) {
                    arr[index++] = i;
                    count[i]--;
                }
            }
        }

        static void radixSort(int[] arr) {
            int n = arr.length;
            if (n == 0) return;
            int max = arr[0];
            for (int i = 1; i < n; i++) {
                if (arr[i] > max) max = arr[i];
            }
            for (int exp = 1; max / exp > 0; exp *= 10) {
                countSortForRadix(arr, n, exp);
            }
        }

        private static void countSortForRadix(int[] arr, int n, int exp) {
            int[] output = new int[n];
            int[] count = new int[10];
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
            System.arraycopy(output, 0, arr, 0, n);
        }

        static int binarySearchLowerBound(int[] arr, int key) {
            int low = 0, high = arr.length;
            while (low < high) {
                int mid = (low + high) / 2;
                if (arr[mid] >= key) high = mid;
                else low = mid + 1;
            }
            return low;
        }

        static int binarySearchUpperBound(int[] arr, int key) {
            int low = 0, high = arr.length;
            while (low < high) {
                int mid = (low + high) / 2;
                if (arr[mid] > key) high = mid;
                else low = mid + 1;
            }
            return low;
        }

        // ====================================================================
        // 3.2  Graph Algorithms: Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal's MST
        // ====================================================================

        static class Edge implements Comparable<Edge> {
            int src, dest, weight;
            Edge(int src, int dest, int weight) {
                this.src = src; this.dest = dest; this.weight = weight;
            }
            @Override
            public int compareTo(Edge o) { return Integer.compare(this.weight, o.weight); }
        }

        static class DijkstraNode implements Comparable<DijkstraNode> {
            int id, dist;
            DijkstraNode(int id, int dist) { this.id = id; this.dist = dist; }
            @Override
            public int compareTo(DijkstraNode o) { return Integer.compare(this.dist, o.dist); }
        }

        static void dijkstra(int[][] graph, int src, int dest) {
            int n = graph.length;
            int[] dist = new int[n];
            int[] parent = new int[n];
            Arrays.fill(dist, Integer.MAX_VALUE);
            Arrays.fill(parent, -1);
            PriorityQueue<DijkstraNode> pq = new PriorityQueue<>();

            dist[src] = 0;
            pq.add(new DijkstraNode(src, 0));

            while (!pq.isEmpty()) {
                DijkstraNode curr = pq.poll();
                int u = curr.id;
                if (u == dest) break;
                if (curr.dist > dist[u]) continue;

                for (int v = 0; v < n; v++) {
                    if (graph[u][v] != 0 && dist[u] + graph[u][v] < dist[v]) {
                        dist[v] = dist[u] + graph[u][v];
                        parent[v] = u;
                        pq.add(new DijkstraNode(v, dist[v]));
                    }
                }
            }

            if (dist[dest] == Integer.MAX_VALUE) {
                System.out.printf("  Dijkstra: No path from %d to %d%n", src, dest);
            } else {
                List<Integer> path = new ArrayList<>();
                for (int at = dest; at != -1; at = parent[at]) path.add(at);
                Collections.reverse(path);
                System.out.printf("  Dijkstra (dest=%d): path=%s, cost=%d%n", dest, path, dist[dest]);
            }
        }

        static void bellmanFord(List<Edge> edges, int numVertices, int src) {
            int[] dist = new int[numVertices];
            Arrays.fill(dist, 1000000); // Represent Infinity
            dist[src] = 0;

            for (int i = 0; i < numVertices - 1; i++) {
                for (Edge edge : edges) {
                    if (dist[edge.src] != 1000000 && dist[edge.src] + edge.weight < dist[edge.dest]) {
                        dist[edge.dest] = dist[edge.src] + edge.weight;
                    }
                }
            }

            boolean hasNegativeCycle = false;
            for (Edge edge : edges) {
                if (dist[edge.src] != 1000000 && dist[edge.src] + edge.weight < dist[edge.dest]) {
                    hasNegativeCycle = true;
                    break;
                }
            }
            System.out.printf("  Bellman-Ford: Negative cycle = %b, dist to last vertex = %d%n",
                               hasNegativeCycle, dist[numVertices - 1]);
        }

        static void floydWarshall(int[][] graph) {
            int n = graph.length;
            int[][] dist = new int[n][n];
            for (int i = 0; i < n; i++) {
                System.arraycopy(graph[i], 0, dist[i], 0, n);
            }

            for (int k = 0; k < n; k++) {
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        if (dist[i][k] != 1000000 && dist[k][j] != 1000000 && dist[i][k] + dist[k][j] < dist[i][j]) {
                            dist[i][j] = dist[i][k] + dist[k][j];
                        }
                    }
                }
            }
            System.out.printf("  Floyd-Warshall: dist[0][%d] = %d%n", n - 1, dist[0][n - 1]);
        }

        static class DSU {
            int[] parent, rank;
            DSU(int n) {
                parent = new int[n];
                rank = new int[n];
                for (int i = 0; i < n; i++) parent[i] = i;
            }
            int find(int i) {
                if (parent[i] == i) return i;
                return parent[i] = find(parent[i]);
            }
            boolean union(int i, int j) {
                int rootI = find(i);
                int rootJ = find(j);
                if (rootI != rootJ) {
                    if (rank[rootI] < rank[rootJ]) {
                        parent[rootI] = rootJ;
                    } else if (rank[rootI] > rank[rootJ]) {
                        parent[rootJ] = rootI;
                    } else {
                        parent[rootJ] = rootI;
                        rank[rootI]++;
                    }
                    return true;
                }
                return false;
            }
        }

        static void kruskalMST(List<Edge> edges, int numVertices) {
            Collections.sort(edges);
            DSU dsu = new DSU(numVertices);
            List<Edge> mst = new ArrayList<>();
            int mstWeight = 0;
            for (Edge edge : edges) {
                if (dsu.union(edge.src, edge.dest)) {
                    mst.add(edge);
                    mstWeight += edge.weight;
                }
            }
            System.out.printf("  Kruskal's MST: Total Weight = %d, edge count = %d%n", mstWeight, mst.size());
        }

        static void primMST(int[][] graph) {
            int V = graph.length;
            int[] parent = new int[V];
            int[] key = new int[V];
            boolean[] mstSet = new boolean[V];
            Arrays.fill(key, Integer.MAX_VALUE);
            key[0] = 0;
            parent[0] = -1;

            for (int count = 0; count < V - 1; count++) {
                int u = -1;
                int min = Integer.MAX_VALUE;
                for (int v = 0; v < V; v++) {
                    if (!mstSet[v] && key[v] < min) {
                        min = key[v];
                        u = v;
                    }
                }
                if (u == -1) break;
                mstSet[u] = true;

                for (int v = 0; v < V; v++) {
                    if (graph[u][v] != 0 && !mstSet[v] && graph[u][v] < key[v]) {
                        parent[v] = u;
                        key[v] = graph[u][v];
                    }
                }
            }

            int totalWeight = 0;
            for (int i = 1; i < V; i++) {
                if (parent[i] != -1) {
                    totalWeight += graph[i][parent[i]];
                }
            }
            System.out.printf("  Prim's MST: Total Weight = %d%n", totalWeight);
        }

        // ====================================================================
        // 3.3  Dynamic Programming & String Matching
        // ====================================================================

        static void knapsack01(int[] wt, int[] val, int W) {
            int N = wt.length;
            int[][] dp = new int[N + 1][W + 1];

            for (int i = 1; i <= N; i++) {
                for (int w = 1; w <= W; w++) {
                    if (wt[i - 1] <= w) {
                        dp[i][w] = Math.max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w]);
                    } else {
                        dp[i][w] = dp[i - 1][w];
                    }
                }
            }

            int res = dp[N][W];
            List<Integer> selected = new ArrayList<>();
            int w = W;
            for (int i = N; i > 0 && res > 0; i--) {
                if (res != dp[i - 1][w]) {
                    selected.add(i - 1);
                    res -= val[i - 1];
                    w -= wt[i - 1];
                }
            }
            Collections.reverse(selected);
            System.out.printf("  0/1 Knapsack W=%d: Max value = %d, Selected items = %s%n", W, dp[N][W], selected);
        }

        static void lcs(String s1, String s2) {
            int m = s1.length(), n = s2.length();
            int[][] dp = new int[m + 1][n + 1];

            for (int i = 1; i <= m; i++) {
                for (int j = 1; j <= n; j++) {
                    if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                        dp[i][j] = dp[i - 1][j - 1] + 1;
                    } else {
                        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                    }
                }
            }

            StringBuilder sb = new StringBuilder();
            int i = m, j = n;
            while (i > 0 && j > 0) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    sb.append(s1.charAt(i - 1));
                    i--; j--;
                } else if (dp[i - 1][j] > dp[i][j - 1]) {
                    i--;
                } else {
                    j--;
                }
            }
            String lcsStr = sb.reverse().toString();
            System.out.printf("  LCS of '%s' and '%s': Length = %d, LCS = '%s'%n", s1, s2, dp[m][n], lcsStr);
        }

        static void levenshteinDistance(String s1, String s2) {
            int m = s1.length(), n = s2.length();
            int[][] dp = new int[m + 1][n + 1];
            for (int i = 0; i <= m; i++) dp[i][0] = i;
            for (int j = 0; j <= n; j++) dp[0][j] = j;

            for (int i = 1; i <= m; i++) {
                for (int j = 1; j <= n; j++) {
                    if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                        dp[i][j] = dp[i - 1][j - 1];
                    } else {
                        dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
                    }
                }
            }
            System.out.printf("  Levenshtein Distance ('%s' vs '%s') = %d%n", s1, s2, dp[m][n]);
        }

        static void matrixChainMultiplication(int[] p) {
            int n = p.length - 1;
            int[][] m = new int[n + 1][n + 1];
            for (int i = 1; i <= n; i++) m[i][i] = 0;

            for (int L = 2; L <= n; L++) {
                for (int i = 1; i <= n - L + 1; i++) {
                    int j = i + L - 1;
                    m[i][j] = Integer.MAX_VALUE;
                    for (int k = i; k <= j - 1; k++) {
                        int q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j];
                        if (q < m[i][j]) m[i][j] = q;
                    }
                }
            }
            System.out.printf("  MCM minimum multiplication cost = %d%n", m[1][n]);
        }

        static void kmpSearch(String txt, String pat) {
            int M = pat.length();
            int N = txt.length();
            int[] lps = new int[M];
            int j = 0;
            computeLPSArray(pat, M, lps);

            int i = 0;
            int matches = 0;
            while (i < N) {
                if (pat.charAt(j) == txt.charAt(i)) { j++; i++; }
                if (j == M) {
                    matches++;
                    j = lps[j - 1];
                } else if (i < N && pat.charAt(j) != txt.charAt(i)) {
                    if (j != 0) j = lps[j - 1];
                    else i = i + 1;
                }
            }
            System.out.printf("  KMP search: Found pattern '%s' in text %d times%n", pat, matches);
        }

        private static void computeLPSArray(String pat, int M, int[] lps) {
            int len = 0;
            int i = 1;
            lps[0] = 0;
            while (i < M) {
                if (pat.charAt(i) == pat.charAt(len)) {
                    len++; lps[i] = len; i++;
                } else {
                    if (len != 0) {
                        len = lps[len - 1];
                    } else {
                        lps[i] = 0; i++;
                    }
                }
            }
        }

        static void rabinKarpSearch(String txt, String pat) {
            int d = 256;
            int q = 101; // A prime number
            int M = pat.length();
            int N = txt.length();
            int i, j;
            int p = 0; // hash value for pattern
            int t = 0; // hash value for txt
            int h = 1;

            for (i = 0; i < M - 1; i++) h = (h * d) % q;

            for (i = 0; i < M; i++) {
                p = (d * p + pat.charAt(i)) % q;
                t = (d * t + txt.charAt(i)) % q;
            }

            int matches = 0;
            for (i = 0; i <= N - M; i++) {
                if (p == t) {
                    for (j = 0; j < M; j++) {
                        if (txt.charAt(i + j) != pat.charAt(j)) break;
                    }
                    if (j == M) matches++;
                }
                if (i < N - M) {
                    t = (d * (t - txt.charAt(i) * h) + txt.charAt(i + M)) % q;
                    if (t < 0) t = (t + q);
                }
            }
            System.out.printf("  Rabin-Karp: Found pattern '%s' in text %d times%n", pat, matches);
        }

        static void sortingDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("3.1  SORTING & BINARY SEARCH DEMO");
            System.out.println("=".repeat(60));
            int[] data1 = {64, 34, 25, 12, 22, 11, 90};
            bubbleSort(data1);
            System.out.println("  Bubble Sorted: " + Arrays.toString(data1));

            int[] data2 = {12, 11, 13, 5, 6, 7};
            quickSort(data2, 0, data2.length - 1);
            System.out.println("  Quick Sorted:  " + Arrays.toString(data2));

            int[] data3 = {38, 27, 43, 3, 9, 82, 10};
            mergeSort(data3, 0, data3.length - 1);
            System.out.println("  Merge Sorted:  " + Arrays.toString(data3));

            int[] data4 = {12, 34, 54, 2, 3};
            shellSort(data4);
            System.out.println("  Shell Sorted:  " + Arrays.toString(data4));

            int[] data5 = {10, 5, 2, 8, 7};
            countingSort(data5);
            System.out.println("  Counting Sorted: " + Arrays.toString(data5));

            int[] data6 = {170, 45, 75, 90, 802, 24, 2, 66};
            radixSort(data6);
            System.out.println("  Radix Sorted:    " + Arrays.toString(data6));

            int[] sorted = {10, 20, 20, 30, 40, 50};
            System.out.println("  BinarySearch lower_bound for 20 (index): " + binarySearchLowerBound(sorted, 20));
            System.out.println("  BinarySearch upper_bound for 20 (index): " + binarySearchUpperBound(sorted, 20));
        }

        static void pathfindingDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("3.2  PATHFINDING & MST ALGORITHMS DEMO");
            System.out.println("=".repeat(60));
            int[][] adjMat = {
                {0, 4, 0, 0, 0, 0},
                {4, 0, 8, 0, 0, 0},
                {0, 8, 0, 7, 0, 4},
                {0, 0, 7, 0, 9, 14},
                {0, 0, 0, 9, 0, 10},
                {0, 0, 4, 14, 10, 0}
            };
            dijkstra(adjMat, 0, 4);

            List<Edge> edges = List.of(
                new Edge(0, 1, 4),
                new Edge(0, 2, 3),
                new Edge(1, 2, 1),
                new Edge(1, 3, 2),
                new Edge(2, 3, 4)
            );
            bellmanFord(edges, 4, 0);

            int[][] fwGraph = {
                {0, 3, 1000000, 7},
                {8, 0, 2, 1000000},
                {5, 1000000, 0, 1},
                {2, 1000000, 1000000, 0}
            };
            floydWarshall(fwGraph);

            List<Edge> mstEdges = new ArrayList<>(List.of(
                new Edge(0, 1, 10),
                new Edge(0, 2, 6),
                new Edge(0, 3, 5),
                new Edge(1, 3, 15),
                new Edge(2, 3, 4)
            ));
            kruskalMST(mstEdges, 4);

            int[][] primGraph = {
                {0, 2, 0, 6, 0},
                {2, 0, 3, 8, 5},
                {0, 3, 0, 0, 7},
                {6, 8, 0, 0, 9},
                {0, 5, 7, 9, 0}
            };
            primMST(primGraph);
        }

        static void dpDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("3.3  DYNAMIC PROGRAMMING & STRING MATCHING DEMO");
            System.out.println("=".repeat(60));
            int[] wt = {2, 3, 4, 5};
            int[] val = {3, 4, 5, 6};
            knapsack01(wt, val, 8);

            lcs("ABCBDAB", "BDCAB");
            levenshteinDistance("kitten", "sitting");
            matrixChainMultiplication(new int[]{10, 20, 30, 40, 30});

            kmpSearch("ABABDABACDABABCABAB", "ABABCABAB");
            rabinKarpSearch("ABABDABACDABABCABAB", "ABABCABAB");
        }
"""
