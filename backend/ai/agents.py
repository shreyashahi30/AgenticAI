import json
import logging

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


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# =========================================================
# JSON PARSING
# =========================================================

def parse_json_response(raw: str):
    """
    Parse JSON returned by Groq.

    Groq JSON Object Mode should return valid JSON.
    Pydantic models are used afterwards to validate
    the structure.
    """

    if not raw:
        raise ValueError(
            "LLM returned an empty response"
        )

    try:
        return json.loads(raw)

    except json.JSONDecodeError as e:

        logger.error(
            "Failed to parse LLM response as JSON: %s",
            e
        )

        logger.error(
            "Raw response: %s",
            raw[:1000]
        )

        raise ValueError(
            "LLM returned invalid JSON"
        ) from e


# =========================================================
# SKILL ASSESSMENT AGENT
# =========================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def skill_assessment_agent(
    resume_text: str
) -> SkillProfile:

    resume_text = resume_text[:4000]

    prompt = resume_skill_prompt(
        resume_text
    )

    logger.info(
        "Calling skill assessment agent"
    )

    logger.info(
        "Skill prompt size: %s chars",
        len(prompt)
    )

    raw = call_llm(prompt)

    logger.info(
        "Skill agent response: %s",
        raw[:500]
    )

    try:

        data = parse_json_response(raw)

        result = SkillProfile(**data)

        logger.info(
            "Skill assessment completed successfully"
        )

        return result

    except Exception as e:

        logger.error(
            "Skill agent error: %s",
            e
        )

        raise ValueError(
            "Invalid skill assessment response"
        ) from e


# =========================================================
# MARKET DEMAND AGENT
# =========================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def market_demand_agent(
    target_role: str
) -> MarketProfile:

    prompt = market_demand_prompt(
        target_role
    )

    logger.info(
        "Calling market demand agent"
    )

    raw = call_llm(prompt)

    logger.info(
        "Market agent response: %s",
        raw[:500]
    )

    try:

        data = parse_json_response(raw)

        result = MarketProfile(**data)

        logger.info(
            "Market demand analysis completed successfully"
        )

        return result

    except Exception as e:

        logger.error(
            "Market agent error: %s",
            e
        )

        raise ValueError(
            "Invalid market analysis response"
        ) from e


# =========================================================
# SKILL GAP AGENT
# =========================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def skill_gap_agent(
    user_skills,
    market_skills
) -> SkillGapProfile:

    prompt = skill_gap_prompt(
        user_skills,
        market_skills
    )

    logger.info(
        "Calling skill gap agent"
    )

    raw = call_llm(prompt)

    logger.info(
        "Skill gap agent response: %s",
        raw[:500]
    )

    try:

        data = parse_json_response(raw)

        result = SkillGapProfile(**data)

        logger.info(
            "Skill gap analysis completed successfully"
        )

        return result

    except Exception as e:

        logger.error(
            "Skill gap agent error: %s",
            e
        )

        raise ValueError(
            "Invalid skill gap response"
        ) from e


# =========================================================
# LEARNING PATH AGENT
# =========================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def learning_path_agent(
    missing_skills
) -> LearningPathProfile:

    prompt = learning_path_prompt(
        missing_skills
    )

    logger.info(
        "Calling learning path agent"
    )

    logger.info(
        "Missing skills: %s",
        missing_skills
    )

    raw = call_llm(prompt)

    logger.info(
        "Learning path response: %s",
        raw[:1000]
    )

    try:

        data = parse_json_response(raw)

        result = LearningPathProfile(**data)

        logger.info(
            "Learning path generated successfully"
        )

        return result

    except Exception as e:

        logger.error(
            "Learning path agent error: %s",
            e
        )

        raise ValueError(
            "Invalid learning path response"
        ) from e
