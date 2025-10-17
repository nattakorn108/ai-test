#!/bin/bash

MODEL="llama3"
PROMPT="Why is the sky blue?"

echo "Benchmarking model: $MODEL"

# Run a warmup iteration to load the model
echo "Running warmup iteration..."
curl -s http://localhost:11434/api/generate -d "{ \"model\": \"$MODEL\", \"prompt\": \"$PROMPT\", \"stream\": false }" > /dev/null

# Run the benchmark and measure time
echo "Running benchmark..."
START_TIME=$(date +%s.%N)
RESPONSE=$(curl -s http://localhost:11434/api/generate -d "{ \"model\": \"$MODEL\", \"prompt\": \"$PROMPT\", \"stream\": false }")
END_TIME=$(date +%s.%N)

# Calculate latency
LATENCY=$(echo "$END_TIME - $START_TIME" | bc)

# Extract performance metrics from the JSON response
EVAL_COUNT=$(echo "$RESPONSE" | jq -r '.eval_count')
EVAL_DURATION=$(echo "$RESPONSE" | jq -r '.eval_duration')

# Calculate tokens per second (TPS)
TPS=$(echo "scale=2; $EVAL_COUNT / ($EVAL_DURATION / 1000000000)" | bc)

echo "------------------------"
echo "Model: $MODEL"
echo "Total Latency: ${LATENCY}s"
echo "Tokens per second (TPS): ${TPS} t/s"
echo "------------------------"
