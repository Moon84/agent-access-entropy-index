# Methodology

This project tracks official-source machine-readable access paths for AI agents and developers.

## Access Paths

The index currently tracks:

- CLI
- Agent Skill / `SKILL.md`
- MCP server or MCP plugin
- SDK
- API
- Webhook / streaming / event interfaces
- Data export

## Verification

Official-source status is assigned conservatively. See [Verification Policy](VERIFICATION_POLICY.md).

## Agent Access Entropy Score

The score estimates how much official-source, machine-readable, automatable access exists for a platform or industry.

```text
Platform Entropy = Access × Velocity × Openness × Reliability
Industry Entropy = Σ Platform Entropy
Agent Access Entropy Index = 100 × Industry Entropy / MaxPossibleEntropy
```

Suggested mappings:

| Factor | Meaning |
|---|---|
| Access | Number and diversity of official access paths. |
| Velocity | How quickly information can move through those paths. |
| Openness | Friction to access: public, API key, review, commercial terminal, or closed. |
| Reliability | Official status, documentation quality, and maintenance. |

Risk is tracked separately from access entropy. A high entropy score does not mean safe.

## Interpretation

| Agent Access Entropy Index | Meaning |
|---:|---|
| 0-20 | Closed or low machine access |
| 20-40 | Limited flow |
| 40-60 | Moderate flow |
| 60-80 | High flow |
| 80-100 | Highly open, fast machine-readable flow |
