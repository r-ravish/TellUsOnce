"""Demo fallback utility - provides fallback AI responses for demo scenarios."""

from app.schemas.intake import AIAnalysisResponse, AIAnalysisNeed


def get_demo_fallback(masked_story: str) -> AIAnalysisResponse | None:
    """
    Check if the story matches a known demo scenario and return a pre-built response.

    This is used when OpenAI is unavailable to still demonstrate the system's capabilities.

    Returns None if no demo match is found.
    """
    story_lower = masked_story.lower()

    # Demo Case A: Routine fee extension
    if "fee extension" in story_lower and ("supporting letter" in story_lower or "sanction letter" in story_lower):
        days = 5  # default
        for word in story_lower.split():
            if word.isdigit():
                days = int(word)
                break

        return AIAnalysisResponse(
            summary="Student requests a fee extension due to family circumstances. Supporting documentation is available.",
            urgency="low",
            risk_flag=False,
            confidence=0.95,
            needs=[
                AIAnalysisNeed(
                    request_type="fee_extension",
                    documents_mentioned=["supporting letter"],
                    days_requested=days,
                    suggested_action="approve",
                    reason="Routine fee extension with supporting documentation available.",
                )
            ],
        )

    # Demo Case B: Complex hospital situation
    if "hospital" in story_lower and any(
        kw in story_lower for kw in ["fee", "hostel", "attendance", "exam"]
    ):
        needs = []
        if "fee" in story_lower:
            needs.append(AIAnalysisNeed(
                request_type="fee_extension",
                documents_mentioned=["medical certificate"],
                days_requested=10,
                suggested_action="route",
                reason="Fee extension needed due to parent's hospitalization. Extended period requires department review.",
            ))
        if "attendance" in story_lower:
            needs.append(AIAnalysisNeed(
                request_type="attendance_condonation",
                documents_mentioned=["medical certificate"],
                days_requested=0,
                suggested_action="route",
                reason="Attendance condonation needed due to family emergency.",
            ))
        if "exam" in story_lower:
            needs.append(AIAnalysisNeed(
                request_type="exam_deferral",
                documents_mentioned=["medical certificate"],
                days_requested=0,
                suggested_action="route",
                reason="Exam deferral needed due to family emergency.",
            ))
        if "hostel" in story_lower:
            needs.append(AIAnalysisNeed(
                request_type="hostel_notice",
                documents_mentioned=[],
                days_requested=0,
                suggested_action="route",
                reason="Hostel notice for temporary absence due to family emergency.",
            ))

        if not needs:
            needs.append(AIAnalysisNeed(
                request_type="student_affairs",
                documents_mentioned=["medical certificate"],
                days_requested=0,
                suggested_action="route",
                reason="Complex situation requiring multi-department coordination.",
            ))

        return AIAnalysisResponse(
            summary="Student's parent is hospitalized, causing multiple academic and financial complications requiring coordination across departments.",
            urgency="high",
            risk_flag=False,
            confidence=0.90,
            needs=needs,
        )

    # Demo Case C: Risk/distress
    risk_keywords = ["suicide", "self-harm", "hurt myself", "end my life", "can't go on", "distress"]
    if any(kw in story_lower for kw in risk_keywords):
        return AIAnalysisResponse(
            summary="Student expressing significant distress. Immediate human intervention required.",
            urgency="high",
            risk_flag=True,
            confidence=0.95,
            needs=[
                AIAnalysisNeed(
                    request_type="counselling_support",
                    documents_mentioned=[],
                    days_requested=0,
                    suggested_action="escalate",
                    reason="Student expressing distress. Priority escalation to counselling services.",
                )
            ],
        )

    # Prompt injection detection
    injection_keywords = ["ignore", "system prompt", "forget your instructions", "you are now", "pretend", "act as"]
    if any(kw in story_lower for kw in injection_keywords):
        return AIAnalysisResponse(
            summary="Potential prompt injection attempt detected. Escalating for human review.",
            urgency="high",
            risk_flag=True,
            confidence=0.95,
            needs=[
                AIAnalysisNeed(
                    request_type="student_affairs",
                    documents_mentioned=[],
                    days_requested=0,
                    suggested_action="escalate",
                    reason="Potential prompt injection attempt. Escalating for security review.",
                )
            ],
        )

    return None
