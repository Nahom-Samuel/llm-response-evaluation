
import json
from pathlib import Path

# Load exported annotations
file_path = Path("data/annotations.json")

with open(file_path, "r", encoding="utf-8") as f:
    annotations = json.load(f)

# Inspect the export structure
print("Total exported tasks:", len(annotations))

first_task = annotations[0]

print("\nTop-level keys:")
print(list(first_task.keys()))

print("\nFirst annotation:")
print(json.dumps(
    first_task.get("annotations", []),
    indent=2,
    ensure_ascii=False
))

def extract_evaluation(task):
    if not task.get("annotations"):
        return None

    annotation = task["annotations"][0]

    preference = None
    reason = None

    for result in annotation["result"]:

        if result["from_name"] == "preference":
            preference = result["value"]["choices"][0]

        elif result["from_name"] == "reason":
            reason = result["value"]["text"][0]

    return {
        "task_id": task["id"],
        "preference": preference,
        "reason": reason
    }
evaluations = []

for task in annotations:
    evaluation = extract_evaluation(task)

    if evaluation is not None:
        evaluations.append(evaluation)

print("\nExtracted evaluations:", len(evaluations))

for evaluation in evaluations:
    print(evaluation)

# Load the original annotation tasks
with open("data/annotation_tasks.json", "r", encoding="utf-8") as f:
    original_tasks = json.load(f)

# Compare original and exported tasks
for original, exported in zip(original_tasks, annotations):
    original_data = original["data"]
    exported_data = exported["data"]

    matches = original_data == exported_data

    print(
        f"Original task {original['id']} | "
        f"Label Studio task {exported['id']} | "
        f"Data matches: {matches}"
    )

# Load original human preferences
with open("data/answer_key.json", "r", encoding="utf-8") as f:
    answer_key = json.load(f)

# Create a lookup dictionary
reference_preferences = {
    item["task_id"]: item["preferred"]
    for item in answer_key
}

# Compare your annotations with the reference
matches = 0
results = []

for evaluation in evaluations:
    task_id = evaluation["task_id"]
    your_choice = evaluation["preference"]
    reference_choice = reference_preferences[task_id]

    is_match = your_choice == reference_choice

    if is_match:
        matches += 1

    results.append({
        "task_id": task_id,
        "your_choice": your_choice,
        "reference_choice": reference_choice,
        "match": is_match
    })

# Calculate agreement percentage
total = len(results)
agreement = (matches / total) * 100 if total else 0

print("\n--- EVALUATION RESULTS ---")
print(f"Total tasks: {total}")
print(f"Matches: {matches}")
print(f"Agreement: {agreement:.1f}%")

print("\nTask-by-task comparison:")
for result in results:
    print(
        f"Task {result['task_id']}: "
        f"Yours={result['your_choice']} | "
        f"Reference={result['reference_choice']} | "
        f"Match={result['match']}"
    )

# Inspect the first disagreement
task_id = 10

task = next(
    task for task in annotations
    if task["id"] == task_id
)

print(f"\n--- TASK {task_id} REVIEW ---")
print("CONTEXT:\n", task["data"]["context"])
print("\nUSER PROMPT:\n", task["data"]["prompt"])
print("\nRESPONSE A:\n", task["data"]["response_a"])
print("\nRESPONSE B:\n", task["data"]["response_b"])
