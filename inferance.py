from json import JSONDecodeError

from mlx_lm import load
from mlx_lm.generate import stream_generate
from mlx_lm.models.cache import make_prompt_cache
from mlx_lm.sample_utils import make_sampler

import json
import time


class MorpheusAI:
    NAME = "MorpheusAI"
    PROMPT_PATH = "saved_prompts"

    def __init__(self, story_name=None):
        print("Loading model and applying custom adapters...")
        self.model, self.tokenizer = load(
            "./dolphin-8b-4bit",
            adapter_path="./adapters"
        )

        self.prompt_cache = make_prompt_cache(self.model)
        self.sampler = make_sampler(temp=0.7)

        if story_name is not None:
            self.story_path = f"test_stories/{story_name}.json"
            self.story_name = story_name

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

        self._initiate_session()

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
                max_tokens=2000,
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

    def _initiate_session(self):
        default_message = "Hi"

        print("\n=== MorpheusAI Online ===")

        if self.story_path is None:
            self.chat_stream(default_message)
        else:
            self.load_story()

        print("\n")

    def load_story(self):
        print("Initialising story...")
        flavor_text = (f"Describe yourself pulling a leather-bound book titled '{self.story_name}' "
                       f"from the dusty shelf, blowing off the grit, and opening it to the first page.")
        self.chat_stream(flavor_text)
        time.sleep(10)  # 10 second cooldown - giving user time to read.
        print("\n------ ------ ------- ------ ------ ------- ------- ------- -------\n\n")

        try:
            with open(self.story_path, 'r') as f:
                story_config = json.load(f)
                prompt_config = self.get_prompt(prompt_type='opening')

                world_state = json.dumps(story_config["world_state"], indent=2)
                narrator_instructions = json.dumps(story_config["narrator_instructions"])
                initial_scene = story_config["initial_scene"]

                system_content = f"{prompt_config["system_directive"]}\n"
                steps = f"{prompt_config["steps"]}"

                self.chat_stream(
                    world_state + "\n\n" +
                    narrator_instructions + "\n\n" +
                    initial_scene + "\n\n" +
                    system_content + "\n\n" +
                    steps
                )

        except FileNotFoundError:
            print("File does not exist.")

    def get_prompt(self, prompt_type):
        try:
            prompt_path = f"{MorpheusAI.PROMPT_PATH}/{prompt_type}_prompt.json"

            with open(prompt_path, 'r') as f:
                config = json.load(f)
                return config

        except JSONDecodeError:
            print("Error: Your JSON file has a syntax error.")
            return None
        except FileNotFoundError:
            print("Error: JSON file does not exist.")
            return None


story_path = "the_wild_lands"
morpheus_ai = MorpheusAI(story_path)

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
