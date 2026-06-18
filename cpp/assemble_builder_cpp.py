# assemble_builder_cpp.py
# Assembles the clean build_cs_ds_encyclopedia_cpp.py from the base and the chunks

import os

# 1. Read build_cs_ds_encyclopedia_cpp.py to extract the clean base content
with open("build_cs_ds_encyclopedia_cpp.py", "r", encoding="utf-8") as f:
    orig_content = f.read()

# The base content ends right before PHASE_2_DSA_PART1 was appended.
cut_idx = orig_content.find("PHASE_2_DSA_PART1")
if cut_idx == -1:
    print("Could not find PHASE_2_DSA_PART1 in build_cs_ds_encyclopedia_cpp.py")
    exit(1)

# Find the end of the previous section (which is the closing quote of cxx17_types_demo)
end_base_idx = orig_content.rfind("''')", 0, cut_idx)
if end_base_idx == -1:
    print("Could not find the closing quote of Phase 1 section")
    exit(1)

base_content = orig_content[:end_base_idx + 4] # Keep the closing ''')
print("Base content length:", len(base_content))

# 2. Let's load the chunk contents from the chunk files
c_quote = "'''"

# Chunk 1
import cpp_chunk1
chunk1 = cpp_chunk1.chunk_content

# Chunk 2
import cpp_chunk2
chunk2 = cpp_chunk2.chunk_content

# Chunk 3
import cpp_chunk3
chunk3 = cpp_chunk3.chunk_content

# Chunk 4
import cpp_chunk4
chunk4 = cpp_chunk4.chunk_content

# Chunk 5
import cpp_chunk5
chunk5 = cpp_chunk5.chunk_content

# Chunk 6
import cpp_chunk6
chunk6 = cpp_chunk6.chunk_content

# We construct the phases as builder section calls
phases_content = f"""
# ---------------------------------------------------------------------------
# PHASE 2: TEMPLATED DATA STRUCTURES (PART 1)
# ---------------------------------------------------------------------------
PHASE_2_DSA_PART1 = emit(r{c_quote}
{chunk1}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 2: TEMPLATED DATA STRUCTURES (PART 2)
# ---------------------------------------------------------------------------
PHASE_2_DSA_PART2 = emit(r{c_quote}
{chunk2}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 3: ALGORITHMS & GRAPH/DP MASTERY & CUSTOM ALLOCATORS
# ---------------------------------------------------------------------------
PHASE_3_ALGS_ALLOCATORS = emit(r{c_quote}
{chunk3}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 4: 23 GoF DESIGN PATTERNS IN MODERN C++
# ---------------------------------------------------------------------------
PHASE_4_DESIGN_PATTERNS = emit(r{c_quote}
{chunk4}
{c_quote})

# ---------------------------------------------------------------------------
# PHASES 5-8: BITWISE, SERIALIZATION, METAPROGRAMMING & CONCURRENCY
# ---------------------------------------------------------------------------
PHASES_5_8_SYSTEMS_CONCURRENCY = emit(r{c_quote}
{chunk5}
{c_quote})

# ---------------------------------------------------------------------------
# PHASES 9-12: ML, STACK VM, DEBUG GOTCHAS & LECTURES
# ---------------------------------------------------------------------------
PHASES_9_12_ML_VM_BUGS_LECTURES = emit(r{c_quote}
{chunk6}
{c_quote})
"""

# C++ Entry Point Main section
main_section = f"""
# ---------------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------------
MAIN_CPP = emit(r{c_quote}
    int main() {{
        srand((unsigned int)time(NULL));
        
        cout << "============================================================\\n";
        cout << "      STARTING COMPREHENSIVE C++ CS & DS ENCYCLOPEDIA\\n";
        cout << "============================================================\\n";

        core_types_demo();
        smart_pointers_demo();
        move_semantics_demo();
        oop_demo();
        cxx17_types_demo();

        // Phase 2
        allocators_demo();
        oop_extension_demo();
        lists_demo();
        trees_demo();
        spatial_structures_demo();
        structures_trie_heap_hash_demo();
        graphs_demo();

        // Phase 3
        stl_demo();
        sorting_mst_demo();
        dp_demo();

        // Phase 4
        design_patterns_demo();

        // Phase 5-8
        bit_manipulation_demo();
        memory_layout_demo();
        strings_io_demo();
        preprocessor_demo();
        concurrency_demo();

        // Phase 9-12
        ml_demo();
        systems_vm_demo();
        bug_challenges_demo();
        complexity_cheat_sheet();

        /* Extra code verifications */
        cout << "\\n============================================================\\n";
        cout << "        ADDITIONAL COMPLEXITY VERIFICATIONS\\n";
        cout << "============================================================\\n";
        
        vector<int> hoare_arr = {{5, 2, 8, 1, 9}};
        quicksort_hoare(hoare_arr, 0, 4);
        cout << "    Hoare Sorted: ";
        for (int x : hoare_arr) cout << x << " ";
        cout << "\\n";

        vector<int> shell_arr = {{12, 34, 54, 2, 3}};
        shell_sort(shell_arr);
        cout << "    Shell Sorted: ";
        for (int x : shell_arr) cout << x << " ";
        cout << "\\n";

        Matrix m_det(3, 3);
        m_det(0,0)=1; m_det(0,1)=2; m_det(0,2)=3;
        m_det(1,0)=0; m_det(1,1)=1; m_det(1,2)=4;
        m_det(2,0)=5; m_det(2,1)=6; m_det(2,2)=0;
        cout << "    Matrix 3x3 Determinant: " << m_det.determinant_3x3() << "\\n";

        string rev_test = "Modern C++";
        reverse(rev_test.begin(), rev_test.end());
        cout << "    Reversed string: '" << rev_test << "'\\n";

        cout << "\\n============================================================\\n";
        cout << "      C++ ENCYCLOPEDIA EXECUTED SUCCESSFULY\\n";
        cout << "============================================================\\n";
        return 0;
    }}
{c_quote})
"""

# Append everything together
assembled_content = (
    base_content + "\n" +
    phases_content + "\n" +
    main_section + "\n" +
    # Write Python writer main logic at the end
    """
def main():
    sections = [
        HEADER,
        PHASE_1,
        PHASE_2_DSA_PART1,
        PHASE_2_DSA_PART2,
        PHASE_3_ALGS_ALLOCATORS,
        PHASE_4_DESIGN_PATTERNS,
        PHASES_5_8_SYSTEMS_CONCURRENCY,
        PHASES_9_12_ML_VM_BUGS_LECTURES,
        MAIN_CPP
    ]
    full = "\\n".join(sections)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT)
    with open(path, "w", encoding="utf-8") as f:
        f.write(full)

    lines = full.count("\\n") + 1
    print("=" * 70)
    print(f"  Successfully generated: {OUTPUT}")
    print(f"  Total lines written:    {lines:,}")
    print(f"  Location:               {path}")
    print("=" * 70)
    print()
    print("  Compile & Run:")
    print(f"    g++ -std=c++17 -Wall -Wextra -O2 -o encyclopedia {OUTPUT}")
    print(f"    ./encyclopedia")

if __name__ == "__main__":
    main()
"""
)

# Replace the original build_cs_ds_encyclopedia_cpp.py
with open("build_cs_ds_encyclopedia_cpp.py", "w", encoding="utf-8") as f:
    f.write(assembled_content)

print("Assembled builder script successfully!")
