# Style Guide

> Writing style and content standards for documentation.

---

## Voice and Tone

### Guidelines

| Aspect     | Guideline                                               |
| ---------- | ------------------------------------------------------- |
| **Voice**  | Professional, friendly, direct                          |
| **Tense**  | Present tense ("Click the button" not "You will click") |
| **Person** | Second person ("You can..." not "Users can...")         |
| **Mood**   | Imperative for instructions ("Run the command")         |

### Examples

**Good:**

> Run the following command to start the server.

**Avoid:**

> The user should run the following command to start the server.

---

## Page Structure

### Standard Page Template

```mdx
---
title: 'Clear, Action-Oriented Title'
description: 'What the reader will learn or accomplish (150 chars)'
---

Brief introduction paragraph explaining what this page covers.

## First Major Section

Content here...

### Subsection if needed

More detail...

## Second Major Section

Content here...

## Next Steps

Links to related content or next actions.
```

### Heading Hierarchy

| Level | Usage                                    |
| ----- | ---------------------------------------- |
| H1    | Never use (title comes from frontmatter) |
| H2    | Major sections                           |
| H3    | Subsections                              |
| H4    | Rarely needed, avoid if possible         |

---

## Writing Guidelines

### Titles

| Type            | Format        | Example                               |
| --------------- | ------------- | ------------------------------------- |
| Page title      | Title Case    | "Getting Started with the API"        |
| Section heading | Sentence case | "Configure your settings"             |
| Description     | Sentence      | "Learn how to set up authentication." |

### Lists

**Use bullet lists for:**

- Non-sequential items
- Feature lists
- Requirements

**Use numbered lists for:**

1. Step-by-step instructions
2. Ordered processes
3. Prioritized items

### Code References

- Use backticks for inline code: `npm install`
- Use code blocks for multi-line code
- Always specify language for syntax highlighting

---

## Content Types

### Conceptual Content

Explains what something is and why it matters.

```mdx
## What is Authentication?

Authentication verifies the identity of users accessing your API.
It ensures that only authorized users can perform actions.
```

### Procedural Content

Step-by-step instructions for completing a task.

```mdx
## Set Up Authentication

1. Navigate to the Dashboard
2. Click **Settings** > **API Keys**
3. Click **Generate New Key**
4. Copy the key and store it securely
```

### Reference Content

Technical specifications and API details.

```mdx
## API Response Codes

| Code | Meaning      |
| ---- | ------------ |
| 200  | Success      |
| 400  | Bad Request  |
| 401  | Unauthorized |
| 500  | Server Error |
```

---

## Formatting Standards

### Emphasis

| Style    | Usage                        | Markdown     |
| -------- | ---------------------------- | ------------ |
| **Bold** | UI elements, important terms | `**text**`   |
| _Italic_ | Introducing new terms        | `*term*`     |
| `Code`   | Commands, file names, code   | `` `code` `` |

### Links

**Internal links:**

```mdx
See the [quickstart guide](/quickstart) for setup instructions.
```

**External links:**

```mdx
Read the [official documentation](https://example.com/docs).
```

### Images

```mdx
![Alt text description](/images/screenshot.png)
```

Always include descriptive alt text.

---

## Best Practices

### DO

- Start with the most important information
- Use concrete examples
- Keep paragraphs short (3-4 sentences max)
- Include code samples for technical content
- Link to related content

### DON'T

- Assume prior knowledge without linking to prerequisites
- Use jargon without explanation
- Write walls of text without visual breaks
- Skip alt text on images
- Use vague language ("simply", "just", "easily")

---

## Quality Checklist

Before publishing:

- [ ] Title is clear and descriptive
- [ ] Description is under 160 characters
- [ ] Headings follow hierarchy (H2 > H3)
- [ ] Code examples are tested and correct
- [ ] Links are valid and point to correct pages
- [ ] Images have alt text
- [ ] Content is scannable (lists, tables, short paragraphs)
