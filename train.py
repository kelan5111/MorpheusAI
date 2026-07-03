from mlx_lm.lora import train

config = {
    "model": "dolphin-8b-4bit",
    "data": "training_data_part1.jsonl",
    "batch_size": 4,
    "lora_layers": 16,
    "lora_rank": 8,
    "iters": 300,  # Start small
    "steps_per_report": 50,
}

train()