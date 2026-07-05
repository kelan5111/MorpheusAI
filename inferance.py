import sys
from mlx_lm import load
from mlx_lm.generate import stream_generate  # <-- IMPORT THIS TO ENABLE STREAMING
from mlx_lm.models.cache import make_prompt_cache
from mlx_lm.sample_utils import make_sampler


class MorpheusAI:
    NAME = "MorpheusAI"

    def __init__(self):
        print("Loading model and applying custom adapters...")
        self.model, self.tokenizer = load(
            "./dolphin-8b-4bit",
            adapter_path="./adapters"
        )

        self.prompt_cache = make_prompt_cache(self.model)
        self.sampler = make_sampler(temp=0.7)

        self.message_list = [
            {
                "role": "system",
                "content": (
                    "You are MorpheusAI, a masterful immersive storyteller and roleplay narrator. "
                    "Always respond in rich, vivid third-person narrative style. Never speak or act "
                    "for the user's character."
                )
            }
        ]

        self._initiate_chat()

    def chat_stream(self, user_prompt):
        self.message_list.append({"role": "user", "content": user_prompt})

        formatted_prompt = self.tokenizer.apply_chat_template(
            self.message_list,
            add_generation_prompt=True
        )

        response_chunks = []
        i = 0
        for response_obj in stream_generate(
                self.model,
                self.tokenizer,
                prompt=formatted_prompt,
                max_tokens=300,
                sampler=self.sampler,
                prompt_cache=self.prompt_cache
        ):
            token_text = response_obj.text

            if i % 25 == 0:
                print("\n" + token_text, end="", flush=True)
            else:
                print(token_text, end="", flush=True)

            response_chunks.append(token_text)
            i += 1

        full_response = "".join(response_chunks)
        self.message_list.append({"role": "assistant", "content": full_response})

        return full_response

    def _initiate_chat(self):
        initial_message = "Hi"
        print("\n=== MorpheusAI Online ===")
        self.chat_stream(initial_message)
        print("\n")


morpheus_ai = MorpheusAI()

while True:
    try:
        prompt = input("\nEnter prompt: ").strip()
        if prompt != "":
            if prompt.lower() in ["quit", "exit"]:
                break
            print("\n========== Response ==========")
            morpheus_ai.chat_stream(prompt)
            print("\n==============================")
    except KeyboardInterrupt:
        break
