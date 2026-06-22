import anthropic
import json
import os
import sys

client = anthropic.Anthropic()
MODEL = os.environ.get("MODEL", "claude-sonnet-4-6")

REVIEW_TOOL = {
    "name": "submit_review",
    "description": (
        "Submit the structured code review result. Call exactly once after completing analysis. "
        "Set approved=False for any critical severity issue. Score reflects overall quality 0-100."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {"type": "string", "description": "One-sentence overall quality assessment"},
            "score": {"type": "integer", "minimum": 0, "maximum": 100},
            "approved": {"type": "boolean", "description": "False if any critical issues exist"},
            "issues": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "severity": {"type": "string", "enum": ["critical", "major", "minor", "suggestion"]},
                        "category": {
                            "type": "string",
                            "enum": ["security", "performance", "correctness", "style", "maintainability"],
                        },
                        "line": {"type": "integer"},
                        "description": {"type": "string"},
                        "suggestion": {"type": "string"},
                    },
                    "required": ["severity", "category", "description", "suggestion"],
                },
            },
            "test_coverage_assessment": {"type": "string"},
            "required_changes": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Blocking changes required before approval",
            },
        },
        "required": ["summary", "score", "approved", "issues", "required_changes"],
    },
}


def review_code(diff: str, pr_title: str = "Code Review") -> dict:
    print(f"Reviewing: {pr_title}")
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=(
            "You are an automated code reviewer in a CI/CD pipeline. Analyze diffs for:\n"
            "- Security vulnerabilities (SQL injection, weak crypto, secrets exposure)\n"
            "- Correctness issues (off-by-one, null handling, race conditions)\n"
            "- Performance problems (N+1 queries, unnecessary allocations)\n"
            "- Style and maintainability\n\n"
            "Be fair: approve PRs that meet quality standards even with minor issues. "
            "Only critical security or correctness issues should block approval."
        ),
        tools=[REVIEW_TOOL],
        tool_choice={"type": "any"},  # Force structured output — no free-text fallback
        messages=[
            {
                "role": "user",
                "content": (
                    f'Review this diff for PR: "{pr_title}"\n\n```diff\n{diff}\n```\n\n'
                    "Analyze thoroughly, then call submit_review with your findings."
                ),
            }
        ],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "submit_review":
            return block.input

    return {"error": "No review submitted", "approved": False, "issues": [], "required_changes": []}


def main():
    sample_diff = """\
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,8 +10,15 @@ import hashlib

 def authenticate_user(username: str, password: str) -> bool:
-    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
-    result = db.execute(query)
+    query = "SELECT id, password_hash FROM users WHERE username = ?"
+    result = db.execute(query, (username,))
+
+    if not result:
+        return False
+
+    user = result[0]
+    return bcrypt.checkpw(password.encode(), user['password_hash'])

-def reset_password(email):
-    token = str(random.random())
+def reset_password(email: str) -> str:
+    token = secrets.token_urlsafe(32)
     send_email(email, f"Reset token: {token}")
+    store_reset_token(email, token, expires_in=3600)
+    return token
"""

    review = review_code(sample_diff, "Fix SQL injection and weak token generation")
    print(json.dumps(review, indent=2))

    critical_issues = [i for i in review.get("issues", []) if i["severity"] == "critical"]
    if critical_issues:
        print(f"\nBLOCKED: {len(critical_issues)} critical issue(s) found")
        sys.exit(1)
    elif review.get("approved"):
        print(f"\nApproved (score: {review.get('score', 'N/A')}/100)")
        sys.exit(0)
    else:
        print(f"\nChanges requested (score: {review.get('score', 'N/A')}/100)")
        sys.exit(1)


if __name__ == "__main__":
    main()
