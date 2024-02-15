import os
import json

llama_7b= 'Llama-2-7b-chat-hf_gsm8k_discriminate/pretrained__meta-llama__Llama-2-7b-chat-hf,tensor_parallel_size__4,dtype__auto_gsm8k_discriminate.jsonl'
llama_13b = 'Llama-2-13b-chat-hf_gsm8k_discriminate/pretrained__meta-llama__Llama-2-13b-chat-hf,tensor_parallel_size__4,dtype__auto_gsm8k_discriminate.jsonl'
llama_70b = 'Llama-2-70b-chat-hf_gsm8k_discriminate/pretrained__meta-llama__Llama-2-70b-chat-hf,tensor_parallel_size__2,dtype__auto_gsm8k_discriminate.jsonl'

with open(llama_7b, 'r') as file:
    data1 = file.read()
with open(llama_70b, 'r') as file2:
    data2 = file2.read()
data1 = json.loads(data1)
data2 = json.loads(data2)


for i in range(len(data1)):
    print(data1[i]['resps'])
    print(data2[i]['resps'])
    print('\n\n')
