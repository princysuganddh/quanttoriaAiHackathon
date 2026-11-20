---
name: ghost_mapper
description: Diagnostic Agent Skill for identifying hidden prerequisite misconceptions ('Ghost Gaps') in K-12 mathematics.
version: 1.0.0
model: gemini-2.5-flash
tags: [math-pedagogy, prerequisite-mapping, diagnostic-ai, curriculum-standards]
---

# GhostMapper Agent Skill

## Purpose
GhostMapper analyzes a student's step-by-step working and final answer to reveal not just *whether* they made a mistake, but the **hidden, foundational prerequisite gap ("Ghost Gap")** that caused it. In Grade 6 math curriculum word problems, students often stumble not on Grade 6 concepts (e.g. algebraic subtraction), but on unstated Grade 4/5 measurement standards.

## Target Curriculum Context
- **Domain**: Grade 6 Measurement, Ratios, and Word Problem Solving
- **Prerequisite Standard**: CCSS.MATH.CONTENT.4.MD.A.1 (Know relative sizes of measurement units within one system of units including lb, oz, ton, gallons, quarts. In the US Customary system: 1 ton = 2,000 lb; 1 gallon = 4 quarts).

## Diagnostic Mapping Rules
1. **The 500 lb Ghost Bug (Weight)**:
   - Symptom: Student assumes `1/2 ton = 500 lb` instead of `1,000 lb`.
   - Root Cause Misconception: The student falsely mapped `1 ton = 1,000 lb` (confusing standard US customary tons with decimal metric prefixes like 1,000 kg, 1,000 g, or 1,000 m).
   - Prerequisite Gap: Grade 4 Customary Weight Units (`1 ton = 2,000 pounds`).

2. **The 2-Quart Ghost Bug (Volume)**:
   - Symptom: Student assumes `1 gallon = 2 quarts`, concluding `4 gallons = 8 quarts`.
   - Root Cause Misconception: The student confuses quarts with liters or pints.
   - Prerequisite Gap: Grade 4 Customary Volume Units (`1 gallon = 4 quarts`).

3. **Output Structure**:
   - `detected`: boolean
   - `ghost_gap_id`: Prerequisite standard tag
   - `ghost_gap_title`: Foundational standard description
   - `student_misconception`: Pedagogical breakdown of error
   - `correct_intermediate_step`: Prerequisite conversion anchor
   - `correct_final_answer`: Target problem solution
   - `spawn_leo_prompt`: Prompt passed to the Deliberate Bug Leo agent
