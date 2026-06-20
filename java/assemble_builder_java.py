# assemble_builder_java.py
# Assembles the clean build_cs_ds_encyclopedia_java.py from the base and the chunks

import os

# 1. Read build_cs_ds_encyclopedia_java.py to extract the clean base content
with open("build_cs_ds_encyclopedia_java.py", "r", encoding="utf-8") as f:
    orig_content = f.read()

# The base content ends right before PHASE_2_HEADER was defined.
cut_idx = orig_content.find("PHASE_2_HEADER")
if cut_idx == -1:
    print("Could not find PHASE_2_HEADER in build_cs_ds_encyclopedia_java.py")
    exit(1)

# Find the end of the previous section (which is the closing quote of PHASE_1D)
end_base_idx = orig_content.rfind("'''", 0, cut_idx)
if end_base_idx == -1:
    print("Could not find the closing quote of Phase 1 section")
    exit(1)

base_content = orig_content[:end_base_idx + 4] # Keep the closing ''')
print("Base content length:", len(base_content))

# 2. Let's load the chunk contents from the chunk files
c_quote = "'''"

# Chunk 1
import java_chunk1
chunk1 = java_chunk1.chunk_content

# Chunk 2
import java_chunk2
chunk2 = java_chunk2.chunk_content

# Chunk 3
import java_chunk3
chunk3 = java_chunk3.chunk_content

# Chunk 4
import java_chunk4
chunk4 = java_chunk4.chunk_content

# Chunk 5
import java_chunk5
chunk5 = java_chunk5.chunk_content

# We construct the phases as builder section calls
phases_content = f"""
# ---------------------------------------------------------------------------
# PHASE 2: TEMPLATED DATA STRUCTURES (PART 1)
# ---------------------------------------------------------------------------
PHASE_2_PART1 = emit(r{c_quote}
{chunk1}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 2: DATA STRUCTURES (PART 2) & PHASE 3: ALGORITHMS
# ---------------------------------------------------------------------------
PHASE_2_PART2_PHASE_3 = emit(r{c_quote}
{chunk2}
{c_quote})

# ---------------------------------------------------------------------------
# PHASE 4: 23 GoF DESIGN PATTERNS
# ---------------------------------------------------------------------------
PHASE_4_DESIGN_PATTERNS = emit(r{c_quote}
{chunk3}
{c_quote})

# ---------------------------------------------------------------------------
# PHASES 5-7: COLLECTIONS, STREAMS, AND CONCURRENCY
# ---------------------------------------------------------------------------
PHASES_5_7_COLLECTIONS_CONCURRENCY = emit(r{c_quote}
{chunk4}
{c_quote})

# ---------------------------------------------------------------------------
# PHASES 8-11: STATISTICAL & ML, STACK VM, BUG CHALLENGES, AND LECTURES
# ---------------------------------------------------------------------------
PHASES_8_11_ML_VM_BUGS_LECTURES = emit(r{c_quote}
{chunk5}
{c_quote})
"""

# Java Entry Point Main method section
main_section = f"""
# ---------------------------------------------------------------------------
# MAIN METHOD
# ---------------------------------------------------------------------------
MAIN_METHOD = emit(r{c_quote}
        public static void main(String[] args) throws Exception {{
            System.out.println("============================================================");
            System.out.println("      STARTING COMPREHENSIVE JAVA CS & DS ENCYCLOPEDIA");
            System.out.println("============================================================");

            // Phase 1: Java Core & OOP
            coreTypesDemo();
            controlFlowDemo();
            oopDemo();
            enumRecordSealedDemo();

            // Phase 2: Data Structures (Part 1)
            linkedListDemo();
            treeDemo();

            // Phase 2 (Part 2) & Phase 3: Algorithms
            graphDemo();
            sortingDemo();
            pathfindingDemo();
            dpDemo();

            // Phase 4: All 23 GoF Design Patterns
            designPatternsDemo();

            // Phase 5-7: Collections, Streams, Concurrency
            collectionsDemo();
            streamsDemo();
            concurrencyDemo();

            // Phase 8-11: ML, Systems VM, Debug challenges, Academic Lectures
            mlDemo();
            systemsVM_Demo();
            bugChallenges();
            academicLectures();
            complexityCheatSheet();

            System.out.println("\\n============================================================");
            System.out.println("      JAVA ENCYCLOPEDIA EXECUTED SUCCESSFULLY");
            System.out.println("============================================================");
        }}
{c_quote})

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
FOOTER = emit(r{c_quote}
    }} // end class JAVA_CS_DS_ENCYCLOPEDIA
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
        PHASE_1_HEADER, PHASE_1A, PHASE_1B, PHASE_1C, PHASE_1D,
        PHASE_2_PART1,
        PHASE_2_PART2_PHASE_3,
        PHASE_4_DESIGN_PATTERNS,
        PHASES_5_7_COLLECTIONS_CONCURRENCY,
        PHASES_8_11_ML_VM_BUGS_LECTURES,
        MAIN_METHOD,
        FOOTER,
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
    print("  Curriculum Coverage:")
    print("  " + "-" * 50)
    print("  Phase 1: Java Core, Internals & OOP          OK")
    print("  Phase 2: Data Structures (Pure CS)            OK")
    print("  Phase 3: Algorithms & Dynamic Programming     OK")
    print("  Phase 4: Design Patterns (GoF)                OK")
    print("  Phase 5: Collections & Generics Deep Dive     OK")
    print("  Phase 6: Streams & Functional Programming     OK")
    print("  Phase 7: Concurrency & Multithreading         OK")
    print("  Phase 8: Statistical & ML from Scratch        OK")
    print("  Phase 9: Systems Stack VM & Assembler         OK")
    print("  Phase 10: 15 Debug Challenges (Gotchas)       OK")
    print("  Phase 11: Academic Textbook Lectures          OK")
    print("  " + "-" * 50)
    print()
    print("  Compile & Run:")
    print(f"    javac -encoding utf-8 {OUTPUT}")
    print(f"    java JAVA_CS_DS_ENCYCLOPEDIA")

if __name__ == "__main__":
    main()
"""
)

# Replace the original build_cs_ds_encyclopedia_java.py
with open("build_cs_ds_encyclopedia_java.py", "w", encoding="utf-8") as f:
    f.write(assembled_content)

print("Assembled Java builder script successfully!")
