"""
Multi-owner test: registers two files from different owners, then tries
to register a merged file and verifies that the system correctly identifies
content from both owners with page-level attribution.
"""
import os
import sys
import json
import requests

API_BASE = "http://127.0.0.1:8000"
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Create test files
TEST_DIR = os.path.join(BACKEND_DIR, "test_multi_owner")
os.makedirs(TEST_DIR, exist_ok=True)

# File A -- owned by Alice
file_a_path = os.path.join(TEST_DIR, "alice_doc.txt")
with open(file_a_path, "w") as f:
    f.write("""Machine learning is a subset of artificial intelligence that provides systems
the ability to automatically learn and improve from experience without being
explicitly programmed. Machine learning focuses on the development of computer
programs that can access data and use it to learn for themselves.

The process of learning begins with observations or data, such as examples,
direct experience, or instruction, in order to look for patterns in data and
make better decisions in the future based on the examples that we provide.
The primary aim is to allow the computers to learn automatically without
human intervention or assistance and adjust actions accordingly.

Deep learning is a class of machine learning algorithms that uses multiple
layers to progressively extract higher-level features from raw input. For
example, in image processing, lower layers may identify edges, while higher
layers may identify the concepts relevant to a human such as digits or letters
or faces. Deep learning has been instrumental in advancing the state of the art
in various fields including computer vision and natural language processing.""")

# File B -- owned by Bob
file_b_path = os.path.join(TEST_DIR, "bob_doc.txt")
with open(file_b_path, "w") as f:
    f.write("""Blockchain is a system of recording information in a way that makes it
difficult or impossible to change, hack, or cheat the system. A blockchain
is essentially a digital ledger of transactions that is duplicated and
distributed across the entire network of computer systems on the blockchain.

Each block in the chain contains a number of transactions, and every time
a new transaction occurs on the blockchain, a record of that transaction is
added to every participant's ledger. The decentralised database managed by
multiple participants is known as Distributed Ledger Technology (DLT).

Smart contracts are simply programs stored on a blockchain that run when
predetermined conditions are met. They typically are used to automate the
execution of an agreement so that all participants can be immediately certain
of the outcome, without any intermediary's involvement or time loss. They
can also automate a workflow, triggering the next action when conditions
are met.""")

# File C -- merged from both
file_c_path = os.path.join(TEST_DIR, "merged_doc.txt")
with open(file_c_path, "w") as f:
    with open(file_a_path) as a:
        content_a = a.read()
    with open(file_b_path) as b:
        content_b = b.read()
    f.write(content_a + "\f" + content_b)


def register(filepath, owner_id, owner_name):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        resp = requests.post(
            f"{API_BASE}/ownership/register",
            files={"file": (filename, f, "text/plain")},
            data={"owner_id": owner_id, "owner_name": owner_name},
        )
    return resp.json()


def verify(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        resp = requests.post(
            f"{API_BASE}/ownership/verify",
            files={"file": (filename, f, "text/plain")},
        )
    return resp.json()


print("=" * 60)
print("MULTI-OWNER TEST")
print("=" * 60)

# Step 1: Register File A as Alice
print("\n1) Registering alice_doc.txt (Owner: Alice)...")
result_a = register(file_a_path, "alice_001", "Alice")
print(f"   Status: {result_a['status']}")

# Step 2: Register File B as Bob
print("\n2) Registering bob_doc.txt (Owner: Bob)...")
result_b = register(file_b_path, "bob_001", "Bob")
print(f"   Status: {result_b['status']}")

# Step 3: Try to register merged file
print("\n3) Attempting to register merged_doc.txt (should be BLOCKED)...")
result_c = register(file_c_path, "charlie_001", "Charlie")
print(f"   Status: {result_c['status']}")
print(f"   Message: {result_c.get('message', 'N/A')}")

if result_c["status"] == "similarity_detected":
    print("\n   [PASS] Registration correctly blocked!")
    print(f"   Overall similarity: {result_c['overall_similarity']}%")
    print(f"\n   Owners detected:")
    for owner in result_c.get("owners", []):
        print(f"     - {owner['owner_name']}: {owner['contribution']}% "
              f"({owner['pages_matched']} pages, avg {owner['avg_similarity']}% similarity)")
        if "matched_documents" in owner:
            print(f"       Source docs: {', '.join(owner['matched_documents'])}")

    print(f"\n   Page-level matches:")
    for m in result_c.get("matched_pages", []):
        print(f"     Merged Page {m['target_page']} -> {m['owner_name']}'s "
              f"'{m['matched_document']}' Page {m['matched_page']} "
              f"({m['similarity']}% {m['match_type']})")

    if result_c.get("unmatched_pages"):
        print(f"\n   Unmatched pages: {result_c['unmatched_pages']}")

    # Check multi-owner detection
    owner_names = [o["owner_name"] for o in result_c.get("owners", [])]
    if "Alice" in owner_names and "Bob" in owner_names:
        print("\n   [PASS] MULTI-OWNER DETECTION WORKS -- Both Alice and Bob identified!")
    else:
        print(f"\n   [FAIL] Expected both Alice and Bob, got: {owner_names}")
else:
    print(f"\n   [FAIL] Expected 'similarity_detected', got '{result_c['status']}'")

# Step 4: Also test verification endpoint
print("\n4) Verifying merged_doc.txt via /verify endpoint...")
result_v = verify(file_c_path)
print(f"   Status: {result_v['status']}")
print(f"   Overall similarity: {result_v['overall_similarity']}%")
if result_v.get("owners"):
    print(f"   Owners detected:")
    for owner in result_v["owners"]:
        print(f"     - {owner['owner_name']}: {owner['contribution']}% "
              f"({owner['pages_matched']} pages)")

    owner_names_v = [o["owner_name"] for o in result_v.get("owners", [])]
    if "Alice" in owner_names_v and "Bob" in owner_names_v:
        print("\n   [PASS] Verify endpoint also detects both owners!")
    else:
        print(f"\n   [FAIL] Verify expected both Alice and Bob, got: {owner_names_v}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

# Cleanup
import shutil
shutil.rmtree(TEST_DIR)
print("\nTest files cleaned up.")
