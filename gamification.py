import difflib
import Levenshtein


# Heuristic points system (Phase 1)
# - Base submission: 10
# - Edit bonus: up to 20 (more thoughtful edits vs raw MT)
# - Reference bonus: up to 70 if moving closer to reference (when provided)
# Max per task: 100


def similarity_ratio(a: str, b: str) -> float:
sm = difflib.SequenceMatcher(None, a.split(), b.split())
return sm.ratio()




def compute_points(mt_text: str, user_edit: str, reference: str | None = None) -> int:
if not user_edit.strip():
return 0


points = 10 # submission


# Edit bonus: encourage meaningful changes (but cap it)
edit_distance = Levenshtein.distance(mt_text, user_edit)
edit_bonus = min(20, max(0, int(edit_distance / 20) + 1))
points += edit_bonus


# Reference improvement (if provided)
if reference and reference.strip():
# Compare closeness to reference vs MT's closeness
mt_sim = similarity_ratio(mt_text, reference)
user_sim = similarity_ratio(user_edit, reference)
improvement = max(0.0, user_sim - mt_sim)
ref_bonus = int(min(70, improvement * 100)) # scale to 0..70
points += ref_bonus


return max(0, min(100, points))