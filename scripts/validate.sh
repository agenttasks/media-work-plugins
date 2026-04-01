#!/usr/bin/env bash
# CI/CD validation script for media-work-plugins
# Validates skills, runs type checking, linting, and tests.
# Stages 1-3 run in parallel for throughput; stage 4 (tests) runs after.
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
TMPDIR="${ROOT_DIR}/.ci-tmp"
mkdir -p "$TMPDIR"
trap 'rm -rf "$TMPDIR"' EXIT

echo "=========================================="
echo "  media-work-plugins CI/CD Validation"
echo "=========================================="

# ---- Parallel stages: skills-ref, mypy, ruff ----

# Stage 1: Skill validation
(
    SKILL_ERRORS=0
    PLUGINS=("marketing-data-science" "platform-engineering" "media-operations")
    for plugin in "${PLUGINS[@]}"; do
        skills_dir="${ROOT_DIR}/${plugin}/skills"
        [ ! -d "$skills_dir" ] && continue
        for skill_dir in "${skills_dir}"/*/; do
            [ ! -d "$skill_dir" ] && continue
            if skills-ref validate "$skill_dir" > /dev/null 2>&1; then
                echo -e "  ${GREEN}✓${NC} ${plugin}/$(basename "$skill_dir")"
            else
                echo -e "  ${RED}✗${NC} ${plugin}/$(basename "$skill_dir")"
                skills-ref validate "$skill_dir" 2>&1 | sed 's/^/    /'
                SKILL_ERRORS=$((SKILL_ERRORS + 1))
            fi
        done
    done
    echo "$SKILL_ERRORS" > "$TMPDIR/skills.rc"
    if [ $SKILL_ERRORS -gt 0 ]; then
        echo -e "${RED}  $SKILL_ERRORS skill(s) failed validation${NC}"
    else
        echo -e "${GREEN}  All skills valid${NC}"
    fi
) &
PID_SKILLS=$!

# Stage 2: mypy
(
    if command -v mypy &> /dev/null; then
        if mypy "${ROOT_DIR}/marketing-data-science/models/" --config-file "${ROOT_DIR}/pyproject.toml" > "$TMPDIR/mypy.log" 2>&1; then
            echo -e "${GREEN}  [mypy] Type checks passed${NC}"
            echo "0" > "$TMPDIR/mypy.rc"
        else
            cat "$TMPDIR/mypy.log"
            echo -e "${RED}  [mypy] Type check failures found${NC}"
            echo "1" > "$TMPDIR/mypy.rc"
        fi
    else
        echo -e "${YELLOW}  [mypy] not installed, skipping${NC}"
        echo "0" > "$TMPDIR/mypy.rc"
    fi
) &
PID_MYPY=$!

# Stage 3: ruff
(
    if command -v ruff &> /dev/null; then
        if ruff check "${ROOT_DIR}/marketing-data-science/models/" > "$TMPDIR/ruff.log" 2>&1; then
            echo -e "${GREEN}  [ruff] Linting passed${NC}"
            echo "0" > "$TMPDIR/ruff.rc"
        else
            cat "$TMPDIR/ruff.log"
            echo -e "${RED}  [ruff] Lint errors found${NC}"
            echo "1" > "$TMPDIR/ruff.rc"
        fi
    else
        echo -e "${YELLOW}  [ruff] not installed, skipping${NC}"
        echo "0" > "$TMPDIR/ruff.rc"
    fi
) &
PID_RUFF=$!

echo ""
echo -e "${YELLOW}[1-3/4] Running skills validation, mypy, and ruff in parallel...${NC}"
wait $PID_SKILLS $PID_MYPY $PID_RUFF

FAILED=0
for stage in skills mypy ruff; do
    rc=$(cat "$TMPDIR/${stage}.rc" 2>/dev/null || echo "0")
    [ "$rc" != "0" ] && FAILED=1
done

# ---- Stage 4: Tests (sequential, needs clean imports) ----
echo ""
echo -e "${YELLOW}[4/4] Running tests...${NC}"

cd "${ROOT_DIR}/marketing-data-science"
if python -m pytest tests/ -v --tb=short 2>&1; then
    echo -e "${GREEN}  All tests passed${NC}"
else
    echo -e "${RED}  Test failures found${NC}"
    FAILED=1
fi

# ---- Summary ----
echo ""
echo "=========================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}  All checks passed ✓${NC}"
else
    echo -e "${RED}  Some checks failed ✗${NC}"
    exit 1
fi
