from openai import AsyncOpenAI
import random
import time
import asyncio
import json
import httpx
import nest_asyncio
from tqdm import tqdm

model = "gpt-4-0125-preview"
client = AsyncOpenAI(
  http_client=httpx.AsyncClient(
    limits=httpx.Limits(
      max_connections=1000,
      max_keepalive_connections=100
    )
  )
)

prompt_list = [{"role": "system", "content": "Please end your answer with #### {number}, where the number is the answer you calculated.\n\n"}, \
        {"role": "user", "content": "Question: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"}, \
        {"role": "assistant", "content": "Natalia sold 48/2 = <<48/2=24>>24 clips in May. Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May. #### 72"}, \
        {"role": "user", "content": "Question: Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?"}, \
        {"role": "assistant", "content": "Weng earns 12/60 = $<<12/60=0.2>>0.2 per minute. Working 50 minutes, she earned 0.2 x 50 = $<<0.2*50=10>>10. #### 10"}, \
        {"role": "user", "content": "Question: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?"}, \
        {"role": "assistant", "content": "In the beginning, Betty has only 100 / 2 = $<<100/2=50>>50. Betty's grandparents gave her 15 * 2 = $<<15*2=30>>30. This means, Betty needs 100 - 50 - 30 - 15 = $<<100-50-30-15=5>>5 more. #### 5"}, \
        {"role": "user", "content": "Question: Julie is reading a 120-page book. Yesterday, she was able to read 12 pages and today, she read twice as many pages as yesterday. If she wants to read half of the remaining pages tomorrow, how many pages should she read?"}, \
        {"role": "assistant", "content": "Maila read 12 x 2 = <<12*2=24>>24 pages today. So she was able to read a total of 12 + 24 = <<12+24=36>>36 pages since yesterday. There are 120 - 36 = <<120-36=84>>84 pages left to be read. Since she wants to read half of the remaining pages tomorrow, then she should read 84/2 = <<84/2=42>>42 pages. #### 42"}, \
        {"role": "user", "content": "Question: James writes a 3-page letter to 2 different friends twice a week. How many pages does he write a year?"}, \
        {"role": "assistant", "content": "He writes each friend 3*2=<<3*2=6>>6 pages a week So he writes 6*2=<<6*2=12>>12 pages every week That means he writes 12*52=<<12*52=624>>624 pages a year #### 624"}, \
    ]

messages = []
i = 0
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/batched_inference/gsm8k/gsm8k-test.jsonl'):
    d = json.loads(line.strip())
    temp_prompt_list = prompt_list.copy()
    
    temp_prompt_list.append({"role": "user", "content": "Question: " + d["question"]})
    messages.append((temp_prompt_list, d["question"], d["answer"]))
    i += 1

pbar = tqdm(total=len(messages), desc='Scanning files')
async def get_result(messages):
    r = random.random()
    if r > 0.33:
        if r > 0.67:
            await asyncio.sleep(120)
        else:
            await asyncio.sleep(60)
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
    # print(response)
    return [response.choices[item].message.content for item in range(0, 4)], price

write_file = open("gpt_3.5_generate_gsm8k.jsonl", 'w')
def apply_async_get_embedding(messages):
    total_price = 0.0
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_result(message[0])) for message in messages]
    result = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    # print(result)
    for i in range(len(result)):
        d = {"price": result[i][1], "question": messages[i][0], "answer":  messages[i][1], "generate_answer": result[i][0]}
        write_file.write(json.dumps(d) + '\n')
        total_price += float(result[i][1])
    return total_price

result = apply_async_get_embedding(messages)
print(result)


print("This run called ")
