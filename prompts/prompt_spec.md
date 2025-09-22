# Prompt Spec – Agent

## Objective

-

## Audience

-

## Role Persona

**Name:**
**Description:**

## Scope

**In-scope:**

**Out-of-scope:**

## Style Guide

- Tone:
- Diction:
- Formatting:

## Context

## Guardrails

- Refusals:
- Disclaimers:
- Boundaries:

## Output Contract

```json
{
  "summary": "string (<= 60 words)",
  "actions": ["string (3–5)"],
  "risks_or_redflags": ["string (1–3)"]
}
```

## Strictness

- Return ONLY JSON. No prose. (Task Mode only.)
- If the task request is out_of_scope OR the Context section is empty/“None”,
return this exact refusal JSON instead:

```json
{
  "summary": "Cannot provide information on this request",
  "actions": [],
  "risks_or_redflags": []
}
```

## Controls

temperature: 0.2
max_words: 180

## Tests

- Input: “Base scenario for your track.”
- Expect: Valid JSON, uses only context, matches style.

## Checklist

Schema valid?
Used only provided context?
Guardrails respected?
Scope respected (refuse out_of_scope)?
Style consistent?
Refusal JSON used if context missing?