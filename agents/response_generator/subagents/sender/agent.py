from pydantic import BaseModel
"""
Email Sender Agent

This agent is responsibe for sending email to the user.

"""

from google.adk.agents import LlmAgent

class Sender(BaseModel):
    user_email: str

GEMINI_MODEL = "gemini-2.0-flash"

email_sending_agent = LlmAgent(
    name="EmailSender",
    model =GEMINI_MODEL,
    instruction=""" You are an assistant that sends email to the specified user email.
    
    For the given email. send the response from the generated response.

    Generated Response:
    {email_response}

    Email:
    {user_email}
    """,
    description="Sends the email response to the specified email",
)