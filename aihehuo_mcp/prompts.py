# prompts.py
"""
Embedded prompts for the aihehuo-mcp server.
This file contains all prompt templates as embedded strings.
"""

# Pitch prompt content
PITCH_PROMPT = """---
  ## 🔧 Prompt Name: generate_60s_pitch_with_context

  ## 🧠 Description:
  Generate 3 tailored versions of a “Golden 60-Second Elevator Pitch” (for investors, co-founders, and customers).  
  You must first extract key information from the **existing conversation context**. Do not proceed unless all 3 core elements are clarified:

  1. 🎯 **Target Customer Profile** — who is this solution for?  
  2. 💥 **Pain Point** — what problem are they facing?  
  3. 💪 **Advantage** — what advantage does the user or their team have?

  If any of these are missing or unclear from context, ask the user follow-up questions to clarify before generating the pitch.

  ---

  ## 🔍 Step 1: Extract Startup Context (from conversation or by asking)

  Carefully review previous conversation turns. Identify or ask:

  - `customer_profile`: Who is the target audience (demographics, behaviors, needs)?
  - `pain_point`: What problem do they face? Use 6-dimension framework below.
  - `advantage`: What is the user/team’s unfair advantage? Use 5-dimension framework below.
  - `cta`: (Optional) What do you want the audience to do after hearing the pitch?

  ✅ If anything is unclear, stop and ask the user. Do not fabricate.

  ---

  ## 💥 Step 2: Map pain point & advantage to strategic dimensions

  ### Pain Point Resonance Dimensions (choose 1–2):
  | ID | Dimension | Description |
  |----|-----------|-------------|
  | 1 | Urgency | If not solved quickly, major harm happens |
  | 2 | Frequency | It happens very often, creating ongoing frustration |
  | 3 | Economic Cost | It wastes money or causes loss |
  | 4 | Universality | Many people suffer from it |
  | 5 | Viral Expansion | Pain is spreading due to trends |
  | 6 | Policy-Driven | New laws make old behaviors obsolete |

  ### Advantage Dimensions (choose 1–3):
  | ID | Dimension | Description |
  |----|-----------|-------------|
  | A | Elite Background | e.g., top-tier school, ex-big tech |
  | B | Low Entry Cost | Naturally low CAC or frictionless growth |
  | C | 10x Better Solution | Dramatically better, faster, cheaper |
  | D | Natural Distribution | Own a large channel to access target users |
  | E | Competitive Moat | IP, exclusive data, tech lock-in |

  ---

  ## ✍️ Step 3: Generate 3 Pitches

  Produce 3 versions of the Golden 60-second pitch, each tailored for:

  - **Investor**: Emphasize market, traction, defensibility, returns
  - **Co-founder**: Emphasize vision, synergy, roles, energy
  - **Customer**: Emphasize empathy, ease, emotional win, quick results

  Each version should be around **90–120 words**, written in a **natural, compelling, and emotionally resonant** tone.  
  Use simple and powerful language. End with a distinct **Call to Action** for each audience.

  ---

  ## 🖥️ Step 4: Render Output as Interactive HTML

  Output a self-contained HTML block that displays the 3 pitches with interactive tabs

  ⚠️ Important Rules:
	•	Never guess user intent or business model. Always extract or clarify.
	•	Do not generate unless context is sufficient.
	•	Use user’s words when generating the pitch to ensure authenticity.
"""

# Business plan prompt content (example for adding more prompts)
BUSINESS_PLAN_PROMPT = """---
description: Create a comprehensive business plan for your startup.
---

You are creating a comprehensive business plan for a lean startup. This command helps structure your business model, market analysis, and financial projections.

**IMPORTANT**: Before generating the business plan, ensure you have validated your business model and have market research data.

Follow this structure:

1. **Executive Summary**
2. **Company Description**
3. **Market Analysis**
4. **Organization & Management**
5. **Service or Product Line**
6. **Marketing & Sales Strategy**
7. **Financial Projections**
8. **Funding Request** (if applicable)

Create a detailed business plan following this structure...
"""

# Dictionary of all prompts
PROMPTS = {
    "pitch": {
        "name": "pitch",
        "description": "Create a compelling 60-second elevator pitch based on your validated business model and required artifacts",
        "arguments": [
            {
                "name": "arguments",
                "description": "User input arguments for the pitch",
                "required": False
            }
        ],
        "content": PITCH_PROMPT
    },
    "business_plan": {
        "name": "business_plan",
        "description": "Create a comprehensive business plan for your startup",
        "arguments": [
            {
                "name": "arguments",
                "description": "User input arguments for the business plan",
                "required": False
            }
        ],
        "content": BUSINESS_PLAN_PROMPT
    }
}
