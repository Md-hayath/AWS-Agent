# AWS DevOps Agent

Natural-language AWS assistant built with LangChain, OpenAI, and boto3.

The agent can call AWS tools for services such as S3, EC2, IAM/STS, EKS, ECS, DynamoDB, CloudFormation, CloudWatch, Lambda, SNS, SQS, and Bedrock.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv aws-agent-env
.\aws-agent-env\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
LLM_MODEL=gpt-4o-mini
```

Do not commit `.env` or paste API keys into chat, logs, GitHub, or screenshots.

## Run The CLI Agent

```powershell
python scripts/run_agent.py
```

Example prompts:

```text
list my s3 buckets
list iam users
list my eks clusters
show health of eks cluster my-cluster
list ecs clusters
show image names used by ecs service api-service in cluster my-cluster
create dynamodb table named test-table with id as partition key
```

Type `exit` or `quit` to stop the CLI.

## Run The API

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

Health check:

```powershell
curl http://127.0.0.1:8000/
```

Chat request:

```powershell
curl -X POST http://127.0.0.1:8000/chat `
  -H "Content-Type: application/json" `
  -d "{\"message\":\"list my s3 buckets\"}"
```

## AWS Permissions

The agent uses boto3, so it needs AWS credentials with permission for the actions you ask it to perform.

For local development, create an IAM user or role for this agent and grant only the permissions you need. Avoid `AdministratorAccess` unless you are testing in a disposable AWS account.

Common managed policies for testing:

- `AmazonS3ReadOnlyAccess` for listing buckets and objects
- `AmazonEC2ReadOnlyAccess` for describing EC2 resources
- `IAMReadOnlyAccess` for listing IAM users and roles
- `AmazonEKSClusterPolicy` or scoped EKS read permissions for EKS operations
- `AmazonECS_FullAccess` includes broad ECS access; prefer a custom read-only ECS policy when possible
- DynamoDB permissions such as `dynamodb:CreateTable`, `dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:Query`, `dynamodb:Scan`, and `dynamodb:DeleteItem` only if you want DynamoDB write actions

## Security Notes

This project can perform real AWS actions. Some tools create, modify, or delete cloud resources.

Use least-privilege IAM permissions, review commands before approving destructive actions, and test in a non-production AWS account first.

If an OpenAI or AWS key is exposed, revoke it immediately and create a new one.

## Useful Checks

Verify the Python environment:

```powershell
python -c "import sys; print(sys.executable)"
```

Verify the agent imports:

```powershell
python -B -c "from agent.agent import create_aws_agent; print(type(create_aws_agent()).__name__)"
```
