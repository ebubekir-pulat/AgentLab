import { describe, expect, it } from "vitest";
import { isResearchPlan } from "../src_/researchPlan";

describe("isResearchPlan", () => {
  it("accepts a valid research plan", () => {
    expect(
      isResearchPlan({
        topic: "Reliable local AI agents",
        research_question: "How can local models support reliable agents?",
        steps: [
          { action: "Review literature", purpose: "Understand prior work" },
          { action: "Run experiments", purpose: "Measure reliability" },
          { action: "Evaluate results", purpose: "Compare approaches" },
        ],
      }),
    ).toBe(true);
  });

  it("rejects plans with too few steps", () => {
    expect(
      isResearchPlan({
        topic: "Reliable local AI agents",
        research_question: "How can local models support reliable agents?",
        steps: [{ action: "Review", purpose: "Understand prior work" }],
      }),
    ).toBe(false);
  });

  it("rejects non-object input", () => {
    expect(isResearchPlan(null)).toBe(false);
    expect(isResearchPlan("not a plan")).toBe(false);
  });

  it("rejects steps with missing fields", () => {
    expect(
      isResearchPlan({
        topic: "Reliable local AI agents",
        research_question: "How can local models support reliable agents?",
        steps: [
          { action: "Review", purpose: "Research" },
          { action: "Run", purpose: "Experiment" },
          { action: "Evaluate" },
        ],
      }),
    ).toBe(false);
  });
});