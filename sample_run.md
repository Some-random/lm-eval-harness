Step 1: Generate multiple candidates for a task by setting repeat=4, temperature=0.7, do_sample=True in yaml file. 

Example yaml: 
```
lm_eval/tasks/gsm8k/gsm8k.yaml
```

To run generation on GSM8k with Llama 7b-chat on 4 GPUs: 
```
sh multi_gpu_task_vllm.sh gsm8k 7b 4
```

Step 2: Go to output dir, run script to calculate average accuracy and select best and worse answers from all answer chocies.

Example: 
```
cd output/meta-llama/Llama-2-7b-chat-hf_gsm8k 
python calculate_generation_accuracy_and_generate_discrimination.py pretrained__meta-llama__Llama-2-7b-chat-hf,tensor_parallel_size__1,dtype__auto_gsm8k.jsonl
```

Step 3: Create a new task with prompts to compare the best and the worse generation

Example: 
```
lm_eval/tasks/gsm8k_discriminate/gsm8k_discriminate_7b.yaml
```

Step 4: Go to output dir of result comparsion, run script to calcualte comparsion accuracy.

Example: 
```
cd output/meta-llama/Llama-2-7b-chat-hf_gsm8k_discriminate_7b
python calculate_eval.py pretrained__meta-llama__Llama-2-7b-chat-hf,tensor_parallel_size__1,dtype__auto_gsm8k_discriminate_7b.jsonl
```
