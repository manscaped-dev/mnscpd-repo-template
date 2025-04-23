# Manscaped 5 Server Workflows Readme

### Git Flow

#### Build/Deploy

```mermaid
flowchart LR
    pr[Pull Request]
    
    cu([Creates/Updates a Draft Release])

    draft_release[Draft Release - PR Merge
    Tag: Version
    isDraft=True
    _release-drafter.yml_]

    pr --> draft_release --> cu --> deploy[De]

```

#### Release to Staging (Pre-Release)

```mermaid
flowchart LR
    workflow[_sre-release-promotions.yml_]

    
    workflow --> promote_stg["Pre-Release (staging)
    Tag: Version"
    isDraft=False
    isPrerelease=True
    isLatest=False] 
    
    promote_stg --> deploy["Deploy Application(s)"]
```

#### Release to Production (Release)

```mermaid
flowchart LR
    workflow[_sre-release-promotions.yml_]
    
    workflow --> promote_prd["Release (prodction)
    Tag: Version
    isDraft=False
    isPrerelease=False
    isLatest=True
    _sre-auto-core-app-dispatch.yml_"]
    
    promote_prd --> deploy["Deploy Application(s)"]
```

### Release SHA Python Document

Here are the commands to get the SHAs for the respective release(s)?

```bash
### If you are running this from your local maching for the github repo - 
# To get the current draft release commit hash (sha)
python .github/workflows/python/release_sha.py --draft

# To get the current prerelease commit hash (sha)
python .github/workflows/python/release_sha.py --prerelease

# To get the current release (latest-published) commit hash (sha)
python .github/workflows/python/release_sha.py --release

# To run the script with Icecream enabled
python .github/workflows/python/release_sha.py --debug
```
