#!/usr/bin/env bash
# CI/CD validation script for media-work-plugins
# Validates all skills against the Agent Skills spec using skills-ref,
# runs type checking, linting, and tests.
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
FAILED=0

echo "=========================================="
echo "  media-work-plugins CI/CD Validation"
echo "=========================================="

# ---- 1. Skill Validation (skills-ref) ----
echo ""
echo -e "${YELLOW}[1/4] Validating skills against Agent Skills spec...${NC}"

PLUGINS=("marketing-data-science" "platform-engineering" "media-operations")
SKILL_ERRORS=0

for plugin in "${PLUGINS[@]}"; do
    skills_dir="${ROOT_DIR}/${plugin}/skills"
    if [ ! -d "$skills_dir" ]; then
        continue
    fi
    for skill_dir in "${skills_dir}"/*/; do
        if [ ! -d "$skill_dir" ]; then
            continue
        fi
        if skills-ref validate "$skill_dir" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓${NC} ${plugin}/$(basename "$skill_dir")"
        else
            echo -e "  ${RED}✗${NC} ${plugin}/$(basename "$skill_dir")"
            skills-ref validate "$skill_dir" 2>&1 | sed 's/^/    /'
            SKILL_ERRORS=$((SKILL_ERRORS + 1))
        fi
    done
done

if [ $SKILL_ERRORS -gt 0 ]; then
    echo -e "${RED}  $SKILL_ERRORS skill(s) failed validation${NC}"
    FAILED=1
else
    echo -e "${GREEN}  All skills valid${NC}"
fi

# ---- 2. Python Type Checking (mypy) ----
echo ""
echo -e "${YELLOW}[2/4] Running type checks (mypy)...${NC}"

if command -v mypy &> /dev/null; then
    if mypy "${ROOT_DIR}/marketing-data-science/models/" --config-file "${ROOT_DIR}/pyproject.toml" 2>&1; then
        echo -e "${GREEN}  Type checks passed${NC}"
    else
        echo -e "${RED}  Type check failures found${NC}"
        FAILED=1
    fi
else
    echo -e "${YELLOW}  mypy not installed, skipping${NC}"
fi

# ---- 3. Linting (ruff) ----
echo ""
echo -e "${YELLOW}[3/4] Running linter (ruff)...${NC}"

if command -v ruff &> /dev/null; then
    if ruff check "${ROOT_DIR}/marketing-data-science/models/" 2>&1; then
        echo -e "${GREEN}  Linting passed${NC}"
    else
        echo -e "${RED}  Lint errors found${NC}"
        FAILED=1
    fi
else
    echo -e "${YELLOW}  ruff not installed, skipping${NC}"
fi

# ---- 4. Tests ----
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
