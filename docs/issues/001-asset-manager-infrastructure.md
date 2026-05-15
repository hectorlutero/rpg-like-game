## What to build

Implement a centralized `AssetManager` capable of loading and caching SpriteSheets and their associated metadata (JSON). This system must be the single source of truth for visual assets in the engine.

- Create `src/core/assets.py` to handle SpriteSheet slicing and caching.
- Implement a `MetadataLoader` to parse JSON files defining sprite dimensions and frame data.
- Ensure the `WorldOrchestrator` can link map grid IDs to these assets.

## Acceptance criteria

- [ ] `AssetManager` successfully slices a SpriteSheet into individual surfaces.
- [ ] `MetadataLoader` correctly parses sprite dimensions and offset data from JSON.
- [ ] Assets are cached to prevent redundant disk I/O.
- [ ] A basic unit test confirms that requesting a non-existent asset returns a clear error or "Missing Asset" handle.

## Blocked by

- None - can start immediately
