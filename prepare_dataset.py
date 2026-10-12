
import random
import json
from datasets import load_dataset

# Make randomization reproducible
random.seed(42)

# Step 1: Load 10 examples
dataset = load_dataset(
    "Anthropic/hh-rlhf",
    split="train[:10]"
)


# Step 2: Extract the final assistant response
def extract_last_response(conversation):
    parts = conversation.rsplit("\n\nAssistant:", 1)
    return parts[-1].strip()


# Step 3: Extract the final user prompt and earlier context
def extract_prompt_and_context(conversation):
    before_response = conversation.rsplit("\n\nAssistant:", 1)[0]
    context, prompt = before_response.rsplit("\n\nHuman:", 1)
    return context.strip(), prompt.strip()


# Step 4: Prepare tasks and answer key
tasks = []
answer_key = []

for i, example in enumerate(dataset):

    chosen_context, chosen_prompt = extract_prompt_and_context(
        example["chosen"]
    )

    rejected_context, rejected_prompt = extract_prompt_and_context(
        example["rejected"]
    )

    # Skip examples with different prompts or contexts
    if (
        chosen_prompt != rejected_prompt
        or chosen_context != rejected_context
    ):
        continue

    chosen_response = extract_last_response(example["chosen"])
    rejected_response = extract_last_response(example["rejected"])

    # Randomly assign the responses to A and B
    if random.choice([True, False]):
        response_a = chosen_response
        response_b = rejected_response
        preferred = "A"
    else:
        response_a = rejected_response
        response_b = chosen_response
        preferred = "B"

    task_id = i + 1

    task = {
        "id": task_id,
        "data": {
            "context": chosen_context,
            "prompt": chosen_prompt,
            "response_a": response_a,
            "response_b": response_b
        }
    }

    tasks.append(task)

    # Store the original preference separately
    answer_key.append({
        "task_id": task_id,
        "preferred": preferred
    })


# Step 5: Inspect the results
print("Number of tasks:", len(tasks))
print("Number of answer keys:", len(answer_key))

if tasks:
    print("\nFirst task:")
    print(json.dumps(tasks[0], indent=2, ensure_ascii=False))

    print("\nFirst answer key:")
    print(answer_key[0])
from pathlib import Path

# Create a folder for our processed data
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

# Save annotation tasks
with open(output_dir / "annotation_tasks.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save the reference answer key
with open(output_dir / "answer_key.json", "w", encoding="utf-8") as f:
    json.dump(answer_key, f, indent=2, ensure_ascii=False)

print("\nFiles saved successfully!")