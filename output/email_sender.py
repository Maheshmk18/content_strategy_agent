import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from langsmith import traceable
from config.settings import settings
from graph.state import DayEntry
from output.pdf_calendar import generate_calendar_pdf


@traceable(name="send_calendar_email")
async def send_calendar_email(
    calendar: list[DayEntry], sheet_url: str, month: str, recipient_email: str = None
) -> bool:
    """Send email with calendar PDF attachment via SMTP. Returns True if sent successfully."""
    if not recipient_email:
        recipient_email = settings.notification_email

    subject = f"Your {month} Content Calendar is Ready!"
    html_body = _format_email_body(calendar, sheet_url, month)

    try:
        # Create email message
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = settings.smtp_email
        msg["To"] = recipient_email

        # Attach HTML body
        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)

        # Generate and attach PDF
        pdf_bytes = generate_calendar_pdf(calendar, month)
        pdf_part = MIMEBase('application', 'octet-stream')
        pdf_part.set_payload(pdf_bytes)
        encoders.encode_base64(pdf_part)
        pdf_part.add_header('Content-Disposition', f'attachment; filename="Calendar_{month.replace(" ", "_")}.pdf"')
        msg.attach(pdf_part)

        # Send via SMTP
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_email, settings.smtp_password)
            server.sendmail(settings.smtp_email, recipient_email, msg.as_string())

        print(f"Email sent successfully to {recipient_email} with PDF attachment")
        return True

    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication failed. Check your email/password.")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@traceable(name="format_email_body")
def _format_email_body(calendar: list[DayEntry], sheet_url: str, month: str) -> str:
    """Format the email body as HTML."""
    table_rows = ""
    for day_entry in calendar[:5]:  # Show first 5 days in email, rest in sheet
        table_rows += f"""
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">{day_entry['day']}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{day_entry['platform']}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{day_entry['content_type']}</td>
            <td style="padding: 10px; border: 1px solid #ddd;">{day_entry['topic']}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            h2 {{ color: #2c3e50; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px; border: 1px solid #ddd; }}
            .cta-button {{ display: inline-block; background-color: #3498db; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ color: #777; font-size: 12px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <h2> Your {month} Content Calendar is Ready!</h2>

        <p>Your content strategy agent has generated a 30-day content plan for your approval.</p>

        <h3> Preview (First 5 Days):</h3>
        <table>
            <tr>
                <th>Day</th>
                <th>Platform</th>
                <th>Type</th>
                <th>Topic</th>
            </tr>
            {table_rows}
        </table>

        <p>
            <a href="{sheet_url}" class="cta-button">View Full Calendar in Google Sheets</a>
        </p>

        <h3>Next Steps:</h3>
        <ol>
            <li>Review the full 30-day calendar in Google Sheets</li>
            <li>Edit any content topics or dates as needed</li>
            <li>Approve the calendar when ready</li>
            <li>Agent will help create the actual content</li>
        </ol>

        <p style="color: #666; margin-top: 30px;">
            <strong>Questions?</strong> Reply to this email or check the calendar notes for details.
        </p>

        <div class="footer">
            <p>Best regards,<br><strong>Your Content Strategy Agent</strong> 🤖</p>
            <p>Sent on {month}</p>
        </div>
    </body>
    </html>
    """

    return html
