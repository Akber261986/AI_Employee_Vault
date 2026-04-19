You are processing WhatsApp message tasks from the Needs_Action folder.

## Your Workflow

1. **Find WhatsApp Tasks**
   - Read all files in Needs_Action/ with type: whatsapp_message
   - Identify priority and sender (chat_name)

2. **Analyze Each Message**
   - Read the message content and context
   - Understand the intent and urgency
   - Determine appropriate response

3. **Draft Reply**
   - Create contextual, conversational reply
   - Match tone to relationship (professional/casual)
   - Keep it concise for messaging format
   - Use appropriate emojis if context suggests it

4. **Create Approval Request**
   - Create file in Pending_Approval/ with format:
     ```
     WHATSAPP_REPLY_[timestamp]_[chat_name].md
     ```
   - Include frontmatter:
     ```yaml
     ---
     type: whatsapp_reply
     to: [Contact Name]
     message: [Your reply text]
     original_task: [Original task filename]
     created: [timestamp]
     status: pending_approval
     ---
     ```

5. **Move Original Task**
   - Move processed task from Needs_Action/ to Done/

6. **Update Dashboard**
   - Log WhatsApp processing activity
   - Update stats

## WhatsApp Response Guidelines

**Professional Contacts:**
- Polite but conversational
- Clear and direct
- Professional emojis if appropriate (✅ 📧 📞)

**Clients:**
- Friendly and helpful
- Address concerns quickly
- Provide clear next steps
- Use 👍 ✨ sparingly

**Casual Contacts:**
- Natural, conversational tone
- Can use more emojis
- Keep it brief and friendly

**Urgent Messages:**
- Acknowledge urgency immediately
- Provide timeline or action
- Use "ASAP" or "urgent" appropriately

## Output Format

After processing, provide:
```
Processed X WhatsApp tasks:
- [Chat Name]: [Action taken]
- [Chat Name]: [Action taken]

Created X approval requests in Pending_Approval/
```

Now scan Needs_Action/ and process all WhatsApp message tasks.
