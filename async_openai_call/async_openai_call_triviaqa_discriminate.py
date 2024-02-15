from openai import AsyncOpenAI
import random
import time
import asyncio
import json
import httpx
import nest_asyncio
from tqdm import tqdm

# model = "gpt-3.5-turbo-0125"
model = "gpt-4-0125-preview"

client = AsyncOpenAI(
  http_client=httpx.AsyncClient(
    limits=httpx.Limits(
      max_connections=1000,
      max_keepalive_connections=100
    )
  )
)

prompt_list = [{"role": "system", "content": "You will be given two choices of answers to a question. Please choose the answer that you think is the best answer to the question. Your final selection should be 1 or 2, where 1 represents the answer you choose is answer 1, 2 represents the answer you choose is answer 2. Please end your generation with 1 or 2"}, \
        {"role": "user", "content": "Question: Who had a 70s No 1 hit with Kiss You All Over?\nHere are the two lists of answer choices.\nAnswer1: L P Hartley\nAnswer2: Sent into exile\nAnswer:"}, \
        {"role": "assistant", "content": "2"}, \
        {"role": "user", "content": "Question: What was the last US state to reintroduce alcohol after prohibition?\nHere are the two lists of answer choices.\nAnswer1: Utah (State)\nAnswer2: Haiwii\nAnswer:"}, \
        {"role": "assistant", "content": "1"}, \
]


messages = []
i = 0
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/gpt-4/gpt-4_triviaqa/triviaqa_gpt_4_evaluative.jsonl'):
    d = json.loads(line.strip())
    temp_prompt_list = prompt_list.copy()
    if not d["answer1"]:
        d["answer1"] = "null"
    if not d["answer2"]:
        d["answer2"] = "null"
    temp_prompt_list.append({"role": "user", "content": "Question: " + d["question"] + "\nHere are the two lists of answer choices.\nAnswer1: " + d["answer1"] + "\nAnswer2: " + d["answer2"] + "\nAnswer:"})
    if "answer" not in d:
        d["answer"] = ""
    messages.append((temp_prompt_list, d["answer1_correct"], d["answer2_correct"], d["question"], d["answer"], d["answer1"], d["answer2"]))
    i += 1

pbar = tqdm(total=len(messages), desc='Scanning files')
async def get_result(messages):
    max_retries = 10  # Maximum number of retries
    retry_delay = 1.0  # Initial delay in seconds
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                        model=model,
                        messages=messages,  # Ensure messages is a list
                        temperature=0.0,
                    )
            # Calculate price based on model
            if model == "gpt-3.5-turbo-0125":
                price = response.usage.prompt_tokens / 1000 * 0.0005 + response.usage.completion_tokens / 1000 * 0.0015
            elif model == "gpt-4-0125-preview":
                price = response.usage.prompt_tokens / 1000 * 0.01 + response.usage.completion_tokens / 1000 * 0.03
            pbar.update(1)
            return response.choices[0].message.content, price
        except Exception as e:  # Replace Exception with your client's specific rate limit exception
            if attempt < max_retries - 1:
                wait = retry_delay * (2 ** attempt)  # Exponential backoff formula
                print(f"Rate limit reached, retrying in {wait:.2f} seconds...")
                await asyncio.sleep(wait)
            else:
                print("Max retries reached, unable to complete request.")
                raise e  # Re-raise the last exception

if model.startswith('gpt-3.5'):
    write_file = open("gpt_3.5_discriminate_triviaqa.jsonl", 'w')
else:
    write_file = open("gpt_4_discriminate_triviaqa.json", 'w')

def apply_async_get_embedding(messages):
    total_price = 0.0
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_result(message[0])) for message in messages]
    result = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    for i in range(len(result)):
        d = {"price": result[i][1], "question": messages[i][3], "answer":  messages[i][4], "answer1_correct": messages[i][1], "answer2_correct": messages[i][2], "answer1": messages[i][5], "answer2": messages[i][6], "discriminate_answer": result[i][0]}
        write_file.write(json.dumps(d) + '\n')
        total_price += float(result[i][1])
    return total_price

result = apply_async_get_embedding(messages)
print(result)


print("This run called ")
