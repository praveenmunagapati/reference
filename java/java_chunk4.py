# java_chunk4.py
# Phase 5: Collections Framework Deep Dive
# Phase 6: Streams & Functional Programming
# Phase 7: Concurrency & Multithreading (including Custom Bounded Buffer and Custom ThreadPool)

chunk_content = r"""
        // ====================================================================
        // 5.1  Collections Framework Deep Dive
        // ====================================================================

        static void collectionsDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("5.1  COLLECTIONS FRAMEWORK DEMO");
            System.out.println("=".repeat(60));

            // --- List implementations ---
            List<String> arrList = new ArrayList<>();
            arrList.add("A"); arrList.add("B"); arrList.add("C");
            List<String> lnkList = new LinkedList<>(arrList);
            Collections.sort(lnkList);
            System.out.println("  ArrayList:  " + arrList);
            System.out.println("  LinkedList: " + lnkList);

            // --- Set implementations ---
            Set<String> hashSet = new HashSet<>();
            Set<String> linkedHashSet = new LinkedHashSet<>();
            Set<String> treeSet = new TreeSet<>();
            for (String val : new String[]{"apple", "banana", "cherry"}) {
                hashSet.add(val); linkedHashSet.add(val); treeSet.add(val);
            }
            System.out.println("  HashSet:       " + hashSet);
            System.out.println("  LinkedHashSet: " + linkedHashSet);
            System.out.println("  TreeSet:       " + treeSet);

            // --- Map implementations ---
            Map<String, Integer> hashMap = new HashMap<>();
            hashMap.put("Alice", 90); hashMap.put("Bob", 85); hashMap.put("Charlie", 92);
            System.out.println("  HashMap:       " + hashMap);
            System.out.println("  getOrDefault:  " + hashMap.getOrDefault("Dave", 0));

            // --- Queue & Deque ---
            PriorityQueue<Integer> pq = new PriorityQueue<>();
            pq.add(30); pq.add(10); pq.add(20);
            System.out.print("  PriorityQueue: ");
            while (!pq.isEmpty()) System.out.print(pq.poll() + " ");
            System.out.println();

            Deque<String> stack = new ArrayDeque<>();
            stack.push("A"); stack.push("B"); stack.push("C");
            System.out.print("  ArrayDeque Stack: ");
            while (!stack.isEmpty()) System.out.print(stack.pop() + " ");
            System.out.println();

            // --- Comparable vs Comparator ---
            List<String> listComp = new ArrayList<>(List.of("banana", "apple", "date", "cherry"));
            listComp.sort(Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder()));
            System.out.println("  Sorted by length then alpha: " + listComp);
        }

        // ====================================================================
        // 6.1  Streams & Functional Programming
        // ====================================================================

        static void streamsDemo() {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("6.1  STREAMS & FUNCTIONAL PROGRAMMING DEMO");
            System.out.println("=".repeat(60));

            List<String> names = List.of("Alice", "Bob", "Charlie", "Diana", "Eve", "Frank");

            // Filter and Map
            List<String> filtered = names.stream()
                .filter(name -> name.length() > 3)
                .map(String::toUpperCase)
                .collect(Collectors.toList());
            System.out.println("  Filtered + Mapped: " + filtered);

            // Sum of name lengths
            int totalLength = names.stream()
                .mapToInt(String::length)
                .sum();
            System.out.println("  Sum of name lengths: " + totalLength);

            // GroupingBy
            Map<Integer, List<String>> grouped = names.stream()
                .collect(Collectors.groupingBy(String::length));
            System.out.println("  Grouped by length: " + grouped);

            // PartitioningBy
            Map<Boolean, List<String>> partitioned = names.stream()
                .collect(Collectors.partitioningBy(name -> name.length() > 3));
            System.out.println("  Partitioned (len > 3): " + partitioned);

            // FlatMap
            List<List<Integer>> nestedList = List.of(List.of(1, 2), List.of(3, 4, 5));
            List<Integer> flatList = nestedList.stream()
                .flatMap(List::stream)
                .collect(Collectors.toList());
            System.out.println("  FlatMap output: " + flatList);

            // Collector statistics
            IntSummaryStatistics stats = names.stream()
                .mapToInt(String::length)
                .summaryStatistics();
            System.out.printf("  Stats: count=%d, sum=%d, min=%d, max=%d, avg=%.2f%n",
                              stats.getCount(), stats.getSum(), stats.getMin(), stats.getMax(), stats.getAverage());

            // Optional findFirst
            Optional<String> firstC = names.stream()
                .filter(name -> name.startsWith("C"))
                .findFirst();
            System.out.println("  FindFirst starting with C: " + firstC.orElse("None"));
        }

        // ====================================================================
        // 7.1  Concurrency & Multithreading
        // ====================================================================

        // Custom Bounded Buffer (Producer-Consumer Queue) from scratch
        static class BoundedBuffer<T> {
            private final Object[] items;
            private int writeIdx, readIdx, count;
            private final ReentrantLock lock = new ReentrantLock();
            private final Condition notFull = lock.newCondition();
            private final Condition notEmpty = lock.newCondition();

            BoundedBuffer(int capacity) {
                this.items = new Object[capacity];
            }

            void put(T item) throws InterruptedException {
                lock.lock();
                try {
                    while (count == items.length) {
                        notFull.await();
                    }
                    items[writeIdx] = item;
                    writeIdx = (writeIdx + 1) % items.length;
                    count++;
                    notEmpty.signal();
                } finally {
                    lock.unlock();
                }
            }

            @SuppressWarnings("unchecked")
            T take() throws InterruptedException {
                lock.lock();
                try {
                    while (count == 0) {
                        notEmpty.await();
                    }
                    T item = (T) items[readIdx];
                    readIdx = (readIdx + 1) % items.length;
                    count--;
                    notFull.signal();
                    return item;
                } finally {
                    lock.unlock();
                }
            }
        }

        // Custom ThreadPool from scratch
        static class CustomThreadPool {
            private final BlockingQueue<Runnable> taskQueue;
            private final List<WorkerThread> workers;
            private volatile boolean isShutdown = false;

            CustomThreadPool(int numThreads) {
                taskQueue = new LinkedBlockingQueue<>();
                workers = new ArrayList<>();
                for (int i = 0; i < numThreads; i++) {
                    WorkerThread t = new WorkerThread("PoolWorker-" + i);
                    workers.add(t);
                    t.start();
                }
            }

            void execute(Runnable r) {
                if (isShutdown) throw new IllegalStateException("ThreadPool has been shutdown!");
                taskQueue.offer(r);
            }

            void shutdown() {
                isShutdown = true;
                for (WorkerThread worker : workers) {
                    worker.interrupt();
                }
            }

            private class WorkerThread extends Thread {
                WorkerThread(String name) { super(name); }
                @Override
                public void run() {
                    while (!isShutdown || !taskQueue.isEmpty()) {
                        try {
                            Runnable task = taskQueue.poll(500, TimeUnit.MILLISECONDS);
                            if (task != null) {
                                task.run();
                            }
                        } catch (InterruptedException e) {
                            break;
                        }
                    }
                }
            }
        }

        static class AtomicCounter {
            private final AtomicInteger val = new AtomicInteger(0);
            void increment() { val.incrementAndGet(); }
            int get() { return val.get(); }
        }

        // ForkJoinPool Parallel Merge Sort
        static class ParallelMergeSort extends RecursiveAction {
            private final int[] arr;
            private final int left, right;
            private static final int THRESHOLD = 2; // Low threshold for demo

            ParallelMergeSort(int[] arr, int left, int right) {
                this.arr = arr; this.left = left; this.right = right;
            }

            @Override
            protected void compute() {
                if (right - left < THRESHOLD) {
                    mergeSort(arr, left, right);
                } else {
                    int mid = left + (right - left) / 2;
                    invokeAll(new ParallelMergeSort(arr, left, mid),
                              new ParallelMergeSort(arr, mid + 1, right));
                    merge(arr, left, mid, right);
                }
            }
        }

        static void concurrencyDemo() throws Exception {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("7.1  CONCURRENCY & MULTITHREADING DEMO");
            System.out.println("=".repeat(60));

            // Atomic counter demo
            final AtomicCounter counter = new AtomicCounter();
            int numThreads = 4;
            int incrementsPerThread = 250;
            ExecutorService exec = Executors.newFixedThreadPool(numThreads);
            List<Callable<Void>> tasks = new ArrayList<>();
            for (int i = 0; i < numThreads; i++) {
                tasks.add(() -> {
                    for (int j = 0; j < incrementsPerThread; j++) counter.increment();
                    return null;
                });
            }
            exec.invokeAll(tasks);
            exec.shutdown();
            System.out.println("  AtomicCounter (expected 1000): " + counter.get());

            // CompletableFuture chaining
            CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "hello")
                .thenApplyAsync(s -> s + " world")
                .thenApply(String::toUpperCase);
            System.out.println("  CompletableFuture async: " + future.get());

            // Bounded Buffer (Producer-Consumer)
            var buffer = new BoundedBuffer<String>(3);
            Thread producer = new Thread(() -> {
                try {
                    for (int i = 0; i < 5; i++) {
                        buffer.put("Item-" + i);
                    }
                } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            });
            Thread consumer = new Thread(() -> {
                try {
                    for (int i = 0; i < 5; i++) {
                        System.out.println("    Consumed: " + buffer.take());
                    }
                } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            });
            consumer.start();
            producer.start();
            producer.join();
            consumer.join();

            // ReentrantReadWriteLock
            ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
            var readLock = rwLock.readLock();
            var writeLock = rwLock.writeLock();
            readLock.lock();
            System.out.println("  ReadWriteLock: Read lock acquired.");
            readLock.unlock();
            writeLock.lock();
            System.out.println("  ReadWriteLock: Write lock acquired.");
            writeLock.unlock();

            // Custom ThreadPool
            System.out.println("  Launching tasks on custom ThreadPool...");
            CustomThreadPool pool = new CustomThreadPool(2);
            for (int i = 0; i < 4; i++) {
                final int id = i;
                pool.execute(() -> System.out.println("    [CustomPool] Task " + id + " running on thread: " + Thread.currentThread().getName()));
            }
            Thread.sleep(1000);
            pool.shutdown();
            System.out.println("  Custom ThreadPool shutdown complete.");

            // ForkJoinPool parallel sort
            int[] fjData = {99, 12, 45, 67, 34, 11, 89, 90, 2, 7};
            ForkJoinPool fjp = ForkJoinPool.commonPool();
            fjp.invoke(new ParallelMergeSort(fjData, 0, fjData.length - 1));
            System.out.println("  ForkJoinPool Parallel MergeSort: " + Arrays.toString(fjData));
        }
"""
