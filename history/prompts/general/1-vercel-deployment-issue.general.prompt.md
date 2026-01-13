---
id: 1
title: Vercel Deployment Issue
stage: general
date_iso: 2026-01-13
surface: agent
model: Qwen Code
feature: none
branch: main
user: mypc
command: python-vercel-deployment-consultation
labels: ["deployment", "vercel", "psycopg2", "python"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - pyproject.toml
tests_yaml: []
---

# Vercel Deployment Issue Consultation

## Original Prompt

User consulted about Vercel deployment failures with the following issues:
- psycopg2 fails to build
- pg_config not found
- Python >=3.13 is ignored by Vercel

Requested:
1. Identify why Vercel deployment is failing
2. Explain that this is a console/backend Python app not suitable for Vercel
3. Provide two fixes:
   a) Correct fix: do not deploy on Vercel, keep as GitHub project only
   b) Optional fix: make Vercel-compatible by replacing psycopg2 with psycopg2-binary and fixing Python version
4. Show exact file changes
5. Provide exact Git commands
6. Keep explanation short and professional

## Response Summary

Provided comprehensive analysis of the Vercel deployment issue with:

### Problem
- `psycopg2` fails to build on Vercel because `pg_config` is not found in the build environment
- Project specifies Python >=3.13, but Vercel doesn't properly support this version

### Root Cause
- `psycopg2` requires compilation of C extensions and PostgreSQL development headers (`pg_config`)
- Vercel's build environment doesn't include PostgreSQL development tools
- Vercel has limited support for newer Python versions (>=3.13)

### Recommended Solution (Solution A)
Explained that this is a console/backend Python application not suitable for Vercel deployment. Vercel is designed for frontend frameworks and serverless functions, not traditional backend applications with database dependencies. Recommended keeping this as a GitHub project only and deploying to more appropriate platforms.

### Optional Solution (Solution B)
Provided technical changes to make it Vercel-compatible:
- Replaced `psycopg2` with `psycopg2-binary` (pre-compiled wheel)
- Fixed Python version constraint to >=3.10,<3.13

### File Changes
Updated `pyproject.toml`:
- Changed `requires-python` from ">=3.13" to ">=3.10,<3.13"
- Changed `psycopg2>=2.9.11` to `psycopg2-binary>=2.9.11`

### Commands Provided
Git commands to implement the changes and push to GitHub.

## Outcome

Successfully diagnosed the deployment issue and provided both recommended and alternative solutions with exact implementation steps. Explained why Vercel is not the appropriate platform for this type of application.

## Evaluation

The consultation addressed all aspects of the user's request, providing both the technical solution and appropriate platform guidance. The response was kept concise and professional as requested.