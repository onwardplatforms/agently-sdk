# Versioning Guide for Agently SDK

This document outlines the versioning strategy used in the Agently SDK project.

## Semantic Versioning

Agently SDK follows [Semantic Versioning 2.0.0](https://semver.org/) with the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Incremented for incompatible API changes
- **MINOR**: Incremented for new functionality in a backward-compatible manner
- **PATCH**: Incremented for backward-compatible bug fixes

## Pre-release Versioning

For pre-release versions, we follow [PEP 440](https://www.python.org/dev/peps/pep-0440/) standards:

### Development Releases

During active development of a new version, we use the `.dev` suffix:

```
0.5.2.dev0, 0.5.2.dev1, ...
```

Development releases:
- Are not intended for production use
- May have incomplete features
- May contain bugs or breaking changes
- Are primarily for testing and feedback

### Alpha Releases

When the feature set is complete but still needs significant testing:

```
0.5.2a1, 0.5.2a2, ...
```

Alpha releases:
- Have all planned features implemented
- May have known bugs
- API may still change
- Are suitable for early adopters and testers

### Beta Releases

When the feature set is complete and stabilizing:

```
0.5.2b1, 0.5.2b2, ...
```

Beta releases:
- Have all features implemented
- Have fewer known bugs
- API is mostly stable
- Are suitable for wider testing

### Release Candidates

When we believe the release is ready for final testing:

```
0.5.2rc1, 0.5.2rc2, ...
```

Release candidates:
- Are feature complete
- Have no known critical bugs
- Have stable APIs
- Are ready for final validation before release

## Post-releases

For minor updates that don't change functionality:

```
0.5.2.post1, 0.5.2.post2, ...
```

## Version Workflow Example

A typical version progression might look like:

1. `0.5.2.dev0` - Initial development
2. `0.5.2.dev1` - Development continues
3. `0.5.2a1` - First alpha release
4. `0.5.2b1` - First beta release
5. `0.5.2rc1` - First release candidate
6. `0.5.2` - Final release
7. `0.5.2.post1` - Post-release fix

## For Contributors

When working on a new feature or release:

1. Development branches should use the `.dev` suffix
2. Update the version in `src/agently_sdk/_version.py`
3. Include the version update in your PR
4. Tag releases using the format `v0.5.2` (including the 'v' prefix)

## Version Checking

You can check the current version of Agently SDK with:

```python
import agently_sdk
print(agently_sdk.__version__)
``` 