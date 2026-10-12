# LLM Response Preference Evaluation

A small-scale human evaluation project comparing AI-generated responses using Label Studio and Python.

## Project Overview

This project explores how human evaluators assess the quality of large language model (LLM) responses. The objective is to practice preference annotation, apply consistent evaluation criteria, and analyze agreement with an existing human-preference dataset.

The project uses a sample of 10 response pairs from the Anthropic HH-RLHF dataset.

## Tools and Technologies

- **Python** — Data preparation and evaluation analysis
- **Hugging Face Datasets** — Dataset loading
- **Label Studio** — Human annotation interface
- **JSON** — Annotation data storage and export

## Evaluation Methodology

Each task presents a conversation context, the latest user prompt, and two candidate AI responses.

The evaluator selects Response A, Response B, or Tie and provides a written justification.

Responses are compared using five criteria:

1. **Safety:** Avoiding harmful guidance and inappropriate content.
2. **Accuracy:** Providing correct information without unsupported claims.
3. **Instruction Following:** Addressing the user's legitimate request.
4. **Helpfulness:** Providing relevant and useful information.
5. **Clarity:** Communicating coherently and understandably.

Response order was randomized to reduce position bias. The original preferred response was stored separately from the annotation tasks.

## Evaluation Results

| Metric | Result |
|---|---|
| Total response pairs | 10 |
| Completed annotations | 10 |
| Exact preference matches | 5 |
| Exact preference agreement | 50% |
| Tie selections | 1 |
| Disagreements | 5 |

The original human-preference labels were used as reference judgments, not as definitive ground truth.

## Disagreement Analysis

Five disagreements were examined manually.

Key findings:

- Directly following a user's instructions is not always appropriate when the request involves harmful activity.
- Additional clarification can be unnecessary or unsafe when the user's harmful intent is already clear.
- Two responses can be similarly appropriate even when the reference dataset expresses a preference.
- Responses should avoid mixed messaging that appears to endorse discriminatory content.
- Conversational consistency should not come at the expense of factual accuracy or misleading claims about AI capabilities.

## Limitations

This project uses only 10 examples and is intended as a learning exercise rather than a statistically representative evaluation.

The dataset contains subjective human preferences. The annotation interface also permits Tie selections, whereas the original dataset records binary preferences. This affects exact-match agreement.

The sample includes sensitive and potentially offensive conversational content.

## Future Improvements

- Expand to a larger, carefully curated evaluation sample.
- Develop more detailed annotation guidelines.
- Measure agreement across multiple independent annotators.
- Analyze individual evaluation dimensions separately.
- Generate structured evaluation reports.

## Dataset Attribution

Source: [Anthropic HH-RLHF on Hugging Face](https://huggingface.co/datasets/Anthropic/hh-rlhf)

This project is an independent educational exercise and is not affiliated with Anthropic.

## Author

Nahom Samuel Yeshitila

Biomedical Engineering MSc Student | Aspiring AI Engineer

Interested in LLM evaluation, AI safety, Python, and healthcare AI.