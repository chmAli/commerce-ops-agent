import re
import pytest
from agent import ask
from evals.cases import CASES


def contains(answer: str, expected: str) -> bool:
    """True if `expected` appears in the answer as a whole word/number.
    Commas are ignored, so 174600 matches 174,600; case is ignored."""
    text = answer.replace(",", "").lower()
    exp = expected.replace(",", "").lower()
    return re.search(rf"(?<![\w#]){re.escape(exp)}(?!\w)", text) is not None


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_case(case):
    trace = []
    answer = ask(case["q"], trace=trace)
    for exp in case.get("must", []):
        assert contains(answer, exp), f"missing {exp!r} in: {answer[:300]}"
    if "any" in case:
        assert any(contains(answer, e) for e in case["any"]), f"none of {case['any']} in: {answer[:300]}"
    if "tool" in case:
        used = [name for name, _ in trace]
        assert case["tool"] in used, f"expected tool {case['tool']}, used {used}"

    for bad in case.get("must_not", []):
        assert not contains(answer, bad), f"should not contain {bad!r}: {answer[:300]}"
    if "max_calls" in case:
        used = [name for name, _ in trace]
        assert len(used) <= case["max_calls"], f"{len(used)} tool calls (max {case['max_calls']}): {used}"