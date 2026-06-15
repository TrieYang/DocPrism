#!/usr/bin/env bash
# Run the three Go-to-Source-Definition sample cases (see samples.md).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
HOPPSCOTCH="$ROOT/hoppscotch"
export PYTHONUNBUFFERED=1

run_sample() {
  local title="$1"
  shift
  echo ""
  echo "================================================================================"
  echo "$title"
  echo "================================================================================"
  python3 "$ROOT/code_navigation_TypeScript.py" "$@" | python3 -c "
import json, sys
d = json.load(sys.stdin)
od = (d.get('definitions') or [{}])[0].get('outer_definition') or {}
reason = d.get('chosen_definition_reason') or {}
print('ok:', d.get('ok'))
print('path:', od.get('repo_relative_path') or od.get('path'))
print('reason:', reason.get('note'), '| go_to_source_definition:', reason.get('go_to_source_definition'))
src_locs = d.get('source_definition_locations') or []
print('source_definition_locations:', len(src_locs))
print('--- full_def_source (first 600 chars) ---')
print((od.get('full_def_source') or '')[:600])
"
}

cd "$ROOT"

run_sample "1. IMPROVED: bcrypt.genSalt (.d.ts -> bcrypt.js)" \
  --repo-root "$HOPPSCOTCH" \
  --script-path "$HOPPSCOTCH/packages/hoppscotch-backend/src/auth/auth.service.ts" \
  --tested-function generateMagicLinkTokens \
  --callee 'bcrypt.genSalt(
      parseInt(this.configService.get('\''TOKEN_SALT_COMPLEXITY'\'')),
    )'

run_sample "2. STILL DECLARATION: prisma personalAccessToken.create (.d.ts)" \
  --repo-root "$HOPPSCOTCH" \
  --script-path "$HOPPSCOTCH/packages/hoppscotch-backend/src/access-token/access-token.service.ts" \
  --tested-function createPAT \
  --callee 'this.prisma.personalAccessToken.create({
      data: {
        userUid: user.uid,
        label: createAccessTokenDto.label,
        expiresOn: calculateExpirationDate(createAccessTokenDto.expiryInDays),
      },
    })'

run_sample "3. WEAK SOURCE-DEF: DateTime.now() (luxon.js but wrong snippet)" \
  --repo-root "$HOPPSCOTCH" \
  --script-path "$HOPPSCOTCH/packages/hoppscotch-backend/src/auth/auth.service.ts" \
  --tested-function generateMagicLinkTokens \
  --callee 'DateTime.now()'

echo ""
echo "Done. See samples.md for details."
