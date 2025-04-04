# Release Checklist

This document outlines the steps to follow when creating a new release of yaml2pydantic.

## Pre-Release Steps

1. **Code Quality**
   - [ ] All tests are passing
   - [ ] Code coverage meets requirements
   - [ ] Linting passes
   - [ ] Type checking passes

2. **Documentation**
   - [ ] README.md is up to date
   - [ ] API documentation is current
   - [ ] Examples are working and documented
   - [ ] CHANGELOG.md is updated with all changes

3. **Version Management**
   - [ ] Update version in `pyproject.toml`
   - [ ] Update version in any other relevant files
   - [ ] Commit version changes with message "Bump version to X.Y.Z"

4. **Dependencies**
   - [ ] All dependencies are up to date
   - [ ] No security vulnerabilities in dependencies
   - [ ] Test with latest dependency versions

## Release Process

1. **Create Release**
   - [ ] Create a new release on GitHub
   - [ ] Use semantic versioning (vX.Y.Z)
   - [ ] Copy relevant CHANGELOG.md entries to release notes
   - [ ] Tag the release
   - [ ] Publish the release

2. **Post-Release Verification**
   - [ ] Verify package is published on PyPI
   - [ ] Test installation from PyPI
   - [ ] Verify documentation is updated
   - [ ] Check GitHub Actions workflows completed successfully

3. **Announcement**
   - [ ] Update any relevant project status pages
   - [ ] Announce on relevant channels (if applicable)

## Rollback Plan

If issues are discovered after release:

1. [ ] Identify the specific issues
2. [ ] Create a hotfix branch if needed
3. [ ] Fix the issues
4. [ ] Create a new patch release
5. [ ] Update documentation if necessary 