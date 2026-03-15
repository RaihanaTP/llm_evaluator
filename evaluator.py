# evaluator.py

import time
import json
from openai import OpenAI
from dataset import EVAL_DATASET
from metrics import compute_all_metrics

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

SYSTEM_PROMPT = "You are a helpful assistant. Answer clearly and accurately."

MODELS_TO_TEST = [
    {
        "model_id": "llama3.2:1b",
        "display_name": "Llama3.2 1B (Meta)",
        "system_prompt": SYSTEM_PROMPT
    },
    {
        "model_id": "gemma:2b",
        "display_name": "Gemma 2B (Google)",
        "system_prompt": SYSTEM_PROMPT
    },
]


def run_single_evaluation(question: str, ideal_answer: str, model_config: dict) -> dict:
    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model=model_config["model_id"],
            messages=[
                {"role": "system", "content": model_config["system_prompt"]},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.3
        )

        latency = time.time() - start_time
        response_text = response.choices[0].message.content

        input_tokens = len(question.split()) + len(model_config["system_prompt"].split())
        output_tokens = len(response_text.split())

        scores = compute_all_metrics(
            response=response_text,
            ideal_answer=ideal_answer,
            question=question,
            model=model_config["model_id"],
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_seconds=latency
        )

        return {
            "status": "success",
            "response_text": response_text,
            **scores
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "response_text": "",
            "relevance_score": 0,
            "hallucination_score": 0,
            "overall_quality": 0,
            "cost_usd": 0,
            "latency_seconds": 0,
            "word_count": 0,
            "length_category": "Error",
            "input_tokens": 0,
            "output_tokens": 0,
        }


def run_full_evaluation(progress_callback=None) -> list:
    results = []
    total_runs = len(EVAL_DATASET) * len(MODELS_TO_TEST)
    current = 0

    for item in EVAL_DATASET:
        for model_config in MODELS_TO_TEST:
            current += 1

            if progress_callback:
                progress_callback(
                    current / total_runs,
                    f"Testing: {model_config['display_name']} on Q{item['id']}"
                )

            result = run_single_evaluation(
                question=item["question"],
                ideal_answer=item["ideal_answer"],
                model_config=model_config
            )

            results.append({
                "question_id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "ideal_answer": item["ideal_answer"],
                "model_name": model_config["display_name"],
                "model_id": model_config["model_id"],
                **result
            })

            time.sleep(0.3)

    return results


def save_results(results: list, filename: str = "eval_results.json"):
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")


def load_results(filename: str = "eval_results.json") -> list:
    with open(filename, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    print("Starting evaluation with Ollama (local)...")
    results = run_full_evaluation()
    save_results(results)
    print(f"Done! Evaluated {len(results)} prompt-question combinations.")