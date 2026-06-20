# java_chunk1.py
# Phase 2 (Part 1): Linked Lists, Trees (BST, AVL, RBT, Segment Tree with Lazy Propagation, Trie), Skip List, and KD-Tree

chunk_content = r"""
        // ====================================================================
        // 2.1  Linked Lists — Singly, Doubly, and Circular Linked Lists
        // ====================================================================

        static class SinglyLinkedList<T> {
            private static class Node<T> {
                T value;
                Node<T> next;
                Node(T value, Node<T> next) { this.value = value; this.next = next; }
            }
            private Node<T> head;
            private int size;

            void insertAtHead(T value) {
                head = new Node<>(value, head);
                size++;
            }

            void insertAtTail(T value) {
                Node<T> newNode = new Node<>(value, null);
                if (head == null) { head = newNode; }
                else {
                    Node<T> current = head;
                    while (current.next != null) current = current.next;
                    current.next = newNode;
                }
                size++;
            }

            boolean delete(T value) {
                if (head == null) return false;
                if (Objects.equals(head.value, value)) {
                    head = head.next;
                    size--;
                    return true;
                }
                Node<T> current = head;
                while (current.next != null) {
                    if (Objects.equals(current.next.value, value)) {
                        current.next = current.next.next;
                        size--;
                        return true;
                    }
                    current = current.next;
                }
                return false;
            }

            boolean contains(T value) {
                Node<T> current = head;
                while (current != null) {
                    if (Objects.equals(current.value, value)) return true;
                    current = current.next;
                }
                return false;
            }

            void reverse() {
                Node<T> prev = null, current = head, next;
                while (current != null) {
                    next = current.next;
                    current.next = prev;
                    prev = current;
                    current = next;
                }
                head = prev;
            }

            int size() { return size; }

            @Override
            public String toString() {
                StringBuilder sb = new StringBuilder();
                Node<T> current = head;
                while (current != null) {
                    sb.append(current.value).append(" -> ");
                    current = current.next;
                }
                sb.append("null");
                return sb.toString();
            }
        }

        static class DoublyLinkedList<T> {
            private static class DNode<T> {
                T value;
                DNode<T> prev, next;
                DNode(T value, DNode<T> prev, DNode<T> next) {
                    this.value = value; this.prev = prev; this.next = next;
                }
            }
            private final DNode<T> sentinelHead = new DNode<>(null, null, null);
            private final DNode<T> sentinelTail = new DNode<>(null, null, null);
            private int size;

            DoublyLinkedList() {
                sentinelHead.next = sentinelTail;
                sentinelTail.prev = sentinelHead;
            }

            private DNode<T> insertBetween(T value, DNode<T> pred, DNode<T> succ) {
                DNode<T> node = new DNode<>(value, pred, succ);
                pred.next = node;
                succ.prev = node;
                size++;
                return node;
            }

            DNode<T> insertAtHead(T value) { return insertBetween(value, sentinelHead, sentinelHead.next); }
            DNode<T> insertAtTail(T value) { return insertBetween(value, sentinelTail.prev, sentinelTail); }

            void deleteNode(DNode<T> node) {
                if (node == sentinelHead || node == sentinelTail) return;
                node.prev.next = node.next;
                node.next.prev = node.prev;
                size--;
            }

            int size() { return size; }

            @Override
            public String toString() {
                StringBuilder sb = new StringBuilder();
                DNode<T> current = sentinelHead.next;
                while (current != sentinelTail) {
                    sb.append(current.value);
                    if (current.next != sentinelTail) sb.append(" <-> ");
                    current = current.next;
                }
                return sb.toString();
            }
        }

        static class CircularLinkedList<T> {
            private static class Node<T> {
                T value;
                Node<T> next;
                Node(T value) { this.value = value; }
            }
            private Node<T> head;
            private int size;

            void insert(T value) {
                Node<T> newNode = new Node<>(value);
                if (head == null) {
                    head = newNode;
                    head.next = head;
                } else {
                    Node<T> temp = head;
                    while (temp.next != head) {
                        temp = temp.next;
                    }
                    temp.next = newNode;
                    newNode.next = head;
                }
                size++;
            }

            @Override
            public String toString() {
                if (head == null) return "empty";
                StringBuilder sb = new StringBuilder();
                Node<T> temp = head;
                do {
                    sb.append(temp.value).append(" -> ");
                    temp = temp.next;
                } while (temp != head);
                sb.append("(head)");
                return sb.toString();
            }
        }

        static void linkedListDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("2.1  LINKED LISTS DEMO");
            System.out.println("=".repeat(60));
            var sll = new SinglyLinkedList<Integer>();
            for (int v : new int[]{10, 20, 30, 40}) sll.insertAtTail(v);
            System.out.println("  SinglyList Original:  " + sll);
            sll.insertAtHead(5);
            sll.delete(30);
            sll.reverse();
            System.out.println("  SinglyList Reversed:  " + sll);

            var dll = new DoublyLinkedList<Integer>();
            dll.insertAtTail(10);
            var node30 = dll.insertAtTail(30);
            dll.insertAtTail(40);
            System.out.println("  DoublyList Original:  " + dll);
            dll.deleteNode(node30);
            dll.insertAtHead(5);
            System.out.println("  DoublyList Modified:  " + dll);

            var cll = new CircularLinkedList<Integer>();
            cll.insert(100);
            cll.insert(200);
            cll.insert(300);
            System.out.println("  CircularList:         " + cll);
        }

        // ====================================================================
        // 2.2  Trees — BST, AVL, Red-Black Tree, Segment Tree, Trie
        // ====================================================================

        static class BST {
            private static class BSTNode {
                int key;
                BSTNode left, right;
                BSTNode(int key) { this.key = key; }
            }
            private BSTNode root;

            void insert(int key) { root = insertRec(root, key); }
            private BSTNode insertRec(BSTNode node, int key) {
                if (node == null) return new BSTNode(key);
                if (key < node.key)      node.left  = insertRec(node.left, key);
                else if (key > node.key) node.right = insertRec(node.right, key);
                return node;
            }

            boolean search(int key) {
                BSTNode current = root;
                while (current != null) {
                    if (key == current.key) return true;
                    current = key < current.key ? current.left : current.right;
                }
                return false;
            }

            List<Integer> inorder() {
                List<Integer> result = new ArrayList<>();
                inorderRec(root, result);
                return result;
            }
            private void inorderRec(BSTNode node, List<Integer> result) {
                if (node == null) return;
                inorderRec(node.left, result);
                result.add(node.key);
                inorderRec(node.right, result);
            }

            void delete(int key) { root = deleteRec(root, key); }
            private BSTNode deleteRec(BSTNode node, int key) {
                if (node == null) return null;
                if (key < node.key)      node.left  = deleteRec(node.left, key);
                else if (key > node.key) node.right = deleteRec(node.right, key);
                else {
                    if (node.left == null)  return node.right;
                    if (node.right == null) return node.left;
                    BSTNode successor = node.right;
                    while (successor.left != null) successor = successor.left;
                    node.key = successor.key;
                    node.right = deleteRec(node.right, successor.key);
                }
                return node;
            }
        }

        static class AVLTree {
            private static class AVLNode {
                int key, height;
                AVLNode left, right;
                AVLNode(int key) { this.key = key; this.height = 1; }
            }
            private AVLNode root;

            private int height(AVLNode n) { return n == null ? 0 : n.height; }
            private int balanceFactor(AVLNode n) { return n == null ? 0 : height(n.left) - height(n.right); }
            private void updateHeight(AVLNode n) { n.height = 1 + Math.max(height(n.left), height(n.right)); }

            private AVLNode rotateRight(AVLNode y) {
                AVLNode x = y.left;
                AVLNode T2 = x.right;
                x.right = y;
                y.left = T2;
                updateHeight(y);
                updateHeight(x);
                return x;
            }

            private AVLNode rotateLeft(AVLNode x) {
                AVLNode y = x.right;
                AVLNode T2 = y.left;
                y.left = x;
                x.right = T2;
                updateHeight(x);
                updateHeight(y);
                return y;
            }

            void insert(int key) { root = insertRec(root, key); }
            private AVLNode insertRec(AVLNode node, int key) {
                if (node == null) return new AVLNode(key);
                if (key < node.key)      node.left  = insertRec(node.left, key);
                else if (key > node.key) node.right = insertRec(node.right, key);
                else return node;

                updateHeight(node);
                int balance = balanceFactor(node);

                if (balance > 1 && key < node.left.key)   return rotateRight(node);
                if (balance < -1 && key > node.right.key) return rotateLeft(node);
                if (balance > 1 && key > node.left.key) {
                    node.left = rotateLeft(node.left);
                    return rotateRight(node);
                }
                if (balance < -1 && key < node.right.key) {
                    node.right = rotateRight(node.right);
                    return rotateLeft(node);
                }
                return node;
            }

            List<Integer> inorder() {
                List<Integer> result = new ArrayList<>();
                inorderRec(root, result);
                return result;
            }
            private void inorderRec(AVLNode node, List<Integer> result) {
                if (node == null) return;
                inorderRec(node.left, result);
                result.add(node.key);
                inorderRec(node.right, result);
            }
        }

        static class RedBlackTree {
            private static final boolean RED = true;
            private static final boolean BLACK = false;

            private static class Node {
                int data;
                boolean color;
                Node left, right, parent;
                Node(int data) {
                    this.data = data;
                    this.color = RED;
                }
            }

            private Node root;

            private void leftRotate(Node x) {
                Node y = x.right;
                x.right = y.left;
                if (y.left != null) y.left.parent = x;
                y.parent = x.parent;
                if (x.parent == null) root = y;
                else if (x == x.parent.left) x.parent.left = y;
                else x.parent.right = y;
                y.left = x;
                x.parent = y;
            }

            private void rightRotate(Node x) {
                Node y = x.left;
                x.left = y.right;
                if (y.right != null) y.right.parent = x;
                y.parent = x.parent;
                if (x.parent == null) root = y;
                else if (x == x.parent.right) x.parent.right = y;
                else x.parent.left = y;
                y.right = x;
                x.parent = y;
            }

            void insert(int data) {
                Node node = new Node(data);
                Node y = null;
                Node x = root;
                while (x != null) {
                    y = x;
                    if (node.data < x.data) x = x.left;
                    else x = x.right;
                }
                node.parent = y;
                if (y == null) root = node;
                else if (node.data < y.data) y.left = node;
                else y.right = node;

                if (node.parent == null) {
                    node.color = BLACK;
                    return;
                }
                if (node.parent.parent == null) return;
                fixInsert(node);
            }

            private void fixInsert(Node k) {
                Node u;
                while (k.parent != null && k.parent.color == RED) {
                    if (k.parent == k.parent.parent.right) {
                        u = k.parent.parent.left;
                        if (u != null && u.color == RED) {
                            u.color = BLACK;
                            k.parent.color = BLACK;
                            k.parent.parent.color = RED;
                            k = k.parent.parent;
                        } else {
                            if (k == k.parent.left) {
                                k = k.parent;
                                rightRotate(k);
                            }
                            k.parent.color = BLACK;
                            k.parent.parent.color = RED;
                            leftRotate(k.parent.parent);
                        }
                    } else {
                        u = k.parent.parent.right;
                        if (u != null && u.color == RED) {
                            u.color = BLACK;
                            k.parent.color = BLACK;
                            k.parent.parent.color = RED;
                            k = k.parent.parent;
                        } else {
                            if (k == k.parent.right) {
                                k = k.parent;
                                leftRotate(k);
                            }
                            k.parent.color = BLACK;
                            k.parent.parent.color = RED;
                            rightRotate(k.parent.parent);
                        }
                    }
                    if (k == root) break;
                }
                root.color = BLACK;
            }

            List<String> inorder() {
                List<String> result = new ArrayList<>();
                inorderRec(root, result);
                return result;
            }
            private void inorderRec(Node node, List<String> result) {
                if (node == null) return;
                inorderRec(node.left, result);
                result.add(node.data + (node.color == RED ? "(R)" : "(B)"));
                inorderRec(node.right, result);
            }
        }

        static class SegmentTree {
            private final int[] tree;
            private final int[] lazy;
            private final int n;

            SegmentTree(int[] arr) {
                this.n = arr.length;
                this.tree = new int[4 * n];
                this.lazy = new int[4 * n];
                build(arr, 0, 0, n - 1);
            }

            private void build(int[] arr, int node, int start, int end) {
                if (start == end) {
                    tree[node] = arr[start];
                    return;
                }
                int mid = (start + end) / 2;
                build(arr, 2 * node + 1, start, mid);
                build(arr, 2 * node + 2, mid + 1, end);
                tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
            }

            void updateRange(int l, int r, int diff) {
                updateRangeRec(0, 0, n - 1, l, r, diff);
            }

            private void updateRangeRec(int node, int start, int end, int l, int r, int diff) {
                if (lazy[node] != 0) {
                    tree[node] += (end - start + 1) * lazy[node];
                    if (start != end) {
                        lazy[2 * node + 1] += lazy[node];
                        lazy[2 * node + 2] += lazy[node];
                    }
                    lazy[node] = 0;
                }
                if (start > end || start > r || end < l) return;
                if (start >= l && end <= r) {
                    tree[node] += (end - start + 1) * diff;
                    if (start != end) {
                        lazy[2 * node + 1] += diff;
                        lazy[2 * node + 2] += diff;
                    }
                    return;
                }
                int mid = (start + end) / 2;
                updateRangeRec(2 * node + 1, start, mid, l, r, diff);
                updateRangeRec(2 * node + 2, mid + 1, end, l, r, diff);
                tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
            }

            int queryRange(int l, int r) {
                return queryRangeRec(0, 0, n - 1, l, r);
            }

            private int queryRangeRec(int node, int start, int end, int l, int r) {
                if (start > end || start > r || end < l) return 0;
                if (lazy[node] != 0) {
                    tree[node] += (end - start + 1) * lazy[node];
                    if (start != end) {
                        lazy[2 * node + 1] += lazy[node];
                        lazy[2 * node + 2] += lazy[node];
                    }
                    lazy[node] = 0;
                }
                if (start >= l && end <= r) return tree[node];
                int mid = (start + end) / 2;
                return queryRangeRec(2 * node + 1, start, mid, l, r) +
                       queryRangeRec(2 * node + 2, mid + 1, end, l, r);
            }
        }

        static class Trie {
            private static class TrieNode {
                Map<Character, TrieNode> children = new HashMap<>();
                boolean isWord;
            }
            private final TrieNode root = new TrieNode();

            void insert(String word) {
                TrieNode curr = root;
                for (char ch : word.toCharArray()) {
                    curr = curr.children.computeIfAbsent(ch, k -> new TrieNode());
                }
                curr.isWord = true;
            }

            boolean search(String word) {
                TrieNode curr = root;
                for (char ch : word.toCharArray()) {
                    curr = curr.children.get(ch);
                    if (curr == null) return false;
                }
                return curr.isWord;
            }

            List<String> getSuggestions(String prefix) {
                List<String> suggestions = new ArrayList<>();
                TrieNode curr = root;
                for (char ch : prefix.toCharArray()) {
                    curr = curr.children.get(ch);
                    if (curr == null) return suggestions;
                }
                suggestRec(curr, prefix, suggestions);
                return suggestions;
            }

            private void suggestRec(TrieNode node, String current, List<String> suggestions) {
                if (node.isWord) suggestions.add(current);
                for (var entry : node.children.entrySet()) {
                    suggestRec(entry.getValue(), current + entry.getKey(), suggestions);
                }
            }
        }

        // ====================================================================
        // 2.3  Search & Spatial Structures — Skip List and KD-Tree
        // ====================================================================

        static class SkipList {
            private static final int MAX_LEVEL = 4;
            private static class Node {
                int key;
                Node[] forward;
                Node(int key, int level) {
                    this.key = key;
                    this.forward = new Node[level + 1];
                }
            }
            private final Node head = new Node(-1, MAX_LEVEL);
            private int level = 0;

            void insert(int key) {
                Node[] update = new Node[MAX_LEVEL + 1];
                Node curr = head;
                for (int i = level; i >= 0; i--) {
                    while (curr.forward[i] != null && curr.forward[i].key < key) {
                        curr = curr.forward[i];
                    }
                    update[i] = curr;
                }
                curr = (curr.forward[0] != null) ? curr.forward[0] : null;

                if (curr == null || curr.key != key) {
                    int rLevel = randomLevel();
                    if (rLevel > level) {
                        for (int i = level + 1; i <= rLevel; i++) {
                            update[i] = head;
                        }
                        level = rLevel;
                    }
                    Node newNode = new Node(key, rLevel);
                    for (int i = 0; i <= rLevel; i++) {
                        newNode.forward[i] = update[i].forward[i];
                        update[i].forward[i] = newNode;
                    }
                }
            }

            boolean search(int key) {
                Node curr = head;
                for (int i = level; i >= 0; i--) {
                    while (curr.forward[i] != null && curr.forward[i].key < key) {
                        curr = curr.forward[i];
                    }
                }
                curr = curr.forward[0];
                return curr != null && curr.key == key;
            }

            private int randomLevel() {
                int lvl = 0;
                while (ThreadLocalRandom.current().nextDouble() < 0.5 && lvl < MAX_LEVEL) {
                    lvl++;
                }
                return lvl;
            }

            List<Integer> toList() {
                List<Integer> list = new ArrayList<>();
                Node curr = head.forward[0];
                while (curr != null) {
                    list.add(curr.key);
                    curr = curr.forward[0];
                }
                return list;
            }
        }

        static class KDTree {
            private static class Node {
                double[] point;
                Node left, right;
                Node(double[] pt) { this.point = pt; }
            }
            private Node root;

            void insert(double[] point) { root = insertRec(root, point, 0); }
            private Node insertRec(Node node, double[] point, int depth) {
                if (node == null) return new Node(point);
                int cd = depth % 2;
                if (point[cd] < node.point[cd]) {
                    node.left = insertRec(node.left, point, depth + 1);
                } else {
                    node.right = insertRec(node.right, point, depth + 1);
                }
                return node;
            }

            double[] nearest(double[] target) {
                BestNode best = new BestNode();
                nearestRec(root, target, 0, best);
                return best.point;
            }

            private static class BestNode {
                double[] point;
                double dist = Double.MAX_VALUE;
            }

            private void nearestRec(Node node, double[] target, int depth, BestNode best) {
                if (node == null) return;
                double d = distance(node.point, target);
                if (d < best.dist) {
                    best.dist = d;
                    best.point = node.point;
                }
                int cd = depth % 2;
                Node next = target[cd] < node.point[cd] ? node.left : node.right;
                Node other = target[cd] < node.point[cd] ? node.right : node.left;

                nearestRec(next, target, depth + 1, best);
                if (Math.abs(target[cd] - node.point[cd]) < best.dist) {
                    nearestRec(other, target, depth + 1, best);
                }
            }

            private double distance(double[] a, double[] b) {
                return Math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]));
            }
        }

        static void treeDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("2.2  TREE & SPATIAL DATA STRUCTURES DEMO");
            System.out.println("=".repeat(60));
            var bst = new BST();
            for (int k : new int[]{50, 30, 70, 20, 40}) bst.insert(k);
            System.out.println("  BST Inorder:        " + bst.inorder());
            bst.delete(30);
            System.out.println("  BST post delete(30):" + bst.inorder());

            var avl = new AVLTree();
            for (int k : new int[]{10, 20, 30, 40, 50, 25}) avl.insert(k);
            System.out.println("  AVL Inorder:        " + avl.inorder());

            var rbt = new RedBlackTree();
            for (int k : new int[]{7, 3, 18, 10, 22, 8, 11}) rbt.insert(k);
            System.out.println("  RBT (Color-tagged): " + rbt.inorder());

            var trie = new Trie();
            trie.insert("algorithm");
            trie.insert("algol");
            trie.insert("alligator");
            System.out.println("  Trie contains 'algol': " + trie.search("algol"));
            System.out.println("  Trie suggestions for 'algo': " + trie.getSuggestions("algo"));

            int[] arr = {1, 3, 5, 7, 9, 11};
            var segTree = new SegmentTree(arr);
            System.out.println("  SegmentTree RangeSum[1..3] (expected 15): " + segTree.queryRange(1, 3));
            segTree.updateRange(1, 5, 2);
            System.out.println("  SegmentTree RangeSum[1..3] post update (expected 21): " + segTree.queryRange(1, 3));

            var skip = new SkipList();
            skip.insert(3);
            skip.insert(6);
            skip.insert(9);
            skip.insert(2);
            System.out.println("  SkipList contains 6: " + skip.search(6));
            System.out.println("  SkipList values: " + skip.toList());

            var kd = new KDTree();
            kd.insert(new double[]{2.0, 3.0});
            kd.insert(new double[]{5.0, 4.0});
            kd.insert(new double[]{9.0, 6.0});
            double[] nearestPoint = kd.nearest(new double[]{4.5, 3.5});
            System.out.printf("  KDTree nearest to (4.5, 3.5): (%.1f, %.1f)%n", nearestPoint[0], nearestPoint[1]);
        }
"""
