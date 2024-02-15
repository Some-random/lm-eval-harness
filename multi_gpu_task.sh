# Default values
default_task_name="mmlu"
default_model_identifier="meta-llama/Llama-2-7b-chat-hf"
# other models: mistralai/Mixtral-8x7B-Instruct-v0.1

# Input variables with defaults
task_name=${1:-$default_task_name}
model_identifier=${2:-$default_model_identifier}
number_of_gpus=${3:-1}

# to split the model to multiple gpus, add ,parallelize=True to the model_args

if [ $number_of_gpus -gt 1 ] && [ $number_of_gpus -lt 5 ]; then
    nohup accelerate launch --multi_gpu --num_processes $number_of_gpus lm_eval --model hf --model_args pretrained=$model_identifier --tasks $task_name --batch_size auto --log_samples --output_path output/${model_identifier}_${task_name} &
elif [ $number_of_gpus -eq 1 ]; then
    nohup lm_eval --model hf --model_args pretrained=$model_identifier --tasks $task_name --batch_size auto --log_samples --output_path output/${model_identifier}_${task_name} &
elif [ $number_of_gpus -gt 100 ]; then
    nohup accelerate launch -m lm_eval --model hf  --model_args pretrained=$model_identifier,parallelize=True --tasks $task_name --batch_size auto --log_samples --output_path output/${model_identifier}_${task_name} &
fi

