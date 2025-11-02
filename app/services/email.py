from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(settings.sendgrid_api_key)
        self.from_email = settings.from_email
    
    async def send_expiring_items_notification(
        self,
        to_email: str,
        user_name: str,
        expiring_items: list
    ):
        """Send email notification for expiring pantry items"""
        
        items_html = "<ul>"
        for item in expiring_items:
            days_left = (item.expires_at - datetime.utcnow()).days
            items_html += f"<li>{item.name} - expires in {days_left} days</li>"
        items_html += "</ul>"
        
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject="🥗 Pantry Items Expiring Soon!",
            html_content=f"""
            <html>
                <body>
                    <h2>Hey {user_name}!</h2>
                    <p>You have some pantry items expiring soon:</p>
                    {items_html}
                    <p>Consider using these ingredients in your next meal plan!</p>
                    <a href="{settings.frontend_url}/plan">Plan Your Week</a>
                </body>
            </html>
            """
        )
        
        try:
            response = self.client.send(message)
            logger.info(f"Email sent to {to_email}: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    async def send_week_plan_ready(
        self,
        to_email: str,
        user_name: str,
        week_plan_id: str
    ):
        """Send email when week plan is generated"""
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject="🎉 Your Meal Plan is Ready!",
            html_content=f"""
            <html>
                <body>
                    <h2>Hi {user_name}!</h2>
                    <p>Your meal plan for this week is ready.</p>
                    <a href="{settings.frontend_url}/plan">View Your Plan</a>
                </body>
            </html>
            """
        )
        
        try:
            response = self.client.send(message)
            logger.info(f"Email sent to {to_email}: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

email_service = EmailService()