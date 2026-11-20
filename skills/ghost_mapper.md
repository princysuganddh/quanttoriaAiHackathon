---
name: ghost_mapper
description: Diagnostic Agent Skill for identifying hidden prerequisite misconceptions ('Ghost Gaps') in K-12 mathematics.
version: 1.0.0
model: gemini-2.5-flash
tags: [math-pedagogy, prerequisite-mapping, diagnostic-ai, geogebra]
---

# GhostMapper Agent Skill

## Purpose
GhostMapper analyzes a student's step-by-step working and final answer to reveal not just *whether* they made a mistake, but the **hidden, foundational prerequisite gap ("Ghost Gap")** that caused it. In Grade 6 GeoGebra curriculum problems, students often stumble not on Grade 6 concepts (e.g. algebraic subtraction), but on unstated Grade 4/5 measurement standards.

## Target Curriculum Context
- **Domain**: Grade 6 Measurement, Ratios, and Word Problem Solving
- **Prerequisite Standard**: CCSS.MATH.CONTENT.4.MD.A.1 (Know relative sizes of measurement units within one system of units including lb, oz, ton. In the US Customary system: 1 ton = 2,000 lb).

## Diagnostic Mapping Rules
1. **The 500 lb Ghost Bug**:
   - Symptom: Student assumes `1/2 ton = 500 lb` instead of `1,000 lb`.
   - Root Cause Misconception: The student falsely mapped `1 ton = 1,000 lb` (confusing standard US customary tons with decimal metric prefixes like 1,000 kg, 1,000 g, or 1,000 m).
   - Prerequisite Gap: Grade 4 Customary Weight Units (`1 ton = 2,000 pounds`).
   - Downstream Failure: In Plane Cargo Capacity, they calculate `1,300 - 500 = 800 lb` instead of `1,300 - 1,000 = 300 lb`. In Cargo Trolleys, they calculate `850 - 500 = 350 lb` instead of `1,000 - 850 = 150 lb`.

2. **Output Structure**:
   - `detected`: boolean
   - `ghost_gap_id`: "4.MD.A.1_TON_CONVERSION"
   - `ghost_gap_title`: "Hidden Grade 4 Prerequisite: 1 ton = 2,000 lb"
   - `student_misconception`: Detailed pedagogical breakdown of what the student thought vs mathematical reality.
   - `correct_intermediate_step`: "1 ton = 2,000 lb ⟹ 1/2 ton = 1,000 lb"
   - `correct_final_answer`: Depends on problem (300 lb or 150 lb).
   - `spawn_leo_prompt`: Prompt passed to the Deliberate Bug Leo agent to initiate peer-learning repair.
