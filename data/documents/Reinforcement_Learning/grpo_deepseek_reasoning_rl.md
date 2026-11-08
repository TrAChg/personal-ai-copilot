# Group Relative Policy Optimization (GRPO) for LLM Reasoning

**Category**: `Reinforcement_Learning` | **Authority Rank**: 5/5 | **Date**: 2026-11-09

## Overview & Key Concepts

Group Relative Policy Optimization (GRPO) eliminates the memory-heavy Critic/Value network from standard PPO. Instead of training a separate value model $V_\phi(s)$ of equal size to the policy, GRPO samples a group of $G$ outputs $\{o_1, o_2, \dots, o_G\}$ for each question $q$, computes rule-based or verifier rewards $\{r_1, r_2, \dots, r_G\}$, and computes the normalized relative advantage:

$$A_i = \frac{r_i - \text{mean}(r)}{\text{std}(r) + \epsilon}$$

This cuts training VRAM usage by over 50% while stabilizing mathematical and algorithmic reasoning trajectories (as demonstrated in DeepSeek-R1 and DeepSeekMath).

## Connected GraphRAG Entities

- `GRPO_Algorithm`
- `PPO_Reinforcement_Learning`
- `DeepSeek_R1_Reasoning`

