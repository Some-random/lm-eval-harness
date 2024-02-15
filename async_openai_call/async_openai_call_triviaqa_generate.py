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

prompt_list = [{"role": "system", "content": "The metrics for this task will be exact match, so just give me the answer that precisely answers the question, note that the answer dosen't have to contain only one word"}, \
        {"role": "user", "content": "Question: Which William wrote the novel Lord Of The Flies?"}, \
        {"role": "assistant", "content": "Golding"}, \
        {"role": "user", "content": "Question: What is Bruce Willis' real first name?"}, \
        {"role": "assistant", "content": "Walter (TV series)"}, \
]

messages = []
i = 0
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/batched_inference/triviaqa/triviaqa-validation.jsonl'):
    d = json.loads(line.strip())
    temp_prompt_list = prompt_list.copy()
    
    temp_prompt_list.append({"role": "user", "content": "Question: " + d["question"]})
    messages.append((temp_prompt_list, d["question"], d["answer"]["aliases"]))
    i += 1

pbar = tqdm(total=len(messages), desc='Scanning files')
async def get_result(messages):
    max_retries = 20  # Maximum number of retries
    retry_delay = 1.0  # Initial delay in seconds
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                n=4,
            )
            if model == "gpt-3.5-turbo-0125":
                price = response.usage.prompt_tokens / 1000 * 0.0005 + response.usage.completion_tokens / 1000 * 0.0015
            elif model == "gpt-4-0125-preview":
                price = response.usage.prompt_tokens / 1000 * 0.01 + response.usage.completion_tokens / 1000 * 0.03
            pbar.update(1)
            return [response.choices[item].message.content for item in range(0, 4)], price
        except Exception as e:  # Replace Exception with your client's specific rate limit exception
            if attempt < max_retries - 1:
                wait = retry_delay * (2 ** attempt)  # Exponential backoff formula
                print(f"Rate limit reached, retrying in {wait:.2f} seconds...")
                await asyncio.sleep(wait)
            else:
                print("Max retries reached, unable to complete request.")
                raise e  # Re-raise the last exception

if model.startswith('gpt-3.5'):
    write_file = open("gpt_3.5_generate_triviaqa.jsonl", 'w')
else:
    write_file = open("gpt-4_generate_triviaqa.jsonl", 'w')

def apply_async_get_embedding(messages):
    total_price = 0.0
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_result(message[0])) for message in messages]
    result = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    # print(result)
    for i in range(len(result)):
        d = {"price": result[i][1], "question": messages[i][1], "answer":  messages[i][2], "generate_answer": result[i][0]}
        write_file.write(json.dumps(d) + '\n')
        total_price += float(result[i][1])
    return total_price

result = apply_async_get_embedding(messages)
print(result)


print("This run called ")
