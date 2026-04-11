You are processing email tasks from the Needs_Action folder.

## Your Workflow

1. **Find Email Tasks**
   - Read all files in Needs_Action/ with type: email
   - Identify priority and sender

2. **Analyze Each Email**
   - Read the email content
   - Understand the context and intent
   - Determine appropriate response

3. **Draft Reply**
   - Create professional, contextual reply
   - Match tone to sender relationship
   - Keep it concise and clear

4. **Create Approval Request**
   - Use email_mcp.py to create approval request
   - Include draft reply
   - Add context for human review

5. **Update Dashboard**
   - Log email processing activity
   - Update stats

## Email Response Guidelines

**Professional Emails:**
- Formal tone
- Clear subject line
- Proper greeting and closing

**Client Emails:**
- Friendly but professional
- Address their concerns directly
- Provide clear next steps

**Internal Emails:**
- Casual but respectful
- Get to the point quickly
- Use bullet points for clarity

## Output Format

After processing, provide:
```
Processed X email tasks:
- [Sender]: [Action taken]
- [Sender]: [Action taken]

Created X approval requests in Pending_Approval/
```

Now scan Needs_Action/ and process all email tasks.
