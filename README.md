# Android Gradle Plugin version finder - GitHub Action

[![.github/workflows/pull_request.yml](https://github.com/usefulness/agp-version-finder-action/actions/workflows/pull_request.yml/badge.svg)](https://github.com/usefulness/agp-version-finder-action/actions/workflows/pull_request.yml)

Find current stable and latest Android Gradle Plugin version for GitHub Actions matrix builds.

## Usage

The action only exposes multiple `output`s containing latest version for each AGP release channel.

### Configuration:
```yml
  jobs:
    provide-agp-version-matrix:
      runs-on: ubuntu-latest
      outputs:
        agp-versions: ${{ steps.build-agp-matrix.outputs.agp-versions }}
      steps:
        # Fetch latest AGP versions
        - id: agp-version-finder
          uses: usefulness/agp-version-finder-action@v1

        # Consume action outputs to build AGP matrix
        - id: build-agp-matrix
          run: echo 'agp-versions=["${{ steps.agp-version-finder.outputs.latest-stable }}", "${{ steps.agp-version-finder.outputs.latest-alpha }}"]' >> $GITHUB_OUTPUT

      actual-tests:
        runs-on: ubuntu-latest
        needs:
          - provide-agp-version-matrix
        strategy:
          fail-fast: false
          matrix:
            javaVersion: [ 17 ]
            gradle: [ current, release-candidate ]
            # When evaluated will be replaced with array ["7.2.2", "7.4.0-alpha13"] 
            agp: ${{ fromJSON(needs.provide-agp-version-matrix.outputs.agp-versions) }}
```
[source](https://docs.github.com/en/actions/learn-github-actions/expressions#fromjson)

All available action outputs, representing respective AGP release channels:

- `latest-stable` i.e. _"7.2.2"_
- `latest-rc` i.e. _"7.3.0-rc01"_
- `latest-beta` i.e. _"7.3.0-beta02"_
- `latest-alpha`  i.e. _"7.4.0-alpha13"_
