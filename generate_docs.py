import os

# Create docs directory
os.makedirs("docs", exist_ok=True)

# List of 57 document topics for CS Interview Coach
documents = [
    "DSA_Basics.md", "Arrays_Strings.md", "Linked_Lists.md", "Stacks_Queues.md",
    "Trees_BinaryTrees.md", "Binary_Search_Trees.md", "Heaps.md", "Graphs.md",
    "Hash_Tables.md", "Sorting_Algorithms.md", "Searching_Algorithms.md",
    "Dynamic_Programming.md", "Greedy_Algorithms.md", "Backtracking.md",
    "System_Design_Basics.md", "Design_Twitter.md", "Design_Uber.md",
    "Design_Instagram.md", "Design_TikTok.md", "Load_Balancing.md",
    "Caching_Strategies.md", "Database_Sharding.md", "CAP_Theorem.md",
    "Operating_Systems.md", "Process_vs_Thread.md", "Deadlocks.md",
    "Memory_Management.md", "Scheduling_Algorithms.md", "DBMS_Basics.md",
    "SQL_vs_NoSQL.md", "Indexing.md", "Normalization.md", "ACID_Transactions.md",
    "Computer_Networks.md", "TCP_vs_UDP.md", "HTTP_HTTPS.md", "DNS.md",
    "OOP_Concepts.md", "SOLID_Principles.md", "Design_Patterns.md",
    "Behavioral_Questions.md", "STAR_Method.md", "Resume_Projects.md",
    "Two_Pointers.md", "Sliding_Window.md", "Binary_Search.md",
    "DFS_BFS.md", "Union_Find.md", "Trie.md", "Segment_Tree.md",
    "Fenwick_Tree.md", "Monotonic_Stack.md", "Top_K_Elements.md",
    "Bit_Manipulation.md", "System_Design_Templates.md", "Low_Level_Design.md"
]

for doc in documents:
    filepath = f"docs/{doc}"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {doc.replace('.md', '').replace('_', ' ')}\n\n")
        f.write("This is a placeholder document for Advanced RAG pipeline.\n")
        f.write("Content will be used for CS Interview preparation.\n")

print("✅ 57 documents created successfully in docs/ folder!")
print(f"Total files: {len(documents)}")