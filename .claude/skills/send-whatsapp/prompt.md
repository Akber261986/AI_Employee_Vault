You are sending approved WhatsApp messages via WhatsApp Web.

## Your Workflow

1. **Check for Approved Messages**
   - Scan Approved/ folder for WHATSAPP_REPLY_*.md files
   - Count how many need to be sent

2. **Process Each Approval**
   - Read the approval file
   - Extract recipient (to) and message content
   - Verify all required fields are present

3. **Send Messages**
   - Run: `python whatsapp_sender.py`
   - This will open WhatsApp Web with saved session
   - Each message is sent and moved to Done/ after success
   - Browser window will open (not headless)

4. **Update Dashboard**
   - Log sent messages
   - Update WhatsApp stats
   - Record any failures

5. **Report Results**
   - Summarize what was sent
   - Note any errors
   - Update activity log

## Safety Checks

Before sending:
- Verify contact name is not empty
- Check message has content
- Confirm approval file is in Approved/ folder
- Ensure WhatsApp Web session is active

## Output Format

```
Sent X WhatsApp messages:
- To: [contact] | Status: Sent
- To: [contact] | Status: Failed (reason)

All sent messages moved to Done/
```

## Important Notes

- WhatsApp Web requires browser window to stay open
- Session must be authenticated (scan QR code first time)
- Messages are sent one at a time with delays
- Contact names must match exactly as in WhatsApp

Now process and send all approved WhatsApp messages.
