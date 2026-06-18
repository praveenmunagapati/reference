# add_demos.py
# Adds the missing lists_bst_demo, balanced_trees_demo, structures_trie_heap_hash_demo, and graphs_demo
# to build_cs_ds_encyclopedia_c.py to clear implicit function declaration and unused warnings.

with open("build_cs_ds_encyclopedia_c.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """    free(g);
}
''')"""

replacement = """    free(g);
}

static void lists_bst_demo(void) {
    print_sep("2.1, 2.2 LINKED LISTS & BINARY SEARCH TREE");
    
    /* Singly list */
    SNode *s_head = NULL;
    s_head = slist_insert_head(s_head, 30);
    s_head = slist_insert_head(s_head, 10);
    s_head = slist_insert_head(s_head, 20);
    printf("  Original ");
    slist_print(s_head);
    slist_merge_sort(&s_head);
    printf("  Merge Sorted ");
    slist_print(s_head);
    s_head = slist_delete(s_head, 20);
    printf("  Deleted 20: ");
    slist_print(s_head);
    printf("  Cycle detected? %s\\n", slist_detect_cycle(s_head) ? "Yes" : "No");
    slist_free(s_head);

    /* Doubly list */
    DNode *d_head = NULL;
    d_head = dlist_insert_tail(d_head, 100);
    d_head = dlist_insert_tail(d_head, 200);
    d_head = dlist_insert_tail(d_head, 300);
    d_head = dlist_reverse(d_head);
    dlist_print(d_head);
    dlist_free(d_head);

    /* Circular list */
    CNode *c_head = NULL;
    c_head = clist_insert_end(c_head, 5);
    c_head = clist_insert_end(c_head, 6);
    c_head = clist_insert_end(c_head, 7);
    clist_print(c_head);
    CNode *c_head1 = NULL, *c_head2 = NULL;
    clist_split(c_head, &c_head1, &c_head2);
    printf("  Split Circular Lists:\\n");
    clist_print(c_head1);
    clist_print(c_head2);
    clist_free(c_head1);
    clist_free(c_head2);

    /* BST */
    BSTNode *bst_root = NULL;
    bst_root = bst_insert(bst_root, 15);
    bst_insert(bst_root, 10);
    bst_insert(bst_root, 20);
    printf("  BST Inorder: ");
    bst_inorder(bst_root);
    printf("\\n");
    bst_root = bst_delete(bst_root, 10);
    bst_free(bst_root);
}

static void balanced_trees_demo(void) {
    print_sep("2.3 BALANCED TREES (AVL & RED-BLACK)");

    /* AVL */
    AVLNode *avl_root = NULL;
    avl_root = avl_insert(avl_root, 10);
    avl_root = avl_insert(avl_root, 20);
    avl_root = avl_insert(avl_root, 30);
    printf("  AVL Inorder: ");
    avl_inorder(avl_root);
    printf("\\n");
    avl_free(avl_root);

    /* RBT */
    RBTNode *rbt_root = NULL;
    rbt_insert(&rbt_root, 7);
    rbt_insert(&rbt_root, 3);
    rbt_insert(&rbt_root, 18);
    printf("  RBT Inorder: ");
    rbt_inorder(rbt_root);
    printf("\\n");
    int error_flag = 0;
    verify_rbt_black_height(rbt_root, &error_flag);
    printf("  RBT black-height verify error flag: %d\\n", error_flag);
    rbt_free(rbt_root);
}

static void structures_trie_heap_hash_demo(void) {
    print_sep("2.4 TRIE, HEAPS, HASH TABLE");

    /* Trie */
    TrieNode *trie_root = trie_new_node();
    trie_insert(trie_root, "hello");
    trie_insert(trie_root, "helper");
    trie_insert(trie_root, "world");
    printf("  Trie search 'hello' (expected 1): %d, 'hell' (expected 0): %d\\n", 
           trie_search(trie_root, "hello"), trie_search(trie_root, "hell"));
    printf("  Trie autocomplete for 'he':\\n");
    trie_print_autocomplete(trie_root, "he");
    trie_free(trie_root);

    /* Heaps */
    MinHeap min_h = heap_create(10);
    heap_push(&min_h, 15);
    heap_push(&min_h, 5);
    heap_push(&min_h, 20);
    printf("  Min-Heap Pop (expected 5): %d\\n", heap_pop(&min_h));
    heap_free(&min_h);

    MaxHeap max_h = maxheap_create(10);
    maxheap_push(&max_h, 15);
    maxheap_push(&max_h, 5);
    maxheap_push(&max_h, 20);
    printf("  Max-Heap Pop (expected 20): %d\\n", maxheap_pop(&max_h));
    maxheap_free(&max_h);

    /* Hash Table */
    ChainHT ht = chain_ht_create(4);
    chain_ht_put(&ht, "computer", 101);
    chain_ht_put(&ht, "science", 202);
    printf("  Hash Get 'computer' (expected 101): %d, 'nonexistent' (expected -1): %d\\n",
           chain_ht_get(&ht, "computer", -1), chain_ht_get(&ht, "nonexistent", -1));
    chain_ht_free(&ht);
}

static void graphs_demo(void) {
    print_sep("2.5 GRAPH REPRESENTATIONS & ALGORITHMS");

    /* Matrix Graph */
    MatrixGraph m_g;
    graph_init(&m_g);
    graph_add_edge(&m_g, 5, 2);
    graph_add_edge(&m_g, 5, 0);
    graph_add_edge(&m_g, 4, 0);
    graph_add_edge(&m_g, 4, 1);
    graph_add_edge(&m_g, 2, 3);
    graph_add_edge(&m_g, 3, 1);
    graph_topological_sort(&m_g);

    /* List Graph */
    AdjListGraph *l_g = graph_list_create();
    graph_list_add_edge(l_g, 0, 1, 1);
    graph_list_add_edge(l_g, 0, 2, 1);
    graph_list_add_edge(l_g, 1, 2, 1);
    graph_list_add_edge(l_g, 2, 0, 1);
    graph_list_add_edge(l_g, 2, 3, 1);
    graph_list_add_edge(l_g, 3, 3, 1);
    graph_list_bfs(l_g, 2);
    graph_list_dfs(l_g, 2);
    printf("  Graph contains cycle? %s\\n", graph_list_has_cycle(l_g) ? "Yes" : "No");
    graph_list_free(l_g);
}
''')"""

# We want to replace target only once. Let's find target.
idx = content.find(target)
if idx == -1:
    print("Could not find the target end of Graph section in build_cs_ds_encyclopedia_c.py")
    exit(1)

content = content[:idx] + replacement + content[idx + len(target):]

with open("build_cs_ds_encyclopedia_c.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Demo functions added successfully to build_cs_ds_encyclopedia_c.py!")
