from pydantic import BaseModel, Field
"""
Response Generator Agent

This agent is responsibe for generating an email response based on the summary.

"""

from google.adk.agents import LlmAgent

class EmailContent(BaseModel):
    subject: str  = Field(
        description="The subject line of the email should be concise and descriptive."
    )
    body:str = Field(
        description="The main content of the email should be well-formatted and address the summary"
    )

GEMINI_MODEL = "gemini-2.0-flash"

response_generator_agent = LlmAgent(
    name="ResponseGeneratorAgent",
    model =GEMINI_MODEL,
    instruction=""" You are an email response generator AI.

    Based on the summary:
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete

        IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting according to the summary",
        }

        DO NOT include any explanations or additional text outside the JSON response.
        
        Summary:
        {summary}
        
    """,
    description="Generates an email response based on the summary",
    output_key="email_response",

)