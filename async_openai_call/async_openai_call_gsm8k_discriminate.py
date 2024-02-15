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

prompt_list = [{"role": "system", "content": "You will be given two answers to a question. Please create the reasoning process that arrive at these two answers and choose the final answer from answer1 and answer2. Your final selection should be 1 or 2. Please end your generation with: Therefore, the final choice is:\n### <1 or 2>\n\n"}, \
        {"role": "user", "content": "Question: Jen and Tyler are gymnasts practicing flips. Jen is practicing the triple-flip while Tyler is practicing the double-flip. Jen did sixteen triple-flips during practice. Tyler flipped in the air half the number of times Jen did. How many double-flips did Tyler do?\nAnswer1: 12\nAnswer2: 16\n"}, \
        {"role": "assistant", "content": "Solution1 that gives answer1 is: Jen did 16 triple-flips, so she did 16 * 3 = <<16*3=48>>48 flips.\nTyler did half the number of flips, so he did 48 / 2 = <<48/2=24>>24 flips.\nA double flip has two flips, so Tyler did 24 / 2 = <<24/2=12>>12 double-flips.\nSolution2 that gives answer2 is: Jen did 16 triple-flips, so she did 16 * 3 = <<16*3=64>>64 flips.\nTyler did half the number of flips, so he did 64 / 2 = <<64/2=32>>32 flips.\nA double flip has two flips, so Tyler did 32 / 2 = <<32/2=16>>16 double-flips.\nSolution 2 made a mistake in the calculation of 16*3, it should be 48, not 64. Therefore, the final choice is:\n### 1\n\n"}, \
        {"role": "user", "content": "Question: Four people in a law firm are planning a party. Mary will buy a platter of pasta for $20 and a loaf of bread for $2. Elle and Andrea will split the cost for buying 4 cans of soda which cost $1.50 each, and chicken wings for $10. Joe will buy a cake that costs $5. How much more will Mary spend than the rest of the firm put together?\nAnswer1: 3\nAnswer2: 1\n"}, \
        {"role": "assistant", "content": "Solution1 that gives answer1 is: Mary will spend $20 + $2 = $<<20+2=22>>22.\nElle and Andrea will spend $1 x 4 = $<<1*4=4>>4 for the soda.\nElle and Andrea will spend $4 + $10 = $<<4+10=14>>14 for the soda and chicken wings.\nElle, Andrea, and Joe together will spend $14 + $5 = $<<14+5=19>>19.\nSo, Mary will spend $22 - $19 = $<<22-19=3>>3 more than all of them combined.\nSolution2 that gives answer2 is: Mary will spend $20 + $2 = $<<20+2=22>>22.\nElle and Andrea will spend $1.5 x 4 = $<<1.5*4=6>>6 for the soda.\nElle and Andrea will spend $6 + $10 = $<<6+10=16>>16 for the soda and chicken wings.\nElle, Andrea, and Joe together will spend $16 + $5 = $<<16+5=21>>21.\nSo, Mary will spend $22 - $21 = $<<22-21=1>>1 more than all of them combined.\nSolution1 made a mistake in the price of soda. It should be $1.5 each, not $1 each. Therefore, the final choice is:\n### 2"}, \
        {"role": "user", "content": "Question: A charcoal grill burns fifteen coals to ash every twenty minutes of grilling. The grill ran for long enough to burn three bags of coals. Each bag of coal contains 60 coals. How long did the grill run?\nAnswer1: 180\nAnswer2: 240\n"},
        {"role": "assistant", "content": "Solution1 that gives answer1 is: The grill burned 3 * 60 = <<360=180>>180 coals.\nSince it burns 15 coals every 20 minutes, the grill ran for 180 / 15 * 10 = <<180/15*10=120>>120 minutes.\nSolution2 that gives answer2 is: The grill burned 3 * 60 = <<360=180>>180 coals.\nIt takes 20 minutes to burn 15 coals, so the grill ran for 180 / 15 * 20 = <<180/15*20=240>>240 minutes.\nSolution1 made a mistake in the multiplication factor for the time calculation. It should be 20 minutes for every 15 coals, not 10. Therefore, the final choice is:\n### 2\n\n"},
        {"role": "user", "content": "Question: A bear is preparing to hibernate for the winter and needs to gain 1000 pounds. At the end of summer, the bear feasts on berries and small woodland animals. During autumn, it devours acorns and salmon. It gained a fifth of the weight it needed from berries during summer, and during autumn, it gained twice that amount from acorns. Salmon made up half of the remaining weight it had needed to gain. How many pounds did it gain eating small animals?\nAnswer1: 200\nAnswer2: 400\n"},
        {"role": "assistant", "content": "Solution1 that gives answer1 is: The bear gained 1 / 5 * 1000 = <<1/5*1000=200>>200 pounds from berries. It gained 2 * 200 = <<2*200=400>>400 pounds from acorns. It still needed 1000 - 200 - 400 = <<1000-200-400=400>>400 pounds. Thus, it gained 400 / 2 = <<400/2=200>>200 pounds from salmon. Therefore, the bear gained 400 - 200 = <<400-200=200>>200 pounds from small animals.\nSolution2 that gives answer2 is: The bear gained 1 / 5 * 1000 = <<1/5*1000=200>>200 pounds from berries. It gained 2 * 200 = <<2*200=400>>400 pounds from acorns. It still needed 1000 - 200 - 400 = <<1000-200-400=400>>400 pounds. Thus, it gained 400 / 2 = <<400/2=200>>200 pounds from salmon. Therefore, the bear gained 1000 - 200 - 400 - 200 = <<1000-200-400-200=400>>400 pounds from small animals.\nSolution2 made a mistake in the final calculation. 1000-200-400-200=200. Therefore, the final choice is:\n### 1\n\n"}]

messages = []
i = 0
for line in open('/bask/projects/j/jlxi8926-auto-sum/dongwei/lm-evaluation-harness/output/gpt-4/gpt-4_gsm8k/gsm8k_gpt-4_evaluative.jsonl'):
    d = json.loads(line.strip())
    temp_prompt_list = prompt_list.copy()
    if not d["answer1"]:
        d["answer1"] = "null"
    if not d["answer2"]:
        d["answer2"] = "null"
    temp_prompt_list.append({"role": "user", "content": "Question: " + d["question"] + "\nAnswer1: " + d["answer1"] + "\nAnswer2: " + d["answer2"] + "\n"})
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
    write_file = open("gpt_3.5_discriminate_gsm8k.jsonl", 'w')
else:
    write_file = open("gpt_4_discriminate_gsm8k.json", 'w')
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
