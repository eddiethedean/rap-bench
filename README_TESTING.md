# Local Testing Guide

To test PyPI builds locally without waiting for GitHub Actions:

## Quick Check (No Build Required)

If you have artifacts from a failed GitHub Actions run:

```bash
# Download artifacts from a failed run
gh run download <RUN_ID> -D test_artifacts

# Copy to dist/ and check metadata
mkdir -p dist
find test_artifacts -name "*.whl" -exec cp {} dist/ \;
find test_artifacts -name "*.tar.gz" -exec cp {} dist/ \;

# Check metadata for issues
python3 check_metadata.py
```

## Full Local Build

This package uses setuptools (not maturin):

```bash
# Install build tools if needed
python3 -m pip install build

# Build and check
./test_pypi_build.sh
```

## Validate with Twine

```bash
# Install twine
python3 -m pip install twine

# Check distributions (validates metadata)
twine check dist/*

# Test upload to TestPyPI (optional, requires TestPyPI account)
twine upload --repository testpypi dist/*
```

## Common Issues

### License-File Field

If you see `License-File: LICENSE` in the metadata, the build system is auto-detecting the LICENSE file. For setuptools packages, this is usually controlled by MANIFEST.in or setup.py configuration.
