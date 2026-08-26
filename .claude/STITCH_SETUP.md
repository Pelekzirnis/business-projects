# Google Stitch skills (vendored)

`.claude/skills/stitch-*` contains the 16 skills from
[google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills)
(Apache-2.0, see `stitch-skills/STITCH-SKILLS-LICENSE`), copied into this repo on
2026-08-26 so they're available in any future Claude Code session opened here —
no re-install needed.

They cover the full Stitch workflow: `stitch-site-md` / `stitch-design-md` define
a project's vision and design system, `stitch-generate-design` /
`stitch-loop` drive the design loop, and `stitch-react-components` /
`stitch-shadcn-ui` / `stitch-react-native` turn designs into code.

## Before first use: connect the Stitch MCP server

The skills call MCP tools (prefixed `stitch*:*` — `list_projects`,
`create_project`, `generate_screen_from_text`, etc.) that only exist once the
Stitch MCP server is registered. Without this step the skills are just
instructions with nothing to call.

1. Get an API key: sign in at [stitch.withgoogle.com](https://stitch.withgoogle.com)
   with your Google account → account settings → generate an API key
   (format `stit_xxxxxxxxxxxxxxxxxxxx`).
2. Register the server (run once per machine/session, not something to commit):
   ```
   claude mcp add stitch --transport http https://stitch.googleapis.com/mcp \
     --header "X-Goog-Api-Key: YOUR-API-KEY" -s user
   ```
3. **Never commit the key.** `-s user` keeps it in your local `~/.claude.json`,
   outside this repo. If you ever add a project-level `.mcp.json` with the key
   inline, gitignore it first.

## Keeping it up to date

This is a point-in-time copy, not a live plugin link — it won't auto-update.
To refresh it later: `npx plugins add google-labs-code/stitch-skills --scope
project --target claude-code` in a session on this repo, then re-copy the
updated `skills/` folders from each plugin over `.claude/skills/stitch-*` here
and commit.
