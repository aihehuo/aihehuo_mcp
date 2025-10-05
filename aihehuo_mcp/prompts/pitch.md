---
description: Create a compelling 60-second elevator pitch based on your validated business model and required artifacts.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

You are creating a 60-second elevator pitch for the lean startup. This command helps craft a concise, compelling pitch that communicates your value proposition clearly.

**IMPORTANT**: Before generating the pitch, you must ensure all required artifacts are available. If any artifacts are missing, you must ask the user to provide them or create them first.

Follow this execution flow:

1. **Check Required Artifacts**:
   - **User Persona**: `.specify/artifacts/user-personas/[PERSONA_NAME].md`
   - **Pain Points**: `.specify/artifacts/pain-points/[PAIN_AREA].md`
   - **Value Proposition**: `.specify/artifacts/value-propositions/[VALUE_PROP].md`
   
   If any artifacts are missing, ask the user:
   - "I need [MISSING_ARTIFACT] to create an effective pitch. Please provide [SPECIFIC_INFORMATION_NEEDED] or run the appropriate command to generate it first."

2. **Load Business Model Context** from:
   - `.specify/memory/business-model-canvas.md`
   - `.specify/memory/current-hypotheses.md`
   - `.specify/templates/value-proposition-canvas.md`

3. **Load Required Artifacts**:
   - User persona data for target audience
   - Pain points analysis for emotional resonance
   - Value proposition details for solution positioning

4. **Analyze User Input** to identify:
   - Target audience for the pitch (investors, customers, partners)
   - Pitch context (competition, demo day, networking event)
   - Key message focus areas
   - Tone and style preferences

5. **Extract Golden 60s Components** from artifacts and business model:
   - **Target Persona**: From user persona artifact
   - **Pain Point Dimensions**: Select 1-3 from pain points analysis:
     - **urgency**: The user needs to solve this *now*
       - *Example*: "Every day you wait, you're losing $500 in revenue"
       - *Example*: "This problem is getting worse by the hour"
       - *Example*: "Your competitors are already solving this"
     
     - **frequency**: This happens *all the time*
       - *Example*: "This happens 3 times a day, every day"
       - *Example*: "You face this problem every Monday morning"
       - *Example*: "This is a constant struggle in your daily workflow"
     
     - **intensity**: This is *really painful* when it happens
       - *Example*: "When this happens, it completely shuts down your business"
       - *Example*: "This causes so much stress that you can't sleep at night"
       - *Example*: "This problem makes you want to quit your job"
     
     - **cost**: This is *expensive* to ignore
       - *Example*: "Every month you don't solve this costs you $10,000"
       - *Example*: "The current workaround costs $2,000 per incident"
       - *Example*: "You're losing 20 hours per week to this problem"
     
     - **risk**: This could *hurt* the user if not addressed
       - *Example*: "If you don't fix this, you'll lose your biggest client"
       - *Example*: "This could result in a lawsuit or regulatory fine"
       - *Example*: "Your reputation is at stake if this continues"
     
     - **frustration**: This is *annoying* and wastes time
       - *Example*: "You spend 2 hours every day on this tedious task"
       - *Example*: "This is so complicated that you need to call IT every time"
       - *Example*: "You've tried 5 different solutions and none work properly"
   
   - **Solution Advantages**: Select 1-3 from value proposition:
     - **uniqueness**: We're the *only* ones who do this
       - *Example*: "We're the only platform that integrates with all your existing tools"
       - *Example*: "No one else offers real-time collaboration in this space"
       - *Example*: "We're the first to use AI for this specific problem"
     
     - **superiority**: We do this *better* than anyone else
       - *Example*: "We're 10x faster than the current market leader"
       - *Example*: "Our accuracy rate is 99.9% vs 85% for competitors"
       - *Example*: "We have 50% fewer bugs than the next best solution"
     
     - **simplicity**: We make this *easier* than alternatives
       - *Example*: "Setup takes 5 minutes instead of 5 hours"
       - *Example*: "One-click solution vs 20-step process"
       - *Example*: "No training required - intuitive interface"
     
     - **speed**: We solve this *faster* than current solutions
       - *Example*: "Get results in 30 seconds instead of 30 minutes"
       - *Example*: "Process 1000x more data in the same time"
       - *Example*: "Instant deployment vs 6-month implementation"
     
     - **cost**: We're *cheaper* than the alternatives
       - *Example*: "50% less expensive than current solutions"
       - *Example*: "Pay only for what you use vs expensive annual contracts"
       - *Example*: "Free tier covers 80% of users' needs"

6. **Generate 60-second pitch** using the Golden 60 Seconds framework:

   **Structure**:
   - **[0-20s] Target Persona & Emotional Pain Resonance**
     - Start with "You know how [target persona]..."
     - Use selected pain dimensions to create emotional connection
     - Make it relatable and specific
   
   - **[20-45s] Why Us – Compelling Advantages**
     - Transition with "That's why we built [solution name]..."
     - Highlight selected solution advantages
     - Use concrete benefits, not features
   
   - **[45-60s] Call to Action Hook**
     - End with specific, low-barrier action
     - Examples: "Want to see how? Let's grab coffee." / "Interested? I'll send you our demo." / "Ready to try it? Here's my card."

7. **Create the pitch using this template**:
   ```
   ## 60-Second Elevator Pitch: [STARTUP_NAME]
   
   **Target Audience**: [INVESTORS/CUSTOMERS/PARTNERS]
   **Context**: [WHERE_THIS_PITCH_WILL_BE_USED]
   **Duration**: 60 seconds (approximately 150 words)
   
   ### The Pitch
   
   [Opening Hook - 10 seconds]
   [Problem Statement - 15 seconds]
   [Solution Description - 20 seconds]
   [Market Opportunity - 10 seconds]
   [Traction/Validation - 10 seconds]
   [Call to Action - 5 seconds]
   
   ### Full Text
   [Complete pitch as a flowing narrative, 150 words]
   
   ### Key Messages
   - [Key Point 1]
   - [Key Point 2]
   - [Key Point 3]
   
   ### Delivery Tips
   - [Tip 1]: [Guidance]
   - [Tip 2]: [Guidance]
   - [Tip 3]: [Guidance]
   
   ### Target Contact Search Keywords
   **For 爱合伙 Database (70万用户)**:
   
   **投资人**:
   - "寻找[行业]早期项目的投资人 对[解决方案类型]感兴趣的天使投资人 [目标市场]领域的风险投资"
   
   **客户**:
   - "[目标行业]企业决策者 [具体职位]负责人 正在寻找[解决方案]的[目标用户群体]"
   
   **合作伙伴**:
   - "[相关行业]渠道合作伙伴 [技术领域]技术合作伙伴 能够推广[产品类型]的合作伙伴"
   
   **导师**:
   - "[行业]创业导师 [技术领域]专家顾问 成功创办[相关业务]的企业家"
   
   **媒体**:
   - "关注[行业]的科技记者 [目标市场]创业媒体 [解决方案类型]行业媒体"
   
   **示例**（AI客服SaaS产品）:
   - 投资人: "寻找企业服务早期项目的投资人 对AI客服SaaS感兴趣的天使投资人 企业服务领域的风险投资"
   - 客户: "电商企业决策者 客服总监负责人 正在寻找AI客服解决方案的电商企业"
   - 合作伙伴: "企业服务渠道合作伙伴 AI技术合作伙伴 能够推广SaaS产品的合作伙伴"
   ```

8. **Validate pitch quality**:
   - Clear problem and solution articulation
   - Compelling value proposition
   - Realistic market opportunity
   - Concrete traction or validation
   - Strong call to action
   - Uses emotional language and "you" statements
   - Fits within 60 seconds when spoken

9. **Create pitch variations**:
   - **Version A**: Investor-focused (funding emphasis)
   - **Version B**: Customer-focused (value emphasis)
   - **Version C**: Partner-focused (collaboration emphasis)

10. **Include target contact search keywords** in the deliverable:
   ```
   ### Target Contact Search Keywords
   **For 爱合伙 Database (70万用户)**:
   
   **投资人**:
   - "寻找[行业]早期项目的投资人 对[解决方案类型]感兴趣的天使投资人 [目标市场]领域的风险投资"
   
   **客户**:
   - "[目标行业]企业决策者 [具体职位]负责人 正在寻找[解决方案]的[目标用户群体]"
   
   **合作伙伴**:
   - "[相关行业]渠道合作伙伴 [技术领域]技术合作伙伴 能够推广[产品类型]的合作伙伴"
   
   **导师**:
   - "[行业]创业导师 [技术领域]专家顾问 成功创办[相关业务]的企业家"
   
   **媒体**:
   - "关注[行业]的科技记者 [目标市场]创业媒体 [解决方案类型]行业媒体"
   
   **示例**（AI客服SaaS产品）:
   - 投资人: "寻找企业服务早期项目的投资人 对AI客服SaaS感兴趣的天使投资人 企业服务领域的风险投资"
   - 客户: "电商企业决策者 客服总监负责人 正在寻找AI客服解决方案的电商企业"
   - 合作伙伴: "企业服务渠道合作伙伴 AI技术合作伙伴 能够推广SaaS产品的合作伙伴"
   ```

11. **Save deliverable** to `.specify/deliverables/pitch/60s-pitch.md` (including the search keywords section above)

12. **Output summary** with:
    - Pitch word count and timing
    - Key strengths and suggestions
    - Recommended practice approach
    - Next steps for refinement
    - **Target contact search keywords** for 爱合伙 database

**Template Structure**:
- Pitch must be concise and impactful
- Use clear, jargon-free language
- Include specific numbers and facts
- End with a clear call to action
- Provide timing guidance for each section
- Use emotional language and "you" statements
- Focus on benefits, not features

**Validation Requirements**:
- Pitch must tell a compelling story
- All claims must be backed by validated learning
- Language must be accessible to target audience
- Pitch must fit within 60 seconds when spoken
- Call to action must be specific and actionable
- Must use emotional resonance with pain dimensions
- Must highlight unique solution advantages

**Required Artifacts**:
- User Persona: Defines target audience characteristics
- Pain Points: Provides emotional resonance and problem context
- Value Proposition: Ensures solution positioning accuracy

**Pain Point Dimensions** (select 1-3):
- **urgency**: The user needs to solve this *now*
  - *Example*: "Every day you wait, you're losing $500 in revenue"
  - *Example*: "This problem is getting worse by the hour"
  - *Example*: "Your competitors are already solving this"

- **frequency**: This happens *all the time*
  - *Example*: "This happens 3 times a day, every day"
  - *Example*: "You face this problem every Monday morning"
  - *Example*: "This is a constant struggle in your daily workflow"

- **intensity**: This is *really painful* when it happens
  - *Example*: "When this happens, it completely shuts down your business"
  - *Example*: "This causes so much stress that you can't sleep at night"
  - *Example*: "This problem makes you want to quit your job"

- **cost**: This is *expensive* to ignore
  - *Example*: "Every month you don't solve this costs you $10,000"
  - *Example*: "The current workaround costs $2,000 per incident"
  - *Example*: "You're losing 20 hours per week to this problem"

- **risk**: This could *hurt* the user if not addressed
  - *Example*: "If you don't fix this, you'll lose your biggest client"
  - *Example*: "This could result in a lawsuit or regulatory fine"
  - *Example*: "Your reputation is at stake if this continues"

- **frustration**: This is *annoying* and wastes time
  - *Example*: "You spend 2 hours every day on this tedious task"
  - *Example*: "This is so complicated that you need to call IT every time"
  - *Example*: "You've tried 5 different solutions and none work properly"

**Solution Advantages** (select 1-3):
- **uniqueness**: We're the *only* ones who do this
  - *Example*: "We're the only platform that integrates with all your existing tools"
  - *Example*: "No one else offers real-time collaboration in this space"
  - *Example*: "We're the first to use AI for this specific problem"

- **superiority**: We do this *better* than anyone else
  - *Example*: "We're 10x faster than the current market leader"
  - *Example*: "Our accuracy rate is 99.9% vs 85% for competitors"
  - *Example*: "We have 50% fewer bugs than the next best solution"

- **simplicity**: We make this *easier* than alternatives
  - *Example*: "Setup takes 5 minutes instead of 5 hours"
  - *Example*: "One-click solution vs 20-step process"
  - *Example*: "No training required - intuitive interface"

- **speed**: We solve this *faster* than current solutions
  - *Example*: "Get results in 30 seconds instead of 30 minutes"
  - *Example*: "Process 1000x more data in the same time"
  - *Example*: "Instant deployment vs 6-month implementation"

- **cost**: We're *cheaper* than the alternatives
  - *Example*: "50% less expensive than current solutions"
  - *Example*: "Pay only for what you use vs expensive annual contracts"
  - *Example*: "Free tier covers 80% of users' needs"

**Golden 60 Seconds Framework**:
1. **[0-20s] Target Persona & Emotional Pain Resonance**
   - Start with "You know how [target persona]..."
   - Use selected pain dimensions to create emotional connection
   - Make it relatable and specific

2. **[20-45s] Why Us – Compelling Advantages**
   - Transition with "That's why we built [solution name]..."
   - Highlight selected solution advantages
   - Use concrete benefits, not features

3. **[45-60s] Call to Action Hook**
   - End with specific, low-barrier action
   - Examples: "Want to see how? Let's grab coffee." / "Interested? I'll send you our demo." / "Ready to try it? Here's my card."