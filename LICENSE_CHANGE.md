# License Change: GPL v3 → AGPL v3

## Summary

The Talk-Less project license has been changed from **GPL v3** to **AGPL v3** (GNU Affero General Public License version 3).

## Date of Change

January 16, 2026

## Rationale

The AGPL v3 license is more appropriate for Talk-Less because:

1. **Network Service Requirement**: AGPL v3 requires that source code be made available even when the software is used as a network service (SaaS). This aligns perfectly with Talk-Less's transparency principles.

2. **Closing the "SaaS Loophole"**: GPL v3 allows someone to modify the software and run it as a web service without releasing their modifications. AGPL v3 closes this loophole.

3. **Mission Alignment**: Talk-Less is a public-good platform that requires complete transparency. AGPL v3 ensures that anyone running a Talk-Less instance (even modified versions) must make their source code available to users.

4. **Protecting Core Principles**: The AGPL v3 ensures that the no-tracking, no-monetization, and transparency principles cannot be hidden in proprietary modifications.

## What Changed

### 1. LICENSE File
- Replaced GPL v3 text with complete AGPL v3 text (661 lines)
- Downloaded from: https://www.gnu.org/licenses/agpl-3.0.txt

### 2. Documentation Updates
- ✅ **README.md**: Already referenced AGPL v3
- ✅ **CONTRIBUTING.md**: Already mentioned AGPL v3 as non-negotiable principle
- ✅ **setup.py**: Already had `license="AGPL-3.0"` and proper classifier

### 3. License Headers Added
Added AGPL v3 license headers to all key source files:

**Pipeline Modules:**
- `backend/pipeline/ingestion.py`
- `backend/pipeline/comparison.py`
- `backend/pipeline/summarization.py`
- `backend/pipeline/bias_detection.py`
- `backend/pipeline/run.py`

**API Modules:**
- `backend/api/server.py`
- `backend/api/models.py`
- `backend/api/database.py`

### 4. License Header Format
All source files now include:
```python
# Copyright (C) 2026 Talk-Less Contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This file is part of Talk-Less.
#
# Talk-Less is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Talk-Less is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Talk-Less. If not, see <https://www.gnu.org/licenses/>.
```

## Key Differences: GPL v3 vs AGPL v3

| Aspect | GPL v3 | AGPL v3 |
|--------|--------|---------|
| **Distribution Trigger** | Binary/source distribution | Network service use OR distribution |
| **Network Service** | No requirement to share source | **Must share source with users** |
| **SaaS Use Case** | Can keep modifications private | **Must disclose modifications** |
| **Best For** | Desktop/embedded software | Web services and network applications |

## Impact on Contributors

### For Contributors
- All contributions are now under AGPL v3
- Contributors retain copyright but license under AGPL v3
- Same contribution process as before
- All code remains open source

### For Users
- Can still use, modify, and distribute the software freely
- **New requirement**: If you run Talk-Less as a web service, you must make your modified source code available to users
- No impact on personal/research use
- Ensures transparency for all public deployments

### For Forks/Derivatives
- Any fork or derivative work must also be AGPL v3
- If you run a modified version as a web service, you must:
  1. Provide a link to your source code
  2. Make it accessible to all users
  3. Include all your modifications

## Compatibility

**Compatible with:**
- AGPL v3 libraries
- GPL v3 libraries (AGPL is more restrictive)
- MIT, BSD, Apache 2.0 libraries (permissive licenses)

**Incompatible with:**
- Proprietary/closed-source components
- GPL v2 (without "or later" clause)
- Some restrictive open source licenses

## Legal Considerations

1. **All files now under AGPL v3**: Every source file has explicit license headers
2. **SPDX Identifier**: Using standard `AGPL-3.0-or-later` identifier
3. **Copyright**: Attribution to "Talk-Less Contributors"
4. **No Warranty**: Standard AGPL v3 warranty disclaimers apply

## Network Service Obligations

If you deploy Talk-Less as a network service (web app), you **must**:

1. ✅ Provide a prominent link to the complete source code
2. ✅ Include all modifications you've made
3. ✅ Use a compatible license (AGPL v3)
4. ✅ Make the source accessible to all users
5. ✅ Include build/deployment instructions

**Example implementation:**
- Add "Source Code" link in footer
- Link to your GitHub repository
- Include README with setup instructions
- Document any configuration changes

## Questions & Answers

**Q: Can I still use Talk-Less for free?**
A: Yes, absolutely. AGPL v3 is free software.

**Q: Can I modify Talk-Less?**
A: Yes, you can modify it freely.

**Q: Can I run Talk-Less on my server?**
A: Yes, but you must make your source code (including modifications) available to users.

**Q: What if I only use Talk-Less internally (not public)?**
A: Internal use doesn't trigger AGPL v3 requirements. Only public network service use does.

**Q: Can I integrate proprietary code?**
A: No. AGPL v3 requires the entire system to be open source if distributed or used as a network service.

**Q: Is this change retroactive?**
A: All code going forward is AGPL v3. Previous commits remain under their original license, but the project as a whole is now AGPL v3.

## Enforcement

Talk-Less maintainers will:
- Monitor for AGPL v3 compliance in known deployments
- Request source code access from public deployments
- Report non-compliant uses to the community
- Work with Free Software Foundation if needed

## Resources

- **AGPL v3 Full Text**: https://www.gnu.org/licenses/agpl-3.0.txt
- **AGPL v3 FAQ**: https://www.gnu.org/licenses/gpl-faq.html#AGPLv3
- **Why AGPL**: https://www.gnu.org/licenses/why-affero-gpl.html
- **SPDX License List**: https://spdx.org/licenses/

## Verification

To verify the license:
```bash
# Check LICENSE file
head -5 LICENSE

# Check source file headers
head -18 backend/pipeline/ingestion.py

# Check package metadata
grep -A 5 "license" setup.py
```

All should reference AGPL v3.

---

**Last Updated**: January 16, 2026  
**Document Version**: 1.0  
**Status**: Complete
