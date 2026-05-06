# AWS DevOps Agent Configuration and IAM Setup

## Setting up your `.env`

Rename `.env.template` to `.env` and fill in the values:

```env
OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_DEFAULT_REGION=us-east-1
```

## Running the Agent

1. Install dependencies: `pip install -r requirements.txt`
2. Run the agent: `python scripts/run_agent.py`
3. Try asking: *"Can you list all my S3 buckets?"*

## AWS IAM Configuration (How to grant the Agent access)

To allow the AI Agent to execute actions on your behalf using natural language, it needs IAM permissions.

### Option 1: Create an IAM User for the Agent (Recommended for Local Dev)
1. Go to the AWS IAM Console.
2. Click **Users** -> **Add users**.
3. Name it `aws-devops-agent`.
4. Choose **Attach policies directly**.
5. *Which policies to attach?* It depends on what you want the agent to do.
   - For full control: Attach `AdministratorAccess` (DANGEROUS: The LLM can do anything).
   - For scoped control (Safer): Create a custom policy restricting actions. For example, if you only want it to manage S3 and EC2:
     - Attach `AmazonS3FullAccess`
     - Attach `AmazonEC2FullAccess`
6. Finish creating the user.
7. Go to the user's **Security credentials** tab.
8. Click **Create access key**.
9. Copy the `Access Key ID` and `Secret Access Key` into your `.env` file.

### Option 2: Assume Role (Advanced)
If you are running this agent on an EC2 instance, you can attach an IAM Role to the instance instead of hardcoding credentials in `.env`. Boto3 will automatically use the instance's credentials.

### Security Warning
Do not run this agent with Administrator credentials in a production AWS account without strict review. The LLM could potentially delete critical infrastructure if instructed maliciously or accidentally. Always use least-privilege principles.
 
## Run the Agent 
### Before running, create a virtual environment
#### 1.)  python -m venv aws-agent-env
#### 2.)  .\aws-agent-env\Scripts\Activate.ps1
#### 3.)  pip install -r requirements.txt
#### 4.)  python scripts/run_agent.py




#### python -c "import sys; print(sys.executable)"
