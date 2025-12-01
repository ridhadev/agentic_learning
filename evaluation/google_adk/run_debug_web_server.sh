# Load the .env environment variables at the root ot the package
source ../../.env

conda activate agentic_learning

adk create research_agent --model gemini-2.5-flash-lite --api_key $GOOGLE_API_KEY