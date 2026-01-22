import json
import logging
import re
from tenacity import retry, stop_after_attempt, wait_fixed

from backend.ai.llm_client import call_llm
from backend.ai.prompts import (
    resume_skill_prompt,
    market_demand_prompt,
    skill_gap_prompt,
    learning_path_prompt
)
from backend.ai.schemas import (
    SkillProfile,
    MarketProfile,
    SkillGapProfile,
    LearningPathProfile
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------- JSON EXTRACTION ----------------

def extract_json(raw: str):
    """
    Robust JSON extractor from LLM output.
    Handles:
    - ```json code blocks
    - Extra text
    - Newlines
    """
    logger.info("Extracting JSON from LLM response")

    # Remove markdown fences
    raw = re.sub(r"```json", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"```", "", raw)

    # Extract JSON object
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM response")

    json_text = match.group(0)
    logger.info(f"Extracted JSON length: {len(json_text)} chars")

    return json.loads(json_text)


# ---------------- SKILL ASSESSMENT AGENT ----------------

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def skill_assessment_agent(resume_text: str) -> SkillProfile:
    resume_text = resume_text[:4000]  # cost control
    prompt = resume_skill_prompt(resume_text)

    logger.info("Skill agent: sending prompt")
    logger.info(f"Prompt size: {len(prompt)} chars")

    raw = call_llm(prompt)
    logger.info(f"Skill agent raw response (first 200 chars): {raw[:200]}")

    try:
        data = extract_json(raw)
        return SkillProfile(**data)
    except Exception as e:
        logger.error(f"Skill agent JSON error: {e}")
        raise ValueError("Invalid AI output. Retrying...")


# ---------------- MARKET DEMAND AGENT ----------------

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def market_demand_agent(target_role: str) -> MarketProfile:
    prompt = market_demand_prompt(target_role)

    logger.info("Market agent: sending prompt")

    raw = call_llm(prompt)
    logger.info(f"Market agent raw response (first 200 chars): {raw[:200]}")

    try:
        data = extract_json(raw)
        return MarketProfile(**data)
    except Exception as e:
        logger.error(f"Market agent JSON error: {e}")
        raise ValueError("Invalid AI output. Retrying...")


# ---------------- SKILL GAP AGENT ----------------

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def skill_gap_agent(user_skills, market_skills) -> SkillGapProfile:
    prompt = skill_gap_prompt(user_skills, market_skills)

    logger.info("Skill gap agent: sending prompt")

    raw = call_llm(prompt)
    logger.info(f"Skill gap raw response (first 200 chars): {raw[:200]}")

    try:
        data = extract_json(raw)
        return SkillGapProfile(**data)
    except Exception as e:
        logger.error(f"Skill gap JSON error: {e}")
        raise ValueError("Invalid AI output. Retrying...")


# ---------------- LEARNING PATH AGENT ----------------

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def learning_path_agent(skill_gap_data) -> LearningPathProfile:
    # Convert Pydantic model → dict for prompt
    skill_gap_dict = skill_gap_data.model_dump()

    prompt = learning_path_prompt(skill_gap_dict)

    logger.info("Learning path agent: sending prompt")

    raw = call_llm(prompt)
    logger.info(f"Learning path raw response (first 200 chars): {raw[:200]}")

    try:
        data = extract_json(raw)
        return LearningPathProfile(**data)
    except Exception as e:
        logger.error(f"Learning path JSON error: {e}")
        raise ValueError("Invalid AI output. Retrying...")
