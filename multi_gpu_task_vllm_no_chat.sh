# Default values
default_task_name="mmlu"
default_model_identifier="meta-llama/Llama-2-7b-chat-hf"
# other models: mistralai/Mixtral-8x7B-Instruct-v0.1

# Input variables with defaults
task_name="${1:-$default_task_name}"
model_identifier="${2:-$default_model_identifier}"
number_of_gpus="${3:-1}"

# Corrected logic for model selection
case "$model_identifier" in
    *7b*)
        model_identifier="meta-llama/Llama-2-7b-hf"
        ;;
    *13b*)
        model_identifier="meta-llama/Llama-2-13b-hf"
        ;;
    *70b*)
        model_identifier="meta-llama/Llama-2-70b-hf"
        ;;
    *mix*)
        model_identifier="mistralai/Mixtral-8x7B-Instruct-v0.1"
        ;;
    *)
        # Default model or custom logic for other cases
        ;;
esac

# gpt-3.5
# Uncomment and customize the following line if needed
# lm_eval --model openai-chat-completions --model_args model=gpt-3.5-turbo-0125 --tasks gsm8k_discriminate  --log_samples --output_path output/gpt-3.5_gsm8k_discriminate

# gpt-4
# lm_eval --model openai-chat-completions --model_args model=gpt-4-turbo-preview --tasks gsm8k_discriminate  --log_samples --output_path output/gpt-3.5_gsm8k_discriminate

nohup lm_eval --model vllm --model_args "pretrained=$model_identifier,tensor_parallel_size=$number_of_gpus,dtype=auto" --tasks $task_name --batch_size auto --log_samples --output_path "output/${model_identifier}_${task_name}" &

