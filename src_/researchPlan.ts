export interface ResearchStep {
  action: string;
  purpose: string;
}

export interface ResearchPlan {
  topic: string;
  research_question: string;
  steps: ResearchStep[];
}

export function isResearchPlan(value: unknown): value is ResearchPlan {
  if (typeof value !== "object" || value === null) return false;

  const plan = value as Record<string, unknown>;

  if (
    typeof plan.topic !== "string" ||
    plan.topic.trim().length === 0 ||
    typeof plan.research_question !== "string" ||
    plan.research_question.trim().length === 0 ||
    !Array.isArray(plan.steps) ||
    plan.steps.length < 3 ||
    plan.steps.length > 5
  ) {
    return false;
  }

  return plan.steps.every(
    (step: unknown) =>
      typeof step === "object" &&
      step !== null &&
      typeof (step as Record<string, unknown>).action === "string" &&
      (step as Record<string, unknown>).action !== "" &&
      typeof (step as Record<string, unknown>).purpose === "string" &&
      (step as Record<string, unknown>).purpose !== "" &&
      Object.keys(step).length === 2 &&
      "action" in step &&
      "purpose" in step,
  );
}