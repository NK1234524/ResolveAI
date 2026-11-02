import pytest
from backend.core.priority_engine import calculate_priority,explain_priority
from backend.schemas.ai_assessment import ImpactLevel, UrgencyLevel


@pytest.mark.parametrize(
    "impact, urgency, expected",
    [
        (ImpactLevel.LOW, UrgencyLevel.LOW, "LOW"),
        (ImpactLevel.LOW, UrgencyLevel.MEDIUM, "LOW"),
        (ImpactLevel.LOW, UrgencyLevel.HIGH, "MEDIUM"),
        (ImpactLevel.LOW, UrgencyLevel.CRITICAL, "HIGH"),

        (ImpactLevel.MEDIUM, UrgencyLevel.LOW, "LOW"),
        (ImpactLevel.MEDIUM, UrgencyLevel.MEDIUM, "MEDIUM"),
        (ImpactLevel.MEDIUM, UrgencyLevel.HIGH, "HIGH"),
        (ImpactLevel.MEDIUM, UrgencyLevel.CRITICAL, "HIGH"),

        (ImpactLevel.HIGH, UrgencyLevel.LOW, "MEDIUM"),
        (ImpactLevel.HIGH, UrgencyLevel.MEDIUM, "HIGH"),
        (ImpactLevel.HIGH, UrgencyLevel.HIGH, "HIGH"),
        (ImpactLevel.HIGH, UrgencyLevel.CRITICAL, "CRITICAL"),

        (ImpactLevel.CRITICAL, UrgencyLevel.LOW, "HIGH"),
        (ImpactLevel.CRITICAL, UrgencyLevel.MEDIUM, "HIGH"),
        (ImpactLevel.CRITICAL, UrgencyLevel.HIGH, "CRITICAL"),
        (ImpactLevel.CRITICAL, UrgencyLevel.CRITICAL, "CRITICAL"),
    ],
)
def test_calculate_priority(impact, urgency, expected):
    result = calculate_priority(impact, urgency)

    assert result == expected

# New test now 
@pytest.mark.parametrize(
    "impact, urgency, expected_priority",
    [
        (ImpactLevel.LOW, UrgencyLevel.LOW, "LOW"),
        (ImpactLevel.HIGH, UrgencyLevel.MEDIUM, "HIGH"),
        (ImpactLevel.CRITICAL, UrgencyLevel.HIGH, "CRITICAL"),
        (ImpactLevel.MEDIUM, UrgencyLevel.CRITICAL, "HIGH"),
    ],
)
def test_explain_priority(impact, urgency, expected_priority):

    explanation = explain_priority(impact, urgency)

    assert impact.value in explanation
    assert urgency.value in explanation
    assert expected_priority in explanation


def test_explain_priority_is_deterministic():

    impact = ImpactLevel.CRITICAL
    urgency = UrgencyLevel.HIGH

    first_result = explain_priority(impact, urgency)
    second_result = explain_priority(impact, urgency)

    assert first_result == second_result