from backend.schemas.ai_assessment import(
    ImpactLevel,
    UrgencyLevel
)

PRIORITY_MATRIX={
    ImpactLevel.LOW:{
        UrgencyLevel.LOW:"LOW",
        UrgencyLevel.MEDIUM:"LOW",
        UrgencyLevel.HIGH:"MEDIUM",
        UrgencyLevel.CRITICAL:"HIGH"
    },

    ImpactLevel.MEDIUM:{
        UrgencyLevel.LOW:"LOW",
        UrgencyLevel.MEDIUM:"MEDIUM",
        UrgencyLevel.HIGH:"HIGH",
        UrgencyLevel.CRITICAL:"HIGH"
    },

    ImpactLevel.HIGH:{
        UrgencyLevel.LOW:"MEDIUM",
        UrgencyLevel.MEDIUM:"HIGH",
        UrgencyLevel.HIGH:"HIGH",
        UrgencyLevel.CRITICAL:"CRITICAL"
    },

    ImpactLevel.CRITICAL:{
        UrgencyLevel.LOW:"HIGH",
        UrgencyLevel.MEDIUM:"HIGH",
        UrgencyLevel.HIGH:"CRITICAL",
        UrgencyLevel.CRITICAL:"CRITICAL"
    }
}

def calculate_priority(
    impact:ImpactLevel,
    urgency:UrgencyLevel
)->str:
    return PRIORITY_MATRIX[impact][urgency]

def explain_priority(
    impact: ImpactLevel,
    urgency: UrgencyLevel
) -> str:

    priority = calculate_priority(impact, urgency)

    return (
        f"This incident has {impact.value} impact and "
        f"{urgency.value} urgency. "
        f"Based on the priority rules, it has been assigned "
        f"{priority} priority."
    )