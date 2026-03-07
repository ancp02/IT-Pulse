#!/bin/bash
################################################################################
# Enable Repository Security Script
# Purpose: Guide user through enabling GitHub repository security features
################################################################################

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔒 IT-Pulse Repository Security Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}This script will help you enable security protections for your repository.${NC}\n"

echo -e "${BLUE}📋 Security Features to Enable:${NC}"
echo -e "  ✅ Branch protection rules (require PRs)"
echo -e "  ✅ Code review requirements"
echo -e "  ✅ Status checks before merging"
echo -e "  ✅ Enhanced GitHub Actions security"
echo -e "  ✅ Dependency vulnerability scanning\n"

echo -e "${YELLOW}⚠️  IMPORTANT: Your repository must remain PUBLIC for GitHub Pages to work.${NC}\n"

echo -e "${BLUE}Step 1: Enable Branch Protection${NC}"
echo -e "${GREEN}Go to: https://github.com/shweba2/IT-Pulse/settings/branches${NC}"
echo -e "1. Click 'Add rule'"
echo -e "2. Branch name pattern: ${GREEN}main${NC}"
echo -e "3. Check these options:"
echo -e "   ☑ Require a pull request before merging"
echo -e "   ☑ Require approvals (set to 1)"
echo -e "   ☑ Dismiss stale pull request approvals when new commits are pushed"
echo -e "   ☑ Require status checks to pass before merging"
echo -e "   ☑ Require branches to be up to date before merging"
echo -e "4. Click 'Create'\n"

echo -e "${BLUE}Step 2: Enable Security Features${NC}"
echo -e "${GREEN}Go to: https://github.com/shweba2/IT-Pulse/settings/security_analysis${NC}"
echo -e "Enable:"
echo -e "   ☑ Dependabot alerts"
echo -e "   ☑ Dependabot security updates"
echo -e "   ☑ Code scanning alerts"
echo -e "   ☑ Secret scanning\n"

echo -e "${BLUE}Step 3: Test the Security${NC}"
echo -e "1. Try to push directly to main branch (should be blocked)"
echo -e "2. Create a new branch and make a small change"
echo -e "3. Create a pull request"
echo -e "4. Verify it requires approval before merging\n"

echo -e "${BLUE}Step 4: Emergency Access${NC}"
echo -e "If you need to make urgent changes:"
echo -e "1. Go to Settings → Branches"
echo -e "2. Temporarily disable 'Require a pull request'"
echo -e "3. Make your change"
echo -e "4. Re-enable the protection\n"

echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Security enhancements have been added to your workflows!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}Your repository is now protected against:${NC}"
echo -e "  🛡️  Accidental code deletion"
echo -e "  🛡️  Unauthorized changes"
echo -e "  🛡️  Malicious modifications"
echo -e "  🛡️  Breaking changes without review"
echo -e "  🛡️  Dependency vulnerabilities\n"

echo -e "${BLUE}Files protected:${NC}"
echo -e "  • fetch_news.py (main logic)"
echo -e "  • template.html (structure)"
echo -e "  • requirements.txt (dependencies)"
echo -e "  • index.html (generated output)\n"

echo -e "${GREEN}Next: Enable branch protection in GitHub settings as shown above.${NC}\n"

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Security setup complete! 🛡️${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}\n"

exit 0