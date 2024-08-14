import openai

# Upload the file
with open('/home/paulj/niru/climate_change_fine_tuning.jsonl', 'rb') as file:
    response = openai.File.create(
        file=file,
        purpose='fine-tune'
    )
file_id = response.id

# Create a fine-tuning job
response = openai.FineTuningJob.create(
    training_file=file_id,
    model="gpt-3.5-turbo"
)
job_id = response.id

print(f"Fine-tuning job created with ID: {job_id}")

# You can check the status of your fine-tuning job
response = openai.FineTuningJob.retrieve(job_id)
print(f"Status: {response.status}")
